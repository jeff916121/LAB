
custom_number = 2 
pageNumber= 18


i = 0
stringOdd = ""
stringEven= ""


j= int(pageNumber/(custom_number*2))
j=j*2

count=0

# print(j)

if(count*8<pageNumber):
    if(pageNumber>=((j+2)*custom_number-(custom_number-1))):    
        stringEven = stringEven + str((j+2)*custom_number-(custom_number-1)) +"-"+str(pageNumber)+"," 
        if((pageNumber%custom_number)!=0):
            stringEven = stringEven +"要分頁喔\n"

while (count!=int(pageNumber/(custom_number*2))):
    if (pageNumber>=(i*custom_number+custom_number)):
        stringOdd = stringOdd + str(i*custom_number+1) +"-"+str(i*custom_number+custom_number) +","
        
        
    if (pageNumber>=(j*custom_number)):    
        stringEven = stringEven + str(j*custom_number-(custom_number-1)) +"-"+str(j*custom_number) +","
        
       
    i=i+2
    j=j-2
    count=count+1  
      
# print(count)    
    
if(count*custom_number*2<pageNumber):
    if(i*custom_number+custom_number>=pageNumber):
        
        stringOdd=stringOdd+ str(i*custom_number+1) +"-"+str(pageNumber) 
        stringOdd=stringOdd+"!!!最上面那一張要從反面列印的紙堆中抽出喔"
        
    else:
        stringOdd=stringOdd+ str(i*custom_number+1) +"-"+str(i*custom_number+custom_number) 
    
print("正面" + str(custom_number) + "合一列印編號:")    
print(stringOdd)
print("")
print("反面" + str(custom_number) + "合一列印編號:")
print(stringEven)


