# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 12:41:58 2019

@author: 19083
"""

# Load libraries
import pandas
import pickle
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import VotingClassifier

# Load dataset
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/iris.csv"
names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
dataset = pandas.read_csv(url, names=names)

array = dataset.values
#first 3 columns
X = array[:,0:4]
#the fourth column
Y = array[:,4]
testsize = 0.20
seed = 5
X_train, X_test, Y_train, Y_test = \
model_selection.train_test_split(X, Y, test_size=testsize, random_state=seed)

# Test options and evaluation metric
seed = 5

# Spot Check Algorithms
models = []
models.append(('LRA', LogisticRegression(solver='liblinear', multi_class='ovr')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('DTC', DecisionTreeClassifier()))
models.append(('GNB', GaussianNB()))
models.append(('SVM', SVC(gamma='auto')))

model = VotingClassifier(estimators=models, voting='hard')
model.fit(X_train,Y_train)
print('accuracy: ',model.score(X_test,Y_test))
predictions = model.predict(X_test)
print(accuracy_score(Y_test, predictions))
print(confusion_matrix(Y_test, predictions))
print(classification_report(Y_test, predictions))

# Saving model to disk
pickle.dump(model, open('modelensemble.pkl','wb'))

# Loading model to compare the results and make sure it works
model = pickle.load(open('modelensemble.pkl','rb'))
print(model.predict([[5.1,3.3,1.6,0.3]]))