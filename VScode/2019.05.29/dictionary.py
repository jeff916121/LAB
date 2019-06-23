





testdictionary ={ 
"op": "clickAfterHover",
"webdriverElement": [ {"ancestorHoverElement": "header", "xpathTrue": "header" , "imagePath": "header"} ]
}

temp_dic = {"ancestorHoverElement": [13], "xpathTrue": "hi" , "imagePath": "try" } 

testdictionary["webdriverElement"].append(temp_dic)


print(testdictionary)

for element in testdictionary["webdriverElement"] :
  if element["ancestorHoverElement"] != "header":
    print(element)

