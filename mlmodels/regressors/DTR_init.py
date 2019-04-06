# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 16:37


from sklearn import tree
import os
from main_entry.Para import Para
para = Para()

def init():
    # Decision Tree Regressor参数
    #['criterion', 'max_depth', 'max_features', 'max_leaf_nodes', 'min_impurity_decrease', 'min_impurity_split',
    # 'min_samples_leaf', 'min_samples_split', 'min_weight_fraction_leaf', 'presort', 'random_state', 'splitter']
    # 初始化模型
    model = tree.DecisionTreeRegressor(min_samples_leaf=150, random_state=para.seed)
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "DTR") == False:
        os.mkdir(para.path_results + "DTR")

    return model, "DTR"