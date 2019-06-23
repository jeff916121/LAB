
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


def screenshot_hover(hoverclassli):

    for hover_class_name in hoverclassli:
                
        ################### finding element ####################################    

        s1=driver.find_elements_by_class_name(hover_class_name)
        
        print( hover_class_name + " 類 共有 "+str(len(s1))+" 個")

    
        for subclass in s1:

            hover_screenshot(subclass) 
            print( "  " + subclass.get_attribute("class")  )
            subclasslist = subclass.find_elements_by_tag_name("*")
            # print( "  "  + "有 "+str(len(subclasslist))+"個 children")

            for subclassitem in subclasslist:  
                if(len(subclassitem.find_elements_by_tag_name("*"))>=1):
                    continue
                print( "    " + str(subclassitem.get_attribute("class")) + ":" + str(subclassitem.get_attribute("innerText")))
                hover_screenshot(subclassitem) 

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

    global wholecount, path
    
    compare_count = 1
    print("partial compare turn")
    while (compare_count <= wholecount ):
        try:
            temp = compare(path+"/partial_count"+str(compare_count*2-1)+".png",path+"/partial_count"+str(compare_count*2)+".png")   
            if( temp >= range ):
                print(str(compare_count*2-1)+" and "+str(compare_count*2)+" move to action does work")
                compare_count = compare_count + 1
            else:
                try:
                    Image.open(path+"/partial_count"+str(compare_count*2-1)+".png")
                    os.remove(path+"/partial_count"+str(compare_count*2-1)+".png")
                    Image.open(path+"/partial_count"+str(compare_count*2)+".png")
                    os.remove(path+"/partial_count"+str(compare_count*2)+".png")
                    compare_count = compare_count + 1
                except:
                    compare_count = compare_count + 1
                    continue
           
        except:     
            try:
                Image.open(path+"/partial_count"+str(compare_count*2-1)+".png")
                os.remove(path+"/partial_count"+str(compare_count*2-1)+".png")
                Image.open(path+"/partial_count"+str(compare_count*2)+".png")
                os.remove(path+"/partial_count"+str(compare_count*2)+".png")
                compare_count = compare_count + 1
            except:
                compare_count = compare_count + 1
                continue

#######################################################

def testall_hover():
    
    ################### finding element ####################################    

    global driver
    s1 = driver.find_elements_by_xpath("/html/body/*")

    if not s1:
        return 

    for subclass in s1:

        if not subclass:
            continue

        hover_screenshot(subclass) 
        # print( "  " + subclass.get_attribute("class")  )
        subclasslist = subclass.find_elements_by_tag_name("*")
        # print( "  "  + "有 "+str(len(subclasslist))+"個 children")

        if not subclasslist:
            continue

        for subclassitem in subclasslist:  
           
            if not subclassitem:
                continue
           
            if(len(subclassitem.find_elements_by_tag_name("*"))>=1):
                continue
            # print( "    " + str(subclassitem.get_attribute("class")) + ":" + str(subclassitem.get_attribute("innerText")))
           
           
            hover_screenshot(subclassitem) 


############################## main method ##############################



############## setting environment ##################

# url="https://programming.ee.ntu.edu.tw/#/home"
# url = "https://zh.wikipedia.org/wiki/%E7%A3%81"
url="https://web.ee.ntu.edu.tw/"

path = "./capture"

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

# screenshot_hover(hoverclassli)
testall_hover()

##############################

range = 35

partial_compare(range)


