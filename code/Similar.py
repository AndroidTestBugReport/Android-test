
#import strand
import re
from xml.dom.minidom import Document
from xml.dom import minidom
from __builtin__ import True


def compareSimiar(beforeResult, newRoot, tag):
    
    sameTag=True
    similarTag=False    
    ###################3check the noListView
    checkListBefore=beforeResult.childNodes
    checkListNew=newRoot.childNodes
    
    beforeLen=len(checkListBefore)
    
    ##################store old list view
    beforeDict={}
    #idDict={}###this is just for the similar case, key is the new id, value is the old id.
    newIdtobeIdDict={}##this is just for the similar case, key is the new id, value is the old id.
    
    newListBol=False
    oldListBol=False
    
    #########################
    newDefaultBol=False
    oldDefaultBol=False
    
    noListnumBefore=0###summarize the no list and default number, in case of different number of the clickable event list
    for i in range(0,len(checkListBefore)):#############check the before
        beforeEvent=checkListBefore[i]
        tagStr=beforeEvent.getAttribute("tag")
        if tagStr.startswith("list") :
            beforeDict[tagStr]=beforeEvent.getAttribute("id")
            oldListBol=True
        elif  tagStr.startswith("default"):
            beforeDict[tagStr]=beforeEvent.getAttribute("id")
            oldDefaultBol=True
        else:
            noListnumBefore+=1
               
    
    #################compare with new
    noListnumNew=0
    firstListBol=True
    for i in range(0,len(checkListNew)):
        
        eventNewEle=checkListNew[i]
    
        tagNewStr=eventNewEle.getAttribute("tag")
        
        if tagNewStr.startswith("normal"):
            noListnumNew+=1
            #############compare structure
            if i>=beforeLen or not checkListBefore[i].getAttribute("tag")==tagNewStr:
                sameTag=False
                similarTag=False
                return sameTag, similarTag, newIdtobeIdDict
            
            ############compare text
            oldText=checkListBefore[i].getAttribute("text")
            newText=eventNewEle.getAttribute("text")
            if not oldText==newText and (bool(re.search('[a-zA-Z]', oldText)) or bool (re.search('[a-zA-Z]', newText))):
                sameTag=False
                similarTag=True###the other returns may have similarTag=false as output
            
            newIdtobeIdDict[i]=i
            
        elif tagNewStr.startswith("special"):
            noListnumNew+=1
            #############compare structure
            if i>=beforeLen or not checkListBefore[i].getAttribute("tag")==tagNewStr:
                sameTag=False
                similarTag=False
                return sameTag, similarTag,newIdtobeIdDict

            newIdtobeIdDict[i]=i
            #beIdtoNewIdDict[beforeDict[tagNewStr]]=[eventNewEle.getAttribute("id")]


        elif tagNewStr.startswith("list"):
            newListBol=True
            
            if firstListBol:#### if new is at first list and old is not. return all false
                firstListBol=False
                if i>=beforeLen or not checkListBefore[i].getAttribute("tag").startswith("list"):
                    sameTag=False
                    similarTag=False
                    return sameTag, similarTag,newIdtobeIdDict 
            
            #############compare structure
            if i>=beforeLen or not checkListBefore[i].getAttribute("tag")==tagNewStr:###just check current and before is same or not at this event
                sameTag=False
                similarTag=True
            
                if tagNewStr in beforeDict:
                    newIdtobeIdDict[int(eventNewEle.getAttribute("id"))]=int(beforeDict[tagNewStr])
            else:
                newIdtobeIdDict[i]=i
                #beIdtoNewIdDict[beforeDict[tagNewStr]]=[eventNewEle.getAttribute("id")]

        elif tagNewStr.startswith("default"):       
            newDefaultBol=True     
            break
           
    if not len(checkListBefore)==len(checkListNew):
        sameTag=False
        
    if newDefaultBol^oldDefaultBol or newListBol^oldListBol:
        sameTag=False
        similarTag=False
        return sameTag, similarTag,newIdtobeIdDict
           
    if not noListnumNew==noListnumBefore:
        sameTag=False
        similarTag=False
        return sameTag, similarTag,newIdtobeIdDict
    return sameTag, similarTag,newIdtobeIdDict
    
    

