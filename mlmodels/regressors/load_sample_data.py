# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 10:46

import pandas as pd
import numpy as np
import h5py
from sklearn import preprocessing
from mlmodels.utities import PCA_algorithm
from sklearn.model_selection import train_test_split
from mlmodels.regressors.Para import Para
para = Para()

# 从分月存储的文件中加载原始数据
def load():
    # 加载原始数据
    data_in_sample = pd.DataFrame()
    n_days_in_sample = 0
    for i_month in para.month_in_sample:  # 按月加载
        data_curr_month = pd.DataFrame()
        file_name = para.path_data + str(i_month) + ".h5"
        f = h5py.File(file_name, 'r')  # 打开h5文件
        # print(file_name)
        for key in f.keys():  # 按天加载,以天为单位处理数据
            n_days_in_sample += 1
            h5 = pd.read_hdf(file_name, key=str(key))
            data_curr_day = pd.DataFrame(h5)
            data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'].abs() >= 10.1)  # 去掉收益率绝对值大于10.1的数据点
            data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'] == 0.0)  # 去掉收益率为0的数据点
            data_curr_day = data_curr_day.dropna(axis=0)  # remove nan
            data_curr_month = pd.concat([data_curr_month, data_curr_day], axis=0, ignore_index=False)  # 把一个月内每天的数据拼接起来
        data_in_sample = pd.concat([data_in_sample, data_curr_month], axis=0, ignore_index=False)  # 把每月的数据拼接起来
    X_in_sample = data_in_sample.loc[:, 'close':'amount'] # 取需要放入模型中的feature
    y_in_sample = data_in_sample.loc[:, 'pct_chg']
    return X_in_sample, y_in_sample, n_days_in_sample


# 从整理好的数据中加载
def load2():
    file_name = para.path_data + "sample_unlabeled.h5"
    x = pd.read_hdf(file_name, key=str("X_in_sample"))
    X_in_sample = pd.DataFrame(x)
    y = pd.read_hdf(file_name, key=str("y_in_sample"))
    y_in_sample = pd.DataFrame(y)
    return X_in_sample, y_in_sample

# 预处理
def preprocess(X_in_sample, y_in_sample):
    X_train, X_cv, y_train, y_cv = train_test_split(X_in_sample, y_in_sample, test_size=para.percent_cv,
                                                    random_state=para.seed)
    # 标准化
    scalar = preprocessing.StandardScaler().fit(X_train)
    X_train = scalar.transform(X_train)
    X_cv = scalar.transform(X_cv)

    X_train = PCA_algorithm.pca(X_train)
    X_cv = PCA_algorithm.pca(X_cv)

    return X_train, X_cv, y_train.values.ravel(),  y_cv.values.ravel()


if __name__ == '__main__':
    import pandas as pd

    store_path = r"D:\Meiying\data\cleaned\sample_unlabeled.h5"
    store = pd.HDFStore(store_path, 'w', complevel=4, complib='blosc')
    X_in_sample, y_in_sample, *args = load()
    store["X_in_sample"] = X_in_sample
    store["y_in_sample"] = y_in_sample
    store.close()