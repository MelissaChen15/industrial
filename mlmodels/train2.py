# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/14 15:26

# 添加grid search和pipline， 因为数据格式问题，依然没有办法写回测


import numpy as np
import pandas as pd
import h5py
import sklearn.model_selection as ms
from sklearn import decomposition, preprocessing, metrics
from mlmodels import PCA_algorithm


# method: SVR svr_kernel = "linear" svr_c = 0.01  svr_epsilon = 0.1
# train mean_absolute_error: 0.871772
# cv mean_absolute_error: 0.794398
# test mean_absolute_error: 0.983643
#
# train r2_score: 0.780536
# cv r2_score: 0.823085
# test r2_score: 0.797116

# 数据概况：3576组， 2014/01/01- 2018/12/31; 000001.SZ - 002948.SZ；300001.SZ - 300760.SZ； 600000.SH - 603999.SH(6开头的不连续)

# 参数类
class Para:
    # LR和DT有一些问题
    method = 'SVR' # SVR/SVC/LR/DT
    method_type = 'regression' # classification or regression
    percent_select = [0.3,0.3] # 30% positive samples amd 30% negative samples
    percent_cv = 0.1 # 10% cross validation samples
    path_data = "D:\Meiying\data\dataset_part5.h5"
    path_results = "path to store results"
    seed = 42 # random seed
    trainset = ["000001.SZ", "002949.SZ"]
    testset = ["300001.SZ", "603999.SH"]
    n_stock_select = 100 # 选择的股票数量

    # --- SVR  超参 ---
    svr_kernel = "linear"
    svr_c = 0.01  # C越大，variance越大，bias越小，类似Lasso的α
    svr_epsilon = 0.1 # epsilon是表示多宽的范围内的点不进行惩罚
    svr_c_range = [1e-3, 1e-2, 1e-1, 0.3,1,3, 5, 10]
    svr_epsilon_range = [1e-4,3e-4,1e-3,3e-3,0.01,0.03,0.1,0.3,1,5,10]
    # --- SVC  超参 ---
    svc_kernel = "linear"
    svc_c = 0.01
    svc_gamma = "auto" #gamma值越小，分类界面越连续；gamma值越大，分类界面越“散”，分类效果越好，但有可能会过拟合
    # --- DT 超参 ---
    dt_criterion =  'entropy' # gini or entropy
para = Para()

# 加载原始数据
def load_data(end,start):
    f = h5py.File(para.path_data, 'r')  # 打开h5文件
    data = pd.DataFrame()
    for k in f.keys():
        if k < start: continue
        h5 = pd.read_hdf(para.path_data, key=str(k))
        df = pd.DataFrame(h5)
        data = pd.concat([data,df],axis=0,ignore_index=True) # 把各个月份拼接起来
        if k >= end: break # 选定train和vc集的范围
    data = data.dropna(axis = 0)# remove nan
    return data

# 分类模型标记数据
def label_data(data):
    """
    label data, 30% positive samples as 1 amd 30% negative samples as 0
    :param data: DataFrame format
    :return: labeled data set, DataFrame format
    """
    data['y'] = np.nan # 新加标签列，初始化为nan
    data = data.sort_values(by='pct_chg', ascending=False) # 对日收益率行进行排序
    # print(data.iloc[,:])
    n_stock_select = np.multiply(para.percent_select, data.shape[0]) # decide how many stocks is selected
    n_stock_select = np.round(n_stock_select).astype(int)
    data.iloc[0:n_stock_select[0],-1] = 1
    data.iloc[-n_stock_select[0]:,-1] = 0
    data = data.dropna(axis = 0)
    return data

