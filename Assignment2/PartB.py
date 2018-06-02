# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 18:45:12 2018

@author: DELL
"""

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import numpy as np

count_vect = CountVectorizer()
tfidf_transformer = TfidfTransformer()


train_data =fetch_20newsgroups(subset='train')
X_train_counts = count_vect.fit_transform(train_data.data)
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)


test_data = fetch_20newsgroups(subset='test')
X_test_counts = count_vect.transform(test_data.data)
X_test_tfidf = tfidf_transformer.transform(X_test_counts)


print('-'*40+'NavieBays_Classification'+'-'*40)
clf = MultinomialNB().fit(X_train_tfidf, train_data.target)
predictions_NB = clf.predict(X_test_tfidf)
print("NB_Accuracy: %.3f\n"%(np.mean(predictions_NB == test_data.target)))
print('NB_confusion_matrix:')
print(metrics.confusion_matrix(test_data.target, predictions_NB))
print('NB_classification_report:')
print(metrics.classification_report(test_data.target,predictions_NB,target_names=test_data.target_names))


#----------------LogisticRegression-----------------------

from sklearn.linear_model.logistic import LogisticRegression
print('-'*40+'LogisticRegression'+'-'*40)
classifier=LogisticRegression()
classifier.fit(X_train_tfidf,train_data.target)
predictions = classifier.predict(X_test_tfidf)

f = open('LogisticRegession_Result.txt','a', encoding = 'utf-8')
for doc, category in zip(test_data.data, predictions):
  f.write('Classified as: %s\n%s\n' %(train_data.target_names[category],doc))

print('LogisticRegession_Result output Success!')



print("LR_Accuracy: %.3f\n"%(np.mean(predictions == test_data.target)))
print('LR_confusion_matrix:')
print(metrics.confusion_matrix(test_data.target, predictions))
print('LR_classification_report:')
print(metrics.classification_report(test_data.target,predictions,target_names=test_data.target_names))

#---------------------KNN--------------------------
print('-'*40+'KNN_Classifier'+'-'*40)
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_tfidf,train_data.target)
KNN_prediction = knn.predict(X_test_tfidf)
print("KNN_Accuracy: %.3f\n"%(np.mean(KNN_prediction == test_data.target)))
print('KNN_confusion_matrix:')
print(metrics.confusion_matrix(test_data.target, KNN_prediction))
print('KNN_classification_report:')
print(metrics.classification_report(test_data.target,KNN_prediction,target_names=test_data.target_names))


#--------------------SVM--------------------------- run too long
from sklearn import svm

SVM_clf = svm.SVC(C=0.8, kernel='rbf', gamma=20, decision_function_shape='ovr')
SVM_clf.fit(X_train_tfidf,train_data.target)
print('-'*40+'SVM_Classifier'+'-'*40)
SVM_Predictions = SVM_clf.predict(X_test_tfidf)

print("SVM_Accuracy: %.3f\n"%(np.mean(SVM_Predictions == test_data.target)))
print('SVM_confusion_matrix:')
print(metrics.confusion_matrix(test_data.target, SVM_Predictions))
print('SVM_classification_report:')
print(metrics.classification_report(test_data.target,SVM_Predictions,target_names=test_data.target_names))

