import numpy as np
import time
import subprocess as sub
import random
#import threading
def dumpTrans( d, address, minidom, os, Trans, packageName, className,commands, port):
    ################dump
    try:
        d.dump(address+"/middleResults/result.xml")
        
    except:
        d.press.back()
        d.wait.update()
        time.sleep(0.5)
        d.dump(address+"/middleResults/result.xml")
        print("uiautomator dump except, solve: click back")
    
    #################check menu
    #menuTag=ENV.checkMenu(commands, port)
    
    ################dump
    d.dump(address+"/middleResults/result.xml")
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

def closekeyBoard(commands, port):
    
    while(1):
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys input_method | grep mInputShown"
        outputStr=commands.getstatusoutput(cmd)
        if "mInputShown=true" in outputStr[1]:
            cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell input keyevent 111"
            commands.getstatusoutput(cmd)
        else:
            break

def step(actionIndex, d, feature, commands, address, port, apkName, packageName, activityName):
    
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
    
    #closekeyBoard(commands,port)
    ############first to fill all blanket
    for eachObject in feature.editAbleList:
        childViewName=eachObject.childViewName
        viewName=eachObject.viewName
        editAction(eachObject, d,commands, port)

            
    ############click
    indexMax=actionIndex
    
    runAbleObject=feature.runableList[indexMax]
    
    action(runAbleObject, d, apkName, packageName, port, commands, activityName)
    
def editAction(runAbleObject, d, commands ,port):
    textid=runAbleObject.ownId
    #closekeyBoard(commands)
    shouldInput=False
    
    defaultInputList=["to","enter","input","password","user"]#,"345678909871231" do not need to fill again
    
    
    if runAbleObject.text=="":
        shouldInput=True
        
    elif not (any(letter.isalnum() for letter in runAbleObject.text) or any(letter.isalpha() for letter in runAbleObject.text)):
        shouldInput=True
        
        
        
    for inputText in defaultInputList:
        if inputText in runAbleObject.text.lower():#some default txt which should be edited
            shouldInput=True
        
    if shouldInput:
        try:
            #d(resourceId=textid).clear_text()
            d(resourceId=textid).set_text("12_';,.~`{[(&345678909871231")
        except:
            print("can not edit the edit box")
            closekeyBoard(commands, port)
    
def action(runAbleObject, d, apkName, packageName, port , commands, activityName):
    textStr=runAbleObject.text
    
    
    if "big game view aaa" in textStr:
        xBounder=runAbleObject.xBounder
        yBounder=runAbleObject.xBounder
        
        int(xBounder.split(":")[0])
        
        xbegin=int(xBounder.split(":")[0])
        xend=int(xBounder.split(":")[1])
        
        
        ybegin=int(yBounder.split(":")[0])
        yend=int(yBounder.split(":")[1])
    
        
        for i in range(0,50):
            xRandom=random.uniform(xbegin, xend)
            yRandom=random.uniform(ybegin, yend)
            print("click game:"+str(int(i)))
            d.click(int(xRandom),int(yRandom))
            #time.sleep(0.1)
    
    if textStr=="scroll button aaa":
        #d.press.back()
        d(scrollable=True).scroll.toEnd(steps=30, max_swipes=3)
        print("do scroll")
        return
    
    
    
    if textStr=="back button aaa":
        d.press.back()
        print("click back")
        return
    
    elif textStr=="menu button aaa":
        d.press.menu()
        print("click menu")
        return
    
    elif textStr=="restart button aaa":
        #just close and restart
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell am force-stop "+packageName
        #print(commands.getstatusoutput(cmd))
        commands.getstatusoutput(cmd)
        print("click restart")
        
        
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell am start -S -n "+packageName+"/"+activityName
        commands.getstatusoutput(cmd)
        
        '''reinstall
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell pm uninstall "+packageName
        print(commands.getstatusoutput(cmd))
        
        cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb install "+apkName
        print(commands.getstatusoutput(cmd))
        '''
        return
        
        
    
    ##################################
    textid=runAbleObject.ownId
    textX=runAbleObject.x
    textY=runAbleObject.y
    #textStr=runAbleObject.text
    #childViewName=runAbleObject.childViewName
    #viewName=runAbleObject.viewName
    clickType=runAbleObject.clickType
    

        
    try:
        if clickType=="short":
            '''
            if not textid=="":
                d(resourceId=textid).click();
                
            #elif textStr=="":
            #    d(text=textStr).click();
            else:
            '''
            d.click(int(textX),int(textY))
                
        elif clickType=="long":
            #if not textid=="":
            #    d(resourceId=textid).long_click()
                
            #elif textStr=="":
            #    d(text=textStr).long_click();
            #else:
            d.long_click(int(textX),int(textY))
    #d.wait.update()
    except Exception as err:
        print("event error")
    
    d.wait.update()
    time.sleep(0.5)
    
    
def writeCrash(logText,iterCount):
    
    
    outputFile = open("crashLog"+str(iterCount), 'a')
    outputFile.write(logText)
    outputFile.close()

def checkBefore(logText,logHistory):
    
    outPutStr=""
    
    count=None
    result=True
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
        
    return result,outPutStr

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
    time.sleep(60)

    
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
    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell rm -r sdcard/*"
    commands.getstatusoutput(cmd)
    
def checkMenu(commands, port):
    cmd="/home/yu/adt-bundle-linux-x86_64-20140702/sdk/platform-tools/adb -s emulator-"+port+" shell dumpsys window policy | grep mLastFocusNeedsMenu"
    menuStr=commands.getstatusoutput(cmd)
    if "Menu=true" in menuStr[1]:
        return True
    return False
        
    print(commands.getstatusoutput(cmd))
    
    