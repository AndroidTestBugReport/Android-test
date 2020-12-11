import numpy as np
import time
import subprocess as sub
import random
from multiprocessing import Process

#import threading
def dumpTrans( d, address, minidom, os, Trans, packageName, className,commands, port):
    ################dump
    try:
        d.dump(address+"/middleResults/result.xml", compressed=False)
        
    except:
        d.press.back()
        d.wait.update()
        time.sleep(0.5)
        d.dump(address+"/middleResults/result.xml", compressed=False)
        print("uiautomator dump except, solve: click back")
    
    #################check menu
    #menuTag=ENV.checkMenu(commands, port)
    
    ################dump
    #d.dump(address+"/middleResults/result.xml")
    while(1):#############wait for result         
        if (os.path.exists(address+'/middleResults/result.xml')):
            time.sleep(0.3)
            ##################read the result.xml and pick the root###############           
            try:
                doc=minidom.parse(address+'/middleResults/result.xml')
                root=doc.documentElement                
                break
            except Exception as err:
                print("null file error : err")
                continue
    
    #########################extract the file
    root_Result, notEmpty, loading=Trans.trans(root, packageName, className,commands, port)
    return root_Result,notEmpty, loading

#def expOtherApp(root_Result,d,height,weight):
def expOtherApp(d,height,weight):

    
    for i in range(0,10):
            xRandom=random.uniform(0, weight)
            yRandom=random.uniform(0, height)
            print("click other app:"+str(int(i)))
            d.click(int(xRandom),int(yRandom))
    return
    
    
    '''
    runableEleList=root_Result.getElementsByTagName('runableID')

    ##############random select
    xAvailableList=[]
    for runableEle in runableEleList:
        
        if len(runableEle.getElementsByTagName("xposition"))>0:
            xAvailableList.append(runableEle)
    
    lastClassName=""
    maxList=[]
    midList=[]
    
    for index in range(len(xAvailableList)):
        eleItem=xAvailableList[index]
        
        if len(runableEle.getElementsByTagName("viewclass"))>0:
            classEle=runableEle.getElementsByTagName("viewclass")[0]
            currentName=classEle.firstChild.nodeValue
            
            
            if currentName==lastClassName:
                midList.append(eleItem)
                
            else:
                if len(midList)>=len(maxList):
                    maxList=midList
                    
                midList=[]
                midList.append(eleItem)
                
                lastClassName=currentName
    
    
    if len(midList)>=len(maxList):
        maxList=midList
    
    if len(maxList)>0:
    
        runableEle=random.choice(maxList)
        xEle=runableEle.getElementsByTagName("xposition")[0]
        yEle=runableEle.getElementsByTagName("yposition")[0]
    
        xPos=xEle.firstChild.nodeValue
        yPos=yEle.firstChild.nodeValue
    
        run_with_limited_time(d.click, (int(xPos),int(yPos),), {}, 5)

        print("aa")
    '''
def closekeyBoard(commands, port):
    
    while(1):
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys input_method | grep mInputShown"
        outputStr=commands.getstatusoutput(cmd)
        if "mInputShown=true" in outputStr[1]:
            cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell input keyevent 111"
            commands.getstatusoutput(cmd)
        else:
            break

def step(actionIndex, d, feature, commands, address, port, apkName, packageName, activityName, specChar, eventNum, height,weight):
    
    d.orientation = "n"
    d.screen.on()
    '''
    #########close the keyboard it detected
    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb shell dumpsys input_method | grep mInputShown"
    outputStr=commands.getstatusoutput(cmd)
    if "mInputShown=true" in outputStr[1]:
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb shell input keyevent 111"
        commands.getstatusoutput(cmd)
    '''
    
    if actionIndex=="text":
        #editLen=len(feature.editAbleList)
        if  feature.editAbleList:
            eachObject=random.choice(feature.editAbleList)
            childViewName=eachObject.childViewName
            viewName=eachObject.viewName
            editAction(eachObject, d,commands, port, specChar)
            eventNum[0]=eventNum[0]+1
            time.sleep(0.5)

            
    elif actionIndex=="menu":
        d.press.menu()
        eventNum[0]=eventNum[0]+1
        time.sleep(0.5)

    elif actionIndex=="back":
        d.press.back()
        eventNum[0]=eventNum[0]+1
        time.sleep(0.5)

    elif actionIndex=="click":
        if feature.shortAbleList:
            eachObject=random.choice(feature.shortAbleList)
            shortLongaction(eachObject, d)
            eventNum[0]=eventNum[0]+1
            time.sleep(0.5)

        
        
    elif actionIndex=="longclick":
        if feature.longAbleList:
            eachObject=random.choice(feature.longAbleList)
            shortLongaction(eachObject, d)
            eventNum[0]=eventNum[0]+1
            time.sleep(0.5)



    elif actionIndex=="swipe":
        if feature.shortAbleList:
        
            eachObject=random.choice(feature.shortAbleList)
            swipeAction(eachObject, d, height,weight)
            eventNum[0]=eventNum[0]+1
            time.sleep(0.5)

        #feature.longAbleList
        
    #time.sleep(0.5)

    
