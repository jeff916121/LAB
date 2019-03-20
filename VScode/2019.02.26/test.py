

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

# url="https://programming.ee.ntu.edu.tw/#/home"

url="https://web.ee.ntu.edu.tw/"

# url = "https://zh.wikipedia.org/wiki/%E7%A3%81"


driver = webdriver.Firefox()
# driver.maximize_window()

driver.get(url)

driversize= driver.get_window_size()

driverwidth = driversize['width']
driverheight = driversize['height']

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



driver.save_screenshot("./capture/whole.png")
im = Image.open("./capture/whole.png")

imageratiox= im.size[0] / driverwidth
imageratioy= im.size[1] / driverheight

# print("imageratiox="+str(imageratiox)+"   imageratioy="+str(imageratioy))

  
def hover_screenshot(wholecount,webelementreference,imageratiox,imageratioy):

  partialcount = wholecount
  # webelementreference.screenshot("./capture/partial_count"+str(wholecount*2-1)+".png")
  driver.save_screenshot("./capture/whole_count"+str(wholecount*2-1)+".png")
  time.sleep(0.001)
  ActionChains(driver).move_to_element(webelementreference).perform()       
  time.sleep(0.001)
  # webelementreference.screenshot("./capture/partial_count"+str(wholecount*2)+".png")
  driver.save_screenshot("./capture/whole_count"+str(wholecount*2)+".png")
  wholecount = wholecount + 1

  ################## partial screenshot ##############################

  x = webelementreference.location['x']
  y = webelementreference.location['y']
 
  width  = webelementreference.size['width']
  height = webelementreference.size['height']

  left = float( (x)*1.5 )
  upper = float( (y)*1.5 )
  right = float( (x+width )*1.5 )
  lower = float( (y+height )*1.5 )


  # print("x="+str(x))
  # print("y="+str(y))
  # print("width="+str(width))
  # print("height="+str(height))

  
  # im.crop（left, upper, right, lower）



  im = Image.open("./capture/whole_count"+str(partialcount*2-1)+".png")
  # im = im.crop(( int((x-controlsize*width)*imageratiox ) , int((y-controlsize*height)*imageratioy) , int((x+controlsize*width)*imageratiox) , int((y+controlsize*height)*imageratioy) ))
  # im = im.crop(int(x), int(y), int(width), int(height))
  im = im.crop( (left, upper, right, lower) )
  im.save("./capture/partial_count"+str(partialcount*2-1)+".png")


  im = Image.open("./capture/whole_count"+str(partialcount*2)+".png")
  im = im.crop( (left, upper, right, lower) )
  im.save("./capture/partial_count"+str(partialcount*2)+".png")


  partialcount = partialcount + 1

  return wholecount



testhoverclass = driver.find_elements_by_class_name(hoverclassli[0])[0].find_elements_by_class_name(hoverclassli[1])
if(len(testhoverclass)>=1):
  hoverclassli.remove(hoverclassli[1])



for hover_class_name in hoverclassli:
              

    
    ################### finding element ####################################    

    s1=driver.find_elements_by_class_name(hover_class_name)
    print( hover_class_name + " 類 共有 "+str(len(s1))+" 個")

    # print(s1)

    

    for subclass in s1:

      wholecount = hover_screenshot(wholecount,subclass,imageratiox,imageratioy) 
      
      print( "  " + subclass.get_attribute("class")  )

      subclasslist = subclass.find_elements_by_tag_name("*")

      print( "  "  + "有 "+str(len(subclasslist))+"個 children")
      for subclassitem in subclasslist:
        
        if(len(subclassitem.find_elements_by_tag_name("*"))>=1):
          continue
        # print( "subclassitem : " + str(type(subclassitem)) + " subclassitem.text : " + str(type(subclassitem.text)))
        print( "    " + str(subclassitem.get_attribute("class")) + ":" + str(subclassitem.get_attribute("innerText")))

        wholecount = hover_screenshot(wholecount,subclassitem,imageratiox,imageratioy)




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
        temp = compare("./capture/partial_count"+str(count*2-1)+".png","./capture/partial_count"+str(count*2)+".png")
        
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
        result = compare("./capture/whole_count"+str(count*2-1)+".png","./capture/whole_count"+str(count*2)+".png")
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