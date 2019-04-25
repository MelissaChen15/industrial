# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 16:37


from sklearn import ensemble
from sklearn.model_selection import ShuffleSplit,GridSearchCV
import os
from main_entry.Para import Para
para = Para()

def init():
    # Random Forest Regression 参数
    #['bootstrap', 'criterion', 'max_depth', 'max_features', 'max_leaf_nodes', 'min_impurity_decrease', 'min_impurity_split',
    # 'min_samples_leaf', 'min_samples_split','min_weight_fraction_leaf', 'n_estimators', 'n_jobs', 'oob_score',
    # 'random_state', 'verbose', 'warm_start']
    param_grid = {
        'max_features': ['auto'],  # 允许单个决策树使用特征的最大数量, 增加可以提高模型的效果，但是会降低树的多样性和降低运算速度,特征小于50的时候一般使用所有的
        'n_estimators': list(range(10, 110, 10)),  # 子树的数量，越大模型越稳定，但是运算变慢
        'min_samples_leaf': list(range(50, 500, 10))  # 叶子节点最小样本数，太小容易过拟合
    }
    cv_split = ShuffleSplit(n_splits=5, train_size=0.9, test_size=0.1)

    # 初始化模型
    model = GridSearchCV(estimator=ensemble.RandomForestRegressor(random_state=para.seed), param_grid=param_grid,
                         cv=cv_split, n_jobs=3)
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "RFR") == False:
        os.mkdir(para.path_results + "RFR")

    return model, "RFR"