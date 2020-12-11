import os
from xml.dom.minidom import Document
from xml.dom import minidom

def main():
    targetFile="com.kvance.Nectroid_11_src"
    
    
    
    fileList=os.listdir("/home/yu/workspace2/rf-android/signalCNN/trainResult")

    ############build rfSet
    cancelWin=0
    noCancelWin=0
    bothWin=0
    bothLost=0
    
    for fileName in os.listdir("/home/yu/workspace2/rf-android/signalCNN/trainResult"):
        
        #if targetFile+"_record" in fileName:

        if "_record" in fileName:
            filePath="/home/yu/workspace2/rf-android/signalCNN/trainResult/"+fileName
            
            doc=minidom.parse(filePath)
            recordRoot=doc.documentElement
            
            bbList = recordRoot.getElementsByTagName('Result')
            
            
            for bb in bbList:
                similarList=bb.getAttribute("similarEx").split(";")
                
                if len(similarList)>0:#==5:
                    cancel=False
                    ok=False
                    runEleList=bb.getElementsByTagName('runableID')
                    
                    textList=[]
                    indexC=0
                    indexO=0
                    lastText=""
                    for runEle in runEleList:
                        text=""
                        testEleList=runEle.getElementsByTagName('viewtext')
                        for testEle in testEleList:
                            textValue=testEle.firstChild.nodeValue.lower()
                            
                            text+=textValue
                            
                        textList.append(text)
                    
                        if text=="cancel":
                            cancel=True
                            cancelIndex=indexC
                            print(lastText)
                            
                            
                        
                        elif text=="ok":
                            ok=True
                            okIndex=indexC
                         
                        indexC+=1
                        lastText=text
                            
                    if cancel and ok:
                        cancelSim=int(similarList[cancelIndex])
                        #noCancelId=cancelIndex-1
                        
                        '''
                        if cancelIndex==4:
                            noCancelId=3
                        elif cancelIndex==3:
                            noCancelId=4
                        '''
                        
                        noCancelSim=int(similarList[okIndex])
                        
                        if not cancelSim==0 and noCancelSim==0:
                            cancelWin+=1
                        elif cancelSim==0 and not noCancelSim==0:
                            noCancelWin+=1
                        elif not cancelSim==0 and not noCancelSim==0: 
                            bothWin+=1
                        elif cancelSim==0 and cancelSim==0:
                            bothLost+=1
                            
    print(cancelWin)
    print(noCancelWin)
    print(bothWin)
    print(bothLost)
        

    
if __name__ == '__main__':
    main()   