# 数据预处理：清洗、标准化、pca
def preprocess(data_labeled):
    # 切分数据
    # 如果是分类模型
    if para.method_type == 'classification':
        X_in_samples = data_labeled.iloc[:,3:-1].drop(columns = 'pct_chg', inplace=False)# 去除股票代码和交易时间、收益率和y四列
        y_in_samples = data_labeled.iloc[:,-1]
    # 如果是回归模型
    if para.method_type == 'regression':
        y_in_samples = data_labeled['pct_chg']
        X_in_samples = data_labeled.iloc[:,3:].drop(columns = 'pct_chg', inplace=False)
    # print(X_in_samples.shape, y_in_samples.shape)

    # 数据标准化
    scaler = preprocessing.StandardScaler().fit(X_in_samples)
    X = scaler.transform(X_in_samples)
    # print(X_train.shape)

    # PCA
    X = PCA_algorithm.pca(X)
    # print(X_train.shape)

    # 统一格式
    y = np.array(y_in_samples)
    return X, y

# 构建和训练模型
def train():
    data_orig = load_data(para.trainset[0], para.trainset[1])

    # 如果是分类模型
    if para.method_type == 'classification':
        # 训练数据加载，label及预处理
        data_labeled = label_data(data_orig)
        X, y= preprocess(data_labeled)
        print("train set size :"+ str(X.shape[0]))
        print("feature set size :"+ str(X.shape[1]))
        # 设置多个交叉验证集
        cv_split = ms.ShuffleSplit(n_splits=5, train_size=0.7, test_size=0.25)  # 进行几次交叉验证；训练集占总样本的百分比；测试集占总样本的百分比
        # 模型设置
        # SVC
        if para.method == 'SVC':
            from sklearn import svm
            model = svm.SVC(kernel=para.svc_kernel, C=para.svc_c, gamma=para.svc_gamma)
        # DT
        if para.method == 'DT':
            from sklearn import tree
            model = tree.DecisionTreeClassifier(criterion = para.dt_criterion)
        # 模型训练
        model.fit(X, y)
        score_ndarray = ms.cross_val_score(model, X, y, cv=cv_split)
        # 模型预测
        # 加载及预处理测试数据
        data_test_orig = load_data(para.testset[0], para.testset[1])
        data_test_labeled = label_data(data_test_orig)
        y_in_tests = data_test_labeled.iloc[:,-1]
        X_in_tests = data_test_labeled.iloc[:, 3:-1].drop(columns='pct_chg', inplace=False)
        X_test, X_none, y_test, y_none = ms.train_test_split(X_in_tests, y_in_tests, test_size=0)
        scaler = preprocessing.StandardScaler().fit(X_test)
        X_test = scaler.transform(X_test)
        # 利用刚刚训练好的模型，在test集上预测
        y_pred_test = model.predict(X_test)
        print("test set size :"+ str(X_test.shape[0]))
        # 模型评价: metrics.roc_auc_score, metrics.accuracy_score
        # print('coefficients:%s, intercept %s' % (model.coef_, model.intercept_))
        print("method: " + str(para.method))
        print("cv score = %.6f" % score_ndarray.mean())
        print("test score = %.6f" % metrics.roc_auc_score(y_test, y_pred_test))

    #----------------------------------------------------------
    # # 如果是回归模型
    if para.method_type == 'regression':
        # 训练数据加载及预处理
        X, y= preprocess(data_orig)

        # 模型设置
        # SVR
        if para.method == "SVR":
            from sklearn import svm
            model = svm.SVR(kernel=para.svr_kernel, C=para.svr_c, epsilon=para.svr_epsilon)
        # 线性回归
        if para.method == "LR":
            from sklearn import linear_model
            model = linear_model.LinearRegression(fit_intercept=True)
        # 设置多个交叉验证集
        cv_split = ms.ShuffleSplit(n_splits=5, train_size=0.7, test_size=0.25)
        # 模型训练
        model.fit(X, y)
        score_ndarray = ms.cross_val_score(model, X, y, cv=cv_split)
        # 模型预测
        # 加载及预处理测试数据
        data_test_orig = load_data(para.testset[0], para.testset[1])
        y_in_tests = data_test_orig['pct_chg']
        X_in_tests = data_test_orig.iloc[:, 3:].drop(columns='pct_chg', inplace=False)
        X_test, X_none, y_test, y_none = ms.train_test_split(X_in_tests, y_in_tests, test_size=0)
        scaler = preprocessing.StandardScaler().fit(X_test)
        X_test = scaler.transform(X_test)
        # 利用刚刚训练好的模型，在test集上预测
        y_pred_test = model.predict(X_test)
        # 模型评价: metrics.mean_absolute_error
        # print('coefficients:%s, intercept %s' % (model.coef_, model.intercept_))
        print("method: " + str(para.method))
        print('cv score: %.6f' % score_ndarray.mean())
        print('test score: %.6f' % metrics.r2_score(y_test, y_pred_test))
        # ----------------------------------------------------------
        # 策略构建
        # strategy = pd.DataFrame({'return':[0]*X_test.shape[0],'value':[1]*X_test.shape[0]})
        returns_pred = pd.DataFrame(y_pred_test).sort_values(by=0, ascending=False)  # 对日收益率行进行排序
        strategy = returns_pred.iloc[:para.n_stock_select,:]
        # strategy.mean()
        import matplotlib.pyplot as plt
        # plt


