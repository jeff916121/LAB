

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
  global driver
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
s1=driver.find_elements_by_class_name(hoverclassli[0])
print( hoverclassli[0] + " 類 共有 "+str(len(s1))+" 個")


for subclass in s1:
    subclasslist = subclass.find_elements_by_tag_name("*")

    for subclassitem in subclasslist:  
        if(len(subclassitem.find_elements_by_tag_name("*"))>=1):
            continue
        hover_screenshot(subclassitem) 




######################################################################################

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

def partial_compare(count,itemnumber,range):

    print("partial compare turn")
    while (count < (itemnumber+1) ):
        print("Number "+str(count)+". item test")
        temp = compare(path+"/partial_count"+str(count*2-1)+".png",path+"/partial_count"+str(count*2)+".png")
        
        if(count==2):
            result = temp

        if( temp < range ):
            print("Move to action doesn't work")
        else:
            print("Move to action does work")
        count = count + 1

    # return result
#######################################################


  
#################### whole compare #####################

def whole_compare(count,itemnumber,range):
    print("whole compare turn")
    while (count < (itemnumber+1) ):
        print("Number "+str(count)+". item test")
        result = compare(path+"/whole_count"+str(count*2-1)+".png",path+"/whole_count"+str(count*2)+".png")
        if( result < range ):
            print("Move to action doesn't work")
        else:
            print("Move to action does work")
        count = count + 1
    return result

#######################################################


# count = 1
# itemnumber = 2
# range = 35

# print ( partial_compare( count , itemnumber , range ) )

# #end of 模擬要測量的function
# tEnd = time.time()#計時結束
# #列印結果
# # print("It cost "+str(tEnd - tStart)+" sec" )#會自動做近位

