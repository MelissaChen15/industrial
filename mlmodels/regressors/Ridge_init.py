# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 16:37


from sklearn import linear_model
from sklearn.model_selection import GridSearchCV, ShuffleSplit
import os
from main_entry.Para import Para
para = Para()

def init():
    # Ridge 参数
    #['alpha', 'copy_X', 'fit_intercept', 'max_iter', 'normalize', 'random_state', 'solver', 'tol']
    param_grid = {'alpha': [0.01,0.02,0.1,0.5,1.0,2.0,5.0]
                  }
    cv_split = ShuffleSplit(n_splits=5, train_size=0.9, test_size=0.1)

    # 初始化模型
    model = GridSearchCV(estimator=linear_model.Ridge(), param_grid=param_grid, cv=cv_split, n_jobs=1)
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "Ridge") == False:
        os.mkdir(para.path_results + "Ridge")

    return model, "Ridge"