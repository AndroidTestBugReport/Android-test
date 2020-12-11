import DQNAgentDdqnNei as DQNAgent
from gensim.models import Word2Vec
import numpy as np

    
    
    
    
    
def main():

    word2VecModel= Word2Vec.load('yumodel').wv
    
    wordVectorLen=400#this is yumodel's len size
    
    neighborLen=10 #this is neighbor list's length
    
    word2Idx, wordEmbeddings=DQNAgent.build_embed( word2VecModel,wordVectorLen)

    str0Id=word2Idx["yes"]
    str1Id=word2Idx["no"]




    matrixDict={}

    agent = DQNAgent.DQNAgentClass( wordEmbeddings, neighborLen, matrixDict)############need to modification
    
    textFeatue=[]
    similarFeature=[]
    nei1Feature=[]
    nei2Feature=[]
    nei3Feature=[]
    
    textFeatue.append([str0Id]+[2]+[0]*4)
    similarFeature.append([0]*10)
    nei1Feature.append([0]*10)
    nei2Feature.append([0]*10)
    nei3Feature.append([0]*10)
    
    
    similarFeature=np.asarray(similarFeature)
    nei1Feature=np.asarray(nei1Feature)
    nei2Feature=np.asarray(nei2Feature)
    nei3Feature=np.asarray(nei3Feature)

    act_values = agent.model.predict([textFeatue,similarFeature, nei1Feature, nei2Feature, nei3Feature])
    
    print(act_values)
    ##################################
    textFeatue=[]
    similarFeature=[]
    nei1Feature=[]
    nei2Feature=[]
    nei3Feature=[]
    
    textFeatue.append([str1Id]+[2]+[0]*4)
    similarFeature.append([0]*10)
    nei1Feature.append([0]*10)
    nei2Feature.append([0]*10)
    nei3Feature.append([0]*10)
    
    
    similarFeature=np.asarray(similarFeature)
    nei1Feature=np.asarray(nei1Feature)
    nei2Feature=np.asarray(nei2Feature)
    nei3Feature=np.asarray(nei3Feature)

    act_values = agent.model.predict([textFeatue,similarFeature, nei1Feature, nei2Feature, nei3Feature])
    
    print(act_values)
    
    
    
    
    



if __name__ == '__main__':
    main()   