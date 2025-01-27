# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 16:37


from sklearn import linear_model
from sklearn.model_selection import GridSearchCV, ShuffleSplit
import os
from main_entry.Para import Para
para = Para()

def init():
    # Lasso 参数
    #['alpha', 'copy_X', 'fit_intercept', 'max_iter',
    # 'normalize', 'positive', 'precompute', 'random_state', 'selection', 'tol', 'warm_start']
    param_grid = {'alpha': [1e-4,3e-4,1e-3,3e-3,0.01,0.03,0.1,0.3,1,5,10]
                  }
    cv_split = ShuffleSplit(n_splits=5, train_size=0.9, test_size=0.1)

    # 初始化模型
    model = GridSearchCV(estimator=linear_model.Lasso(), param_grid=param_grid, cv=cv_split, n_jobs=1)
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "Lasso") == False:
        os.mkdir(para.path_results + "Lasso")

    return model, "Lasso"