# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 10:57

from sklearn import svm
from sklearn.model_selection import StratifiedShuffleSplit,GridSearchCV
import os
from main_entry.Para import Para
para = Para()

def init():
    # SVC 参数
    # ['C', 'cache_size', 'class_weight', 'coef0', 'decision_function_shape', 'degree', 'gamma', 'kernel', 'max_iter',
    #  'probability', 'random_state', 'shrinking', 'tol', 'verbose']
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 0.3,1,3, 5, 10],
                  'gamma':[1e-4,3e-4,1e-3,3e-3,0.01,0.03,0.1,0.3,1,5,10]
                  }
    cv_split = StratifiedShuffleSplit(n_splits=5, train_size=0.9, test_size=0.1)

    #初始化模型
    model = GridSearchCV(estimator=svm.SVC(), param_grid=param_grid, cv=cv_split, n_jobs=3)
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "SVC") == False:
        os.mkdir(para.path_results + "SVC")

    return model, "SVC"
