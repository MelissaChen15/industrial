# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 10:57

from sklearn import svm
from sklearn.model_selection import GridSearchCV, ShuffleSplit
import os
from main_entry.Para import Para
para = Para()

def init():
    # SVR 参数
    #['C', 'cache_size', 'coef0', 'degree', 'epsilon', 'gamma', 'kernel',
    # 'max_iter', 'shrinking', 'tol', 'verbose']
    # param_grid = {'C': [1e-3, 1e-2, 1e-1, 0.3,1,3, 5, 10],
    #               'gamma':[1e-4,3e-4,1e-3,3e-3,0.01,0.03,0.1,0.3,1,5,10]
    #               }
    param_grid = {'C': [1e-3, 1e-2, 1e-1],
                  'gamma':[1e-3,3e-3,0.01,0.03]
                  }
    cv_split = ShuffleSplit(n_splits=5, train_size=0.9, test_size=0.1)

    #初始化模型
    model = GridSearchCV(estimator=svm.SVR(), param_grid=param_grid, cv=cv_split, n_jobs=3)
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "SVR") == False:
        os.mkdir(para.path_results + "SVR")

    return model, "SVR"
