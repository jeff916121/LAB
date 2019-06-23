

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from PIL import ImageChops 



import math
import operator
from functools import reduce

import time



url="https://web.ee.ntu.edu.tw/"
path = "./capture"

driver = webdriver.Firefox()
driver.maximize_window()

driver.get(url)

driversize= driver.get_window_size()

# driverwidth = driversize['width']
# driverheight = driversize['height']

# print("driverwidth="+str(driverwidth)+" driverheight="+str(driverheight))




############################## parsing ##############################


import requests

r=requests.get(url)

while True:
  if r.status_code == requests.codes.ok:
    # 以 BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, 'html.parser')
    break

# print(soup)


peekstyle =  soup.find('style')

# print( str(peekstyle) )

hoverclassli = []

subData=str(peekstyle).split('.')

# print( str(subData) )

searchwords = ":hover"

for name in subData:
  if (searchwords in name):
    
    hoverclassli.append((name.split(':',1))[0])

print(hoverclassli)


#####################################################################

wholecount=1    
  
def hover_screenshot(webelementreference):

    global wholecount
    webelementreference.screenshot(path+"/partial_count"+str(wholecount*2-1)+".png")
#   driver.save_screenshot(path+"/whole_count"+str(wholecount*2-1)+".png")

    time.sleep(0.1)

#   time.sleep(0.001)


    ActionChains(driver).move_to_element(webelementreference).perform()       


    time.sleep(0.1)

    webelementreference.screenshot(path+"/partial_count"+str(wholecount*2)+".png")
    #   driver.save_screenshot(path+"/whole_count"+str(wholecount*2)+".png")

    wholecount = wholecount + 1
    
################### finding element ####################################    

print( hoverclassli[0] + " 類 ")
s1=driver.find_elements_by_class_name(str(hoverclassli[0]))
print( hoverclassli[0] + " 類 共有 "+str(len(s1))+" 個")

def Rhover_screenshot(s1):

    subclasslist = s1.find_elements_by_xpath("./*")

    print( hoverclassli[0] + " 類 共有 "+str(len(subclasslist))+" 個")

    if not subclasslist:
        # hover_screenshot(s1)
        return

    hover_screenshot(s1)

    for subclass in subclasslist:
        Rhover_screenshot(subclass)

# for s1_item in s1:

#     Rhover_screenshot(s1_item)


s1=driver.find_elements_by_class_name("space")


print( "    " + str(s1[0].get_attribute("class")) + ":" + str(s1[0].get_attribute("innerText")))


subclasslist = s1[0].find_elements_by_xpath("./*")


print( "    " + str(subclasslist[0].get_attribute("class")) + ":" + str(subclasslist[0].get_attribute("innerText")))

subclasslist_item = subclasslist[0].find_elements_by_xpath("./*")

print( "    " + str(subclasslist_item[0].get_attribute("class")) + ":" + str(subclasslist_item[0].get_attribute("innerText")))

subclasslist_item2 = subclasslist_item[0].find_elements_by_xpath("./*")

print( "    " + str(subclasslist_item2[0].get_attribute("class")) + ":" + str(subclasslist_item2[0].get_attribute("innerText")))





