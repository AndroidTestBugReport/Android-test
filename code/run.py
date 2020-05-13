'''
Created on Jun 12, 2017

@author: yu
'''
#from uiautomator import device as d
from uiautomator import Device
import time
import sys

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


import time
###############################

###############################
#import DQNAgent
import Feature

import DQNAgentDDQN as DQNAgent


##################
from gensim.models import Word2Vec


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
    
    
    for folderName in os.listdir("/SPACE/test/"):
        
        for i in range(0,3):#for the test
            sourceCodePath="/SPACE/test/"+folderName+"/bin/"
            apkFile,coverageEm,packageName,activityName=ENV.compileApkEmma(sourceCodePath, commands, os)
        
            apkList.append((apkFile,coverageEm,packageName,activityName,sourceCodePath))
        break#for the test
    
    
    
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
    
    word2Idx, wordEmbeddings=DQNAgent.build_embed( word2VecModel,wordVectorLen)
    
        
    
   
    
    ###############start app
    #cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell am start -S -n "+packageName+"/"+activityName
    #commands.getstatusoutput(cmd)
    
    
    
    ##############
    apkCount=0
    
    for apkItem in apkList:
        agent = DQNAgent.DQNAgentClass( wordEmbeddings)############need to modification
        agent.memory={}
        ############################3
        
        
        resultId=0
        ############generate a record root in every apk
        recordDoc=Document()
        recordRoot=recordDoc.createElement("recdrodRoot")
        
        ###test
        doc=minidom.parse(address+'/middleResults/record.xml')
        recordRoot=doc.documentElement
        ###test end
        doc_write =Document()
        doc_write.appendChild(recordRoot)  
        with codecs.open(address+"/middleResults/record.xml","wb","utf-8") as out:
            doc_write.writexml(out)
        out.close()
        
        
        
        
        ####################install apk
        
        
        
        apkName=apkItem[0]
        coverageEm=apkItem[1]
        packageName=apkItem[2]
        activityName=apkItem[3]
        sourceCodePath=apkItem[4]
    
    
        #ENV.restartAndroidEumlator(port,commands)         for the text close
        d = Device('emulator-'+port)
        
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" uninstall "+packageName
        commands.getstatusoutput(cmd) 
    
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" install "+apkName
        commands.getstatusoutput(cmd) 
        
    
        
        
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
        
        for iterCount in range(10000):
            
            #menuTag=False
            #adb -s emulator-5556 shell rm -r sdcard/*
            print("apkCount:"+str(apkCount))
            
            
            ####################3every apk only train 2 hours
            end=time.time()
            if end-start>720:
                break
            
            
            print("iterCount:"+str(iterCount))
            print("currentReward"+str(countReward))
            
            if not iterCount==0:#it is the first time
                ##################clean
                cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" logcat -c"
                commands.getstatusoutput(cmd)
                
                #run
                ENV.step(actionIndex, d, feature, commands, address, port, apkName, packageName, activityName)
                
                
                
                #################check crash
                cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" logcat -d"
                logText=commands.getstatusoutput(cmd)
                logText=logText[1]
                
                
                
                if "FATAL" in logText or "fatal" in logText:
                    
                    
                    
                    
                    logBoolean,newLogAdd=ENV.checkBefore(logText,logHistory)
                    if not logBoolean:
                    
                        crashTag=True
                        ENV.writeCrash(logText,iterCount)
                        logHistory+=newLogAdd
                        className=ENV.restartApp(port,commands, packageName, activityName)
                        print("catch a crash and restart app")
                        '''
                        recordName=source.rsplit("/",1)[1]
                        cmd="adb -s emulator-"+port+" logcat -d>./trainResult/"+recordName+"_crash_"+str(crashID)+".txt"                            
                        crashID+=1
                            
                        print("restore crash log")
                        '''
                    else:
                        crashTag=False
                else:
                    crashTag=False
            
            
            
            cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys window windows | grep -E 'mFocusedApp'"
            tupleLine=commands.getstatusoutput(cmd)
            className=str(tupleLine).split(" ")[-2]
    
            if not packageName in tupleLine[1]:
                appCloseTag=True
                className=ENV.restartApp(port,commands, packageName, activityName)
                
                
            else:
                appCloseTag=False
            
            #################check menu
            #menuTag=ENV.checkMenu(commands, port)
            
            ################dump
            root_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, packageName, className, commands, port)
            
            if loading==1:
                for iterTimes in range(0,20):
                    if notEmpty==False:####may be dump at a middle page
                        time.sleep(0.4)
                        root_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, packageName, className, commands, port)
                        print("dumped a empty and loading page, so repeat dump"+str(iterTimes))
                    else:
                        break
            else:
                for iterTimes in range(0,2):
                    if notEmpty==False:####may be dump at a middle page
                        time.sleep(0.4)
                        root_Result, notEmpty, loading=ENV.dumpTrans(d, address, minidom, os, Trans, packageName, className, commands, port)
                        print("dumped a empty page, so repeat dump"+str(iterTimes))
                    else:
                        break
            
            
    
            ##########################remove
            os.remove(address+'/middleResults/result.xml')
            
            #######################compare similarity
            sameEvent, similarEventList, sameResultListMiddle,similarResultListMiddle=Similar.getSimilar(recordRoot,root_Result)
            
            ######################extract feature
            feature=Feature.FeatureClass(root_Result,sameResultListMiddle, similarResultListMiddle, sameEvent, similarEventList)
            
            
            
            featureStepNum=len(feature.runableList)
            
            
            textFeatue=Feature2Digit.textFeature2Digit(feature,word2Idx)####just encode to the word ID
            sameFeature,similarFeature=Feature2Digit.sameFeatureExtract(feature)
            
            featureTuple=(textFeatue,sameFeature,similarFeature)#########generate feature for machine learning input
            
            ######################run model
            actionIndex=agent.act(featureTuple, iterCount)
            #actionIndex=np.argmax(action)
            
            print("actionIndex: "+str(actionIndex))
            ##########################recordRoot
            Similar.addToRecordRoot(recordRoot, root_Result,resultId,feature,featureStepNum,actionIndex,sameEvent, similarEventList)
            
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
            if iterCount==0:#it is the first time
                lastFeature=feature
                lastActionIndex=actionIndex 
                
            else:
                #reward=Similar.computeRewardSimilar(feature)
                
                reward=ENV.computeRewardCoverage(commands, port, sourceCodePath, coverageData)
                
                
                
                
                
                
                if crashTag:#######good catch
                    reward=5
                
                
                countReward+=reward
                
                #reward=-0.5
                agent.memorize(lastFeatureTuple, lastActionIndex, reward, featureTuple)
                
                testLastTuple=(lastFeatureTuple, lastActionIndex, reward, featureTuple)
                #################train DQN
                if iterCount > 0:
                    recordMiddleList=[]
                    agent.replay(batch_size, len(lastFeature.runableList),Feature2Digit,word2VecModel,word2Idx, testLastTuple, recordMiddleList)
                    print("str: "+str(recordMiddleList))
                
            lastFeature=feature
            lastFeatureTuple=featureTuple
            lastActionIndex=actionIndex
            
        agent.save("./model/keras_model.h5")
        
        outputFile = open("./experimentRecord.txt", 'a')
        outputFile.write("\n")
        outputFile.write("coverage:"+str(coverageData[0])+"\n")
        outputFile.close()
    
if __name__ == '__main__':
    main()         