# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 21:25:31 2019

@author: 19083
"""

import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score,KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline

dataframe = pd.read_csv("iris.csv",header=None)
dataset = dataframe.values
X = dataset[:,0:4].astype(float)
Y = dataset[:,4]
#encode class value
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
model_y = np_utils.to_categorical(encoded_Y)

#define baseline model
def baseline_model():
    model = Sequential()
    model.add(Dense(8,input_dim=4,activation='relu'))
    model.add(Dense(3,activation='softmax'))
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    return model

estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5,verbose=0)
kfold = KFold(n_splits=10,shuffle=True)
 
results = cross_val_score(estimator,X,model_y,cv=kfold)
print("baseline: %.2f%% (%.2f%%)" % (results.mean()*100,results.std()*100))
