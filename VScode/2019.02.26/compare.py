#coding=utf-8
#author='Shichao-Dong'

from PIL import Image
import math
import operator
from functools import reduce

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

count = 1
itemnumber = 3
while (count < (itemnumber+1) ):
    print("Number "+str(count)+". item test")
    if(compare("./capture/partial_count"+str(count*2-1)+".png","./capture/partial_count"+str(count*2)+".png") < 20 ):
        print("Move to action doesn't work")
    else:
        print("Move to action does work")
    count = count + 1


