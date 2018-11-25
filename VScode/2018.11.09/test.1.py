

from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from PIL import ImageChops 


import time





url="http://localhost:8080/foodDropdownforAction.html"
# url="http://localhost:8080/hover.html"

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
         
         



   
driver = webdriver.Firefox()
driver.maximize_window()
 
driver.get(url)
 

count=0    


    
    
for item in ali:
              
    if (chooseMode==0):
        s1=driver.find_element_by_id(item)
    else:
        s1=driver.find_element_by_xpath("//select[@name='"+item+"']")
    
    location=s1.location
    size=s1.size
            
    print(location)
    print(size)

    ## to record time cost 
    # 計時開始
    tStart = time.time()
 
    
    driver.save_screenshot("./capture/capture1.png")

    ActionChains(driver).move_to_element(s1).perform() 

    driver.save_screenshot("./capture/capture2.png")  
    
    ActionChains(driver).click(s1).perform() 

    driver.save_screenshot("./capture/capture3.png")  
    

    x = location['x']+0.5*size['width']
    y = location['y']+0.5*size['height']
    width  = size['width']
    height = size['height']

    # magnify percentage
    controlsize=2

    im = Image.open("./capture/capture1.png")
    im = im.crop((int(x-controlsize*width), int(y-controlsize*height), int(x+controlsize*width), int(y+controlsize*height)))
    im.save("./capture/capture1partial.png")

    im = Image.open("./capture/capture2.png")
    im = im.crop((int(x-controlsize*width), int(y-controlsize*height), int(x+controlsize*width), int(y+controlsize*height)))
    im.save("./capture/capture2partial.png")

    im = Image.open("./capture/capture3.png")
    im = im.crop((int(x-controlsize*width), int(y-controlsize*height), int(x+controlsize*width), int(y+controlsize*height)))
    im.save("./capture/capture3partial.png")






def compare_images(path_one, path_two, diff_save_location):
    """
    比較圖片，如果有不同則生成展示不同的圖片
 
    @參數一: path_one: 第一張圖片的路徑
    @參數二: path_two: 第二張圖片的路徑
    @參數三: diff_save_location: 不同圖的保存路徑
    """
    image_one = Image.open(path_one)
    image_two = Image.open(path_two)
    try: 
        diff = ImageChops.difference(image_one, image_two)
 

        if diff.getbbox() is None:
        # 圖片間沒有任何不同則直接退出
            print("Didn't work")
            # print("【+】We are the same!")
        else:
            print("Works")
            diff.save(diff_save_location)
    except ValueError as e:
        text = ("表示圖片大小和box對應的寬度不一致，參考API説明：Pastes another image into this image."
                "The box argument is either a 2-tuple giving the upper left corner, a 4-tuple defining the left, upper, "
                "right, and lower pixel coordinate, or None (same as (0, 0)). If a 4-tuple is given, the size of the pasted "
                "image must match the size of the region.使用2緯的box避免上述問題")
        print("【{0}】{1}".format(e,text))


## compare with whole screenshot
# print("Move_to_element action:")
# compare_images("./capture/capture2.png","./capture/capture1.png","./capture/capturediff.png")

# print("Click action:")
# compare_images("./capture/capture3.png","./capture/capture2.png","./capture/capturediff.png")
  
print("Move_to_element action:")
compare_images("./capture/capture2partial.png","./capture/capture1partial.png","./capture/capturediff.png")

print("Click action:")
compare_images("./capture/capture3partial.png","./capture/capture2partial.png","./capture/capturediff.png")

#end of 模擬要測量的function
tEnd = time.time()#計時結束
#列印結果
print("It cost "+str(tEnd - tStart)+" sec" )#會自動做近位
