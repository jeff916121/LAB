

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


url="http://localhost:8080/foodDropdownforAction.html"
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



############################## parsing ##############################

html_doc = urlopen(url)
soup = BeautifulSoup(html_doc,'html.parser')


selsoup=soup.select('select')
 
 
ali = []
chooseMode=0
 
for sel in selsoup:

 
    dataTemp=str(sel)
    

    if(str(dataTemp).find('id=')!=-1):
     
        subData=dataTemp.split('id=\"',1)
        wantedData=subData[1].split('\"')
        ali.append(wantedData[0])
     
    else:
        subData=dataTemp.split('name=\"',1)

        wantedData=subData[1].split('\"')
        ali.append(wantedData[0])
        chooseMode=1
         
############################################################

wholecount=1    
partialcount=1
    
print(ali)

##################### monitor picture size #################

driver.save_screenshot("./capture/whole.png")
im = Image.open("./capture/whole.png")

imageratiox= im.size[0] / driverwidth
imageratioy= im.size[1] / driverheight

print("imageratiox="+str(imageratiox)+"   imageratioy="+str(imageratioy))

###############################################################################

########################### finding element and testing #######################

for item in ali:
              

    
    ################### finding element ####################################    

    s1=driver.find_element_by_id(item)


    ####################### to record time cost #######################
    # 計時開始
    tStart = time.time()
 
    ####################### whole screenshot  ###############################


    driver.save_screenshot("./capture/whole_count"+str(wholecount*2-1)+".png")
    # time.sleep(1)
    # ActionChains(driver).reset_actions()

    ActionChains(driver).move_to_element(s1).perform() 
    # time.sleep(1)
    driver.save_screenshot("./capture/whole_count"+str(wholecount*2)+".png")


    wholecount = wholecount + 1

    ##########################################################################

    ################## partial screenshot ##############################

    print(s1.location)
    print(s1.size)

    x = s1.location['x']+0.5*s1.size['width']
    y = s1.location['y']+0.5*s1.size['height']
    width  = s1.size['width']
    height = s1.size['height']

    print("x="+str(x))
    print("y="+str(y))
    print("width="+str(width))
    print("height="+str(height))

    # magnify percentage
    controlsize=0.5
    # im.crop（left, upper, right, lower）



    im = Image.open("./capture/whole_count"+str(partialcount*2-1)+".png")
    im = im.crop(( int((x-controlsize*width)*imageratiox ) , int((y-controlsize*height)*imageratioy) , int((x+controlsize*width)*imageratiox) , int((y+controlsize*height)*imageratioy) ))
    # im = im.crop(int(x), int(y), int(width), int(height))
    im.save("./capture/partial_count"+str(partialcount*2-1)+".png")


    im = Image.open("./capture/whole_count"+str(partialcount*2)+".png")
    im = im.crop(( int((x-controlsize*width)*imageratiox ) , int((y-controlsize*height)*imageratioy) , int((x+controlsize*width)*imageratiox) , int((y+controlsize*height)*imageratioy) ))
    im.save("./capture/partial_count"+str(partialcount*2)+".png")


    partialcount = partialcount + 1


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

##########################################################################################



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

count = 1
itemnumber = 3
range = 35

print ( partial_compare( count , itemnumber , range ) )

#end of 模擬要測量的function
tEnd = time.time()#計時結束
#列印結果
print("It cost "+str(tEnd - tStart)+" sec" )#會自動做近位
