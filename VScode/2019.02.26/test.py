

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


driver = webdriver.Firefox()
driver.maximize_window()


driversize= driver.get_window_size()

driverwidth = driversize['width']
driverheight = driversize['height']

print("driverwidth="+str(driverwidth)+" driverheight="+str(driverheight))


driver.get(url)


############################## parsing ##############################

html_doc = urlopen(url)
soup = BeautifulSoup(html_doc,'html.parser')

# print(soup)

peekstyle =  soup.find('style')

print( str(peekstyle) )

hoverclassli = []

subData=str(peekstyle).split('.')

print( str(subData) )

serachwords = ":hover"

if(subData.__contains__)


# for sel in selsoup:

 
#     dataTemp=str(sel)
    

#     if(str(dataTemp).find('id=')!=-1):
     
#         subData=dataTemp.split('id=\"',1)
#         wantedData=subData[1].split('\"')
#         ali.append(wantedData[0])
     
#     else:
#         subData=dataTemp.split('name=\"',1)

#         wantedData=subData[1].split('\"')
#         ali.append(wantedData[0])
#         chooseMode=1
         
############################################################
