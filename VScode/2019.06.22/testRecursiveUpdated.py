
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



def maintain_temp_dic(ancestorHoverElement,xpathTrue,subclass):

    global driver

    driversize= driver.get_window_size()
    driverwidth = driversize['width']
    driverheight = driversize['height']

    image_Path = save_hover_pic(subclass)
    innerText = str(subclass.get_attribute("innerText"))

    xpos = subclass.location['x']
    ypos = subclass.location['y']
    width = subclass.size['width']
    height = subclass.size['height']

    xPercentage = ( xpos + 0.5 * width ) *100 / driverwidth
    yPercentage = ( ypos + 0.5 * height ) *100 / driverheight
    wp  = ( width ) *100 / driverwidth
    hp = ( height ) *100 / driverheight

    temp_dic = {"ancestorHoverElement": ancestorHoverElement, "xpathTrue": xpathTrue , "imagePath": image_Path , "innerText": innerText, "identity": "root", \
        "xpos": xpos, "ypos": ypos, "width": width, "height": height, "xPercentage": str(round(xPercentage)) + '%', "yPercentage": str(round(yPercentage)) + '%', \
        "wp": str(round(wp)) + '%', "hp": str(round(hp)) + '%'     }

    return temp_dic

def iterate_hover(hoverclassli):

    global driver

    ancestorHoverElement = []

    for hover_class_name in hoverclassli:
                
        ################### get hover class name ######################   

        s1=driver.find_elements_by_class_name(hover_class_name)
        
        print( hover_class_name + " 類 共有 "+str(len(s1))+" 個")

    
        for subclass in s1:


            ################### get hover class  #######################

            ancestorHoverElement = []
            ancestorHoverElement.append(subclass)

            xpathTrue = "/body/"
            xpathTrue = xpathTrue + str(hover_class_name) + "/"

            temp_dic = maintain_temp_dic(ancestorHoverElement,xpathTrue,subclass)

            testdictionary["webdriverElement"].append(temp_dic)


            print( "  " + subclass.get_attribute("class")  )
            subclasslist = subclass.find_elements_by_tag_name("*")
            # print( "  "  + "有 "+str(len(subclasslist))+"個 children")

            temp_xpath = xpathTrue

            for subclassitem in subclasslist:  
                if(len(subclassitem.find_elements_by_tag_name("*"))>=1):
                    xpathTrue = xpathTrue + str(subclassitem.get_attribute("class")) + "/"
                    temp_xpath = xpathTrue
                    continue


                ancestorHoverElement.append(subclassitem)
                xpathTrue = temp_xpath + str(subclassitem.get_attribute("class")) + "/"

                temp_dic = maintain_temp_dic(ancestorHoverElement,xpathTrue,subclassitem)
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

###########################################################################################


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

########################## Brutal Force ###############################

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

            xpathTrue = "/body/"
            xpathTrue = xpathTrue + str(subclass.get_attribute("class")) + "/"

            flag = partial_compare(range)
            if flag:
                
                
                xpathTrue = "/body/"
                for testitem in ancestorHoverElement:
                    xpathTrue = xpathTrue + str(testitem.get_attribute("class")) + "/"

                temp_dic = maintain_temp_dic(ancestorHoverElement,xpathTrue,subclass)
                testdictionary["webdriverElement"].append(temp_dic)



        for subclassitem in subclasslist:  
           
            if(len(subclassitem.find_elements_by_tag_name("*"))>=1):
                ancestorHoverElement.append(subclassitem)
                hover_screenshot(subclassitem)  

                flag = partial_compare(range)

                if flag:

                    xpathTrue = "/body/"
                    for testitem in ancestorHoverElement:
                        xpathTrue = xpathTrue + str(testitem.get_attribute("class")) + "/"

                    temp_dic = maintain_temp_dic(ancestorHoverElement,xpathTrue,subclassitem)
                    testdictionary["webdriverElement"].append(temp_dic)

                continue
            # print( "    " + str(subclassitem.get_attribute("class")) + ":" + str(subclassitem.get_attribute("innerText")))
        
            hover_screenshot(subclassitem)  

            flag = partial_compare(range)

            if flag:

                ancestorHoverElement.append(subclassitem)
                
                xpathTrue = "/body/"
                for testitem in ancestorHoverElement:
                    xpathTrue = xpathTrue + str(testitem.get_attribute("class")) + "/"

                temp_dic = maintain_temp_dic(ancestorHoverElement,xpathTrue,subclassitem)               
                testdictionary["webdriverElement"].append(temp_dic)

            ancestorHoverElement = []


########################## Generate Dictionary ###############################
def give_Dictionary(choose_mode, url, path):

    global driver

    r=requests.get(url)

    while True:
        if r.status_code == requests.codes.ok:
            # 以 BeautifulSoup 解析 HTML 程式碼
            soup = BeautifulSoup(r.text, 'html.parser')
            break

    #########################################################

    

    

    ######### screenshot hover element method 1 or 2 ###########

    range = 0

    if choose_mode == 1:
        hoverclassli = parsing_hover(soup)
        iterate_hover(hoverclassli)
    if choose_mode == 2:
        testall_hover(range)

    ########### test dictionary ############

    return testdictionary


########################## Act on the given dictionary ###############################

def action_on_Dictionary(testdictionary):

    for testitem in testdictionary["webdriverElement"]:

        if testitem["ancestorHoverElement"] == "null":
            continue
        if testitem["identity"] != "leave":
            continue
        for testancestorHoverElement in testitem["ancestorHoverElement"]:
            hover_screenshot(testancestorHoverElement)
        



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

wholecount = 1

testdictionary ={ 
"op": "clickAfterHover",
"webdriverElement": [ {"ancestorHoverElement": "header", "xpathTrue": "null" , "imagePath": "header", "description": "null" , "identity": "default"} ]
}

###### choose_mode = 1 for iterate_hover(hoverclassli), choose_mode = 2 for testall_hover(range) ######
choose_mode = 2

###### Give Dictionary ######
testdictionary = give_Dictionary(choose_mode, url, path)

print(testdictionary)

###### Act on the given dictionary ######
action_on_Dictionary(testdictionary)

