

from bs4 import BeautifulSoup
from urllib.request import urlopen



url="http://localhost:8080/foodDropdownforAction.html"

html_doc = urlopen(url)
soup = BeautifulSoup(html_doc,'html.parser')

# print(str(soup).replace(u'\xbb', u' '))



# selsoup=soup.find_all('select', {'class:select'})
# selsoup=soup.select('select',{'class':'select'})
selsoup=soup.select('select')
 
# print(selsoup)
 
ali = []
chooseMode=0
 
for sel in selsoup:
#     f=open('sel',''r'')
#     data = f.read()
#     print(data)
 
#     print(type(sel))
#     print(sel)
 
    dataTemp=str(sel)
#     print(dataTemp)
     
    if(str(dataTemp).find('id=')!=-1):
     
        subData=dataTemp.split('id=\"',1)
        wantedData=subData[1].split('\"')
        ali.append(wantedData[0])
     
    else:
        subData=dataTemp.split('name=\"',1)
#         print(subData)
        wantedData=subData[1].split('\"')
        ali.append(wantedData[0])
        chooseMode=1
         
         
      
     
# for item in ali:
#     print(item) 
  
  
  
#  
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

    
    
   
driver = webdriver.Firefox()
driver.maximize_window()
 
# driver.get("file:///C:/Users/張道寬/eclipse-workspace/test-python/my_package/food.html")
   
driver.get(url)
 

print("\n")
 
   
       
count=0    


    
    
for item in ali:
     
    print(item+"類選中:", end="")
    print("\n")
          
    if (chooseMode==0):
        s1=driver.find_element_by_id(item)
    else:
        s1=driver.find_element_by_xpath("//select[@name='"+item+"']")
    
    #     Select(s1);
        
        
    #     actions = ActionChains(driver)    
    #     actions.move_to_element(s1)
    #     actions.click(s1)
    #     actions.perform()
        
    
        
    ActionChains(driver).move_to_element(s1).perform() 
    driver.save_screenshot("./capture/capture1.png")  

    ActionChains(driver).click(s1).perform() 
    driver.save_screenshot("./capture/capture2.png")  




#         
#     ActionChains(driver).click(s1).perform() 
#     driver.save_screenshot("./capture/capture3.png")  
    
    



from PIL import Image
from PIL import ImageChops 

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
            print("【+】We are the same!")
        else:
            diff.save(diff_save_location)
    except ValueError as e:
        text = ("表示圖片大小和box對應的寬度不一致，參考API説明：Pastes another image into this image."
                "The box argument is either a 2-tuple giving the upper left corner, a 4-tuple defining the left, upper, "
                "right, and lower pixel coordinate, or None (same as (0, 0)). If a 4-tuple is given, the size of the pasted "
                "image must match the size of the region.使用2緯的box避免上述問題")
        print("【{0}】{1}".format(e,text))

  
    
compare_images("./capture/capture2.png","./capture/capture1.png","./capture/capturediff.png")