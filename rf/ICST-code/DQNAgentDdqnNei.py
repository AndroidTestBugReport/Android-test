'''
Created on Jun 12, 2017

@author: yu
'''



import time



###############################
import random
import numpy as np
from collections import deque
import os
from docutils.io import FileOutput
import pickle


EPISODES = 1000

class DQNAgentClass:
    def __init__(self, matrixDict):
        
        self.matrixDict=matrixDict
        
        self.ranPcur=1
        #self.neighborLen=neighborLen
        self.maxwordEvent=6
        self.vectorSize=400
        self.memory={}
        #self.memory = deque(maxlen=2000)
        
        #self.gamma = 0.7    # discount rate
        #self.gamma = 0.4    # discount rate   use by july 5
        #self.gamma = 0.6    # discount rate july 14
        self.gamma = 0.6
        '''
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        #self.learning_rate = 0.001
        '''        
        self.stateDict=self._buildQ()
        self.Ndict=self._buildN()



    def _buildQ(self):
        
        #[menu, back, click, longclick,text, swipe, contextual]
        
        #[<1,<3,<8,<15,>15]

        if os.path.exists("./model/qDict.pkl"):
            a_file = open("./model/qDict.pkl", "rb")
            stateDict = pickle. load(a_file)
            print("existing Qtable")
            print(stateDict)
            a_file. close()
            return stateDict

        else:        
            actionDict={}
            actionDict["menu"]=0
            actionDict["back"]=0
            actionDict["click"]=0
            actionDict["longclick"]=0
            actionDict["text"]=0
            actionDict["swipe"]=0
            actionDict["contextual"]=0
            
            
            stateDict={}
            stateDict["<1"]=actionDict.copy()
            stateDict["<3"]=actionDict.copy()
            stateDict["<8"]=actionDict.copy()
            stateDict["<15"]=actionDict.copy()
            stateDict[">15"]=actionDict.copy()
        
            return stateDict


    def _buildN(self):
        
        #[menu, back, click, longclick,text, swipe, contextual]
        
        #[<1,<3,<8,<15,>15]
        
        actionDict={}
        actionDict["menu"]=0
        actionDict["back"]=0
        actionDict["click"]=0
        actionDict["longclick"]=0
        actionDict["text"]=0
        actionDict["swipe"]=0
        actionDict["contextual"]=0
        
        
        stateDict={}
        stateDict["<1"]=actionDict.copy()
        stateDict["<3"]=actionDict.copy()
        stateDict["<8"]=actionDict.copy()
        stateDict["<15"]=actionDict.copy()
        stateDict[">15"]=actionDict.copy()
        
        return stateDict

        
    def memorize(self, lastFeatureTuple, action, reward, featureTuple):
        
        stepNum=len(lastFeatureTuple[0])
        if not stepNum in self.memory:
            self.memory[stepNum]=[[],[]]#first element is postive and second element is negative
            
        if reward>0:
            self.memory[stepNum][0].append((lastFeatureTuple, action, reward, featureTuple))
        else:
            self.memory[stepNum][1].append((lastFeatureTuple, action, reward, featureTuple))
                        
            #self.memory[stepNum]=[(lastFeatureTuple, action, reward, featureTuple)]



    def act(self, featureTuple, iterCount, test):
        
        '''
        if np.random.rand() <= self.epsilon:
            return random.randrange(state.shape[0])#there is 0.01 probability random select after 17 eouside
        '''
        
        
        
        actionDict=self.stateDict[featureTuple]
        
        maxValue=-1
        maxKey=-1
        
        for key in actionDict:
            Qvalue=actionDict[key]
            if Qvalue>maxValue:
                maxValue=Qvalue
                
                maxKey=key
                
        
        self.ranPcur=self.ranPcur*0.995
        
        
        if np.random.rand()<self.ranPcur:
            
            return random.choice(actionDict.keys()),0
            #return "random", 0
        else:
            return maxKey, 0
            

    def actMatrix(self, featureTuple, iterCount, test):
        
        
        textFeatue,sameFeature,similarFeature, neighborFeatureList=featureTuple
        
        simVector=[]
        
        for index in range(len(similarFeature)):
            vector=similarFeature[index]
            value=vector[0]
            simVector.append(value)
            
        minVal=min(simVector)
        
        minVector=[]
        for index in range(len(simVector)):
            if simVector[index]==minVal:
                minVector.append(index)
        
        if test:
            self.middleTest(textFeatue, sameFeature, similarFeature, neighborFeatureList)

        
        
        if iterCount<20 or np.random.rand()<=0.2:
        
        #if iterCount<3:# or np.random.rand()<=0.2:
            return random.choice(minVector), 0
        
        '''
        if iterCount<1:
            return 2, 0
        '''
            #return random.choice(minVector), 0
            #return random.randrange(len(textFeatue)), 0
        textFeatue = np.asarray([textFeatue])
        sameFeature=np.asarray([sameFeature])
        similarFeature=np.asarray([similarFeature])
        nei1Feature=np.asarray([neighborFeatureList[0]])
        nei2Feature=np.asarray([neighborFeatureList[1]])
        nei3Feature=np.asarray([neighborFeatureList[2]])
        
        
        
        
        #vector=self.middleModel.predict([textFeatue,sameFeature,similarFeature])
        
        #for l in self.model.layers:
        #    print(l.name, l.trainable)        
        '''
        start=time.time()
        act_values = self.model.predict([textFeatue,sameFeature,similarFeature, nei1Feature, nei2Feature, nei3Feature])
        end=time.time()
        '''
        lastList=[]
        
        
        lastLen=len(similarFeature[0])
        
        for item in similarFeature[0]:
            lastList.append(str(item[0]))
            
        lastNei1Feature=neighborFeatureList[0]
        lastNei2Feature=neighborFeatureList[1]
        lastNei3Feature=neighborFeatureList[2]
    
        for index in range(lastLen):
            if lastNei1Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)
            
                        
        for index in range(lastLen):
            if lastNei2Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)
                            
        for index in range(lastLen):
            if lastNei3Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)        
        
        maxVal=-1000
        for index in range(len(lastList)):
            if lastList[index] in self.matrixDict and self.matrixDict[lastList[index]]>maxVal:
                maxVal=self.matrixDict[lastList[index]]

        maxIndexList=[]
        for index in range(len(lastList)):
            if lastList[index] in self.matrixDict and self.matrixDict[lastList[index]]==maxVal:
                maxIndexList.append(index)
                
        if len(maxIndexList)==0:
            maxIndex=random.choice(minVector)
        else:
            maxIndex=random.choice(maxIndexList)
        
        return maxIndex,  0 # returns action

    
    def middleTest(self, textFeatue, sameFeature, similarFeature, neighborFeatureList):
        np.set_printoptions(precision=3, suppress=True)
        
        outputFile = open("./testRecords/middleRecord.txt", 'w')
        textFeatue = np.asarray([textFeatue])
        sameFeature=np.asarray([sameFeature])
        similarFeature=np.asarray([similarFeature])
        nei1Feature=np.asarray([neighborFeatureList[0]])
        nei2Feature=np.asarray([neighborFeatureList[1]])
        nei3Feature=np.asarray([neighborFeatureList[2]])

        #neiFeature=neighborFeatureList
        
        ###test
        
        numberLen=len(similarFeature[0])

        ###0
        for freq in ["1;","2;","3;","4;"]:
        
            
            action0=freq+"(5#1);(0#0);(0#0)"
            action1=freq+"(1#5);(0#0);(0#0)"
            action2=freq+"(0#0);(5#1);(0#0)"
            action3=freq+"(0#0);(1#5);(0#0)"
            action4=freq+"(0#0);(0#0);(5#1)"
            action5=freq+"(0#0);(0#0);(1#5)"
            action6=freq+"(0#0);(0#0);(0#0)"
            action7=freq+"(5#0);(0#0);(0#0)"
            action8=freq+"(0#0);(5#0);(0#0)"
            action9=freq+"(0#0);(0#0);(5#0)"
            action10=freq+"(0#5);(0#0);(0#0)"
            action11=freq+"(0#0);(0#5);(0#0)"
            action12=freq+"(0#0);(0#0);(0#5)"
            action13="0;"+"(0#0);(0#0);(0#0)"
            
            
            actionList=[action0,action1,action2,action3,action4,action5,action6,action7,action8,action9,action10, action11, action12, action13]
            for i in range(0,len(actionList)):
            
                for index in range(numberLen):
                    
                    action=actionList[i]
                    newaction=action.replace("(", "")
                    newaction=newaction.replace(")","")
                    
                    
                    visitFreq=int(newaction.split(";")[0])
                    nei1=newaction.split(";")[1]
                    nei2=newaction.split(";")[2]
                    nei3=newaction.split(";")[3]
                    
                    nei1_0=-int(nei1.split("#")[0])
                    nei1_1=-int(nei1.split("#")[1])
                    
                    nei2_0=-int(nei2.split("#")[0])
                    nei2_1=-int(nei2.split("#")[1])
                    
                    nei3_0=-int(nei3.split("#")[0])
                    nei3_1=-int(nei3.split("#")[1])
                    
                    
                    similarFeature=[]
                    nei1Feature=[]
                    nei2Feature=[]
                    nei3Feature=[]
            
                    #textFeatue[0]
                    similarFeature.append([visitFreq]*10)
                    nei1Feature.append([nei1_0, nei1_1]+[0]*8)
                    nei2Feature.append([nei2_0, nei2_1]+[0]*8)
                    nei3Feature.append([nei3_0, nei3_1]+[0]*8)
                    
                    
                    similarFeature=np.asarray(similarFeature)
                    nei1Feature=np.asarray(nei1Feature)
                    nei2Feature=np.asarray(nei2Feature)
                    nei3Feature=np.asarray(nei3Feature)
            
                    act_values = self.model.predict([[textFeatue[0][index]],similarFeature, nei1Feature, nei2Feature, nei3Feature])
                    
                    print(act_values)
                    outputFileAA = open("./humanEva/human_eval"+".txt", 'a')
        
                    outputFileAA.write(action+":::"+str(act_values[0][0])+"\n")
        
                    outputFileAA.close()
        
        print("finish")
        
    
        
        
    def middleTestOld(self, textFeatue, sameFeature, similarFeature, neighborFeatureList):
        np.set_printoptions(precision=3, suppress=True)
        
        outputFile = open("./testRecords/middleRecord.txt", 'w')
        textFeatue = np.asarray([textFeatue])
        sameFeature=np.asarray([sameFeature])
        similarFeature=np.asarray([similarFeature])
        nei1Feature=np.asarray([neighborFeatureList[0]])
        nei2Feature=np.asarray([neighborFeatureList[1]])
        nei3Feature=np.asarray([neighborFeatureList[2]])

        #neiFeature=neighborFeatureList
        
        ###test
        
        numberLen=len(similarFeature[0])

        
        
        
        '''
        sameFeature=[]
        similarFeature=[]
        nei1Feature=[]
        nei2Feature=[]
        nei3Feature=[]
        '''
        
        similarFeature=[]
        nei1Feature=[]
        nei2Feature=[]
        nei3Feature=[]
        
        
        
        similarFeature.append([0]*10)
        similarFeature.append([0]*10)
        similarFeature.append([0]*10)
        similarFeature.append([1]*10)
        similarFeature.append([0]*10)

        
        nei1Feature.append([0]*10)
        nei1Feature.append([0]*10)
        nei1Feature.append([0]*10)
        #nei1Feature.append([0]*10)

        nei1Feature.append([-10, -1]+[0]*8)
        nei1Feature.append([0]*10)
        
        nei2Feature.append([0]*10)
        nei2Feature.append([0]*10)
        nei2Feature.append([0]*10)
        #nei2Feature.append([0]*10)

        nei2Feature.append([0, -5]+[0]*8)
        nei2Feature.append([0]*10)
        
        nei3Feature.append([0]*10)
        nei3Feature.append([0]*10)
        nei3Feature.append([0]*10)
        nei3Feature.append([0, -5]+[0]*8)
        #nei3Feature.append([0]*10)
        nei3Feature.append([0]*10)

        
        similarFeature=np.asarray(similarFeature)
        nei1Feature=np.asarray(nei1Feature)

        nei2Feature=np.asarray(nei2Feature)
        nei3Feature=np.asarray(nei3Feature)

        
        act_values = self.model.predict([textFeatue[0],similarFeature, nei1Feature, nei2Feature, nei3Feature])
                
        outputFile.write("similar:"+"\n")
        outputFile.write(str(similarFeature)+"\n")
        outputFile.write("nei1Feaure:"+"\n")
        outputFile.write(str(nei1Feature)+"\n")
        outputFile.write("nei2Feaure:"+"\n")
        outputFile.write(str(nei2Feature)+"\n")
        outputFile.write("nei3Feaure:"+"\n")
        outputFile.write(str(nei3Feature)+"\n")
        outputFile.write("perdictValue:"+"\n")
        outputFile.write(str(act_values)+"\n")
        outputFile.write("######################################"+"\n")

        
        
        
        '''
        
        ##########all 0 part
        
        mutalVal=0
        
        simlarValue=0
        
        mutalNeiVal=0
        
        targList=[0,3,4]
        
        doubleTargList=[3,5,6]

        for targ in targList:

            for i in range(6):
                sameFeature=[]
                similarFeature=[]
                nei1Feature=[]
                nei2Feature=[]
                nei3Feature=[]
                for index in range(numberLen):
                    
                    if index in doubleTargList:
                        similarFeature.append([mutalVal]*10)
                        sameFeature.append([mutalVal]*10)
                        nei1Feature.append([0,0,0]+[0]*7)
                        nei2Feature.append([0,0,0]+[0]*7)
                        nei3Feature.append([0]*10)
                        
                        continue
                    
                    
                    if i==0:
                        if index==targ:
                            similarFeature.append([simlarValue]*10)
                            sameFeature.append([simlarValue]*10)
                            nei1Feature.append([0,0,0]+[0]*7)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                        
                    
                    if i==1:
                        if index==targ:
                            similarFeature.append([mutalVal]*10)
                            sameFeature.append([mutalVal]*10)
                            nei1Feature.append([0,0,0]+[0]*7)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                        
                        
                    if i==2:
                        if index==targ:
                            similarFeature.append([mutalVal]*10)
                            sameFeature.append([mutalVal]*10)
                            nei1Feature.append([mutalNeiVal,0,0,0]+[0]*6)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                            
                    if i==3:
                        if index==targ:
                            similarFeature.append([mutalVal]*10)
                            sameFeature.append([mutalVal]*10)
                            nei1Feature.append([0,mutalNeiVal,0,0]+[0]*6)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                            
                    if i==4:
                        if index==targ:
                            similarFeature.append([mutalVal]*10)
                            sameFeature.append([mutalVal]*10)
                            nei1Feature.append([0,0,mutalNeiVal,0]+[0]*6)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                            
                    if i==5:
                        if index==targ:
                            similarFeature.append([mutalVal]*10)
                            sameFeature.append([mutalVal]*10)
                            nei1Feature.append([0,0,0,mutalNeiVal]+[0]*6)
                            nei2Feature.append([0,0,0]+[0]*7)
                            nei3Feature.append([0]*10)
                            continue
                    
                    similarFeature.append([simlarValue]*10)
                    sameFeature.append([simlarValue]*10)
                
                    #nei1Feature.append([0]*10)
                    nei1Feature.append([0,0,0,0]+[0]*6)
                    nei2Feature.append([0]*10)
                    nei3Feature.append([0]*10)
                
                similarFeature=np.asarray([similarFeature])
                nei1Feature=np.asarray([nei1Feature])
                nei2Feature=np.asarray([nei2Feature])
                nei3Feature=np.asarray([nei3Feature])
                sameFeature=np.asarray([sameFeature])
        
                #middleValues1=self.model1.predict([textFeatue,sameFeature,similarFeature, nei1Feature, nei2Feature, nei3Feature])
                #middleValues2=self.model2.predict([textFeatue,sameFeature,similarFeature, nei1Feature, nei2Feature, nei3Feature])
                
                
                
                
                ####test end
                act_values = self.model.predict([textFeatue[0],similarFeature[0], nei1Feature[0], nei2Feature[0], nei3Feature[0]])
                
                #outputFile.write("value2:"+"\n")
                #outputFile.write(str(middleValues1)+"\n")
                outputFile.write("similar:"+"\n")
                outputFile.write(str(similarFeature)+"\n")
                outputFile.write("nei1Feaure:"+"\n")
                outputFile.write(str(nei1Feature)+"\n")
                outputFile.write("nei2Feaure:"+"\n")
                outputFile.write(str(nei2Feature)+"\n")
                outputFile.write("nei3Feaure:"+"\n")
                outputFile.write(str(nei3Feature)+"\n")
                outputFile.write("perdictValue:"+"\n")
                outputFile.write(str(act_values)+"\n")
                outputFile.write("######################################"+"\n")
        time.sleep(1)
        outputFile.close()
        
        
        
        '''
        
        
        
        print("finish")
        
        
    def replay(self, testLastTuple):
        
        
        outputFile = open("./testRecordsICST/Qmatrix.txt", 'a')
        outputFile.write("#######################"+"\n")
        for key in self.stateDict:
            
            outputFile.write(key+"\n")
            outputFile.write(str(self.stateDict[key])+"\n")
            #outputFile.write("iterate:"+str(iteTime)+"\n")
            
            print(key)
            print(self.stateDict[key])
        
        outputFile.close()
        
        
        lastState=testLastTuple[0]
        actionState=testLastTuple[1]
        reward=testLastTuple[2]
        thisState=testLastTuple[3]
        
        #try:
        print("Ndict key: "+lastState)
        print("actionState: "+str(actionState))
        print(str(lastState in self.Ndict))
        self.Ndict[lastState][actionState]=self.Ndict[lastState][actionState]+1
        '''
        except:
            print("bingo")
        '''
        maxVal=0
        for key in self.stateDict[thisState].keys():
            if self.stateDict[thisState][key]>maxVal:
                maxVal=self.stateDict[thisState][key]
        
        
        self.stateDict[lastState][actionState]=(reward+ 0.9*maxVal - self.stateDict[lastState][actionState])/self.Ndict[lastState][actionState]+self.stateDict[lastState][actionState]
        
        sumVal=0
        for key in self.stateDict[lastState]:
            sumVal+=self.stateDict[lastState][key]
            
        if not sumVal==0:
            for key in self.stateDict[lastState]:
                self.stateDict[lastState][key]=self.stateDict[lastState][key]/sumVal
                
        sumVal=0
        for key in self.stateDict[lastState]:
            sumVal+=self.stateDict[lastState][key]
        
        print("sumVal")
        print(sumVal)
        
        
        #############################

    def save(self, name):
        #self.model.save_weights(name)
        #self.stateDict
        a_file = open(name, "wb")
        pickle. dump(self.stateDict, a_file)
        a_file. close()

    def matrixTrain(self, lastFeatureTuple, featureTuple, action, reward, iteTime, iterCount,i):

        lastTextFeatue,lastSameFeature,lastSimilarFeature,lastNeighborFeatureList=lastFeatureTuple
        currentTextFeatue,currentSameFeature,currentSimilarFeature,currentNeighborFeatureList=featureTuple
        ###############lastFeature
        lastList=[]
        
        
        lastLen=len(lastSimilarFeature)
        
        for item in lastSimilarFeature:
            
            if item[0]>5:
                lastList.append(str(5))
            else:
                lastList.append(str(item[0]))
                        
        lastNei1Feature=lastNeighborFeatureList[0]
        lastNei2Feature=lastNeighborFeatureList[1]
        lastNei3Feature=lastNeighborFeatureList[2]
    
        for index in range(lastLen):
            if lastNei1Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)

                        
        for index in range(lastLen):
            if lastNei2Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)
                            
        for index in range(lastLen):
            if lastNei3Feature[index][0]==0:
                lastList[index]=lastList[index]+"-"+str(0)
            else:
                lastList[index]=lastList[index]+"-"+str(1)
        
        for item in lastList:
            
            if not item in self.matrixDict:
                self.matrixDict[item]=0
                
        
        #################thisFeature

        currentList=[]

        
        currentLen=len(currentSimilarFeature)
        
        for item in currentSimilarFeature:
            if item[0]>5:
                currentList.append(str(5))
            else:
                currentList.append(str(item[0]))
                                    
        currentNei1Feature=currentNeighborFeatureList[0]
        currentNei2Feature=currentNeighborFeatureList[1]
        currentNei3Feature=currentNeighborFeatureList[2]
    
        for index in range(currentLen):
            if currentNei1Feature[index][0]==0:
                currentList[index]=currentList[index]+"-"+str(0)
            else:
                currentList[index]=currentList[index]+"-"+str(1)
                            
        for index in range(currentLen):
            if currentNei2Feature[index][0]==0:
                currentList[index]=currentList[index]+"-"+str(0)
            else:
                currentList[index]=currentList[index]+"-"+str(1)
            
        for index in range(currentLen):
            if currentNei3Feature[index][0]==0:
                currentList[index]=currentList[index]+"-"+str(0)
            else:
                currentList[index]=currentList[index]+"-"+str(1)                
                
        for item in lastList:
            if not item in self.matrixDict:
                self.matrixDict[item]=0
        
        
        for item in currentList:
            if not item in self.matrixDict:
                self.matrixDict[item]=0
                
                
        ##################3
        lastStatus=lastList[action]
        
        nextVal=-1000
        for item in currentList:
            if self.matrixDict[item]>nextVal:
                nextVal=self.matrixDict[item]
                
        updateVal=reward+0.6*nextVal
        if updateVal>100:
            updateVal=100
        if updateVal<-50:
            updateVal=-50
        
        if i==1:
            outputFile = open("./testRecords/trainRecord"+str(iteTime)+".txt", 'a')
        else:
            outputFile = open("./testRecords/trainRecordOther"+str(iteTime)+".txt", 'a')

        '''
        if lastStatus.startswith("1-0") and updateVal>0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")

        if lastStatus.startswith("1-1") and updateVal<0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")
        
        
        if lastStatus.startswith("2-0") and updateVal>0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")

            
        if lastStatus.startswith("2-1") and updateVal<0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")
            
        if lastStatus.startswith("3-0") and updateVal>0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")
            
        if lastStatus.startswith("3-1") and updateVal<0:
            outputFile.write("bingo################################"+"\n")
            outputFile.write("nei: "+str(lastNeighborFeatureList)+"\n")
        '''
        updateVal=0.2*updateVal+ 0.8*self.matrixDict[lastStatus]

        

        
        
        self.matrixDict[lastStatus]=updateVal
        
        
        outputFile.write("#############################iter:" + str(iterCount)+ "\n")
        outputFile.write("currentList: "+str(currentList)+"\n")
        outputFile.write("index: "+str(action)+"\n")
        outputFile.write("reward: "+str(reward)+"\n")
        
        
        
        
        outputFile.write("updateKey: "+lastStatus+" reward: "+str(reward)+ " nextMax: "+str(nextVal) +" updateQ: "+str(reward+0.6*nextVal)+"\n")

        
        keyList=self.matrixDict.keys()
        keyList.sort()
        
        for key in keyList:
            keyVal=self.matrixDict[key]
            outputFile.write("key: "+key+" val: "+str(keyVal)+"\n")
              

        outputFile.close()



    def matrixReplay(self, batch_size, lastStateStepNum, Feature2Digit, word2VecModel,word2Idx, testLastTuple, recordMiddleList, sameBefore, iterCount, iteTime):         
        
        minibatch0=[]
        minibatch0.append(testLastTuple)
        
        postiveSameNumHisList=self.memory[lastStateStepNum][0]
        negativeSameNumHisList=self.memory[lastStateStepNum][1]

        if len(postiveSameNumHisList)>2:
            minibatch0=minibatch0+random.sample(postiveSameNumHisList,2)
        else:
            minibatch0=minibatch0+random.sample(postiveSameNumHisList,len(postiveSameNumHisList))

        leftLen=5-len(minibatch0)
        
        if len(negativeSameNumHisList)>leftLen:
            minibatch0=minibatch0+random.sample(negativeSameNumHisList,leftLen)
        else:
            minibatch0=minibatch0+random.sample(negativeSameNumHisList,len(negativeSameNumHisList))
        
        
        ##################
        i=0
        for lastFeatureTuple, action, reward, featureTuple in minibatch0:
            i=i+1
            print(i)
            lastTextFeatue,lastSameFeature,lastSimilarFeature,lastNeighborFeatureList=lastFeatureTuple
            currentTextFeatue,currentSameFeature,currentSimilarFeature,currentNeighborFeatureList=featureTuple
        
            #lastFeatureTuple, action, reward, featureTuple=testLastTuple


            self.matrixTrain(lastFeatureTuple, featureTuple, action, reward, iteTime, iterCount,i)


        '''
        #######################3old and time
        minibatch0=[]
        minibatch0.append(testLastTuple)
        
        postiveSameNumHisList=self.memory[lastStateStepNum][0]
        negativeSameNumHisList=self.memory[lastStateStepNum][1]

        if len(postiveSameNumHisList)>2:
            minibatch0=minibatch0+random.sample(postiveSameNumHisList,2)
        else:
            minibatch0=minibatch0+random.sample(postiveSameNumHisList,len(postiveSameNumHisList))

        leftLen=5-len(minibatch0)
        
        if len(negativeSameNumHisList)>leftLen:
            minibatch0=minibatch0+random.sample(negativeSameNumHisList,leftLen)
        else:
            minibatch0=minibatch0+random.sample(negativeSameNumHisList,len(negativeSameNumHisList))
                    
        
        
       
        #(self.memory.keys(),1)
        
        #############batch0
        states=[[], [], [], [], [], []]
        targets_f = []
        
        start=time.time()
        i=0
        with self.session.as_default():
            with self.graph.as_default():
                for lastFeatureTuple, action, reward, featureTuple in minibatch0:
                    i=i+1
                    print(i)
                    lastTextFeatue,lastSameFeature,lastSimilarFeature,lastNeighborFeatureList=lastFeatureTuple
                    currentTextFeatue,currentSameFeature,currentSimilarFeature,currentNeighborFeatureList=featureTuple
                    
                    ########transfer format
                    lastTextFeatueTran = np.asarray([lastTextFeatue])
                    lastSameFeatureTran=np.asarray([lastSameFeature])
                    lastSimilarFeatureTran=np.asarray([lastSimilarFeature])
                    
                    lastNei1Feature=np.asarray([lastNeighborFeatureList[0]])
                    lastNei2Feature=np.asarray([lastNeighborFeatureList[1]])
                    lastNei3Feature=np.asarray([lastNeighborFeatureList[2]])

                                        
                    currentTextFeatueTran = np.asarray([currentTextFeatue])
                    currentSameFeatureTran=np.asarray([currentSameFeature])
                    currentSimilarFeatureTran=np.asarray([currentSimilarFeature])
                    
                    currentNei1Feature=np.asarray([currentNeighborFeatureList[0]])
                    currentNei2Feature=np.asarray([currentNeighborFeatureList[1]])
                    currentNei3Feature=np.asarray([currentNeighborFeatureList[2]])

                    
                    
                    #self.graph.as_default()
                    t=self.target_model.predict([currentTextFeatueTran,currentSameFeatureTran,currentSimilarFeatureTran, currentNei1Feature, currentNei2Feature, currentNei3Feature])[0]
                    #t=self.target_model._make_predict_function([currentTextFeatueTran,currentSameFeatureTran,currentSimilarFeatureTran])[0]
                    
                    Qvalue = (1-self.gamma)*reward + self.gamma * np.amax(t)
                    # Qvalue = reward + self.gamma * np.amax(t)
                    
                    target_f = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran, lastNei1Feature, lastNei2Feature, lastNei3Feature])[0]
                    
                    bb=self.target_model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran, lastNei1Feature, lastNei2Feature, lastNei3Feature])[0]
                    
                    a=target_f.copy()
                    
                    target_f[action]=Qvalue
                    
                    for index in range(len(target_f)):
                        if target_f[index]>30:
                            target_f[index]=30
                        elif target_f[index]<-15:
                            target_f[index]=-15
                                
                    b=target_f.copy()
                    
                    #recordMiddleList.append((a,bb,Qvalue, index, lastSimilarFeatureTran, lastNei1Feature, lastNei2Feature, lastNei3Feature))
                                
                    states[0].append(lastTextFeatue)
                    states[1].append(lastSameFeature)
                    states[2].append(lastSimilarFeature)
                    states[3].append(lastNei1Feature[0])
                    states[4].append(lastNei2Feature[0])
                    states[5].append(lastNei3Feature[0])

                    
                    
                    targets_f.append(target_f)
                    
                    
                
                history0 = self.model.fit(states, np.array(targets_f), epochs=20, verbose=0)
                
                print("target")
                print(targets_f)
                
                end=time.time()
                trainTimeCost=end-start

                
                print("trainTimeCost: "+str(end-start))
        #target_f = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran])
        
        #history0 = self.model.fit([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran], np.array(target_f), epochs=300, verbose=2)
        
        
        #target_fTest = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran])[0]
    
        
        
        
        loss0 = history0.history['loss']
        print("loss0")      
        print(loss0)
        
        #loss1 = history1.history['loss']
        #print(loss1)
        print("alive")
        #############################
        '''
        return [0,0,0], 0



