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


url="http://localhost:8080/0226.html"



driver = webdriver.Firefox()

driver.get(url)

# driver.maximize_window()

driver.set_window_size(800,600)

# driver.set_window_size(1918,912)

driversize= driver.get_window_size()

driverwidth = driversize['width']
driverheight = driversize['height']

print("driverwidth = "+str(driverwidth)+", driverheight = "+str(driverheight))








driver.save_screenshot("./capture/whole.png")
im = Image.open("./capture/whole.png")


imageratiox= im.size[0] / driverwidth
imageratioy= im.size[1] / driverheight
print(f'image:{im.size[0]}x{im.size[1]}')
print("imageratiox="+str(imageratiox)+"   imageratioy="+str(imageratioy))

############################## parsing ##############################


import requests

r=requests.get(url)
while True:
  if r.status_code == requests.codes.ok:
    # 以 BeautifulSoup 解析 HTML 程式碼
    soup = BeautifulSoup(r.text, 'html.parser')
    # html_doc = urlopen(url)
    # soup = BeautifulSoup(html_doc,'html.parser')
    break
#####################################################################


# def testcoordinate(webelementreference,imageratiox,imageratioy):
def testcoordinate(webelementreference):

  
  x_point = webelementreference.location['x']
  y_point = webelementreference.location['y']
  element_width  = webelementreference.size['width']
  element_height = webelementreference.size['height']

  

  print("x = "+str(x_point) + ", y = "+str(y_point) )
  print("width = "+str(element_width) + ", height = "+str(element_height))


  webelementreference.screenshot("./capture/whole_count1.png")
  # driver.save_screenshot("./capture/whole_count1.png")
  time.sleep(0.001)
  ActionChains(driver).move_to_element(webelementreference).perform()       
  time.sleep(0.001)
  # driver.save_screenshot("./capture/whole_count2.png")
  webelementreference.screenshot("./capture/whole_count2.png")

  ################## partial screenshot ##############################

  # left = float( (x_point)*1.5)
  # upper = float( (y_point)*1.5 )
  # right = float( (x_point+element_width )*1.5 )
  # lower = float( (y_point+element_height)*1.5 )

  # left = float( (x_point) )
  # upper = float( (y_point)  )
  # right = float( (x_point+element_width )  )
  # lower = float( (y_point+element_height)  )

  
  print( "left : " + str(left) + ", upper : " + str(upper) ) 
  print( " right : " + str(right) + ", lower = " + str(lower) )
  
  im = Image.open("./capture/whole_count1.png")
  im = im.crop( (left, upper, right, lower) )

  im.save("./capture/partial_count1.png")

  im = Image.open("./capture/whole_count2.png")

  im = im.crop( (left, upper, right, lower) )
  
  # im = im.crop(int(x), int(y), int(width), int(height))
  im.save("./capture/partial_count2.png")


testhoverclass = driver.find_element_by_class_name("container").find_element_by_class_name("box")

# testhoverclass.screenshot("C:/Taad/capture/whole3.png")

testcoordinate(testhoverclass) 
      