def editAction(runAbleObject, d, commands ,port, specChar):
    
    textX=runAbleObject.x
    textY=runAbleObject.y
    
    d.click(int(textX),int(textY))
    
    if specChar:#specChar trigger a crash before
        cmd="adb -e shell input text \"test123\""
    else:
        cmd="adb -e shell input text \"input%stext\\'\\{\\.345678909871231\""
    #cmd="adb -e shell input text 123asd"
    commands.getstatusoutput(cmd) 
    
def swipeAction(runAbleObject, d, height,weight):
    textX=runAbleObject.x
    textY=runAbleObject.y
    
    xRandom=random.uniform(0, weight)
    yRandom=random.uniform(0, height)
    #print("click other app:"+str(int(i)))
    d.click(int(xRandom),int(yRandom))
    d.swipe(textX, textY, int(xRandom),int(yRandom), steps=5)
    
def shortLongaction(runAbleObject, d):
    #textid=runAbleObject.ownId
    textX=runAbleObject.x
    textY=runAbleObject.y
    #textStr=runAbleObject.text
    #childViewName=runAbleObject.childViewName
    #viewName=runAbleObject.viewName
    clickType=runAbleObject.clickType
    '''
    outputFile = open("./testRecordsICST/"+"textRecord"+".txt", 'a')
    outputFile.write(str(str(runAbleObject.text))+"\n")
    outputFile.write(str(str(clickType))+"\n")
    outputFile.close()
    '''
    #runAbleObject.text
    
    
    #print("aaaaa")
        
    try:
        if clickType=="short":
            run_with_limited_time(d.click, (int(textX),int(textY),), {}, 6)
                
        elif clickType=="long":
            run_with_limited_time(d.long_click, (int(textX),int(textY),), {}, 6)
            #print("aa")
            #d.long_click(int(textX),int(textY))
    #d.wait.update()
    except Exception as err:
        print("event error")
    
    d.wait.update()
    time.sleep(0.5)
    
    
    
    
    
    

    
def run_with_limited_time(func, args, kwargs, time):
    """Runs a function with time limit

    :param func: The function to run
    :param args: The functions args, given as tuple
    :param kwargs: The functions keywords, given as dict
    :param time: The time limit in seconds
    :return: True if the function ended successfully. False if it was terminated.
    """
    p = Process(target=func, args=args, kwargs=kwargs)
    p.start()
    p.join(time)
    if p.is_alive():
        p.terminate()
        return False

    return True
'''
def writeCrash(logText,iterCount):
    
    
    outputFile = open("crashLog"+str(iterCount), 'a')
    outputFile.write(logText)
    outputFile.close()
'''
def writeCrash(logText, recordNameCrash ,crashID,eventNum):
    
    outputFile = open("./trainResultICST/"+recordNameCrash+"_crash_"+str(crashID)+".txt", 'a')
    #outputFile = open("crashLog"+str(iterCount), 'a')
    outputFile.write(str(eventNum[0]))
    outputFile.write(logText)
    outputFile.close()



    #outputFile = open("./trainResult/"+recordName+"_crash_"+str(crashID)+".txt", 'a')



def checkBefore(logText,logHistory):
    
    outPutStr=""
    
    count=None
    result=True
    specialChar=False
    for line in logText.splitlines():
        if "FATAL" in line or "fatal" in line:
            count=1
            
        if count and count<4 and "at" in line:
            
            subLineIndex=line.index("at")
            subLine=line[subLineIndex:]
            outPutStr+=subLine
            count+=1
            
            if not subLine in logHistory:
                result=False
                
        
        if "345678909871231" in line and "AndroidRuntime" in line:
            specialChar=True
        
    return result,outPutStr, specialChar

def restartApp(port,commands, packageName, activityName):
    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell am start -S -n "+packageName+"/"+activityName
    commands.getstatusoutput(cmd)
    ##############take class name
    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys window windows | grep -E 'mFocusedApp'"
    tupleLine=commands.getstatusoutput(cmd)
    className=str(tupleLine).split(" ")[-2]
    return className

