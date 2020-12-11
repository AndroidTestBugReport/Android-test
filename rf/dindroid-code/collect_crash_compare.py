import os

def noIntent(outPutStr):
    if not "handleReceiver(ActivityThread.java" in outPutStr:
        if not "performLaunchActivity(ActivityThread.java" in outPutStr:
            if not "handleServiceArgs(ActivityThread.java" in outPutStr:
                if not "performResumeActivity(ActivityThread.java" in outPutStr:
                    return True
    return False    


def main():
    dataDict={}
    compareWith="QBE"#### monkey  stoat   sapnize  QBE
    '''
    monkeyFileNameList=[]
    
    ###############store monkey file name
    for fileName in os.listdir("/home/yu/workspace2/reinfocement-exploration/monkey"):
        monkeyFileNameList
    ''' 
    interNum=0
    rWinNum=0
    oWinNum=0
    
    fileList=os.listdir("/home/yu/workspace2/rf-android/signalCNN/trainResult")
    
    intentSet=set()
    
    for fileName in os.listdir("/home/yu/workspace2/rf-android/signalCNN/trainResult"):
        ########for the reforcement train
        
        
        
        if "_coverage_0" in fileName:
            
            
            if "mileage_3110_src" in fileName:
                print("bingo")
            
            
            strIndex=fileName.find("_coverage_0")
            fileSp=fileName[0:strIndex]
            
            if not fileSp in dataDict:
                dataDict[fileSp]=[0,0,0,0]###first is R, second is monkey,third is stoat, fouth is sap
                ####explore stoat
            
            trainPath="/home/yu/workspace2/rf-android/signalCNN/trainResult/"+fileSp
            
            rCrashSet=set()
            
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
                                
                                
                                #if "handleReceiver(ActivityThread.java" in outPutStr or "ActivityThread.performLaunchActivity(ActivityThread.java" in outPutStr:
                                if noIntent(outPutStr):
                                        intentSet.add(outPutStr)                            
                                        uniqueCrashNum+=1
                                        rCrashSet.add(outPutStr)
                            count=None
                            outPutStr=""

                else:
                    break
            print(uniqueCrashNum)
            
            if uniqueCrashNum>1:
                print("bingo")
            #dataDict[fileSp][0]=uniqueCrashNum
            
            ########for the QBE
            ########for the QBE
            if compareWith=="QBE":
                trainPathq="/home/yu/workspace2/rf-android/ICST/trainResultICST/"+fileSp
            
                qCrashSet=set()
                
                logHistory=""
                
                fileListq=os.listdir("/home/yu/workspace2/rf-android/ICST/trainResultICST")

                
                indexq=0
                uniqueCrashNum=0
                while(True):
                    indexq+=1
                    trainFileq=trainPathq+"_crash_"+str(indexq)+".txt"
                    TrainFileNameq=fileSp+"_crash_"+str(indexq)+".txt"
                    
                    if TrainFileNameq in fileListq:
                        readFile = open(trainFileq, 'r')
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
                                        qCrashSet.add(outPutStr)
                                                                        
                                        
                                    uniqueCrashNum+=1
                                count=None
                                outPutStr=""
    
                    else:
                        break
                
                
                interSet=[]
                rWin=[]
                mWin=[]
                
                interSet=rCrashSet.intersection(qCrashSet)
                
                rWin=rCrashSet.difference(qCrashSet)
                mWin=qCrashSet.difference(rCrashSet)
        
            
            
            
            
            ########for the monkey
            
            if compareWith=="monkey":
            
                mCrashSet=set()
                
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
                                    #mCrashSet.add(outPutStr)
                                    if noIntent(outPutStr):
                                        uniqueCrashNum+=1
                                        mCrashSet.add(outPutStr)
                                count=None
                                outPutStr=""
    
                                
                        print(uniqueCrashNum)
                        
                        if uniqueCrashNum>1:
                            print("bingo")
                        dataDict[fileSp][1]=uniqueCrashNum
                    except:
                        print("Monkey not found: "+monkeyPath)
                        
                    
                    interSet=[]
                    rWin=[]
                    mWin=[]
                    
                    interSet=rCrashSet.intersection(mCrashSet)
                    
                    rWin=rCrashSet.difference(mCrashSet)
                    mWin=mCrashSet.difference(rCrashSet)
                    
                    
                    
                
                
                    
                    
                    
            
            ########for the stoat
            if compareWith=="stoat":
            
                stCrashSet=set()
            
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
                                            stCrashSet.add(outPutStr)
                                    count=None
                                    outPutStr=""
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
                                        stCrashSet.add(outPutStr)
                                count=None
                        
                                outPutStr=""

                        
                except:
                    print("no stoat: "+ filePath1)

                
                print(logHistory)
                print(uniqueCrashNum)
                    
                if uniqueCrashNum>1:
                    print("bingo")
                
                interSet=[]
                rWin=[]
                mWin=[]
                    
                interSet=rCrashSet.intersection(stCrashSet)
                
                rWin=rCrashSet.difference(stCrashSet)
                mWin=stCrashSet.difference(rCrashSet)
                
                
            ###########for the sanpize
            if compareWith=="sapnize":
            
                spCrashSet=set()

            
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
                                        spCrashSet.add(outPutStr)
                                count=None
                                outPutStr=""
    
                                
                        print(uniqueCrashNum)
                        
                        if uniqueCrashNum>1:
                            print("bingo")
                        dataDict[fileSp][3]=uniqueCrashNum
                    except:
                        print("sapienze not found: "+sapienzePath)
                
                interSet=[]
                rWin=[]
                mWin=[]
                    
                interSet=rCrashSet.intersection(spCrashSet)
                
                rWin=rCrashSet.difference(spCrashSet)
                mWin=spCrashSet.difference(rCrashSet)
    
    
            interNum+=len(interSet)
            rWinNum+=len(rWin)
            oWinNum+=len(mWin)
    print("interNum: "+str(interNum))
    print("rWinNum: "+str(rWinNum))   
    print("oWinNum: "+str(oWinNum))    
    print(intentSet)
    
if __name__ == '__main__':
    main()   



