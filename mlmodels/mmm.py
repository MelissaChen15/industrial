# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/13 8:44

import numpy as np
import pandas as pd
import h5py
from sklearn.model_selection import train_test_split
from sklearn import decomposition, preprocessing, metrics

# SVM分类问题，收益率前30%的标记为1， 后30%标记为0

# 将参数单独的写在一个类里面
class Para:
    method = 'SVM'
    # 这样取值对级值过分重视？？？
    percent_select = [0.3,0.3] # 30% positive samples amd 30% negative samples
    percent_cv = 0.1 # 10% cross validation samples
    path_data = "D:\Meiying\data\dataset_part5.h5"
    path_results = "path to store results"
    seed = 42 # random seed
    # --- SVM  Parameters ---
    svm_kernel = "linear"
    scm_c = 0.01 # 线性支持向量机的惩罚系数
para = Para()

def load_data(end,start = "000001.SZ"):
    f = h5py.File(para.path_data, 'r')  # 打开h5文件
    data = pd.DataFrame()
    for k in f.keys():
        if k < start: continue
        h5 = pd.read_hdf(para.path_data, key=str(k))
        df = pd.DataFrame(h5)
        data = pd.concat([data,df],axis=0,ignore_index=True) # 把各个月份拼接起来
        if k >= end: break # 选定train和vc集的范围
    # print(data)
    data = data.dropna(axis = 0)# remove nan
    return data

def label_data(data):
    """
    label data, 30% positive samples as 1 amd 30% negative samples as 0
    :param data: DataFrame format
    :return: labeled data set, DataFrame format
    """
    data['y'] = np.nan # 新加标签列，初始化为nan
    data = data.sort_values(by='pct_chg', ascending=False) # 对日收益率行进行排序
    n_stock_select = np.multiply(para.percent_select, data.shape[0]) # decide how many stocks is selected
    n_stock_select = np.round(n_stock_select).astype(int)
    data.iloc[0:n_stock_select[0],-1] = 1
    data.iloc[-n_stock_select[0]:,-1] = 0
    data = data.dropna(axis = 0)
    return data

def preprocess(data_labeled):
    X_in_samples = data_labeled.iloc[:,3:-1]# 去除股票代码和交易时间两列
    y_in_samples = data_labeled.iloc[:,-1] # 如果是分类模型
    # y_in_samples = data_labeled['pct_chg'] # 如果是回归模型
    # 生成train和cv集
    X_train, X_cv, y_train,y_cv = train_test_split(X_in_samples, y_in_samples, test_size=para.percent_cv,random_state=para.seed)

    # 数据标准化
    scaler = preprocessing.StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_cv = scaler.transform(X_cv)
    # print(X_train.shape)

    # 主成分分析 PCA, 设定n_components = 0.95
    # pca = decomposition.PCA(n_components = 0.95)
    # pca.fit(X_train)
    # X_train = pca.transform(X_train)
    # X_cv = pca.transform(X_cv)
    # # print(X_train.shape)

    return X_train,X_cv, np.array(y_train),np.array(y_cv)