# 优化模型
def grid_search_and_pipline():
    from sklearn.svm import SVC
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import ShuffleSplit
    from sklearn.model_selection import GridSearchCV
    from sklearn.tree import DecisionTreeClassifier

    data_orig = load_data(para.trainset[0], para.trainset[1])
    # 如果是分类模型
    if para.method_type == 'classification':
        # 训练数据加载，label及预处理
        data_labeled = label_data(data_orig)
        X, y= preprocess(data_labeled)

    pipe_steps = [
        ('svc', SVC())
    ]
    pipeline = Pipeline(pipe_steps)
    cv_split = ShuffleSplit(n_splits=5, train_size=0.7, test_size=0.25)
    param_grid = {
        'svc__cache_size': [100, 200, 400],
        'svc__C': [1, 10, 100],
        'svc__kernel': ['rbf', 'linear'],
        'svc__degree': [1, 2, 3, 4],
    }
    grid = GridSearchCV(pipeline, param_grid, cv=cv_split)
    grid.fit(X, y)
    print(grid.best_params_)
    print(grid.best_score_)
    from sklearn.metrics import classification_report
    predict_y = grid.predict(X)
    print(classification_report(y, predict_y))


if __name__ == "__main__":
    # TODO:  随机 train_test split/ 考虑手续费
    # TODO:  测试每一种方法
    # train()
    # grid_search_and_pipline()

# 测试：数据按时序排列
    f = h5py.File(para.path_data, 'r')  # 打开h5文件
    data = pd.DataFrame()
    count = 0
    for k in f.keys():
        count += 1
        print(count)
        h5 = pd.read_hdf(para.path_data, key=str(k))
        df = pd.DataFrame(h5)
        data = pd.concat([data, df], axis=0, ignore_index=True)  # 把各个月份拼接起来
    data = data.dropna(axis=0)  # remove nan
    print(data)


    # # 测试： iris 数据集
    # from sklearn import datasets
    # iris = datasets.load_iris()
    # # 将数据集拆分为训练集和测试集
    # X_train, X_cv, y_train, y_cv = train_test_split(
    #     iris.data, iris.target, test_size=0.10, random_state=0)
    # if para.method == "LR":
    #     from sklearn import linear_model
    #     model = linear_model.LinearRegression(fit_intercept=True)
    # model.fit(X_train, y_train)
    # y_pred_train = model.predict(X_train)
    # y_pred_cv = model.predict(X_cv)
    # print('Coefficients:%s, intercept %s' % (model.coef_, model.intercept_))
    # print("train accuracy_score = %.6f" % metrics.accuracy_score(y_train, y_pred_train))
    # print("test accuracy_score = %.6f" % metrics.accuracy_score(y_cv, y_pred_cv))


