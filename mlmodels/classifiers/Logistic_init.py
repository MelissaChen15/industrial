# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 16:37


from sklearn import linear_model
from sklearn.model_selection import GridSearchCV, ShuffleSplit
import os
from main_entry.Para import Para
para = Para()

def init():
    # Logistic 参数
    #['C', 'class_weight', 'dual', 'fit_intercept', 'intercept_scaling', 'max_iter',
    # 'multi_class', 'n_jobs', 'penalty', 'random_state', 'solver', 'tol', 'verbose', 'warm_start']
    param_grid = {
        'penalty' : ['l1'],
        'C': [1e-3, 1e-2, 1e-1, 0.3,1,3, 5, 10] # 默认:1.0 正则化强度， 与支持向量机一样，较小的值指定更强的正则化
                  }
    cv_split = ShuffleSplit(n_splits=5, train_size=0.9, test_size=0.1)

    # 初始化模型
    model = GridSearchCV(estimator=linear_model.LogisticRegression(random_state = para.seed), param_grid=param_grid, cv=cv_split, n_jobs=1)
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "Logistic") == False:
        os.mkdir(para.path_results + "Logistic")

    return model, "Logistic"