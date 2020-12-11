import os
import numpy as np

def main():
    f1 = open("./humanEva/human_eval.txt", 'r')
    contents=f1.readlines()
    dataDict={}

    totalEvent=0

    for line in contents:
        if "1;(5#1);(0#0);(0#0)" in line:
            totalEvent+=1
        key=line.split(":::")[0]
        value=float(line.split(":::")[1])
        
        if key in dataDict:
            dataDict[key].append(value)
        else:
            dataDict[key]=[value]
    
    newDict={}
    for key in dataDict:
        valueList=dataDict[key]
        
        argValue=sum(valueList)/len(valueList)
        
        
        
        stdVal=np.std(valueList)
        '''
        if key=="2;(5#1);(0#0);(0#0)":
            print("bingo")
        '''
        print(key)
        print("argValue: "+str(argValue))
        print("stdVal: "+str(stdVal))
        print("############")
        newDict[key]=(argValue,stdVal)
        
    
    sortedList=newDict.keys()
    sortedList.sort()
    
    stdList=[]
    
    for key in sortedList:
        print(key)
        print(newDict[key])
        stdList.append(newDict[key][1])
        
    print(totalEvent)
    print("std"+str(sum(stdList) / len(stdList) ))
    
    print("aa")
if __name__ == '__main__':
    main()   