if __name__ == "__main__":
    # TODO:  parameter grid search / pipline /  performance tests
    # TODO: 啊，试一试用其他的数据集

    # 训练数据加载，label及预处理
    data_orig = load_data(end = "000080.SZ")
    data_labeled  = label_data(data_orig)
    # print(data_labeled)
    X_train, X_cv, y_train, y_cv = preprocess(data_labeled)
    # print(X_train.shape)
    # print(X_cv.shape)
    # print(y_train)
    # print(y_cv.shape)

    # 模型设置
    # SVM
    if para.method == 'SVM':
        from sklearn import svm
        model = svm.SVC(kernel=para.svm_kernel, C = para.scm_c)
    # 线性回归
    if para.method == "LR":
        from sklearn import linear_model
        model = linear_model.LinearRegression(fit_intercept=True)

    # 模型训练
    if para.method == "SVM":
        model.fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_score_train = model.decision_function(X_train)
        y_pred_cv = model.predict(X_cv)
        y_score_cv = model.decision_function(X_cv)
    if para.method == "LR":
        model.fit(X_train, y_train)
        y_score_train = model.predict(X_train)
        y_score_cv = model.predict(X_cv)

    # # 模型预测
    # # 加载及预处理测试数据
    # data_test_orig = load_data(start="000100.SZ", end = "000200.SZ")
    # data_test_labeled  = label_data(data_test_orig)
    # X_in_tests = data_test_labeled.iloc[:,3:-1]  # 去除股票代码和交易时间两列
    # y_in_tests = data_test_labeled.iloc[:, -1]  # 如果是分类模型
    # # # y_in_tests = data_labeled['pct_chg'] # 如果是回归模型
    # X_test, X_none, y_test,y_none = train_test_split(X_in_tests, y_in_tests, test_size=0)
    # scaler = preprocessing.StandardScaler().fit(X_test)
    # X_test = scaler.transform(X_test)
    # # PCA?
    # # pca = decomposition.PCA(n_components = 0.95)
    # # pca.fit(X_test)
    # # X_test = pca.transform(X_test)
    # # print(X_train.shape, X_test.shape)
    # # 综上，测试集为 x_test, y_test
    # # 利用刚刚训练好的模型，在test集上预测
    # if para.method == "SVM":
    #     y_pred_test = model.predict(X_test)
    #     y_score_test = model.decision_function(X_test)
    # if para.method == "LR":
    #     y_score_test = model.predict(X_test)

    # 模型评价: 正确率和AUC
    # print("train accurancy = %.4f"%metrics.accuracy_score(y_train, y_pred_train))
    print("train AUC = %.4f"%metrics.roc_auc_score(y_train, y_score_train))
    # print("cv accurancy = %.4f"%metrics.accuracy_score(y_cv, y_pred_cv))
    print("cv AUC = %.4f"%metrics.roc_auc_score(y_cv, y_score_cv))
    # print("test  accurancy = %.4f" % metrics.accuracy_score(y_test, y_pred_test))
    # print("test AUC = %.4f" % metrics.roc_auc_score(y_test, y_score_test))
























# ------------------------------ h5操作 --------------------------
    # f = h5py.File('D:\Meiying\data\part1_modified.h5', 'r')  # 打开h5文件
    # h5 = pd.HDFStore('temp.h5', 'w', complevel=4, complib='blosc')
    # dataset=dict()
    # for k in f.keys():
    #     data = pd.read_hdf("D:\Meiying\data\part1_modified.h5", key=str(k))
    #     df = pd.DataFrame(data)
    #     print(df)
    #     h5[df['trade_date'][0]] = df.iloc[:, :"trade_date"]
        # h5.close()

    # h5 = pd.HDFStore('temp.h5', 'w', complevel=4, complib='blosc')
    # for j in dataset.keys():
    #     h5[j] = dataset[j]
    # h5.close()
    # f = h5py.File('D:\Meiying\data\dataset_part5', 'r')  # 打开h5文件


    # keys = f.keys() # 每一个key是一个str
    # for k in keys:
    #     print(k)
    #     data = pd.read_hdf("D:\Meiying\data\part1_modified.h5", key=str(k))
    #     print(data)

    # a = np.random.standard_normal((900, 4))
    # b = pd.DataFrame(a)
    # h5 = pd.HDFStore("D:\Meiying\data\ test.h5", 'w', complevel=4, complib='blosc')
    # h5['data'] = b
    # h5.close()

    # store = pd.HDFStore('D:\Meiying\data\ test.h5')
    # b = np.ones((900, 1))
    # df = pd.DataFrame(b)
    # #
    # data = pd.read_hdf("D:\Meiying\data\ test.h5", key='data')
    # print(data)
