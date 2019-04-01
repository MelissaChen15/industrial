# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/15 17:03

# 数据：训练数据去掉nan、收益率绝对值大于10、收益率为0， 预测数据中将收益率大于10的按10处理

import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from sklearn import preprocessing, metrics, svm, tree,linear_model
from mlmodels.main_etry import PCA_algorithm
from sklearn.model_selection import ShuffleSplit,GridSearchCV,train_test_split
from sklearn import ensemble


# 参数类
class Para:
    method = 'LinearR' # LinearR\RidgeR\LassoR\SVR\DT\SVC\LogisticR\RFC
    method_type = 'r' # classification or regression
    percent_select = [0.3,0.3] # 30% positive samples amd 30% negative samples
    percent_cv = 0.1 # 10% cross validation samples
    path_data = "D:\Meiying\data\cleaned\\"
    path_results = "path to store results"
    seed = 42 # random seed
    # month_in_sample = range(1, 120+1) # 训练: 200401-201312 120个月 [2042256 rows x 14 columns]
    # month_in_test = range(121,180+1) # 测试：201401-201812 60个月 [1781298 rows x 14 columns]
    month_in_sample = range(1, 12+1)
    month_in_test = range(13, 15+1)
    n_stock_select = 100 # 选择的股票数量


    # --- SVR  超参 ---
    svr_kernel = 'linear'
    svr_C = 0.01  # C越大，variance越大，bias越小，类似Lasso的α
    svr_epsilon = 0.1  # epsilon是表示多宽的范围内的点不进行惩罚
    svr_grid = {
        'kernel' : ['linear', 'rbf'],
        'C' : [1e-3, 1e-2, 1e-1, 0.3, 1, 3, 5, 10],
        'epsilon' : [1e-4, 3e-4, 1e-3, 3e-3, 0.01, 0.03, 0.1, 0.3, 1, 5, 10]
    }
    # --- DT 超参 ---
    dt_criterion = 'gini'  # gini or entropy
    # --- SVC  超参 ---
    svc_kernel = "linear"
    svc_C = 0.01
    svc_gamma = "auto"  # gamma值越小，分类界面越连续；gamma值越大，分类界面越“散”，分类效果越好，但有可能会过拟合
    # --- Ridge Regression 超参 ---
    rr_alpha = 500.0
    rr_alphas = {
        "alpha" : [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    }
    # --- Lasso Regression 超参 ---
    lr_alpha = 0.01
    lr_alphas = {
        "alpha": [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    }
    # --- Lasso Regression 超参 ---
    logr_C = 1e5
    logr_grid = {
        "C": [0.01]
    }
    # --- Random Forest Classifier超参 ---
    rfc_grid = {
        "n_estimators": [10], # 树的个数，越高模型越稳定，运行越慢
        "min_samples_leaf" : [5] # 叶子节点上应有的最少样例数，越小越可能受noise data的影响
    }

para = Para()

# 加载原始数据
def load_data(datarange):
    data = pd.DataFrame()
    for i_month in datarange:# 按月加载
        data_curr_month = pd.DataFrame()
        file_name  = para.path_data +str(i_month)+".h5"
        f = h5py.File(file_name, 'r')  # 打开h5文件
        # print(file_name)
        for key in f.keys(): #按天加载
            h5 = pd.read_hdf(file_name, key=str(key))
            df = pd.DataFrame(h5)
            data_curr_month = pd.concat([data_curr_month,df],axis=0,ignore_index=False) # 把一个月内每天的数据拼接起来
        data_curr_month = data_curr_month.mask(data_curr_month['pct_chg'].abs() >= 10.0)# 去掉收益率绝对值大于10的数据点
        data_curr_month = data_curr_month.mask(data_curr_month['pct_chg'] == 0.0) # 去掉收益率为0的数据点
        data_curr_month = data_curr_month.dropna(axis = 0)# remove nan
        if(para.method_type == 'c'): data_curr_month = label_data(data_curr_month) # 标记数据
        data = pd.concat([data, data_curr_month], axis=0, ignore_index=False)  # 把每月的数据拼接起来
    return data


# 分类模型，标记数据
def label_data(data):
    data['y'] = np.nan # 新加标签列，初始化为nan
    data = data.sort_values(by='pct_chg', ascending=False) # 对日收益率行进行排序
    # print(data)
    n_stock_select = np.multiply(para.percent_select, data.shape[0]) # decide how many stocks is selected
    n_stock_select = np.round(n_stock_select).astype(int)
    data.iloc[0:n_stock_select[0],-1] = 1
    data.iloc[-n_stock_select[0]:,-1] = 0
    data = data.dropna(axis = 0) # 去除异常值
    return data


# 数据预处理: 标准化，pca
def preprocess(data_labeled):
    # 切分数据
    X_in_samples = pd.DataFrame()
    y_in_samples = pd.DataFrame()
    # 如果是分类模型
    if para.method_type == 'c':
        X_in_samples = data_labeled.iloc[:,1:-1].drop(columns = 'pct_chg', inplace=False)# 去除交易时间、收益率列
        y_in_samples = data_labeled.iloc[:,-1] # y为0,1标签
    # 如果是回归模型
    if para.method_type == 'r':
        y_in_samples = data_labeled['pct_chg'] # y为收益率
        X_in_samples = data_labeled.iloc[:,1:-1] #去除交易时间、收益率列
    # print(X_in_samples.shape,y_in_samples.shape)
    # print(X_in_samples, y_in_samples)
    # 数据标准化
    scaler = preprocessing.StandardScaler().fit(X_in_samples)
    X = scaler.transform(X_in_samples)
    # print(X_train.shape)

    # PCA
    X = PCA_algorithm.pca(X)
    # print(X_train.shape)

    # 统一格式
    X = pd.DataFrame(X_in_samples)
    y = pd.DataFrame(y_in_samples)
    # print(X.shape,y.shape)
    return X, y

# 训练模型
def classifier_train_with_grid_search(X, y, model, param_grid):
    cv_split = ShuffleSplit(n_splits=5, train_size=0.9, test_size=0.1)
    grid = GridSearchCV(estimator = model, param_grid = param_grid, cv=cv_split, n_jobs=1) # n_jobs=-1 代表使用全部的cpu
    grid.fit(X, y)
    print("best params : ",grid.best_params_)
    print("best score : ", grid.best_score_)
    return grid

# Linear Regression
def LinearR(X, y):
    model = linear_model.LinearRegression(fit_intercept=True)
    model.fit(X, y)
    y_train_pred = model.predict(X)
    print("LinearR")
    print("train set MSE = %6f" % metrics.mean_squared_error(y, y_train_pred))
    return model

# Ridge Regression
def RidgeR(X, y):
    print("RidgeR")
    model  = linear_model.Ridge(fit_intercept=True)
    model = classifier_train_with_grid_search(X, y, model, para.rr_alphas)
    y_train_pred = model.predict(X)
    print("train/cv set MSE = %6f" % metrics.mean_squared_error(y, y_train_pred))

    # model = linear_model.RidgeCV(fit_intercept=True, alphas=[500,0.03,0.01],scoring= "neg_mean_squared_error")#cv自动交叉验证, Leave-One-Out cross-validation
    # print("best alpha = %f" % model.alpha_)

    # model  = linear_model.Ridge(fit_intercept=True, alpha= para.rr_alpha)
    # model.fit(X, y)
    # y_train_pred = model.predict(X)
    # print("RidgeR")
    # print("train set MSE = %6f" % metrics.mean_squared_error(y, y_train_pred))

    return model

# Lasso Regression
def LassoR(X, y):
    print("LassoR")
    model = linear_model.Lasso(fit_intercept=True)
    model = classifier_train_with_grid_search(X, y, model, para.rr_alphas)
    y_train_pred = model.predict(X)
    print("train/cv set MSE = %6f" % metrics.mean_squared_error(y, y_train_pred))

    # model = linear_model.LassoCV(fit_intercept=True)
    # print("best alpha = %f" % model.alpha_)

    # model = linear_model.Lasso(fit_intercept=True, alpha=para.lr_alpha)
    # model.fit(X, y)
    # y_train_pred = model.predict(X)
    # print("LassoR")
    # print("train set MSE = %6f" % metrics.mean_squared_error(y, y_train_pred))

    return model

# SVM Regression
def SVR(X,y):
    # 用grid research
    # print("SVR")
    # model = svm.SVR()
    # classifier_train_with_grid_search(X, y, model, para.svr_grid)

    # 不用grid research
    model = svm.SVR(C=para.svr_C, kernel=para.svr_kernel, epsilon=para.svr_epsilon)
    X_train, X_cv, y_train,y_cv = train_test_split(X, y, test_size=para.percent_cv,random_state=para.seed)
    model.fit(X_train,y_train)
    y_train_pred = model.predict(X_train)
    y_cv_pred = model.predict(X_cv)
    print("SVR")
    print("train set MSE = %6d" % metrics.mean_squared_error(y_train, y_train_pred))
    print("cv set MSE = %6d" % metrics.mean_squared_error(y_cv, y_cv_pred))
    return model

# Decision Tree
def DT(X, y):
    model = tree.DecisionTreeClassifier(para.dt_criterion)
    model.fit(X, y)
    y_train_pred = model.predict(X)
    print("DT")
    print("train set accurancy = %6f" % metrics.accuracy_score(y, y_train_pred))
    return model

# SVM Classifier
def SVC(X, y):
    # 用grid research
    # print("SVC")
    # model = svm.SVC()
    # classifier_train_with_grid_search(X, y, model, para.svr_grid)

    # 不用grid research
    model = svm.SVC(C=para.svc_C, kernel=para.svc_kernel, gamma=para.svc_gamma)
    X_train, X_cv, y_train, y_cv = train_test_split(X, y, test_size=para.percent_cv, random_state=para.seed)
    model.fit(X_train, y_train)
    y_train_pred = model.predict(X_train)
    y_cv_pred = model.predict(X_cv)
    print("SVC")
    y_train_pred = model.predict(X_train)
    print("train set accurancy = %6f" % metrics.accuracy_score(y_train, y_train_pred))
    print("cv set accurancy = %6f" % metrics.accuracy_score(y_cv, y_cv_pred))
    return model

# Logistic Regression
def LogisticR(X, y):
    print("LogisticR")
    model = linear_model.LogisticRegression()
    model = classifier_train_with_grid_search(X, y, model, para.logr_grid)
    y_train_pred = model.predict(X)
    print("train/cv set accurancy = %6f" % metrics.accuracy_score(y, y_train_pred))

    return model

# Random Forest Classifier
def RFC(X, y):
    print("Random Forest Classifier")
    model = ensemble.RandomForestClassifier()
    model = classifier_train_with_grid_search(X, y, model, para.rfc_grid)
    y_train_pred = model.predict(X)
    print("train/cv set accurancy = %6f" % metrics.accuracy_score(y, y_train_pred))

    return model

# 策略构建
def select(result):
    result = result.mask(result['pred_chg'] > 10.0, 10.0) # 预测收益率大于10 的按10计算
    result = result.sort_values(by='pred_chg', ascending=False) # 按预测的回报率排序
    select = result.iloc[:para.n_stock_select, 1:]
    ave_return = select.mean()
    return float(ave_return),select


if __name__ == "__main__":

    # 加载数据
    data_orig = load_data(para.month_in_sample)
    X, y = preprocess(data_orig)
    print("train data loading done, shape: "+str(X.shape)+str(y.shape))


    # 训练模型
    # print(linear_model.LassoCV().get_params().keys()) # 查看模型需要的参数
    if para.method == 'LinearR': model_trained = LinearR(X, y)
    if para.method == 'SVR': model_trained = SVR(X, y)
    if para.method == 'DT': model_trained = DT(X, y)
    if para.method == 'SVC': model_trained = SVC(X, y)
    if para.method == 'RidgeR': model_trained = RidgeR(X, y)
    if para.method == 'LassoR': model_trained = LassoR(X, y)
    if para.method == 'LogisticR': model_trained = LogisticR(X, y)
    if para.method == 'RFC': model_trained = RFC(X, y)

    # 模型评价
    print("running on test set")
    accurancy = {} # 分类模型评估指标
    MSE = {} # 回归模型评估指标
    n_test = para.month_in_test[-1]-para.month_in_test[0]+1
    strategy = pd.DataFrame({'return': [0]*para.month_in_test[-1],'value': [1]*para.month_in_test[-1]})
    # 按月计算模型在测试集上的表现
    for i_month in para.month_in_test:
        print("month #%d" %i_month)
        data_test_month = load_data(range(i_month,i_month+1)) #加载测试数据
        X_month, y_month = preprocess(data_test_month)
        y_pred_month = model_trained.predict(X_month) #预测
        # y_score_month = model_trained.decision_function(X_month)
        result  = pd.DataFrame(y_month)         # 预测结果存储在result里
        result['pred_chg'] = y_pred_month  # result有pct_chg和pred_chg两列，index为股票代码
        if para.method_type == 'c':
            acc = metrics.accuracy_score(result['pct_chg'],result['pred_chg'])
            accurancy[i_month] = acc
            print("test set accuracy = %6f" % acc)
        if para.method_type == 'r':
            mse = metrics.mean_squared_error(result['pct_chg'],result['pred_chg'])
            MSE[i_month] = mse
            print("test set MSE = %6f" % mse)



        # 策略构建
        ave, *arg = select(result)
        strategy.iloc[i_month-1, 0] = ave
    # print(accurancy, MSE)
    strategy['value'] = (strategy['return']*0.01 + 1).cumprod()
    print(strategy)

    # 策略评价
    #画图
    plt.plot(para.month_in_test, strategy.loc[para.month_in_test,'value'],'r-')
    plt.show()











