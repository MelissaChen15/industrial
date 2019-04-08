# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/22 8:32

import xgboost as xgb
import os
from main_entry.process import load_sample_data, evaluate_strategy, build_strategy
from utilities import PCA_algorithm
from sklearn import preprocessing, metrics
from main_entry.Para import Para
para = Para()

import h5py
import pandas as pd
import numpy as np

# 对于通用的predict进行了修改，适应xgboost
def predict_xgboost(bst, model_name):
    # 模型预测
    n_days_in_test = 0  # 记录test set包含的天数
    accuracy_all_tests = []  # 记录每一天的预测准确度
    roc_all_tests = []  # 记录每一天的roc
    for i_month in para.month_test:  # 按月加载
        file_name = para.path_data + str(i_month) + ".h5"
        f = h5py.File(file_name, 'r')
        # print(file_name)
        for key in f.keys():  # 按天加载，按天预处理数据
            n_days_in_test += 1
            # 加载
            h5 = pd.read_hdf(file_name, key=str(key))
            data_curr_day = pd.DataFrame(h5)
            data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'].abs() >= 10.1)  # 去掉收益率绝对值大于10.1的数据点
            data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'] == 0.0)  # 去掉收益率为0的数据点
            data_curr_day = data_curr_day.dropna(axis=0)  # remove nan
            data_curr_day = load_sample_data.label_data(data_curr_day)  # 标记数据
            # 预处理
            X_curr_day = data_curr_day.loc[:, 'close':'amount'] # X的实际值
            y_curr_day = data_curr_day.loc[:, 'return_bin'] # y的实际标签
            # y_true_day = data_curr_day.loc[:, 'pct_chg'] # y的实际值

            scalar = preprocessing.StandardScaler().fit(X_curr_day) # 标准化
            X_curr_day = scalar.transform(X_curr_day)

            X_curr_day = PCA_algorithm.pca(X_curr_day) # pca

            X_curr_day = xgb.DMatrix(X_curr_day) # 将dataframe转化为dmatrix

            # 预测
            y_score_curr_day = bst.predict(X_curr_day) # predict输出的就是概率
            y_pred_curr_day = np.int64(y_score_curr_day>0.50) # 概率>0.5的标签为1


            # 保存结果到csv文件
            result_curr_day = pd.DataFrame(y_curr_day.index)
            result_curr_day['date_pred'] = np.nan
            result_curr_day['return_true'] = np.nan
            result_curr_day['return_pred_bin'] = y_pred_curr_day  # 预测y标签
            result_curr_day['y_score'] = y_score_curr_day  # y score
            result_curr_day = result_curr_day.sort_values(by='y_score', ascending=False)


            store_path = para.path_results + model_name + "\\" + str(n_days_in_test) + ".csv"
            result_curr_day.to_csv(store_path, sep=',', header=True, index=False)

            # 计算accuracy，roc
            accuracy_curr_day =  metrics.accuracy_score(y_curr_day, y_pred_curr_day)
            accuracy_all_tests.append(accuracy_curr_day)
            roc_curr_day = metrics.roc_auc_score(y_curr_day, y_score_curr_day)
            roc_all_tests.append(roc_curr_day)
            print("day #%d, accuracy = %6f, roc = %6f" %(n_days_in_test,accuracy_curr_day, roc_curr_day))
    print("average accuracy on all test days = %6f" % np.mean(accuracy_all_tests))
    print("average roc on all test days = %6f" % np.mean(roc_all_tests))

    return n_days_in_test


if __name__ == '__main__':

    # 加载训练数据
    X_in_sample, y_in_sample = load_sample_data.load_class()
    X_train, X_cv, y_train, y_cv, *args = load_sample_data.preprocess(X_in_sample, y_in_sample)
    print("X_train shape, y_train shape:", X_train.shape, y_train.shape)
    print("X_cv shape, y_cv shape:", X_cv.shape, y_cv.shape)
    # 转换为DMatrix格式
    dtrain = xgb.DMatrix(data=X_train, label=y_train)
    dcv = xgb.DMatrix(data=X_cv, label=y_cv)

    # 设置参数
    param_grid = {
        'max_depth' : 2,
        'eta' :  3e-1,
        'silent' : 1,
        'eval_metric' : 'auc',
        'nthread' : 3,
    }
    # 设置需要评估的数据集
    evallist = [(dtrain, 'train'), (dcv, 'cv')]

    # 训练模型
    num_round = 10
    bst = xgb.train(param_grid, dtrain, num_round, evallist)

    # 存储模型
    # 需要在存储路径上提前创建文件夹和.model文件
    if os.path.exists(para.path_results + "xgboost") == False:
        os.mkdir(para.path_results + "xgboost")
    store_path = para.path_results + "xgboost/xgboost_model.model"
    bst.save_model(store_path)
    # bst.load_model(store_path) # 加载模型

    # 模型预测,保存预测结果
    n_days_in_test = predict_xgboost(bst, "xgboost")

    # 策略构建
    build_strategy.add_next_day_return("xgboost")
    strategy = build_strategy.build(n_days_in_test, "xgboost")

    # 策略评价
    evaluate_strategy.evaluate(strategy, n_days_in_test)
