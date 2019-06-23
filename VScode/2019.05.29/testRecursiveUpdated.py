
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from PIL import ImageChops 

import requests

import math
import operator
from functools import reduce

import time
import os


############################## parsing ##############################

def parsing_hover(soup):
    peekstyle =  soup.find('style')

    hoverclassli = []

    subData=str(peekstyle).split('.')

    searchwords = ":hover"

    for name in subData:
        if (searchwords in name):
            hoverclassli.append((name.split(':',1))[0])

    # print(hoverclassli)

    for i in range(len(hoverclassli)) :
        for j in range(i+1,len(hoverclassli)):
            if(len(driver.find_elements_by_class_name(hoverclassli[i])[i].find_elements_by_class_name(hoverclassli[j]))):
                hoverclassli.remove(hoverclassli[j])

    # print(hoverclassli)

    return hoverclassli

#####################################################################




def save_hover_pic(webelementreference):

    global driver

    try: 
        driversize= driver.get_window_size()
        driverwidth = driversize['width']
        driverheight = driversize['height']

        xPercentage = ( webelementreference.location['x']+0.5*webelementreference.size['width'] ) *100 / driverwidth
        yPercentage = ( webelementreference.location['y']+0.5*webelementreference.size['height'] ) *100 / driverheight
        wp  = ( webelementreference.size['width'] ) *100 / driverwidth
        hp = ( webelementreference.size['height'] ) *100 / driverheight

    
        imagePath = 'hover('+ str(round(xPercentage)) + '%,' + str(round(yPercentage)) + '%)['+ str(round(wp))+'%,' + str(round(hp)) + '%].png'


        ActionChains(driver).move_to_element(webelementreference).perform()       
        time.sleep(0.05)
        webelementreference.screenshot(path+imagePath)

        return path+imagePath

    except:
        return

def hover_screenshot(webelementreference):

    global wholecount
    global driver

    try: 
        webelementreference.screenshot(path+"/partial_count"+str(wholecount*2-1)+".png")
        time.sleep(0.01)
        ActionChains(driver).move_to_element(webelementreference).perform()       
        time.sleep(0.01)
        webelementreference.screenshot(path+"/partial_count"+str(wholecount*2)+".png")
        wholecount = wholecount + 1
    except:
        return


testdictionary ={ 
"op": "clickAfterHover",
"webdriverElement": [ {"ancestorHoverElement": "header", "xpathTrue": "null" , "imagePath": "header", "identity": "default"} ]
}


def iterate_hover(hoverclassli):

    ancestorHoverElement = []

    for hover_class_name in hoverclassli:
                
        ################### get hover class name ######################   

        s1=driver.find_elements_by_class_name(hover_class_name)
        
        print( hover_class_name + " 類 共有 "+str(len(s1))+" 個")

    
        for subclass in s1:


            ################### get hover class  #######################

            image_Path = save_hover_pic(subclass)

            temp_dic = {"ancestorHoverElement": "null", "xpathTrue": subclass , "imagePath": image_Path } 
                
            testdictionary["webdriverElement"].append(temp_dic)

            ancestorHoverElement = []
            ancestorHoverElement.append(subclass)

            print( "  " + subclass.get_attribute("class")  )
            subclasslist = subclass.find_elements_by_tag_name("*")
            # print( "  "  + "有 "+str(len(subclasslist))+"個 children")



            for subclassitem in subclasslist:  
                if(len(subclassitem.find_elements_by_tag_name("*"))>=1):
 
                    continue

                image_Path = save_hover_pic(subclassitem)

                temp_dic = {"ancestorHoverElement": ancestorHoverElement, "xpathTrue": subclassitem , "imagePath": image_Path } 
                
                testdictionary["webdriverElement"].append(temp_dic)


                print( "    " + str(subclassitem.get_attribute("class")) + ":" + str(subclassitem.get_attribute("innerText")))

                
                # hover_screenshot(subclassitem) 




############################## comparison method ##############################

def compare(pic1,pic2):
    '''
    :param pic1: 图片1路径
    :param pic2: 图片2路径
    :return: 返回对比的结果
    '''
    image1 = Image.open(pic1)
    image2 = Image.open(pic2)

    histogram1 = image1.histogram()
    histogram2 = image2.histogram()

    differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2,histogram1, histogram2)))/len(histogram1))

    # print(differ)
    return differ

# ##########################################################################################



#################### partial compare #####################


