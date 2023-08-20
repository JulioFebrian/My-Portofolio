# -*- coding: utf-8 -*-
"""Crop recommendation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DGmiHt78n3ig47Zfi8EsSJSt-e7Z_Ek9
"""

# Importing libraries

from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn import metrics
from sklearn import tree
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('/content/Dataset_Rekomendasi_Tanaman.csv')

df.head()

df.tail()

df.size

df.shape

df.columns

df['Label'].unique()

df.dtypes

df['Label'].value_counts()

sns.heatmap(df.corr(),annot=True)

"""**Memisahkan fitur dan label target**"""

features = df[['Nitrogen (N)', 'Fosforus (P)','Kalium (K)','Suhu', 'Kelembaban', 'pH', 'Curah Hujan']]
target = df['Label']
#features = df[['Suhu', 'Kelembaban', 'pH', 'Curah Hujan']]
labels = df['Label']

# Inisialisasi list kosong untuk menambahkan semua nama model dan nama yang sesuai
acc = []
model = []

from sklearn.model_selection import train_test_split
Xtrain, Xtest, Ytrain, Ytest = train_test_split(features,target,test_size = 0.2,random_state =2)

"""**Decision Tree**"""

from sklearn.tree import DecisionTreeClassifier

DecisionTree = DecisionTreeClassifier(criterion="entropy",random_state=2,max_depth=5)

DecisionTree.fit(Xtrain,Ytrain)

nilai_prediksi = DecisionTree.predict(Xtest)
x = metrics.accuracy_score(Ytest, nilai_prediksi)
acc.append(x)
model.append('Decision Tree')
print("Akurasi Decision Tree: ", x*100)

print(classification_report(Ytest,nilai_prediksi))

from sklearn.model_selection import cross_val_score

# Nilai cross validation (Decision Tree)
score = cross_val_score(DecisionTree, features, target,cv=5)
score

"""Menyimpan trained model dari Decision Tree"""

import pickle
# Dump the trained Naive Bayes classifier with Pickle
DT_pkl_filename = '/content/DecisionTree.pkl'
# Open the file to save as pkl file
DT_Model_pkl = open(DT_pkl_filename, 'wb')
pickle.dump(DecisionTree, DT_Model_pkl)
# Close the pickle instances
DT_Model_pkl.close()

"""Gaussian Naive Bayes"""

from sklearn.naive_bayes import GaussianNB

NaiveBayes = GaussianNB()

NaiveBayes.fit(Xtrain,Ytrain)

nilai_prediksi = NaiveBayes.predict(Xtest)
x = metrics.accuracy_score(Ytest, nilai_prediksi)
acc.append(x)
model.append('Naive Bayes')
print("Akurasi Naive Bayes: ", x*100)

print(classification_report(Ytest,nilai_prediksi))

# Cross validation score (NaiveBayes)
score = cross_val_score(NaiveBayes,features,target,cv=5)
score

import pickle
# Dump the trained Naive Bayes classifier with Pickle
NB_pkl_filename = '/content/NaiveBayes.pkl'
# Open the file to save as pkl file
NB_Model_pkl = open(NB_pkl_filename, 'wb')
pickle.dump(NaiveBayes, NB_Model_pkl)
# Close the pickle instances
NB_Model_pkl.close()

"""**Support Vector Machine (SVM)**"""

from sklearn.svm import SVC
# data normalization with sklearn
from sklearn.preprocessing import MinMaxScaler
# fit scaler on training data
norm = MinMaxScaler().fit(Xtrain)
X_train_norm = norm.transform(Xtrain)
# transform testing dataabs
X_test_norm = norm.transform(Xtest)
SVM = SVC(kernel='poly', degree=3, C=1)
SVM.fit(X_train_norm,Ytrain)
nilai_prediksi = SVM.predict(X_test_norm)
x = metrics.accuracy_score(Ytest, nilai_prediksi)
acc.append(x)
model.append('SVM')
print("Akurasi SVM: ", x*100)

