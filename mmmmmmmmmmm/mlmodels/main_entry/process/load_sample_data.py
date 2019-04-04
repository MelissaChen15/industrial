# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 10:46

import pandas as pd
import h5py
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from main_entry.process import Para
from utilities import PCA_algorithm

para = Para.Para()

# 回归模型：从分月存储的文件中加载数据
def load_regress():
    # 加载原始数据
    data_in_sample = pd.DataFrame() # x和y未分开的数据
    n_days_in_sample = 0 # 计数train set有多少天
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
    return X_in_sample, y_in_sample*0.01

# 回归模型：从处理之后拼接好的数据中加载
def load2_regress():
    file_name = para.path_data + "sample_unlabeled.h5"
    x = pd.read_hdf(file_name, key=str("X_in_sample"))
    X_in_sample = pd.DataFrame(x)
    y = pd.read_hdf(file_name, key=str("y_in_sample"))
    y_in_sample = pd.DataFrame(y)
    return X_in_sample, y_in_sample*0.01

# 分类模型：标记数据
def label_data(data):
    data['return_bin'] = np.nan # 新加标签列，初始化为nan
    data = data.sort_values(by='pct_chg', ascending=False) # 对日收益率行进行排序
    # print(data)
    n_stock_select = np.multiply(para.percent_select, data.shape[0]) # decide how many stocks is selected
    n_stock_select = np.around(n_stock_select).astype(int)
    data.iloc[0:n_stock_select[0],-1] = 1
    data.iloc[-n_stock_select[0]:,-1] = 0
    data = data.dropna(axis = 0)
    return data

# 分类模型：从分月存储的文件中加载原始数据
def load_class():
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
            data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'].abs() >= 10.2)  # 去掉收益率绝对值大于10.2的数据点
            data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'] == 0.0)  # 去掉收益率为0的数据点
            data_curr_day = data_curr_day.dropna(axis=0)  # remove nan
            data_curr_day = label_data(data_curr_day)  # 标记数据
            data_curr_month = pd.concat([data_curr_month, data_curr_day], axis=0, ignore_index=False)  # 把一个月内每天的数据拼接起来
        data_in_sample = pd.concat([data_in_sample, data_curr_month], axis=0, ignore_index=False)  # 把每月的数据拼接起来
    X_in_sample = data_in_sample.loc[:, 'close':'amount'] # 取需要放入模型中的feature
    y_in_sample = data_in_sample.loc[:, 'return_bin']
    return X_in_sample, y_in_sample

# 分类模型：从处理之后拼接好的数据中加载
def load2_class():
    file_name = para.path_data + "sample_labeled.h5"
    x = pd.read_hdf(file_name, key=str("X_in_sample"))
    X_in_sample = pd.DataFrame(x)
    y = pd.read_hdf(file_name, key=str("y_in_sample"))
    y_in_sample = pd.DataFrame(y)
    return X_in_sample, y_in_sample

# 预处理
def preprocess(X_in_sample, y_in_sample):
    # 划分train和cv集，参数见para类
    X_train, X_cv, y_train, y_cv = train_test_split(X_in_sample, y_in_sample, test_size=para.percent_cv,
                                                    random_state=para.seed)
    # 标准化
    scalar = preprocessing.StandardScaler().fit(X_train)
    X_train = scalar.transform(X_train)
    X_cv = scalar.transform(X_cv)

    X_train = PCA_algorithm.pca(X_train)
    X_cv = PCA_algorithm.pca(X_cv)

    # 将y转化为1d array适应模型
    return X_train, X_cv, y_train.values.ravel(),  y_cv.values.ravel()


if __name__ == '__main__':
    # import pandas as pd
    #
    # store_path = r"D:\Meiying\data\cleaned\sample_unlabeled.h5"
    # store = pd.HDFStore(store_path, 'w', complevel=4, complib='blosc')
    # X_in_sample, y_in_sample, *args = load()
    # store["X_in_sample"] = X_in_sample
    # store["y_in_sample"] = y_in_sample
    # store.close()
    pass