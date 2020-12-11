import os



def main():
    
    right1=0#0 button
    wrong1=0
    
    totalRight1=0
    totalWrong1=0
    
    rightEqu=0
    wrongEqu=0
    
    rightEquTotal=0
    wrongEquTotal=0
    
    rightChild=0
    wrongChild=0
    
    rightTotal=0
    wrongTotal=0
    
    rightChildNei1=0
    wrongChildNei1=0
    
    rightTotalNei1=0
    wrongTotalNei1=0
    
    rightChildNei3=0
    wrongChildNei3=0
    
    rightTotalNei3=0
    wrongTotalNei3=0
    
    fileList=os.listdir("/home/yu/workspace2/rf-android/signalCNN/trainResult")
    
    for fileName in os.listdir("/home/yu/workspace2/rf-android/signalCNN/trainResult"):
        ########for the reforcement train
        if "_coverage_0" in fileName:
            strIndex=fileName.find("_coverage_0")
            fileSp=fileName[0:strIndex]
            
            
            '''
            if not fileSp in dataDict:
                dataDict[fileSp]=[0,0,0,0]###first is R, second is monkey,third is stoat, fouth is sap
                ####explore stoat
            ''' 
                
            #oldTrainCoverage=dataDict[fileSp][0]
            index=-1
            trainPath="/home/yu/workspace2/rf-android/signalCNN/trainResult/"+fileSp
            while(True):
                index+=1
                trainFile=trainPath+"_trainRecord_"+str(index)+".txt"
                TrainFileName=fileSp+"_trainRecord_"+str(index)+".txt"
                
                
                if TrainFileName in fileList:
                    readFile = open(trainFile, 'r')
                    
                    contents=readFile.readlines()
                    
                    
                    
                    lastSim=False
                    thisModel=False
                    
                    for line in contents:####for 0 and non-0
                        if "lastSim" in line:
                            lastSim=True
                            record=[]
                            QvalueList=[]
                            continue
                        
                        if "lastNei1Feature" in line:
                            lastSim=False
                            
                            
                            bothVal=False    
                            if 0 in record:
                                for item in record:
                                    if not item == 0:
                                        bothVal=True#it has 0 and non 0 value
                            
                        if lastSim:
                            #try:
                            record.append(int(line.replace("[","").replace("]","").replace(" ","")[0]))
                            '''
                            except:
                                print("bingo")
                            '''     
                        
                        if "thisModle:" in line:
                            thisModel=True
                            continue
                            
                        if "beforeModle:" in line:
                            thisModel=False
                            
                            if bothVal:
                                #QvalueList
                                maxIndex=QvalueList.index(max(QvalueList))
                                if record[maxIndex]==0:
                                    right1+=1
                                    #print(right1)
                                else:
                                    wrong1+=1
                                    
                                for indexTotal1 in range(len(record)):
                                    
                                    if record[indexTotal1]==0:
                                        totalRight1+=1
                                        
                                    else:
                                        totalWrong1+=1
                                    
                                    
                            record=[]
                            QvalueList=[]
                                    
                            
                    
                        if thisModel:
                            QvalueList.append(float(line.replace("[","").replace("]","")))
                            
                    ###################################################################################        
                    for line in contents:####for all 0 event equal or no equal
                        if "lastSim" in line:
                            lastSim=True
                            record=[]
                            QvalueList=[]
                            continue
                        
                        if "lastNei1Feature" in line:
                            lastSim=False
                            
                            
                            bothValEquZe=True    
                            
                            '''
                            for item in record:
                                if  not item == record[0]:
                                    bothValEquZe=False#it has 0 and non 0 value
                            '''
                            for item in record:
                                if not item == 0:
                                    bothValEquZe=False#it has 0 and non 0 value
                            
                            
                            '''
                            if 0 in record:
                                for item in record:
                                    if not item == 0:
                                        bothValEquZe=False#it has 0 and non 0 value
                            '''
                            
                        if lastSim:
                            #try:
                            record.append(int(line.replace("[","").replace("]","").replace(" ","")[0]))
                            '''
                            except:
                                print("bingo")
                            '''     
                        
                        if "thisModle:" in line:
                            thisModel=True
                            continue
                            
                        if "beforeModle:" in line:
                            thisModel=False
                            
                            if bothValEquZe:
                                
                                firstVal=QvalueList[0]
                                rightBol=False
                                for qVal in QvalueList:
                                    if not qVal==firstVal:
                                        rightEqu+=1
                                        rightBol=True
                                        break
                                if not rightBol:
                                    wrongEqu+=1
                                    #print(QvalueList)
                                #print(record)
                                rightEquTotal+=len(QvalueList)
                                    
                                    
                            record=[]
                            QvalueList=[]
                                    
                            
                    
                        if thisModel:
                            QvalueList.append(float(line.replace("[","").replace("]","")))
                        
                    #########################################ne1+nei2#########################################
                    lastNei1Feature=False
                    lastNei2Feature=False
                    neiAllzero=True
                    neiHasZero=False
                    for line in contents:####for first child has and first child has no
                        if "lastSim" in line:
                            lastSim=True
                            record=[]
                            QvalueList=[]
                            lastNei1FeatureList=[]
                            lastNei2FeatureList=[]
                            lastNei1Feature=False
                            lastNei2Feature=False
                            continue
                        
                        if "lastNei1Feature" in line:
                            lastSim=False
                            
                            
                            bothValNotEquZe=True    
                            if 0 in record:
                                for item in record:
                                    if item == 0:
                                        bothValNotEquZe=False#it has 0 and non 0 value
                                        
                            lastNei1Feature=True
                            continue
                            
                        if "lastNei2Feature" in line:
                            lastNei1Feature=False
                            lastNei2Feature=True
                            continue
                            
                        if "lastNei3Feature" in line:
                            lastNei2Feature=False
                            
                        if  lastNei1Feature:
                            
                            try:
                                lastNei1FeatureList.append(int(line.replace("[","").replace("]","").strip().split(" ")[0]))
                            except:
                                print("bingo")
                            
                        
                            
                        if  lastNei2Feature:
                            
                            try:
                                lastNei2FeatureList.append(int(line.replace("[","").replace("]","").strip().split(" ")[0]))
                            except:
                                print("bingo")
                            
                            
                            
                        if lastSim:
                            #try:
                            record.append(int(line.replace("[","").replace("]","").replace(" ","")[0]))
                            '''
                            except:
                                print("bingo")
                            '''     
                        
                        if "thisModle:" in line:
                            thisModel=True
                            continue
                            
                        if "beforeModle:" in line:
                            thisModel=False
                            neiHasZero=False
                            
                            if 0 in lastNei1FeatureList or 0 in lastNei2FeatureList:
                                neiHasZero=True
                            
                            
                            
                            
                            neiAllzero=True
                            for item in lastNei1FeatureList:
                                if not item==0:
                                #if item<-5:
                                    
                                    neiAllzero=False
                                    break
                            
                            for item in lastNei2FeatureList:
                                if not item==0:
                                #if item<-5:
                                    neiAllzero=False
                                    break
                            
                            
                            if bothValNotEquZe and not neiAllzero and neiHasZero:
                                
                                maxIndex=QvalueList.index(max(QvalueList))
                                if lastNei1FeatureList[maxIndex]<0 or lastNei2FeatureList[maxIndex]<0:
                                    rightChild+=1
                                else:
                                    wrongChild+=1
                                
                                for itemIndex in range(len(lastNei1FeatureList)):
                                    
                                    if lastNei1FeatureList[itemIndex]<0 or lastNei2FeatureList[itemIndex]<0:
                                        rightTotal+=1
                                        #print(rightTotal)
                                    else:
                                        wrongTotal+=1
                                        #print(wrongTotal)
                                
                                '''
                                maxIndex=QvalueList.index(max(QvalueList))
                                if lastNei1FeatureList[maxIndex]<0:
                                    rightChild+=1
                                else:
                                    wrongChild+=1
                                
                                for itemIndex in range(len(lastNei1FeatureList)):
                                    
                                    if lastNei1FeatureList[itemIndex]<0 or lastNei2FeatureList[itemIndex]<0:
                                        rightTotal+=1
                                        #print(rightTotal)
                                    else:
                                        wrongTotal+=1
                                        #print(wrongTotal)
                                '''
                                
                            record=[]
                            QvalueList=[]
                            lastNei1FeatureList=[]
                                    
                            
                    
                        if thisModel:
                            QvalueList.append(float(line.replace("[","").replace("]","")))
                            
                            
                            
                    ##################################################################################
                    lastNei1Feature=False##3only nei1
                    lastNei2Feature=False
                    neiAllzero=True
                    neiHasZero=False
                    for line in contents:####for first child has and first child has no
                        if "lastSim" in line:
                            lastSim=True
                            record=[]
                            QvalueList=[]
                            lastNei1FeatureList=[]
                            lastNei2FeatureList=[]
                            lastNei1Feature=False
                            lastNei2Feature=False
                            continue
                        
                        if "lastNei1Feature" in line:
                            lastSim=False
                            
                            
                            bothValNotEquZe=True    
                            if 0 in record:
                                for item in record:
                                    if item == 0:
                                        bothValNotEquZe=False#it has 0 and non 0 value
                                        
                            lastNei1Feature=True
                            continue
                            
                        if "lastNei2Feature" in line:
                            lastNei1Feature=False
                            lastNei2Feature=True
                            continue
                            
                        if "lastNei3Feature" in line:
                            lastNei2Feature=False
                            
                        if  lastNei1Feature:
                            
                            try:
                                lastNei1FeatureList.append(int(line.replace("[","").replace("]","").strip().split(" ")[0]))
                            except:
                                print("bingo")
                            
                        
                            
                        if  lastNei2Feature:
                            
                            try:
                                lastNei2FeatureList.append(int(line.replace("[","").replace("]","").strip().split(" ")[0]))
                            except:
                                print("bingo")
                            
                            
                            
                        if lastSim:
                            #try:
                            record.append(int(line.replace("[","").replace("]","").replace(" ","")[0]))
                            '''
                            except:
                                print("bingo")
                            '''     
                        
                        if "thisModle:" in line:
                            thisModel=True
                            continue
                            
                        if "beforeModle:" in line:
                            thisModel=False
                            neiHasZero=False
                            
                            if 0 in lastNei1FeatureList:# or 0 in lastNei2FeatureList:
                                neiHasZero=True
                            
                            
                            
                            
                            neiAllzero=True
                            for item in lastNei1FeatureList:
                                if not item==0:
                                #if item<-5:
                                    
                                    neiAllzero=False
                                    break
                            
                            if bothValNotEquZe and not neiAllzero and neiHasZero:
                                
                                maxIndex=QvalueList.index(max(QvalueList))
                                if lastNei1FeatureList[maxIndex]<0:
                                    
                                    rightChildNei1+=1
                                else:
                                    wrongChildNei1+=1
                                
                                for itemIndex in range(len(lastNei1FeatureList)):
                                    
                                    if lastNei1FeatureList[itemIndex]<0 :
                                        rightTotalNei1+=1
                                        #print(rightTotal)
                                    else:
                                        wrongTotalNei1+=1
                                        #print(wrongTotal)
                                
                                
                            record=[]
                            QvalueList=[]
                            lastNei1FeatureList=[]
                                    
                            
                    
                        if thisModel:
                            QvalueList.append(float(line.replace("[","").replace("]","")))    
                    #########################################ne1+nei2+nei3#########################################
                    lastNei1Feature=False
                    lastNei2Feature=False
                    lastNei3Feature=False
                    neiAllzero=True
                    neiHasZero=False
                    for line in contents:####for first child has and first child has no
                        if "lastSim" in line:
                            lastSim=True
                            record=[]
                            QvalueList=[]
                            lastNei1FeatureList=[]
                            lastNei2FeatureList=[]
                            lastNei3FeatureList=[]
                            lastNei1Feature=False
                            lastNei2Feature=False
                            lastNei3Feature=False
                            continue
                        
                        if "lastNei1Feature" in line:
                            lastSim=False
                            
                            
                            bothValNotEquZe=True    
                            if 0 in record:
                                for item in record:
                                    if item == 0:
                                        bothValNotEquZe=False#it has 0 and non 0 value
                                        
                            lastNei1Feature=True
                            continue
                            
                        if "lastNei2Feature" in line:
                            lastNei1Feature=False
                            lastNei2Feature=True
                            continue
                            
                        if "lastNei3Feature" in line:
                            lastNei2Feature=False
                            lastNei3Feature=True
                            continue
                        
                        if "thisSim" in line:
                            lastNei3Feature=False
                            
                        if  lastNei1Feature:
                            try:
                                lastNei1FeatureList.append(int(line.replace("[","").replace("]","").strip().split(" ")[0]))
                            except:
                                print("bingo")
                            
                        
                            
                        if  lastNei2Feature:
                            
                            try:
                                lastNei2FeatureList.append(int(line.replace("[","").replace("]","").strip().split(" ")[0]))
                            except:
                                print("bingo")
                            
                        if  lastNei3Feature:
                            
                            try:
                                lastNei3FeatureList.append(int(line.replace("[","").replace("]","").strip().split(" ")[0]))
                            except:
                                print("bingo")
                            
                        if lastSim:
                            #try:
                            record.append(int(line.replace("[","").replace("]","").replace(" ","")[0]))
                        
                        if "thisModle:" in line:
                            thisModel=True
                            continue
                            
                        if "beforeModle:" in line:
                            thisModel=False
                            neiHasZero=False
                            
                            if 0 in lastNei1FeatureList or (0 in lastNei2FeatureList) or (0 in lastNei3FeatureList):
                                neiHasZero=True
                            
                            
                            
                            
                            neiAllzero=True
                            for item in lastNei1FeatureList:
                                if not item==0:
                                #if item<-5:
                                    
                                    neiAllzero=False
                                    break
                            
                            for item in lastNei2FeatureList:
                                if not item==0:
                                #if item<-5:
                                    neiAllzero=False
                                    break
                                
                            for item in lastNei3FeatureList:
                                if not item==0:
                                #if item<-5:
                                    neiAllzero=False
                                    break
                            
                            
                            if bothValNotEquZe and not neiAllzero and neiHasZero:
                                
                                
                                maxIndex=QvalueList.index(max(QvalueList))
                                if lastNei1FeatureList[maxIndex]<0 or lastNei2FeatureList[maxIndex]<0 or lastNei3FeatureList[maxIndex]<0:
                                    rightChildNei3+=1
                                else:
                                    wrongChildNei3+=1
                                
                                for itemIndex in range(len(lastNei1FeatureList)):
                                    
                                    if lastNei1FeatureList[itemIndex]<0 or lastNei2FeatureList[itemIndex]<0 or lastNei3FeatureList[itemIndex]<0:
                                        rightTotalNei3+=1
                                        #print(rightTotal)
                                    else:
                                        wrongTotalNei3+=1
                                        #print(wrongTotal)
                                
                                '''
                                maxIndex=QvalueList.index(max(QvalueList))
                                if lastNei1FeatureList[maxIndex]<0:
                                    rightChild+=1
                                else:
                                    wrongChild+=1
                                
                                for itemIndex in range(len(lastNei1FeatureList)):
                                    
                                    if lastNei1FeatureList[itemIndex]<0 or lastNei2FeatureList[itemIndex]<0:
                                        rightTotal+=1
                                        #print(rightTotal)
                                    else:
                                        wrongTotal+=1
                                        #print(wrongTotal)
                                '''
                                
                            record=[]
                            QvalueList=[]
                            lastNei1FeatureList=[]
                                    
                            
                    
                        if thisModel:
                            QvalueList.append(float(line.replace("[","").replace("]","")))
                    
                    
                else:
                    break            
                            
    print("right1: "+str(right1))   
    print("wrong1: "+str(wrong1))                      
    
    
    print("totalRight1: "+str(totalRight1))   
    print("totalWrong1: "+str(totalWrong1))    
    
                            
    print("rightEqu: "+str(rightEqu))   
    print("wrongEqu: "+str(wrongEqu))     
    
    print("rightEquTotal"+str(rightEquTotal))
    
    print("rightChildNei1: "+str(rightChildNei1))   
    print("wrongChildNei1: "+str(wrongChildNei1))     
    
    print("rightTotalNei1: "+str(rightTotalNei1))   
    print("wrongTotalNei1: "+str(wrongTotalNei1)) 
    
    print("rightChildNei2: "+str(rightChild))   
    print("wrongChildNei2: "+str(wrongChild))     
    
    print("rightTotalNei2: "+str(rightTotal))   
    print("wrongTotalNei2: "+str(wrongTotal))  
      
    print("rightChildNei3: "+str(rightChildNei3))   
    print("wrongChildNei3: "+str(wrongChildNei3))     
    
    print("rightTotalNei3: "+str(rightTotalNei3))   
    print("wrongTotalNei3: "+str(wrongTotalNei3)) 
                    
if __name__ == '__main__':
    main()   



