
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

def dropdown_screenshot(webelementreference):

    global wholecount
    global driver

    try: 
        webelementreference.screenshot(path+"/partial_count"+str(wholecount*2-1)+".png")
        time.sleep(0.01)
        ActionChains(driver).click(webelementreference).perform()       
        time.sleep(0.01)
        webelementreference.screenshot(path+"/partial_count"+str(wholecount*2)+".png")
        wholecount = wholecount + 1
    except:
        return


def maintain_temp_dic(hovertype,ancestorHoverElement,xpathTrue,subclass,identity):

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

    temp_dic = {"hovertype" : hovertype, "ancestorHoverElement": ancestorHoverElement, "xpathTrue": xpathTrue , "imagePath": image_Path , "innerText": innerText, "identity": identity, \
        "xpos": xpos, "ypos": ypos, "width": width, "height": height, "xPercentage": str(round(xPercentage)) + '%', "yPercentage": str(round(yPercentage)) + '%', \
        "wp": str(round(wp)) + '%', "hp": str(round(hp)) + '%'     }

    return temp_dic

def iterate_hover(hoverclassli):

    global driver

   

    for hover_class_name in hoverclassli:
                
        ################### get hover class name ######################   

        s1=driver.find_elements_by_class_name(hover_class_name)
        
       

        for subclass in s1:

            ancestorHoverElement = []
            xpathTrue = "/"

            recursive_hover(subclass,ancestorHoverElement,xpathTrue,"root")
    



def recursive_hover(subclass,ancestors,xpath,identity):

    global testdictionary

    ancestorHoverElement =  ancestors.copy()
    ancestorHoverElement.append(subclass)

    xpathTrue = xpath
    xpathTrue = xpathTrue + str(subclass.tag_name) + "/"
    

    subclasslist = subclass.find_elements_by_xpath("./*")

    if len(subclasslist)<1: # leaf
   
        temp_dic = maintain_temp_dic("hover element",ancestorHoverElement,xpathTrue,subclass,"leaf")
        testdictionary["webdriverElement"].append(temp_dic)
        return
    
    temp_dic = maintain_temp_dic("hover element",ancestorHoverElement, xpathTrue, subclass, identity)
    testdictionary["webdriverElement"].append(temp_dic)

    for subclassitem in subclasslist:  

        if len(subclassitem.find_elements_by_xpath("./*")) < 1 :

            temp_xpath = xpathTrue
            temp_ancestors = ancestorHoverElement.copy()

            temp_ancestors.append(subclassitem)
            temp_xpath = temp_xpath + str(subclassitem.tag_name) + "/"


            temp_dic = maintain_temp_dic("hover element",temp_ancestors, temp_xpath, subclassitem, "leaf")
            testdictionary["webdriverElement"].append(temp_dic)

            continue


        recursive_hover(subclassitem,ancestorHoverElement,xpathTrue, "internal node")
        ancestorHoverElement =  ancestors.copy()
        xpathTrue = xpath    

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

def partial_compare(range_given):

    global wholecount
    compare_count = wholecount - 1
    
    
    # print("partial compare turn")
    
    try:
        temp = compare(path+"/partial_count"+str(compare_count*2-1)+".png",path+"/partial_count"+str(compare_count*2)+".png")   
        # print(temp)
        if( temp > range_given ):
            # print(str(compare_count*2-1)+" and "+str(compare_count*2)+" move to action does work")
            
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


def maintain_dic(hovertype,ancestorHoverElement,xpathTrue,subclass,identity):
    global testdictionary

    temp_dic = maintain_temp_dic(hovertype,ancestorHoverElement,xpathTrue,subclass,identity)
    testdictionary["webdriverElement"].append(temp_dic)

def compare_detect_hover_and_maintain_dic(range_given,ancestorHoverElement,xpathTrue,subclass,identity):

    hover_screenshot(subclass) 
    flag = partial_compare(range_given)
    
    if flag:

        maintain_dic("hover element",ancestorHoverElement,xpathTrue,subclass,identity)
    # else:
    #     dropdown_screenshot(subclass) 
    #     flag = partial_compare(range_given)
    #     if flag:
    #         maintain_dic("dropdownlist",ancestorHoverElement,xpathTrue,subclass,identity)


