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

def noIntent(outPutStr):
    if not "handleReceiver(ActivityThread.java" in outPutStr:
        if not "performLaunchActivity(ActivityThread.java" in outPutStr:
            if not "handleServiceArgs(ActivityThread.java" in outPutStr:
                if not "performResumeActivity(ActivityThread.java" in outPutStr:
                    return True
    return False    

def main():
    dataDict={}
    '''
    monkeyFileNameList=[]
    
    ###############store monkey file name
    for fileName in os.listdir("/home/yu/workspace2/reinfocement-exploration/monkey"):
        monkeyFileNameList
    ''' 
    
    
    fileList=os.listdir("/home/yu/workspace2/rf-android/ICST/trainResultICST")
    
    for fileName in os.listdir("/home/yu/workspace2/rf-android/ICST/trainResultICST"):
        ########for the reforcement train
        if "_coverage_0" in fileName:
            strIndex=fileName.find("_coverage_0")
            fileSp=fileName[0:strIndex]
            
            if not fileSp in dataDict:
                dataDict[fileSp]=[0,0,0,0]###first is R, second is monkey,third is stoat, fouth is sap
                ####explore stoat
                
                
            #oldTrainCoverage=dataDict[fileSp][0]
            
            trainPath="/home/yu/workspace2/rf-android/ICST/trainResultICST/"+fileSp
            logHistory=""
            index=0
            uniqueCrashNum=0
            while(True):
                index+=1
                trainFile=trainPath+"_crash_"+str(index)+".txt"
                TrainFileName=fileSp+"_crash_"+str(index)+".txt"
                
                if TrainFileName in fileList:
                    readFile = open(trainFile, 'r')
                    
                    contents=readFile.readlines()
                    
                    count=None
                    #result=True
                    #specialChar=False
                    
                    for line in contents:
                        if "FATAL" in line or "fatal" in line:
                            count=1
                            outPutStr=""
                            
                        if count and count<4 and "\tat " in line:
                            
                            subLineIndex=line.index("\tat ")
                            subLine=line[subLineIndex:]
                            outPutStr+=subLine
                            count+=1
                            
                                
                        if count>1 and not "\tat " in line:
                            if outPutStr in logHistory:
                                print("exited")
                            else:
                                logHistory+=outPutStr
                                if noIntent(outPutStr):
                                    uniqueCrashNum+=1
                            count=None
                            outPutStr=""

                else:
                    break
            print(uniqueCrashNum)
            
            if uniqueCrashNum>1:
                print("bingo")
            dataDict[fileSp][0]=uniqueCrashNum
            
            
            
            '''
            newTrainCoverage=computeLineCoverage(trainPath)

            
            if newTrainCoverage>oldTrainCoverage:
                dataDict[fileSp][0]=newTrainCoverage
            '''
            ########for the monkey
            if dataDict[fileSp][1]==0:
                try:
                    path="/home/yu/workspace2/reinfocement-exploration/monkey/"
                    fileName=fileSp+"_logcat"
                    
                    '''
                    if "com.zoffcc.applications.aagtl_31_src_logcat" in fileName:
                        print("bingo")
                    '''
                    monkeyPath=path+fileName
                    
                    readFile = open(monkeyPath, 'r')
                    
                    contents=readFile.readlines()
                    
                    logHistory=""
                    
                    
                    
                    #outPutStr=""
                    count=None
                    #result=True
                    #specialChar=False
                    uniqueCrashNum=0
                    
                    for line in contents:
                        if "FATAL" in line or "fatal" in line:
                            count=1
                            outPutStr=""
                            
                        if count and count<4 and "\tat " in line:
                            
                            subLineIndex=line.index("\tat ")
                            subLine=line[subLineIndex:]
                            outPutStr+=subLine
                            count+=1
                            
                                
                        if count>1 and not "\tat " in line:
                            if outPutStr in logHistory:
                                print("exited")
                            else:
                                logHistory+=outPutStr
                                if noIntent(outPutStr):
                                    uniqueCrashNum+=1
                            count=None
                            outPutStr=""

                            
                    print(uniqueCrashNum)
                    
                    if uniqueCrashNum>1:
                        print("bingo")
                    dataDict[fileSp][1]=uniqueCrashNum
                except:
                    print("Monkey not found: "+monkeyPath)
            ########for the stoat
            if dataDict[fileSp][2]==0:
                logHistory=""
                uniqueCrashNum=0

                path="/SPACE/reforce-project/dataset/stoat/finished/"
                
                filePath0=path+fileSp+"/stoat_fsm_output/crashes/"
                filePath1=path+fileSp+"/stoat_mcmc_sampling_output/crashes/"
                
                if ("caldwell" in filePath1):
                    print("bingo")
                
                
                try:
                    for folderName in os.listdir(filePath0):
                        crashPath=filePath0+folderName+"/emulator-5554_logcat.txt"
                        
                        
                        
                        readFile = open(crashPath, 'r')
                        
                        contents=readFile.readlines()
                                            
                        #outPutStr=""
                        count=None
                        #result=True
                        #specialChar=False                    
                        #count=1
                        outPutStr=""
                        
                        for line in contents:
                            if "FATAL" in line or "fatal" in line:
                                
                                
                                count=1
                                outPutStr=""
                                
                            if count and count<4 and "\tat " in line:
                                
                                subLineIndex=line.index("\tat ")
                                subLine=line[subLineIndex:]
                                outPutStr+=subLine
                                count+=1
                                
                                    
                            if count>1 and not "\tat " in line:
                                if outPutStr in logHistory:
                                    print("exited")
                                else:
                                    logHistory+=outPutStr
                                    if noIntent(outPutStr):
                                        uniqueCrashNum+=1
                                count=None
                                outPutStr=""

                        
                        
                        '''
                        
                        readFile = open(crashPath, 'r')
                        
                        contents=readFile.readlines()
                                            
                        #outPutStr=""
                        count=None
                        #result=True
                        #specialChar=False                    
                        count=1
                        outPutStr=""
                        for line in contents:
                            #if "FATAL" in line or "fatal" in line:
                                
                            if count and count<4 and "\tat " in line:
                                
                                subLineIndex=line.index("\tat ")
                                subLine=line[subLineIndex:]
                                outPutStr+=subLine
                                count+=1
                                
                                    
                            if count>1 and not "\tat " in line:
                                if outPutStr in logHistory:
                                    print("exited")
                                else:
                                    logHistory+=outPutStr
                                    uniqueCrashNum+=1
                                count=None
                        '''
                except:
                    print("no stoat: "+ filePath0)
                
                
                    
                    
                    
                try:
                    for folderName in os.listdir(filePath1):
                        
                        crashPath=filePath1+folderName+"/emulator-5554_logcat.txt"
                        
                        readFile = open(crashPath, 'r')
                        
                        contents=readFile.readlines()
                                            
                        #outPutStr=""
                        count=None
                        #result=True
                        #specialChar=False                    
                        #count=1
                        outPutStr=""
                        
                        for line in contents:
                            
                            if "439" in outPutStr:
                                print("bingo")
                            
                            if "FATAL" in line or "fatal" in line:
                                count=1
                                outPutStr=""
                                
                            if count and count<4 and "\tat " in line:
                                
                                subLineIndex=line.index("\tat ")
                                subLine=line[subLineIndex:]
                                outPutStr+=subLine
                                count+=1
                                
                                    
                            if count>1 and not "\tat " in line:
                                if outPutStr in logHistory:
                                    print("exited")
                                else:
                                    logHistory+=outPutStr
                                    if noIntent(outPutStr):
                                        uniqueCrashNum+=1
                                count=None
                        
                                outPutStr=""

                        
                        
                        '''
                        readFile = open(crashPath, 'r')
                        
                        contents=readFile.readlines()
                                            
                        #outPutStr=""
                        count=None
                        #result=True
                        #specialChar=False                    
                        count=1
                        outPutStr=""
                        for line in contents:
                            #if "FATAL" in line or "fatal" in line:
                                
                            if count and count<4 and "\tat " in line:
                                
                                subLineIndex=line.index("\tat ")
                                subLine=line[subLineIndex:]
                                outPutStr+=subLine
                                count+=1
                                
                                    
                            if count>1 and not "\tat " in line:
                                if outPutStr in logHistory:
                                    print("exited")
                                else:
                                    logHistory+=outPutStr
                                    uniqueCrashNum+=1
                                count=None
                        '''
                except:
                    print("no stoat: "+ filePath1)

                
                print(logHistory)
                print(uniqueCrashNum)
                    
                if uniqueCrashNum>1:
                    print("bingo")
                dataDict[fileSp][2]=uniqueCrashNum
            ###########for the sanpize
            if dataDict[fileSp][3]==0:
                
                try:
                    path="/home/yu/workspace2/reinfocement-exploration/sapienze/"
                    fileName=fileSp+"_logcat"
                    sapienzePath=path+fileName
                    #monkeyPath=path+fileName
                    
                    readFile = open(sapienzePath, 'r')
                    
                    contents=readFile.readlines()
                    
                    logHistory=""
                    
                    
                    
                    #outPutStr=""
                    count=None
                    #result=True
                    #specialChar=False
                    uniqueCrashNum=0
                    
                    for line in contents:
                        if "FATAL" in line or "fatal" in line:
                            count=1
                            outPutStr=""
                            
                        if count and count<4 and "\tat " in line:
                            
                            subLineIndex=line.index("\tat ")
                            subLine=line[subLineIndex:]
                            outPutStr+=subLine
                            count+=1
                            
                                
                        if count>1 and not "\tat " in line:
                            if outPutStr in logHistory:
                                print("exited")
                            else:
                                logHistory+=outPutStr
                                if noIntent(outPutStr):
                                    uniqueCrashNum+=1
                            count=None
                            outPutStr=""

                            
                    print(uniqueCrashNum)
                    
                    if uniqueCrashNum>1:
                        print("bingo")
                    dataDict[fileSp][3]=uniqueCrashNum
                except:
                    print("sapienze not found: "+sapienzePath)
    
    
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
            
            
            
    print(sum(Rf))
    print(sum(M))
    print(sum(St))
    print(sum(Sap))
    '''    
    print(sum(Rf) / len(Rf))
    print(sum(M) / len(M))
    print(sum(St) / len(St))
    print(sum(Sap) / len(Sap))
    '''
if __name__ == '__main__':
    main()   



