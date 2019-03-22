# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 13:10

import numpy as np
import pandas as pd
import h5py
from sklearn import preprocessing, metrics, svm
from mlmodels.utities import PCA_algorithm
from mlmodels.classifiers import load_sample_data
from mlmodels.classifiers.Para import Para
para = Para()

def predict(model, model_name):
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
            y_true_day = data_curr_day.loc[:, 'pct_chg'] # y的实际值

            scalar = preprocessing.StandardScaler().fit(X_curr_day) # 标准化
            X_curr_day = scalar.transform(X_curr_day)

            X_curr_day = PCA_algorithm.pca(X_curr_day) # pca

            # 预测
            y_pred_curr_day = model.predict(X_curr_day)

            # 保存结果到csv文件
            result_curr_day = pd.DataFrame(y_true_day).rename(columns={'pct_chg': 'return_true'})
            result_curr_day['return_true_bin'] = y_curr_day # 真实y标签
            result_curr_day['return_pred_bin'] = y_pred_curr_day # 预测y标签
            try: # 如果是有decision function的模型，以y_score排序存入csv
                y_score_curr_day = model.decision_function(X_curr_day)
                result_curr_day['y_score'] = y_score_curr_day # y score
                result_curr_day = result_curr_day.sort_values(by='y_score', ascending=False)
            except:# 如果是有decision function的模型
                result_curr_day = result_curr_day.sort_values(by='return_pred_bin', ascending=False)
            store_path = para.path_results + model_name+ "\\"+str(n_days_in_test) + ".csv"
            result_curr_day.to_csv(store_path, sep=',', header=True, index=True)

            # 计算accuracy，roc
            accuracy_curr_day =  metrics.accuracy_score(y_curr_day, y_pred_curr_day)
            accuracy_all_tests.append(accuracy_curr_day)
            try:
                roc_curr_day = metrics.roc_auc_score(y_curr_day, y_score_curr_day)
                roc_all_tests.append(roc_curr_day)
                print("day #%d, accuracy = %6f, roc = %6f" %(n_days_in_test,accuracy_curr_day, roc_curr_day))
            except:
                print("day #%d, accuracy = %6f" % (n_days_in_test, accuracy_curr_day))
    print("average accuracy on all test days = %6f" % np.mean(accuracy_all_tests))
    print("average roc on all test days = %6f (nan, if no decision function)" % np.mean(roc_all_tests))

    return n_days_in_test

if __name__ == '__main__':
    from sklearn.externals import joblib
    model = joblib.load(para.path_results  + "RFC/RFC_model.m") # 模型加载
    predict(model, "RFC")
