'''
Created on Jun 12, 2017

@author: yu
'''

###############################
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K

from keras.layers import TimeDistributed,Conv1D,Dense,Embedding,Input,Dropout,LSTM,Bidirectional,MaxPooling1D,Flatten,concatenate
from keras.initializers import Constant
from keras.models import Model
from keras.models import load_model




import tensorflow as tf

###############################
import random
import numpy as np
from collections import deque
import os




EPISODES = 1000

class DQNAgentClass:
    def __init__(self, wordEmbeddings):
        
        self.maxwordEvent=20
        self.vectorSize=400
        self.memory={}
        #self.memory = deque(maxlen=2000)
        
        #self.gamma = 0.7    # discount rate
        self.gamma = 0.4    # discount rate
        '''
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        #self.learning_rate = 0.001
        '''
        self.wordEmbeddings=wordEmbeddings
        self.model = self._build_model()
        #self.middleModel=Model(inputs=self.model.input,outputs=self.model.get_layer("middle").output)
        
        if os.path.exists("./model/keras_model.h5"):
            #self.model = load_model("./model/keras_model.h5")
            self.model.load_weights("./model/keras_model.h5")
            print("existing model")
        
        
        
        '''
        if not os.path.exists("./model/keras_model.h5"):
            self.model = self._build_model()
        else:
            #self.model = load_model("./model/keras_model.h5")
            self.model.load_weights("./model/keras_model.h5")
            print("existing model")
        '''


    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        
        
        #sents_input = Input(shape=(5,Maxwordsent), name='sents_input')
        sents_input = Input(shape=(None, self.maxwordEvent), name='sents_input')
        words = TimeDistributed(Embedding(input_dim=self.wordEmbeddings.shape[0], output_dim=self.wordEmbeddings.shape[1], embeddings_initializer=Constant(self.wordEmbeddings), trainable=False), trainable=False,  name='middle')(sents_input)#shape[0]is the vacoabilry size, shape[1] is output size #embedding_1 (Embedding)         (None, None, 100)  the first None is the batch, the second None is the number of word in a sentence
        
        
        text_conv1d_out= TimeDistributed(Conv1D(kernel_size=3, filters=self.maxwordEvent, padding='same',activation='tanh', strides=1))(words) #(None, None, 52, 30) filters is the kernel number, it decide output how many vecters
        text_maxpool_out=TimeDistributed(MaxPooling1D(self.maxwordEvent))(text_conv1d_out)#in every items in 30, pick the max 52 the output is (None, None, 1, 30)
        text_flatten = TimeDistributed(Flatten())(text_maxpool_out)#(TimeDistrib (None, None, 500)   #TimeDistributed targets the time, it can accept the None.
        text_output = Dropout(0.5)(text_flatten)#(None, None, 500)
        ##################same and similar
        same_input = Input(shape=(None, 10), name='same_input')
        same_output=TimeDistributed(Dense(10, activation='relu'))(same_input)
                
        similar_input= Input(shape=(None, 10), name='similar_input')
        similar_output=TimeDistributed(Dense(10, activation='relu'))(similar_input)
        ##################
        
        output = concatenate([text_output, same_output, similar_output])
        
        
        ###################
        LSTM_output=Bidirectional(LSTM(self.vectorSize, return_sequences=True, dropout=0.50, recurrent_dropout=0.25))(output)
        Dense_output=Dense(self.vectorSize,activation='relu')(LSTM_output)
        Dropout_output=Dropout(0.5)(Dense_output)
        output=Dense(1, activation='linear')(Dropout_output)
        
        model=Model(inputs=[sents_input, same_input, similar_input],outputs=[output])
        model.compile(loss='mse', optimizer=Adam(lr=0.0001), metrics=['mse'])#before is 0.0001
        
        model.summary()
        
        
        '''
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        '''
        
        
        return model

    def memorize(self, lastFeatureTuple, action, reward, featureTuple):
        
        stepNum=len(lastFeatureTuple[0])
        if stepNum in self.memory:
            self.memory[stepNum].append((lastFeatureTuple, action, reward, featureTuple))
        else:
            self.memory[stepNum]=[(lastFeatureTuple, action, reward, featureTuple)]

    def act(self, featureTuple, iterCount):
        
        '''
        if np.random.rand() <= self.epsilon:
            return random.randrange(state.shape[0])#there is 0.01 probability random select after 17 eouside
        '''
        
        textFeatue,sameFeature,similarFeature=featureTuple
        
        if iterCount<20 or np.random.rand()<=0.2:
            return random.randrange(len(textFeatue))
        
        textFeatue = np.asarray([textFeatue])
        sameFeature=np.asarray([sameFeature])
        similarFeature=np.asarray([similarFeature])
        
        act_values = self.model.predict([textFeatue,sameFeature,similarFeature])
        
        #vector=self.middleModel.predict([textFeatue,sameFeature,similarFeature])
        '''
        for l in self.model.layers:
            print(l.name, l.trainable)
        '''
        
        
        
        #print(vector)
        
        
        
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size, lastStateStepNum, Feature2Digit, word2VecModel,word2Idx, testLastTuple, recordMiddleList):
        
        
        
        minibatch0=[]
        minibatch0.append(testLastTuple)
        
        sameNumHisList=self.memory[lastStateStepNum][:-1]
        
        if len(sameNumHisList)>5:
            minibatch0=minibatch0+random.sample(self.memory[lastStateStepNum][:-1],5)
        else:
            minibatch0=minibatch0+random.sample(self.memory[lastStateStepNum][:-1],len(sameNumHisList))
        #(self.memory.keys(),1)
        
        #############batch0
        states=[[], [], []]
        targets_f = []
        
        for lastFeatureTuple, action, reward, featureTuple in minibatch0:
            
            lastTextFeatue,lastSameFeature,lastSimilarFeature=lastFeatureTuple
            currentTextFeatue,currentSameFeature,currentSimilarFeature=featureTuple
            
            ########transfer format
            lastTextFeatueTran = np.asarray([lastTextFeatue])
            lastSameFeatureTran=np.asarray([lastSameFeature])
            lastSimilarFeatureTran=np.asarray([lastSimilarFeature])
            
            currentTextFeatueTran = np.asarray([currentTextFeatue])
            currentSameFeatureTran=np.asarray([currentSameFeature])
            currentSimilarFeatureTran=np.asarray([currentSimilarFeature])
            
            
            Qvalue = (reward + self.gamma * np.amax(self.model.predict([currentTextFeatueTran,currentSameFeatureTran,currentSimilarFeatureTran])[0]))
            #Qvalue = ((1-self.gamma)*reward + self.gamma * np.amax(self.model.predict([currentTextFeatueTran,currentSimilarFeatureTran])[0]))
            
            target_f = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran])[0]
            
            
            target_f[action]=Qvalue
            
            recordMiddleList.append((a,b,Qvalue))
                        
            states[0].append(lastTextFeatue)
            states[1].append(lastSameFeature)
            states[2].append(lastSimilarFeature)
            
            
            
            targets_f.append(target_f)
        
        history0 = self.model.fit(states, np.array(targets_f), epochs=30, verbose=0)
        
        
        
        #target_f = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran])
        
        #history0 = self.model.fit([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran], np.array(target_f), epochs=300, verbose=2)
        
        
        #target_fTest = self.model.predict([lastTextFeatueTran,lastSameFeatureTran,lastSimilarFeatureTran])[0]
    
        
        
        
        loss0 = history0.history['loss']
        print("loss0")      
        print(loss0)
        
        #loss1 = history1.history['loss']
        #print(loss1)
        
        #############################
        return loss0
        

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


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

    
