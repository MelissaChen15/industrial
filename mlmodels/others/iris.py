# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/13 8:44

from sklearn.datasets import load_iris

X = load_iris().data
y = load_iris().target

from sklearn.svm import SVC
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import cross_val_score

cv_split = ShuffleSplit(n_splits=5, train_size=0.7, test_size=0.25) # 进行几次交叉验证；训练集占总样本的百分比；测试集占总样本的百分比
svc_model = SVC()
score_ndarray = cross_val_score(svc_model, X, y, cv=cv_split)
print(score_ndarray)
print(score_ndarray.mean())