def partial_compare(range):

    global wholecount
    compare_count = wholecount - 1
    
    
    # print("partial compare turn")
    
    try:
        temp = compare(path+"/partial_count"+str(compare_count*2-1)+".png",path+"/partial_count"+str(compare_count*2)+".png")   
        if( temp > range ):
            print(str(compare_count*2-1)+" and "+str(compare_count*2)+" move to action does work")
            
            Image.open(path+"/partial_count"+str(compare_count*2-1)+".png")
            os.remove(path+"/partial_count"+str(compare_count*2-1)+".png")
            Image.open(path+"/partial_count"+str(compare_count*2)+".png")
            os.remove(path+"/partial_count"+str(compare_count*2)+".png")
            try:
                Image.open(path+"/partial_count"+str(compare_count*2-1)+".png")
                os.remove(path+"/partial_count"+str(compare_count*2-1)+".png")
                Image.open(path+"/partial_count"+str(compare_count*2)+".png")
                os.remove(path+"/partial_count"+str(compare_count*2)+".png")
            except:
                return 1
            return 1
        else:
            try:
                Image.open(path+"/partial_count"+str(compare_count*2-1)+".png")
                os.remove(path+"/partial_count"+str(compare_count*2-1)+".png")
                Image.open(path+"/partial_count"+str(compare_count*2)+".png")
                os.remove(path+"/partial_count"+str(compare_count*2)+".png")
            except:
                return 0
    except:     
        try:
            Image.open(path+"/partial_count"+str(compare_count*2-1)+".png")
            os.remove(path+"/partial_count"+str(compare_count*2-1)+".png")
            Image.open(path+"/partial_count"+str(compare_count*2)+".png")
            os.remove(path+"/partial_count"+str(compare_count*2)+".png")

        except:
            return 0
    return 0

#######################################################

def testall_hover(range):
    
    ################### finding element ####################################    

    global driver
    s1 = driver.find_elements_by_xpath("/html/body/*")


    for subclass in s1:

        hover_screenshot(subclass) 


        
     

        ancestorHoverElement = []
        ancestorHoverElement.append(subclass)

        # print( "  " + subclass.get_attribute("class")  )
        subclasslist = subclass.find_elements_by_tag_name("*")
        # print( "  "  + "有 "+str(len(subclasslist))+"個 children")

        if not subclasslist:

            flag = partial_compare(range)
            if flag:
                image_Path = save_hover_pic(subclass)
                description = str(subclass.get_attribute("innerText"))
                temp_dic = {"ancestorHoverElement": "null", "xpathTrue": subclass , "imagePath": image_Path , "description": description, "identity": "root" } 
                testdictionary["webdriverElement"].append(temp_dic)

        for subclassitem in subclasslist:  
           
            if(len(subclassitem.find_elements_by_tag_name("*"))>=1):
                ancestorHoverElement.append(subclassitem)
                hover_screenshot(subclassitem)  

                flag = partial_compare(range)

                if flag:
                    image_Path = save_hover_pic(subclassitem)
                    description = str(subclassitem.get_attribute("innerText"))
                    temp_dic = {"ancestorHoverElement": ancestorHoverElement, "xpathTrue": subclassitem , "imagePath": image_Path, "description": description , "identity": "internal" } 
                    testdictionary["webdriverElement"].append(temp_dic)

                continue
            # print( "    " + str(subclassitem.get_attribute("class")) + ":" + str(subclassitem.get_attribute("innerText")))
        
            hover_screenshot(subclassitem)  

            flag = partial_compare(range)

            if flag:
                image_Path = save_hover_pic(subclassitem)
                description = str(subclassitem.get_attribute("innerText"))
                temp_dic = {"ancestorHoverElement": ancestorHoverElement, "xpathTrue": subclassitem , "imagePath": image_Path, "description": description , "identity": "leave" } 
                testdictionary["webdriverElement"].append(temp_dic)
            
            ancestorHoverElement = []


############################## main method ##############################



############## setting environment ##################

# url = "https://programming.ee.ntu.edu.tw"
url = "https://web.ee.ntu.edu.tw/"
# url = "https://zh.wikipedia.org/"
# url = "https://www.google.com.tw/"
# url = "https://ceiba.ntu.edu.tw"
# url = "https://www.facebook.com/"
# url = "https://www.baidu.com/"
# url = "https://www.iii.org.tw/"
# url = "https://www.eztravel.com.tw/"
# url = "https://www.mirrorfiction.com/"



path = "./capture/"

driver = webdriver.Firefox()
driver.maximize_window()

driver.get(url)

driversize= driver.get_window_size()



r=requests.get(url)

while True:
    if r.status_code == requests.codes.ok:
        # 以 BeautifulSoup 解析 HTML 程式碼
        soup = BeautifulSoup(r.text, 'html.parser')
        break

#########################################################

hoverclassli = parsing_hover(soup)

wholecount=1

######### screenshot hover element method 1 or 2 ###########

range = 0


# iterate_hover(hoverclassli)
testall_hover(range)

########### test dictionary ############



# partial_compare(range)

print(testdictionary)



for testitem in testdictionary["webdriverElement"]:

    if testitem["ancestorHoverElement"] == "null":
        continue
    if testitem["identity"] != "leave":
        continue
    for testancestorHoverElement in testitem["ancestorHoverElement"]:
        hover_screenshot(testancestorHoverElement)
    hover_screenshot(testitem["xpathTrue"])


