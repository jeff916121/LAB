
from PIL import Image
from functools import reduce

import math
import operator

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

def partial_compare(range):

    global wholecount, path
    
    compare_count = 1
    print("partial compare turn")
    while (compare_count <= wholecount ):
        # print("Number "+str(compare_count)+". item test")

        try:
            temp = compare(path+"/partial_count"+str(compare_count*2-1)+".png",path+"/partial_count"+str(compare_count*2)+".png")   
        except: 
            compare_count = compare_count + 1
            continue

        if(compare_count==2):
            result = temp

        if( temp >= range ):
            print(str(compare_count*2-1)+" and "+str(compare_count*2)+" move to action does work")
        compare_count = compare_count + 1

#######################################################

wholecount = 102
range = 35
path = "./capture"

partial_compare( range ) 
