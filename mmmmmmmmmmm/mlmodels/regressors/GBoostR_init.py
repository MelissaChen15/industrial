# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 16:37


from sklearn import ensemble
import os
from main_entry.process.Para import Para
para = Para()

def init():
    #  Gradient Boosting Regressor参数
    #['alpha', 'criterion', 'init', 'learning_rate', 'loss', 'max_depth', 'max_features', 'max_leaf_nodes',
    # 'min_impurity_decrease', 'min_impurity_split', 'min_samples_leaf', 'min_samples_split', 'min_weight_fraction_leaf',
    # 'n_estimators', 'n_iter_no_change', 'presort', 'random_state', 'subsample', 'tol',
    #   'validation_fraction', 'verbose', 'warm_start']
    # 初始化模型
    model = ensemble.GradientBoostingRegressor(random_state=para.seed)
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "GBoostR") == False:
        os.mkdir(para.path_results + "GBoostR")

    return model, "GBoostR"