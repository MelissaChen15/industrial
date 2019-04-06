# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 16:37


from sklearn import ensemble
import os
from main_entry.Para import Para
para = Para()

def init():
    # Random Forest Regression 参数
    #['bootstrap', 'criterion', 'max_depth', 'max_features', 'max_leaf_nodes', 'min_impurity_decrease', 'min_impurity_split',
    # 'min_samples_leaf', 'min_samples_split','min_weight_fraction_leaf', 'n_estimators', 'n_jobs', 'oob_score',
    # 'random_state', 'verbose', 'warm_start']
    # 初始化模型
    model = ensemble.RandomForestRegressor(min_samples_leaf=150, random_state=para.seed)
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "RFR") == False:
        os.mkdir(para.path_results + "RFR")

    return model, "RFR"