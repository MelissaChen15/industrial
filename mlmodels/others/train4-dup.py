import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from sklearn import preprocessing, metrics, svm
from mlmodels.others import PCA_algorithm
from sklearn.model_selection import ShuffleSplit,GridSearchCV,train_test_split


# 参数类
class Para:
    method = 'SVM' # LinearR\RidgeR\LassoR\SVR\DT\SVC\LogisticR\RFC
    method_type = 'c' # classification or regression
    percent_select = [0.3,0.3] # 30% positive samples amd 30% negative samples
    percent_cv = 0.1 # 10% cross validation samples
    path_data = r"D:\Meiying\data\cleaned\\"
    path_results = r"D:\Meiying\data\result\\"
    seed = 42 # random seed
    month_in_sample = range(10, 11+1)
    month_test = range(12, 12+1)
    n_stock_select = 100 # 选择的股票数量
    svm_kernel = 'linear'
    svm_c = 0.01
para = Para()

# 分类模型，标记数据
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

# 加载原始数据
data_in_sample = pd.DataFrame()
n_days_in_sample = 0
for i_month in para.month_in_sample:  # 按月加载
    data_curr_month = pd.DataFrame()
    file_name = para.path_data + str(i_month) + ".h5"
    f = h5py.File(file_name, 'r')  # 打开h5文件
    # print(file_name)
    for key in f.keys():  # 按天加载
        n_days_in_sample += 1
        h5 = pd.read_hdf(file_name, key=str(key))
        data_curr_day = pd.DataFrame(h5)
        data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'].abs() >= 10.1)  # 去掉收益率绝对值大于10.1的数据点
        data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'] == 0.0)  # 去掉收益率为0的数据点
        data_curr_day = data_curr_day.dropna(axis=0)  # remove nan
        if (para.method_type == 'c'): data_curr_day = label_data(data_curr_day)  # 标记数据
        data_curr_month = pd.concat([data_curr_month, data_curr_day], axis=0, ignore_index=False)  # 把一个月内每天的数据拼接起来
    data_in_sample = pd.concat([data_in_sample, data_curr_month], axis=0, ignore_index=False)  # 把每月的数据拼接起来
# print(n_days_in_sample)
# print(data_in_sample.keys())
# print(data_in_sample.sort_index())

# 数据预处理
X_in_sample = data_in_sample.loc[:,'close':'amount']
y_in_sample = data_in_sample.loc[:,'return_bin']
X_train, X_cv, y_train, y_cv = train_test_split(X_in_sample, y_in_sample, test_size=para.percent_cv, random_state=para.seed)

scalar = preprocessing.StandardScaler().fit(X_train)
X_train = scalar.transform(X_train)
X_cv = scalar.transform(X_cv)
# pca = decomposition.PCA(n_components=0.95)
# pca.fit(X_train)
# X_train = pca.transform(X_train)
# X_cv = pca.transform(X_cv)
X_train = PCA_algorithm.pca(X_train)
X_cv = PCA_algorithm.pca(X_cv)


print("X_train shape :", X_train.shape)
# 构建模型
cv_split = ShuffleSplit(n_splits=1, train_size=0.9, test_size=0.1)
if para.method == 'SVM':
    model = GridSearchCV(estimator=svm.SVC(), param_grid={'C':[1]}, cv=cv_split, n_jobs=1)  # n_jobs=-1 代表使用全部的cp


#训练模型
# tic = time.time()
if para.method == 'SVM':
    model.fit(X_train, y_train)
    print("best params : ", model.best_params_)
    print("best score : ", model.best_score_)
    # model.fit(X_train, y_train)
    # toc = time.time()
    # print(toc - tic)
    y_pred_train = model.predict(X_train)
    y_score_train = model.decision_function(X_train)
    y_pred_cv = model.predict(X_cv)
    y_score_cv = model.decision_function(X_cv)

# 模型预测
n_days_in_test = 0
accu = []
for i_month in para.month_test:  # 按月加载
    file_name = para.path_data + str(i_month) + ".h5"
    f = h5py.File(file_name, 'r')  # 打开h5文件
    # print(file_name)
    for key in f.keys():  # 按天加载
        n_days_in_test += 1
        # 加载
        h5 = pd.read_hdf(file_name, key=str(key))
        data_curr_day = pd.DataFrame(h5)
        data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'].abs() >= 10.1)  # 去掉收益率绝对值大于10.1的数据点
        data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'] == 0.0)  # 去掉收益率为0的数据点
        data_curr_day = data_curr_day.dropna(axis=0)  # remove nan
        if (para.method_type == 'c'): data_curr_day = label_data(data_curr_day)  # 标记数据
        # 预处理
        X_curr_day = data_curr_day.loc[:,'close':'amount']
        y_curr_day = data_curr_day.loc[:,'return_bin']
        y_true_day = data_curr_day.loc[:,'pct_chg']

        scalar = preprocessing.StandardScaler().fit(X_curr_day)
        X_curr_day = scalar.transform(X_curr_day)

        # pca = decomposition.PCA(n_components=0.95)
        # pca.fit(X_curr_day)
        # X_curr_day = pca.transform(X_curr_day)
        X_curr_day = PCA_algorithm.pca(X_curr_day)

        # 计算
        if para.method == 'SVM':
            y_pred_curr_day = model.predict(X_curr_day)
            y_score_curr_day = model.decision_function(X_curr_day)

        # 打印结果
        result_curr_day = pd.DataFrame(y_true_day).rename(columns={'pct_chg':'return_true'})
        result_curr_day['return_true_bin'] = y_curr_day
        result_curr_day['return_pred_bin'] = y_pred_curr_day
        result_curr_day['y_score'] = y_score_curr_day
        result_curr_day = result_curr_day.sort_values(by='y_score', ascending=False)
        store_path = para.path_results + str(n_days_in_test) + ".csv"
        result_curr_day.to_csv(store_path, sep=',', header=True, index=True)

        accu.append(metrics.accuracy_score(y_curr_day,y_pred_curr_day))
        print("day #%d, accurancy = %6f, roc = %6f" %(n_days_in_test, metrics.accuracy_score(y_curr_day,y_pred_curr_day), metrics.roc_auc_score(y_curr_day, y_score_curr_day)))

# 策略构建
strategy = pd.DataFrame({'return': [0] * n_days_in_test, 'value': [1] * n_days_in_test})
for i_day in range(1,n_days_in_test+1):
    file_name = para.path_results + str(i_day) + ".csv"
    csv = pd.read_csv(file_name)
    result_csv_day = pd.DataFrame(csv)
    select = result_csv_day.iloc[:100,1:2] # return_true列
    strategy.iloc[i_day-1, 0] = float(select.mean())
strategy['value'] = (strategy['return']*0.01 + 1).cumprod()
print(strategy)

plt.plot(range(1,n_days_in_test+1), strategy.loc[range(n_days_in_test),'value'],'r-')
plt.show()