def restartAndroidEumlator(port,commands):
    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" emu kill"
    print(commands.getstatusoutput(cmd))
    time.sleep(10)
    print("restarting the Emulator")
    
    cmd="./start.sh"
    #cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/tools/emulator -writable-system -avd testAVD -wipe-data"
    #subprocess.check_output(["/home/yu/adt-bundle-linux-x86_64-20140702/sdk/tools/emulator","-writable-system","-avd","testAVD","-wipe-data","&"])
    
    sub.Popen('/home/yu/adt-bundle-linux-x86_64-20140702/sdk/tools/emulator -writable-system -avd ' + "testAVD" + " -wipe-data", stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
    #sub.Popen('/home/yu/adt-bundle-linux-x86_64-20140702/sdk/tools/emulator -avd ' + "and-4" + " -wipe-data", stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
    
    #thread = subprocess.Popen(["/home/yu/adt-bundle-linux-x86_64-20140702/sdk/tools/emulator","-writable-system","-avd","testAVD","-wipe-data"])
    #thread.start()
    
    #print(commands.getstatusoutput(cmd))
    print("lacunching the Emulator")
    time.sleep(90)

    
def compileApkEmma(sourceCodePath,commands, os):
    '''not useful
    cmd="android update project -p "+sourceCodePath
    print(commands.getstatusoutput(cmd))
    
    cmd="ant instrument "+sourceCodePath
    print(commands.getstatusoutput(cmd))
    
    cmd="ant installi "+sourceCodePath
    print(commands.getstatusoutput(cmd))
    '''
    apkFile=""
    coverageEm=""
    packageName=""
    activityName=""
    
    for fileName in os.listdir(sourceCodePath):
        if fileName.endswith("debug.apk"):
        #if fileName.endswith("instrumented.apk"):
            apkFile=sourceCodePath+fileName
        if fileName.endswith("coverage.em"):
            coverageEm=sourceCodePath+fileName
            
        


    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/build-tools/23.0.3/aapt dump badging "+apkFile+" | awk '/package/{gsub(\"name=|'\"'\"'\",\"\");  print $2}'"
    packageName=commands.getstatusoutput(cmd)
    
    
    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/build-tools/23.0.3/aapt dump badging "+apkFile+" | awk '/launchable-activity/{gsub(\"name=|'\"'\"'\",\"\");  print $2}'"
    activityName=commands.getstatusoutput(cmd)
            
    return apkFile,coverageEm,packageName[1],activityName[1]
    
def computeRewardCoverage(commands,port, path, coverageData):
    
    
    ###############clean coverage.ec
    cmd="rm -r ./coverage.ec"
    print(commands.getstatusoutput(cmd))
    cmd="rm -r ./emmaOutput.txt"
    print(commands.getstatusoutput(cmd))
    
    ##############
    cmd1="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell am broadcast -a edu.gatech.m3.emma.COLLECT_COVERAGE"
    print(commands.getstatusoutput(cmd1))
    #########################
    cmd2="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" pull /mnt/sdcard/coverage.ec ./coverage.ec"
    print(commands.getstatusoutput(cmd2))
    ########################
    cmd3="java -cp /home/yu/adt-bundle-linux-x86_64-20140702/sdk/tools/lib/emma.jar emma report -r txt -in "+ path  +"coverage.em,./coverage.ec -Dreport.txt.out.file=./emmaOutput.txt"
    print(commands.getstatusoutput(cmd3))
    
    ##################read the outputFile
    f1=open("./emmaOutput.txt")
    contents=f1.readlines()
    
    lineCoverageNew=0
    methodCoverageNew=0
    classCoverageNew=0#class is not the activity
    
    for line in contents:
        if "(" in line:
            for i in range(0,4):
                index=line.find("(")
                numStr=""
                while(1):
                    index+=1
                    if line[index].isdigit():
                        numStr+=line[index]
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
    
    reward=0
    if lineCoverageNew>coverageData[0]:
        reward=5#5 for linear
        coverageData[0]=lineCoverageNew
    else:
        reward=-2#-2 for linear
    
    return reward
    '''
    if lineCoverageNew>coverageData[0]:
        reward+=20
        coverageData[0]=lineCoverageNew
    '''
    
def cleanSd(commands, port):
    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell rm -r sdcard/coverage.ec"
    commands.getstatusoutput(cmd)
    
    
    
    
def checkMenu(commands, port):
    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys window policy | grep mLastFocusNeedsMenu"
    menuStr=commands.getstatusoutput(cmd)
    if "Menu=true" in menuStr[1]:
        return True
    return False
        
    print(commands.getstatusoutput(cmd))
    
    