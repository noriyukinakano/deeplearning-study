# coding:utf-8
from __future__ import print_function, division

import os.path
import sys
import pandas as pd
import seaborn
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score
from mpl_toolkits.mplot3d import axes3d

original_df = pd.read_csv('/usr/local/src/20180417_test.csv')
print('original_df shape: {}'.format(original_df.shape))
original_df.stage.value_counts()

target_df = original_df.drop(original_df.columns[np.isnan(original_df).any()], axis=1)
print('target_df shape: {}'.format(target_df.shape))

y = pd.Series(target_df.stage)
len(y)

X = target_df.drop(["stage","rowid"], axis=1).iloc[:,0:50]
len(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

logistic = LogisticRegressionCV(cv=10, random_state=0)
logistic.fit(X_train_scaled, y_train)

print('Train score: {:.3f} \n'.format(logistic.score(X_train_scaled, y_train)))
print('Test score: {:.3f} \n'.format(logistic.score(X_test_scaled, y_test)))
print('Confustion matrix:\n{}'.format(confusion_matrix(y_true=y_test, y_pred=logistic.predict(X_test_scaled))))
print('accuracy_score:\n{}'.format(accuracy_score(y_true=y_test, y_pred=logistic.predict(X_test_scaled))))

# pipeline
pca_pipeline = Pipeline([
    ('scale', StandardScaler()),
    ('decomposition', PCA(n_components=30)),
    ('model', LogisticRegressionCV(cv=10, random_state=0))
])
pca_pipeline.fit(X_train, y_train)

print('Train score: {:.3f}'.format(pca_pipeline.score(X_train, y_train)))
print('Test score: {:.3f}'.format(pca_pipeline.score(X_test, y_test)))
print('Confustion matrix:\n{}'.format(confusion_matrix(y_true=y_test, y_pred=pca_pipeline.predict(X_test))))
print('accuracy_score:\n{}'.format(accuracy_score(y_true=y_test, y_pred=logistic.predict(X_test_scaled))))
