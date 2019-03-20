

# from bs4 import BeautifulSoup
# from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from PIL import ImageChops 



import math
import operator
from functools import reduce

import time

import requests
from bs4 import BeautifulSoup

url="https://irs.thsrc.com.tw/IMINT/"

# r = requests.get(url)






driver = webdriver.Firefox()
driver.maximize_window()

import time

# 計時開始
tStart = time.time()

driver.get(url)


# ############################## parsing ##############################

r=requests.get(url)

if r.status_code == requests.codes.ok:
  # 以 BeautifulSoup 解析 HTML 程式碼
  soup = BeautifulSoup(r.text, 'html.parser')

print(soup)

#end of 模擬要測量的function
tEnd = time.time()#計時結束
#列印結果
print("It cost "+str(tEnd - tStart)+" sec" )#會自動做近位