def getSimilar(wholeRoot,newRoot):
    sameStr=""
    similarStrList=[]
    sameEvent=None
    similarEventList=[]
    
    newRoot=newRoot.getElementsByTagName("Easyoperate")[0]
    
    for beforeResult in wholeRoot.childNodes:#beforeResult means histroy node
        simiarCount=[0]
        beforeEasyoperate=beforeResult.getElementsByTagName("Easyoperate")[0]
        #newRoot=newRoot.getElementsByTagName("Easyoperate")[0]
        #compareResult=compareSimiar(beforeResult,newRoot,simiarCount, "normal")
        sameTag, similarTag, newIdtobeIdDict=compareSimiar(beforeEasyoperate,newRoot,simiarCount)
        
        #if 
        
        if sameTag==True:
            sameStr=beforeResult.getAttribute("sameEx")
            sameEvent=beforeResult
            similarStrList.append((beforeResult.getAttribute("similarEx"), newIdtobeIdDict))
        
        elif similarTag==True:
            similarEventList.append((beforeResult,newIdtobeIdDict))
            similarStrList.append((beforeResult.getAttribute("similarEx"), newIdtobeIdDict))
        
    sameResult=[]
    similarResult=[]
    
    
    ###########compute the runNum for the new one, it is easy to be understood in the coding but waste effienent
    newRunAbleNum=0
    checkListNew=newRoot.childNodes
    for i in range(0,len(checkListNew)):#############check the before
        beforeEvent=checkListNew[i]
        tagStr=beforeEvent.getAttribute("tag")
        if tagStr.startswith("default"):
            break
        newRunAbleNum+=1
    
    
    
    #############string process from "1;2;3" to [1,2,3] pick the max value for all similar results
    #newRunAbleNum=len(newRoot.childNodes)
    
    for index in range(0,newRunAbleNum):
        similarResult.append(0)
    
    
    if similarStrList:
        for oneSimilar,newIdtobeIdDict in similarStrList:####pick the maximum similarity
            itemList=oneSimilar.split(";")#
            
            for newIndex in range(0,len(similarResult)):
                if newIndex in newIdtobeIdDict:
                    oldIndex=newIdtobeIdDict[newIndex]
                    
                    oldSimVal=int(itemList[oldIndex])
                    '''
                    try:
                        oldSimVal=int(itemList[oldIndex])
                    except:
                        print("eeor")
                    '''
                    if similarResult[newIndex]<oldSimVal:
                        similarResult[newIndex]=oldSimVal
                        ###############
    
    if not sameStr=="":
        itemList=sameStr.split(";")
        for itemStr in itemList:
            sameResult.append(int(itemStr))
    
        
        
    return sameEvent,similarEventList,sameResult,similarResult
    
        
    '''
        if sameTag==True:#means similar or same
            if simiarCount[0]==0:#means just same
                sameStr=beforeResult.getAttribute("sameEx")
                sameEvent=beforeResult
                
                
            else:#means just similar
                #similarStrList.append(beforeResult.getAttribute("similarEx"))
                
                similarEventList.append(beforeResult)
            
            similarStrList.append(beforeResult.getAttribute("similarEx"))########similarEventList should update both same and similar, then the similar will be bigger than the same all the time
        
    
    sameResult=[]
    similarResult=[]
    
    
    
    #############string process from "1;2;3" to [1,2,3] pick the max value for all similar results
    
    if similarStrList:
    
        stepsNum=len(similarStrList[0].split(";"))
        
        
        for index in range(0,stepsNum):
            similarResult.append(0)
        
               
        for oneSimilar in similarStrList:
            itemList=oneSimilar.split(";")
            for index in range(0,stepsNum):
                if int(itemList[index])> similarResult[index]:
                    similarResult[index]=int(itemList[index])
    
    if not sameStr=="":
        itemList=sameStr.split(";")
        for itemStr in itemList:
            sameResult.append(int(itemStr))
    
        
        
    return sameEvent,similarEventList,sameResult,similarResult
    '''
def addToRecordRoot(recordRoot, root_Result,resultId,feature,featureStepNum,actionIndex,sameEvent, similarEventList):
    root_Result.setAttribute("id",str(resultId))##########add an id
    resultId+=1
    
    #############similar
    similarHisStr=""
    for i in range(featureStepNum):
        if i==actionIndex:
            similarHisStr+=str(feature.similarResultList[i]+1)+";"
        else:
            similarHisStr+=str(feature.similarResultList[i])+";"
            
    ###########same
    sameHisStr=""
    for i in range(featureStepNum):
        if i==actionIndex:
            sameHisStr+=str(feature.sameResultList[i]+1)+";"
        else:
            sameHisStr+=str(feature.sameResultList[i])+";"
            
    
    #######
    similarHisStr=similarHisStr[:-1]#remove the last ;
    sameHisStr=sameHisStr[:-1]#remove the last ; 
            
    if feature.sameExist:
        sameEvent.setAttribute("similarEx",similarHisStr)
        sameEvent.setAttribute("sameEx",sameHisStr)
        
        
    else:
        root_Result.setAttribute("similarEx",similarHisStr)
        root_Result.setAttribute("sameEx",sameHisStr)##########add same
        
        recordRoot.appendChild(root_Result)
    
    updateAllSimilar(similarEventList, actionIndex)
    #print(similarHisStr)
    
def updateAllSimilar(similarEventList, actionIndex):
    for oneSimEvent, newIdtobeIdDict in similarEventList:
        newStr=""
        oneSimliar=oneSimEvent.getAttribute("similarEx")
        itemList=oneSimliar.split(";")
        
        for i in range(0,len(itemList)):
            
            if actionIndex in newIdtobeIdDict and i==newIdtobeIdDict[actionIndex]:#sometimes current event is longer than before
                newStr+=str(int(itemList[i])+1)+";"
            else:
                newStr+=str(int(itemList[i]))+";"
                    
        newStr=newStr[:-1]
        oneSimEvent.setAttribute("similarEx",newStr)
        #print("getAttribute:   "+oneSimEvent.getAttribute("similarEx"))
    
def oldupdateAllSimilar_copy(similarEventList, similarHisStr):
    for oneSimEvent in similarEventList:
        oneSimEvent.setAttribute("similarEx",similarHisStr)
        #print("getAttribute:   "+oneSimEvent.getAttribute("similarEx"))
        
        
                
def computeRewardSimilar(feature):
    ############################similarity reward
    if not feature.similarExist and not feature.sameExist:
        return 10
    else:
        return -5
        
        
        
        
        