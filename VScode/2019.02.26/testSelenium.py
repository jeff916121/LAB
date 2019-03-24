

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


url="https://irs.thsrc.com.tw/IMINT/"
# url="http://localhost:8080/hover.html"

driver = webdriver.Firefox()
driver.maximize_window()
# driver.set_window_size(1920,910)

driversize= driver.get_window_size()

driverwidth = driversize['width']
driverheight = driversize['height']

print("driverwidth="+str(driverwidth)+" driverheight="+str(driverheight))

# driver.set_window_size(driverwidth,driverheight)
driver.get(url)

time.sleep(0.001)

############################## parsing ##############################

soup = BeautifulSoup(driver.page_source,'html.parser')

tStart = time.time() 
driver.save_screenshot("./capture/1.png")
tEnd = time.time()  #計時結束

print(soup)

# #列印結果
print("It cost "+str(tEnd - tStart)+" sec" )    #會自動做近位