print(classification_report(Ytest,nilai_prediksi))

# Cross validation score (SVM)
score = cross_val_score(SVM,features,target,cv=5)
score

#Saving trained SVM model
import pickle
# Dump the trained SVM classifier with Pickle
SVM_pkl_filename = '/content/SVM.pkl'
# Open the file to save as pkl file
SVM_Model_pkl = open(SVM_pkl_filename, 'wb')
pickle.dump(SVM, SVM_Model_pkl)
# Close the pickle instances
SVM_Model_pkl.close()

"""**Logistic Regression**"""

from sklearn.linear_model import LogisticRegression

LogReg = LogisticRegression(random_state=2)

LogReg.fit(Xtrain,Ytrain)

nilai_prediksi = LogReg.predict(Xtest)

x = metrics.accuracy_score(Ytest, nilai_prediksi)
acc.append(x)
model.append('Logistic Regression')
print("Akurasi Logistic Regression: ", x*100)

print(classification_report(Ytest,nilai_prediksi))

# Cross validation score (Logistic Regression)
score = cross_val_score(LogReg,features,target,cv=5)
score

import pickle
# Dump the trained Logistic Regression classifier with Pickle
LR_pkl_filename = '/content/LogisticRegression.pkl'
# Open the file to save as pkl file
LR_Model_pkl = open(LR_pkl_filename, 'wb')
pickle.dump(LogReg, LR_Model_pkl)
# Close the pickle instances
LR_Model_pkl.close()

"""**Random Forest**"""

from sklearn.ensemble import RandomForestClassifier

RF = RandomForestClassifier(n_estimators=20, random_state=0)
RF.fit(Xtrain,Ytrain)

nilai_prediksi = RF.predict(Xtest)

x = metrics.accuracy_score(Ytest, nilai_prediksi)
acc.append(x)
model.append('RF')
print("Akurasi Random Forest: ", x*100)

print(classification_report(Ytest,nilai_prediksi))

# Cross validation score (Random Forest)
score = cross_val_score(RF,features,target,cv=5)
score

import pickle
# Dump the trained Naive Bayes classifier with Pickle
RF_pkl_filename = '/content/RandomForest.pkl'
# Open the file to save as pkl file
RF_Model_pkl = open(RF_pkl_filename, 'wb')
pickle.dump(RF, RF_Model_pkl)
# Close the pickle instances
RF_Model_pkl.close()

"""**XGBoost**"""

import xgboost as xgb
XB = xgb.XGBClassifier()
XB.fit(Xtrain,Ytrain)

nilai_prediksi = XB.predict(Xtest)

x = metrics.accuracy_score(Ytest, nilai_prediksi)
acc.append(x)
model.append('XGBoost')
print("Akurasi XGBoost: ", x*100)

print(classification_report(Ytest,nilai_prediksi))

# Cross validation score (XGBoost)
score = cross_val_score(XB,features,target,cv=5)
score

import pickle
# Dump the trained Naive Bayes classifier with Pickle
XB_pkl_filename = '/content/XGBoost.pkl'
# Open the file to save as pkl file
XB_Model_pkl = open(XB_pkl_filename, 'wb')
pickle.dump(XB, XB_Model_pkl)
# Close the pickle instances
XB_Model_pkl.close()

"""**Accuracy Comparison**"""

plt.figure(figsize=[10,5],dpi = 100)
plt.title('Accuracy Comparison')
plt.xlabel('Accuracy')
plt.ylabel('Algorithm')
sns.barplot(x = acc ,y = model,palette='dark')

accuracy_models = dict(zip(model, acc))
for k, v in accuracy_models.items():
    print (k, '-->', v)

"""**Making a prediction**"""

data = np.array([[104,18, 30, 23.603016, 60.3, 6.7, 140.91]])
prediction = RF.predict(data)
print(prediction)

data = np.array([[83, 45, 60, 28, 70.3, 7.0, 150.9]])
prediction = RF.predict(data)
print(prediction)