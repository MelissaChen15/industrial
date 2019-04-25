# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 16:37


from sklearn import tree
import os
from sklearn.model_selection import ShuffleSplit,GridSearchCV
from main_entry.Para import Para
para = Para()

def init():
    # Decision Tree Regressor参数
    #['criterion', 'max_depth', 'max_features', 'max_leaf_nodes', 'min_impurity_decrease', 'min_impurity_split',
    # 'min_samples_leaf', 'min_samples_split', 'min_weight_fraction_leaf', 'presort', 'random_state', 'splitter']
    param_grid = {
        'min_samples_leaf': list(range(50, 500, 10)),  # 叶子节点最小样本数，太小容易过拟合
        'splitter': ['random'],  # 在部分特征中找最好的切分点（数据量大的时候）
        'max_depth': list(range(10, 100, 10))  # 限制这个最大深度,防止过拟合

    }
    cv_split = ShuffleSplit(n_splits=5, train_size=0.9, test_size=0.1)
    # 初始化模型
    model = GridSearchCV(estimator=tree.DecisionTreeRegressor(random_state=para.seed), param_grid=param_grid, cv=cv_split, n_jobs=3)
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "DTR") == False:
        os.mkdir(para.path_results + "DTR")

    return model, "DTR"