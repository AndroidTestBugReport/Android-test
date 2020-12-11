import os


def computeLineCoverage(filePath):

    #f1=open("./emmaOutput.txt")
    
    f1=open(filePath)
    
    contents=f1.readlines()
    
    lineCoverageNew=0
    methodCoverageNew=0
    classCoverageNew=0#class is not the activity
    
    for line in contents:
        if "(" in line:
            for i in range(0,4):
                index=line.find("%")
                
                pointer=index
                numStr=""
                while(1):
                    pointer-=1
                    if line[pointer].isdigit():
                        numStr=line[pointer]+numStr
                    else:break
                    
                line=line[index+1:]
                
                
                if i==0:
                    classCoverageNew=int(numStr)
                
                if i==1:
                    methodCoverageNew=int(numStr)
                        
                    
                if i==3:
                    lineCoverageNew=int(numStr)
            break
            
    f1.close()
    return lineCoverageNew



def main():
    dataDict={}
    '''
    monkeyFileNameList=[]
    
    ###############store monkey file name
    for fileName in os.listdir("/home/yu/workspace2/reinfocement-exploration/monkey"):
        monkeyFileNameList
    ''' 
    
    
    fileList=os.listdir("/home/yu/workspace2/rf-android/signalCNN/trainResult")
    
    for fileName in os.listdir("/home/yu/workspace2/rf-android/signalCNN/trainResult"):
        ########for the reforcement train
        if "_coverage_2" in fileName:
            strIndex=fileName.find("_coverage_2")
            fileSp=fileName[0:strIndex]
            
            if not fileSp in dataDict:
                dataDict[fileSp]=[0,0,0,0]###first is R, second is monkey,third is stoat, fouth is sap
                ####explore stoat
                
                
            #oldTrainCoverage=dataDict[fileSp][0]
            
            trainPath="/home/yu/workspace2/rf-android/signalCNN/trainResult/"+fileSp
            logHistory=""
            uniqueCrashNum=0
                
            trainFile=trainPath+"_eventNum_"+str(2)+".txt"
            readFile = open(trainFile, 'r')
                
            contents=readFile.readlines()
            eventNum=int(contents[0])
                
            dataDict[fileSp][0]=eventNum
            
            ########for the monkey
            if dataDict[fileSp][1]==0:
                try:
                    
                    eventNumMonkey=0
                    
                    path="/home/yu/workspace2/reinfocement-exploration/monkey/"
                    fileName=fileSp
                    
                    monkeyPath=path+fileName
                    
                    readFile = open(monkeyPath, 'r')
                    
                    contents=readFile.readlines()
                    
                    for line in contents:
                        if "Sending" in line :
                            eventNumMonkey+=1
                        
                        
                    
                    dataDict[fileSp][1]=eventNumMonkey
                except:
                    print("Monkey not found: "+monkeyPath)
            ########for the stoat
            if dataDict[fileSp][2]==0:
                logHistory=""
                uniqueCrashNum=0

                path="/SPACE/reforce-project/dataset/stoat/finished/"
                
                filePath0=path+fileSp+"/stoat_fsm_output/all_action_execution_history.txt"
                filePath1=path+fileSp+"/stoat_mcmc_sampling_output/mcmc_all_history_testsuites.txt"
                
                
                eventStoatNum=0
                
                readFile = open(filePath0, 'r')
                contents=readFile.readlines()
                try:
                    for line in contents:
                        eventStoatNum+=1
                except:
                    print("no stoat: "+filePath0)        
                
                try: 
                    readFile = open(filePath1, 'r')
                    contents=readFile.readlines()
                
                    for line in contents:
                    
                        eventStoatNum+=len(line.split("("))-1
                except:
                    print("no stoat: "+filePath1)
                
                dataDict[fileSp][2]=eventStoatNum
            ###########for the sanpize
            if dataDict[fileSp][3]==0:
                try:
                    eventSapNum=0
                    
                    
                    path="/home/yu/workspace2/reinfocement-exploration/sapienze/"
                    fileName=fileSp
                    
                    sapPath=path+fileName
                    
                    readFile = open(sapPath, 'r')
                    
                    contents=readFile.readlines()
                    
                    for line in contents:
                        if "Sending" in line :
                            eventSapNum+=1
                        
                        
                    
                    dataDict[fileSp][3]=eventSapNum
                except:
                    print("Sap not found: "+sapPath)
        
    
    total=0
    Rmax=0
    Mmax=0
    Smax=0
    SapMax=0
    
    for name in dataDict:
        total+=1
        
        
        print(name+str(dataDict[name]))
        maxVal=max(dataDict[name])
        
        if dataDict[name][0]==maxVal:
            Rmax+=1
        if dataDict[name][1]==maxVal:
            Mmax+=1
        if dataDict[name][2]==maxVal:
            Smax+=1
        if dataDict[name][3]==maxVal:
            SapMax+=1

    print("total:"+str(total))
    print("Rmax:"+str(Rmax))
    print("Mmax:"+str(Mmax))
    print("Smax:"+str(Smax))
    print("Sapmax:"+str(SapMax))
    
    Rf=[]
    M=[]
    St=[]
    Sap=[]
    
    for name in dataDict:
    
        if not dataDict[name][0]==0:
            Rf.append(dataDict[name][0])
        
        if not dataDict[name][1]==0:
            M.append(dataDict[name][1])
            
        if not dataDict[name][2]==0:
            St.append(dataDict[name][2])
            
        if not dataDict[name][3]==0:
            Sap.append(dataDict[name][3])
        
    print(sum(Rf) / len(Rf))
    print(sum(M) / len(M))
    print(sum(St) / len(St))
    print(sum(Sap) / len(Sap))
    
    
    

if __name__ == '__main__':
    main()   



