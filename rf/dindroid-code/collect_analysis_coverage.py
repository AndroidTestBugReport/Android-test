import os
from xml.dom.minidom import Document
from xml.dom import minidom

def main():
    targetFile="anymemo-stable-8.3"
    
    
    
    fileList=os.listdir("/home/yu/workspace2/rf-android/signalCNN/trainResult")

    ############build rfSet
    rfSet=set()
    
    rfTextSet=set()
    
    for fileName in os.listdir("/home/yu/workspace2/rf-android/signalCNN/trainResult"):
        if targetFile+"_record" in fileName:
            filePath="/home/yu/workspace2/rf-android/signalCNN/trainResult/"+fileName
            #readFile = open(filePath, 'r')
            #contents=readFile.readlines()
            
            doc=minidom.parse(filePath)
            recordRoot=doc.documentElement
            
            
            bbList = recordRoot.getElementsByTagName('Classname')
            
            for itemEle in bbList:
                className=itemEle.firstChild.nodeValue
                #print(className)
                rfSet.add(className)
                
                
            bb2List=recordRoot.getElementsByTagName('viewtext')
            for itemEle in bb2List:
                textValue=itemEle.firstChild.nodeValue.lower()
                rfTextSet.add(textValue)
                
    ###########anaylze monkey
    path="/home/yu/workspace2/reinfocement-exploration/monkey/"
    fileName=targetFile+"_logcat"
    
    readFile = open(path+fileName, 'r')
                        
    contents=readFile.readlines()
    
    for key in rfSet:
        match=False
        for line in contents:
            if key in line:
                match=True
                break
            
        if not match:
            print("Monkey no find")
            print(key)
            
    print("bingo")
    
    ##########analyze sap
    path="/home/yu/workspace2/reinfocement-exploration/sapienze/"
    fileName=targetFile+"_logcat"
    
    readFile = open(path+fileName, 'r')
                        
    contents=readFile.readlines()
    
    for key in rfSet:
        match=False
        for line in contents:
            try:
                if key in line:
                    match=True
                    break
            except:
                a=1
                #print("exception")
            
        if not match:
            print("Sap no find")
            print(key)
            
    print("bingo")
    ##########analyze stoat
    
    
    
    
    
    
    path="/home/yu/workspace2/reinfocement-exploration/stoat123/"
    fileName=targetFile
    
    readFile = open(path+fileName, 'r')
                        
    contents=readFile.readlines()
    
    for key in rfSet:
        
        key=key.replace("/","")
        match=False
        for line in contents:
            try:
                if key in line:
                    match=True
                    break
            except:
                a=1
                #print("exception")
            
        if not match:
            print("Stoat no find")
            print(key)
            
    print("bingo")
    
    
    path="/SPACE/reforce-project/dataset/stoat/finished/"
    
    filePath0=path+targetFile+"/stoat_fsm_output/"
    filePath1=path+targetFile+"/stoat_mcmc_sampling_output/"
    
    readFile1 = open(filePath0+"all_action_execution_history.txt", 'r')
    readFile2 = open(filePath1+"test_suite_to_execute.txt", 'r')

    contents1=readFile1.readlines()
    for line in contents1:
        for key in rfTextSet:
            try:
                if key in line.lower():
                    rfTextSet.remove(key)
                    break
            except:
                a=1
    
    
    contents2=readFile1.readlines()
    for line in contents2:
        for key in rfTextSet:
            try:
                if key in line.lower():
                    rfTextSet.remove(key)
                    break
            except:
                a=1
    for key in rfTextSet:
        print(key)

    
if __name__ == '__main__':
    main()   



