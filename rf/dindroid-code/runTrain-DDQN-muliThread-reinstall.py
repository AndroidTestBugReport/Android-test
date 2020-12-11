'''
Created on Jun 12, 2017

@author: yu
'''
#from uiautomator import device as d
from uiautomator import Device
import time
import sys
import pickle

from xml.dom.minidom import Document
from xml.dom import minidom
import commands
import os
import Trans
import codecs
import Similar
import Feature2Digit
import ENV
import numpy as np
import shutil

import time
###############################

###############################
import DQNAgentDdqnNei as DQNAgent
#import DQNAgentNei as DQNAgent

import Feature

import threading
##################
from gensim.models import Word2Vec


def func(batch_size, featureListLen, Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList, agent, finishTag):
    
    lock.acquire()
    agent.replay(batch_size, featureListLen, Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList)
    finishTag[0]=1
    lock.release()

def main():
    
    
    #model.save("keras_mode.h5")
    
    
    #port='5554'
    #cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" logcat -d"
    #logText=commands.getstatusoutput(cmd)
    countReward=0
    #################
    
    batch_size = 30
    init_step=5
    ############inital
    apkList=[]
    
    
    for folderName in os.listdir("/SPACE/reforce-project/dataset/train/unfinished"):
        
            sourceCodePath="/SPACE/reforce-project/dataset/train/unfinished/"+folderName+"/bin/"
            source="/SPACE/reforce-project/dataset/train/unfinished/"+folderName
            destination="/SPACE/reforce-project/dataset/train/finished/"+folderName
            
            apkFile,coverageEm,packageName,activityName=ENV.compileApkEmma(sourceCodePath, commands, os)
        
            apkList.append((apkFile,coverageEm,packageName,activityName,sourceCodePath, source, destination))  
    
    
    port='5554'
    #d = Device('emulator-'+port)
    #time.sleep(4)
    address='.'
    '''
    packageName="bander.notepad"
    activityName="bander.notepad.NoteList"
    apkName="notepad_debug.apk"
    '''
    ##############agent
    
    ###word embeding
    word2VecModel= Word2Vec.load('yumodel').wv
    
    wordVectorLen=400#this is yumodel's len size
    
    neighborLen=10 #this is neighbor list's length
    
    word2Idx, wordEmbeddings=DQNAgent.build_embed( word2VecModel,wordVectorLen)
    
    
    agent = DQNAgent.DQNAgentClass( wordEmbeddings, neighborLen)############need to modification
    
    
   
    
    ###############start app
    #cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell am start -S -n "+packageName+"/"+activityName
    #commands.getstatusoutput(cmd)
    
    #avaiableAnotherList=["com.android.documentsui"]

    
    ##############
    apkCount=0
    
    for apkItem in apkList:
        
        
        crashID=0
        
        
        for iteTime in range(0,50):
        
            recordMiddleList=[]
            #simiarMap={}
            
        
        
        
            agent.memory={}###### brent's suggestion
            ############################3
            
            
            resultId=0
            ############generate a record root in every apk
            recordDoc=Document()
            recordRoot=recordDoc.createElement("recdrodRoot")
            
            
            ###test
            #doc=minidom.parse(address+'/middleResults/record.xml')
            #recordRoot=doc.documentElement
            ###test end
            
            doc_write =Document()
            doc_write.appendChild(recordRoot)  
            with codecs.open(address+"/middleResults/record.xml","wb","utf-8") as out:
                doc_write.writexml(out)
            out.close()
            
            ENV.restartAndroidEumlator(port,commands) #        for the text close
            
            cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb shell dumpsys window displays | grep 'init'"
            tupleLine=commands.getstatusoutput(cmd)
            heightAndWeight=tupleLine[1].strip().split(" ")[0].split("=")[1]
            height=int(heightAndWeight.split("x")[1])
            weight=int(heightAndWeight.split("x")[0])
            
            
            ####################install apk
            
            
            
            apkName=apkItem[0]
            coverageEm=apkItem[1]
            packageName=apkItem[2]
            activityName=apkItem[3]
            sourceCodePath=apkItem[4]
            source=apkItem[5]
            destination=apkItem[6]
        
        
            d = Device('emulator-'+port)
            
            cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" uninstall "+packageName
            commands.getstatusoutput(cmd) 
        
            cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" install "+apkName
            commands.getstatusoutput(cmd) 
            
        
            specChar=False
            
            actionIndex=None
            feature=None
            lastFeature=None
            lastActionIndex=None
            appCloseTag=False
            lastFeatureTuple=None
            crashTag=False
            logHistory=""
            
            
            ######################################coverage data
            lineCoverage=0
            methodCoverage=0
            classCoverage=0
            
            coverageData=[lineCoverage,methodCoverage,classCoverage]#class is not the activity coverage
            
            
            ####################clean sdcard
            ENV.cleanSd(commands, port)
            
            
            start = time.time()
            
            apkCount+=1
            
            lastEventInRecord=None
            lastSimilarEleList=[]
            restartTag=False
            
            finishTag=[1]
            
            for iterCount in range(10000):
                
                #menuTag=False
                #adb -s emulator-5556 shell rm -r sdcard/*
                print("apkCount:"+str(apkCount))
                
                if iterCount%200==0:
                    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" uninstall "+packageName
                    commands.getstatusoutput(cmd) 
                
                    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" install "+apkName
                    commands.getstatusoutput(cmd)
                    
                    
                
                
                ####################3every apk only train 2 hours
                end=time.time()
                if end-start>3600:
                    break
                
                
                print("iterCount:"+str(iterCount))
                print("currentReward"+str(countReward))
                
                if not iterCount==0 and not iterCount%200==0:#it is the first time
                    ##################clean
                    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" logcat -c"
                    commands.getstatusoutput(cmd)
                    
                    try:
                        #run
                        ENV.step(actionIndex, d, feature, commands, address, port, apkName, packageName, activityName,specChar)
                    except:
                        d.press.back()
                        print("except to click back")
                    
                    
                    #################check crash
                    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" logcat -d"
                    logText=commands.getstatusoutput(cmd)
                    logText=logText[1]
                    
                    #send a random intent
                    if iterCount % 10==0:
                        cmd="python /SPACE/stoat/Stoat-master/Stoat/trigger/tester.py -s emulator-5554 -f /SPACE/test/QuickSettings/bin/ShowSettingsActivity-debug.apk -p random"
                        intent=commands.getstatusoutput(cmd)
                        print(intent)
                    
                    if "FATAL" in logText or "fatal" in logText:
                    
                    
                        logBoolean,newLogAdd, specOut=ENV.checkBefore(logText,logHistory)
                        if specOut==True and specChar==False:
                            specChar=True
                        if not logBoolean:
                        
                            crashTag=True
                            ENV.writeCrash(logText,iterCount)
                            logHistory+=newLogAdd
                            className=ENV.restartApp(port,commands, packageName, activityName)
                            print("catch a crash and restart app")
                            
                        else:
                            crashTag=False
                            className=ENV.restartApp(port,commands, packageName, activityName)
                            print("catch a crash and restart app")
                    else:
                        crashTag=False
                    
                
                
                
                cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys window windows | grep -E 'mFocusedApp'"
                tupleLine=commands.getstatusoutput(cmd)
                className=str(tupleLine).split(" ")[-2]
                
                if not packageName in tupleLine[1] and not "com.android" in tupleLine[1] or "com.android.launcher" in tupleLine[1]:

                    appCloseTag=True
                    className=ENV.restartApp(port,commands, packageName, activityName)
                    restartTag=True
                    
                else:
                    appCloseTag=False
                    
                
                root_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, packageName, className, commands, port)
                            
                
                if notEmpty==False:
                    if loading==1:
                        for iterTimes in range(0,20):
                            if notEmpty==False:####may be dump at a middle page
                                time.sleep(0.4)
                                root_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, packageName, className, commands, port)
                                print("dumped a empty and loading page, so repeat dump"+str(iterTimes))
                            else:
                                break
                    else:                            
                        #permitOtherApp="anypackageisok"
                        #otherRoot_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, permitOtherApp, className, commands, port)
                        
                        
                        ENV.expOtherApp(d,height,weight)####just random find one to click
                            
                        for iterTimes in range(0,5):
                            
                            cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys window windows | grep -E 'mFocusedApp'"
                            tupleLine=commands.getstatusoutput(cmd)
                            
                            if not packageName in tupleLine[1]:
                                print(iterTimes)
                                d.press.back()
                                d.wait.update()
                                time.sleep(0.5)
                            else:
                                className=str(tupleLine).split(" ")[-2]
                                break
                            
                            if iterTimes==4:
                                print("restart")
                                className=ENV.restartApp(port,commands, packageName, activityName)
                                restartTag=True
                                break
                        root_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, packageName, className, commands, port)
    
                ##########################remove
                os.remove(address+'/middleResults/result.xml')
                
                
                #Similar.findComplement(recordRoot,root_Result,sameEvent, similarEventList)
                
                
                #######################compare similarity
                sameEvent, similarEventList, sameResultListMiddle,similarResultListMiddle=Similar.getSimilar(recordRoot,root_Result)
                
                ######################extract feature
                feature=Feature.FeatureClass(root_Result,sameResultListMiddle, similarResultListMiddle, sameEvent, similarEventList)
                
                
                
                featureStepNum=len(feature.runableList)
                
                
                textFeatue=Feature2Digit.textFeature2Digit(feature,word2Idx)####just encode to the word ID
                sameFeature,similarFeature=Feature2Digit.sameFeatureExtract(feature)
                
                
                
                #neighborFeatureList=Similar.findNeighbor(recordRoot,root_Result,sameEvent, similarEventList, featureStepNum)
                neighborFeatureList=Similar.findNeighborCount(recordRoot,root_Result,sameEvent, similarEventList, featureStepNum, neighborLen)
                ###########################
                
                
                
                
                featureTuple=(textFeatue,sameFeature,similarFeature, neighborFeatureList)#########generate feature for machine learning input
                
                ######################run model
                actionIndex, timeCost=agent.act(featureTuple, iterCount)
                #actionIndex=np.argmax(action)
                #actionIndex=2
                print("actionIndex: "+str(actionIndex))
                ##########################recordRoot
                #Similar.addToRecordRoot(recordRoot, root_Result,resultId,feature,featureStepNum,actionIndex,sameEvent, similarEventList)
                lastEventInRecord, lastSimilarEleList=Similar.addToRecordRoot(recordRoot, root_Result,resultId,feature,featureStepNum,actionIndex,sameEvent, similarEventList, lastEventInRecord, restartTag, lastSimilarEleList)
                ############################record into file
                doc_write =Document()
                doc_write.appendChild(recordRoot)  
                with codecs.open(address+"/middleResults/record.xml","wb","utf-8") as out:
                    doc_write.writexml(out)
                out.close()
                
                ########################add page ID
                resultId+=1
                
                ##################run
                #className=ENV.step(actionIndex, d, feature, commands, address, port)
                
                
                
                ##################memorize and update model, this part can be implemented parallel with run
                if iterCount==0 or iterCount%200==0:#it is the first time
                    lastFeature=feature
                    lastActionIndex=actionIndex 
                    
                else:
                    #reward=Similar.computeRewardSimilar(feature)
                    
                    reward=ENV.computeRewardCoverage(commands, port, sourceCodePath, coverageData)
                    
                    if crashTag:#######good catch
                        #reward=10
                        reward=5
                    
                    
                    countReward+=reward
                    
                    agent.memorize(lastFeatureTuple, lastActionIndex, reward, featureTuple)
                    
                    
                    testLastTuple=(lastFeatureTuple, lastActionIndex, reward, featureTuple)
                    #################train DQN
                    if iterCount > 0:
                        
                        while True:
                            if finishTag[0]==1:
                                finishTag=[0]
                                break
                        t = threading.Thread(target=func, args=(batch_size, len(lastFeature.runableList),Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList, agent, finishTag, )) 
                        t.start()
                        
                        #func(batch_size, len(lastFeature.runableList),Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList, agent, finishTag)
                        
                        
                        #t.isAlive()
                        
                        #agent.replay(batch_size, len(lastFeature.runableList),Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList)
                        
                    
                lastFeature=feature
                lastFeatureTuple=featureTuple
                lastActionIndex=actionIndex
                
                
            ###
            #np.save("./model/memory.npy",agent.memory)
            pickle.dump( agent.memory, open( "./model/memory.p", "wb" ) )
            # favorite_color = pickle.load( open( "save.p", "rb" ) )
            
            agent.save("./model/keras_model.h5")
            
            recordName=source.rsplit("/",1)[1]
            shutil.move("./emmaOutput.txt", "./trainResult/"+recordName+"_coverage_"+str(iteTime)+".txt")
            shutil.move("./middleResults/record.xml", "./trainResult/"+recordName+"_record_"+str(iteTime)+".xml")
                        
            outputFile = open("./experimentRecord.txt", 'a')
            outputFile.write("\n")
            outputFile.write("coverage:"+str(coverageData[0])+"\n")
            outputFile.close()
            
            ##test
            outputFile = open("/SPACE/reforce-project/dataset/train/result/"+recordName+"_middle_"+str(iteTime)+".txt", 'a')
            for line in recordMiddleList:
                outputFile.write(str(line)+"\n")
            outputFile.close()
            agent.save("/SPACE/reforce-project/dataset/train/result/"+recordName+"_model_"+str(iteTime)+".h5")            
            
        dest = shutil.move(source, destination)
    
if __name__ == '__main__':
    lock=threading.Lock()
    main()         