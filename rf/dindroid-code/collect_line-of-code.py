import os
import commands

def computeLineCoverage(filePath):

    #f1=open("./emmaOutput.txt")
    
    f1=open(filePath)
    
    contents=f1.readlines()
    
    lineCoverageNew=0
    methodCoverageNew=0
    classCoverageNew=0#class is not the activity
    num=0
    for line in contents:
        if "(" in line:
            try:
                #print(line.split("!")[3])
                if "Amazed" in  filePath:
                    print("bingo")
                num=int(line.split(")")[3].split("/")[1].replace(")",""))
                
                
                if num==0:
                    print("bingo")
            except:
                print("bingo")
            break
            
            
            '''
            
            
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
            '''
    f1.close()
    return int(num)



def main():
    dataDict={}
    '''
    monkeyFileNameList=[]
    
    ###############store monkey file name
    for fileName in os.listdir("/home/yu/workspace2/reinfocement-exploration/monkey"):
        monkeyFileNameList
    ''' 
    
    
    
    
    for fileName in os.listdir("/home/yu/workspace2/rf-android/signalCNN/trainResult"):
        ########for the reforcement train
        if "_coverage" in fileName:
            strIndex=fileName.find("_coverage")
            fileSp=fileName[0:strIndex]
            
            if not fileSp in dataDict:
                dataDict[fileSp]=[0,0,0,0]###first is R, second is monkey,third is stoat, fouth is sap
                ####explore stoat
                
                
            oldTrainCoverage=dataDict[fileSp][0]
            
            trainPath="/home/yu/workspace2/rf-android/signalCNN/trainResult/"+fileName
            newTrainCoverage=computeLineCoverage(trainPath)

            
            if newTrainCoverage>oldTrainCoverage:
                dataDict[fileSp][0]=newTrainCoverage
            
            ########for the monkey
            if dataDict[fileSp][1]==0:
                try:
                    path="/home/yu/workspace2/reinfocement-exploration/monkey/"
                    fileName=fileSp+"_coverage.txt"
                    monkeyPath=path+fileName
                    newMonkeyCoverage=computeLineCoverage(monkeyPath)
                    dataDict[fileSp][1]=newMonkeyCoverage
                except:
                    print("Monkey not found: "+monkeyPath)
            
            ########for the stoat
            if dataDict[fileSp][2]==0:
                
                path="/SPACE/reforce-project/dataset/stoat/finished/"
                filePath0=path+fileSp+"/stoat_fsm_output/coverage/coverage.txt"
                filePath1=path+fileSp+"/stoat_mcmc_sampling_output/coverage.txt"
                
                newFsmCoverage=0
                newMcmcCoverage=0
                
                
                
                sourceCodePath=path+fileSp+"/bin/"
                
                for fileName in os.listdir(sourceCodePath):
                    if fileName.endswith("debug.apk"):
                    #if fileName.endswith("instrumented.apk"):
                        apkFile=sourceCodePath+fileName
                
                
                
                cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/build-tools/23.0.3/aapt dump badging "+apkFile+" | awk '/package/{gsub(\"name=|'\"'\"'\",\"\");  print $2}'"
                packageName=commands.getstatusoutput(cmd)[1]
                dataDict[fileSp][2]=packageName
                
                '''
                
                try:    
                    newFsmCoverage=computeLineCoverage(filePath0)
                except:
                    print("Stoat not found: "+filePath0)
                    
                try:
                    newMcmcCoverage=computeLineCoverage(filePath1)
                except:
                    print("Stoat not found: "+filePath1)
                    
                if newFsmCoverage>newMcmcCoverage:
                    dataDict[fileSp][2]=newFsmCoverage
                else:
                    dataDict[fileSp][2]=newMcmcCoverage
                
                #print("aa")
                '''
            '''
            ###########for the sanpize
            if dataDict[fileSp][3]==0:
                
                try:
                    path="/home/yu/workspace2/reinfocement-exploration/sapienze/"
                    fileName=fileSp+"_coverage.txt"
                    sapienzePath=path+fileName
                    newsapienzeCoverage=computeLineCoverage(sapienzePath)
                    dataDict[fileSp][3]=newsapienzeCoverage
                except:
                    print("sapienze not found: "+sapienzePath)
            '''
    
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
    
    import operator
    sorted_x = sorted(dataDict.items(), key=operator.itemgetter(1))
    print(sorted_x)

if __name__ == '__main__':
    main()   



