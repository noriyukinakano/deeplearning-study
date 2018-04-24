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

target_columns = ["column1",
                "column2",
                "column3",
                "column4",
                "column5",
                "column6"]

target_label = "target"

original_df = pd.read_csv('/usr/local/src/test.csv')
print('original_df shape: {}'.format(original_df.shape))

target_df = original_df.drop(original_df.columns[np.isnan(original_df).any()], axis=1)
print('target_df shape: {}'.format(target_df.shape))

y = target_df[target_label]
len(y)

X = target_df[target_columns]
len(X)

W = pd.merge(X, pd.DataFrame(y), right_index=True, left_index=True)
seaborn.pairplot(W, hue = target_label)
plt.savefig('/usr/local/src/pairplot_noscalled.png')
plt.clf()

scaler = StandardScaler()
X_scaled=scaler.fit_transform(X)
Z = pd.merge(pd.DataFrame(X_scaled), pd.DataFrame(y), right_index=True, left_index=True)

target_columns.append(target_label)
Z.columns = target_columns
plt.figure(figsize=(50, 50))
seaborn.pairplot(Z, hue = target_label)
plt.savefig('/usr/local/src/pairplot_scalled.png')
plt.clf()
