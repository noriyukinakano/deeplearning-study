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

y = pd.Series(target_df.action)
len(y)

X = target_df.drop(["action","stage","rowid"], axis=1).iloc[:,0:50]
len(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

## PCA n_components 2
pca = PCA(n_components=2)
X_train_pca = pca.fit_transform(X_train_scaled)
print('X_train_pca shape: {}\n'.format(X_train_pca.shape))
print('explained variance ratio: {}\n'.format(pca.explained_variance_ratio_))

temp = pd.DataFrame(X_train_pca)
temp['stage'] = y_train.values
stage_1 = temp[temp['stage'] == 1]
stage_2 = temp[temp['stage'] == 2]
stage_3 = temp[temp['stage'] == 3]
stage_4 = temp[temp['stage'] == 4]
stage_5 = temp[temp['stage'] == 5]
plt.scatter(x=stage_1[0], y=stage_1[1], marker='.')
plt.scatter(x=stage_2[0], y=stage_2[1], marker='o')
plt.scatter(x=stage_3[0], y=stage_3[1], marker='v')
plt.scatter(x=stage_4[0], y=stage_4[1], marker='s')
plt.scatter(x=stage_5[0], y=stage_5[1], marker='+')

plt.xlabel('PC 1')
plt.ylabel('PC 2')
plt.savefig('/usr/local/src/temp2.png')
plt.clf()