def testall_hover(range_given):
    
    ################### finding element ####################################    

    global driver

    s1 = driver.find_elements_by_xpath("/html/body/*")

    for subclass in s1:

        xpathTrue = "/html/body/"

        recursive_testall_hover(range_given,subclass,[],xpathTrue,"root")


def recursive_testall_hover(range_given,subclass,ancestors,xpath,identity):

    global testdictionary

    if not subclass:

        return

    

    ancestorHoverElement =  ancestors.copy()
    ancestorHoverElement.append(subclass)

    xpathTrue = xpath
    xpathTrue = xpathTrue + str(subclass.tag_name) + "/"

    subclasslist = subclass.find_elements_by_xpath("./*")

    if len(subclasslist) < 1 :

        compare_detect_hover_and_maintain_dic(range_given,ancestorHoverElement,xpathTrue,subclass,"leaf")
                 
        return
        
    compare_detect_hover_and_maintain_dic(range_given,ancestorHoverElement,xpathTrue,subclass,identity)

    for subclassitem in subclasslist:  

        if len(subclassitem.find_elements_by_xpath("./*")) < 1 :

            temp_xpath = xpathTrue
            temp_ancestors = ancestorHoverElement.copy()

            temp_ancestors.append(subclassitem)
            temp_xpath = temp_xpath + str(subclassitem.tag_name) + "/"


            compare_detect_hover_and_maintain_dic(range_given,temp_ancestors,temp_xpath,subclassitem,"leaf")

            # print("Come in")

            continue


        recursive_testall_hover(range_given,subclassitem,ancestorHoverElement,xpathTrue, "internal node")
        ancestorHoverElement =  ancestors.copy()
        xpathTrue = xpath         

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

    range_given = 8

    if choose_mode == 1:
        hoverclassli = parsing_hover(soup)
        iterate_hover(hoverclassli)
    if choose_mode == 2:
        testall_hover(range_given)

    ########### test dictionary ############

    


########################## Act on the given dictionary ###############################

def action_on_Dictionary(testdictionary):

    for testitem in testdictionary["webdriverElement"]:

        if testitem["ancestorHoverElement"] == "null":
            continue
        if testitem["identity"] != "leaf":
            continue
        for testancestorHoverElement in testitem["ancestorHoverElement"]:
            if testitem["hovertype"] == "hover element":
                hover_screenshot(testancestorHoverElement)
            elif testitem["hovertype"] == "dropdownlist":
                dropdown_screenshot(testancestorHoverElement)
            
        # print("change another element")


############################## main method ##############################


############## setting environment ##################

# url = "https://programming.ee.ntu.edu.tw"
# url = "https://web.ee.ntu.edu.tw/"
# url = "https://zh.wikipedia.org/"
# url = "https://www.google.com.tw/"

url = "https://ceiba.ntu.edu.tw"
# url = "https://www.facebook.com/"
# url = "https://www.baidu.com/"
# url = "https://www.iii.org.tw/"
# url = "https://www.eztravel.com.tw/"
# url = "https://www.mirrorfiction.com/"

# url = "http://192.168.56.1:8080/Hover.html"

path = "./capture/"

driver = webdriver.Firefox()
driver.maximize_window()
driver.get(url)

wholecount = 1

testdictionary ={ 
    "op": "clickAfterHover",
    "webdriverElement": [ {"hovertype" : "null","ancestorHoverElement": "null", "xpathTrue": "null" , "imagePath": "null" , "innerText": "null", "identity": "null", \
        "xpos": "null", "ypos": "null", "width": "null", "height": "null", "xPercentage": "null (%)", "yPercentage": "null (%)", \
        "wp": "null (%)", "hp": "null (%)"} ]
    }

###### choose_mode = 1 for iterate_hover(hoverclassli), choose_mode = 2 for testall_hover(range_given) ######
choose_mode = 2

###### Give Dictionary ######
give_Dictionary(choose_mode, url, path)

# print(testdictionary)

# 開啟檔案
fp = open("dictionary.txt", "w")

# 寫入 This is a testing! 到檔案
fp.write(str(testdictionary).encode("utf8").decode("cp950", "ignore"))
 
# 關閉檔案
fp.close()

print("Begin testing")

###### Act on the given dictionary ######
action_on_Dictionary(testdictionary)

