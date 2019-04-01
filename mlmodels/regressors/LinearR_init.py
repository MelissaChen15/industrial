# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 10:57

from sklearn import linear_model
from sklearn.model_selection import StratifiedShuffleSplit,GridSearchCV
import os
from mlmodels.main_etry.Para import Para
para = Para()

def init():
    # LinearR 参数
    # ['copy_X', 'fit_intercept', 'n_jobs', 'normalize']
    model = linear_model.LinearRegression()
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "LinearR") == False:
        os.mkdir(para.path_results + "LinearR")

    return model, "LinearR"