############################not in the class
def build_embed( word2VecModel, vectorSize):
    
        if os.path.exists("./model/word2Idx_wordEmbeddings.npy"):
            #self.model = load_model("./model/keras_model.h5")
            word2Idx,wordEmbeddings=np.load('model/word2Idx_wordEmbeddings.npy', allow_pickle=True)
            print("existing embedding")
            return word2Idx,wordEmbeddings
        else:
            word2Idx = {}
            wordEmbeddings = []#22949
        
        
            for word in word2VecModel.vocab:
            
                if len(word2Idx) == 0: #Add padding+unknown
                    word2Idx["PADDING_TOKEN"] = len(word2Idx)
                    vector = np.zeros(vectorSize) #Zero vector vor 'PADDING' word
                    wordEmbeddings.append(vector)
                    
                    word2Idx["dividebysen"] = len(word2Idx)
                    vector = np.random.uniform(-0.25, 0.25, vectorSize)
                    wordEmbeddings.append(vector)
                    
                    word2Idx["UNKNOWN_TOKEN"] = len(word2Idx)
                    vector = np.random.uniform(-0.25, 0.25, vectorSize)
                    wordEmbeddings.append(vector)
                
                
                word2Idx[word]=len(word2Idx)
                wordEmbeddings.append(word2VecModel[word])
            
            wordEmbeddings = np.array(wordEmbeddings)
            
            np.save("model/word2Idx_wordEmbeddings.npy",(word2Idx,wordEmbeddings))
            return word2Idx,wordEmbeddings

    