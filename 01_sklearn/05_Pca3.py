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

## PCA n_components 3
pca = PCA(n_components=3)
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

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.scatter(stage_1[0],stage_1[1], stage_1[2], marker='.')
ax.scatter(stage_2[0],stage_2[1], stage_2[2], marker='o')
ax.scatter(stage_3[0],stage_3[1], stage_3[2], marker='v')
ax.scatter(stage_4[0],stage_4[1], stage_4[2], marker='s')
ax.scatter(stage_5[0],stage_5[1], stage_5[2], marker='+')
ax.set_xlabel('PC 1')
ax.set_ylabel('PC 2')
ax.set_zlabel('PC 3')
plt.savefig('/usr/local/src/temp3.png')
plt.clf()
