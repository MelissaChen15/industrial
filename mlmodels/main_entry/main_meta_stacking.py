# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/4 8:34

# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/1 13:36
import numpy as np
import os
import pandas as pd
from sklearn import metrics,preprocessing,clone
from sklearn.model_selection import train_test_split,KFold
import h5py
from main_entry.process import train, load_sample_data, evaluate_strategy, build_strategy
from utilities import PCA_algorithm
from main_entry.Para import Para
para = Para()
from regressors import Ridge_init, RFR_init, SVR_init


def meta_stack_predict(models_1st_layer, meta_model): # 写成这样子是因为数据的格式
    # 模型预测
    n_days_in_test = 0  # 记录test set包含的天数
    r2_all_tests = []  # 记录每一天的r2
    mse_all_tests = []  # 记录每一天的mse
    for i_month in para.month_test:  # 按月加载
        file_name = para.path_data + str(i_month) + ".h5"
        f = h5py.File(file_name, 'r')
        # print(file_name)
        for key in f.keys():  # 按天加载，按天预处理数据
            n_days_in_test += 1
            # 加载
            h5 = pd.read_hdf(file_name, key=str(key))
            data_curr_day = pd.DataFrame(h5)
            data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'].abs() >= 10.2)  # 去掉收益率绝对值大于10.2的数据点
            data_curr_day = data_curr_day.mask(data_curr_day['pct_chg'] == 0.0)  # 去掉收益率为0的数据点
            data_curr_day = data_curr_day.dropna(axis=0)  # remove nan
            # 预处理
            X_curr_day = data_curr_day.loc[:, 'close':'amount'] # X的实际值
            y_curr_day = data_curr_day.loc[:, 'pct_chg'] * 0.01 # y的实际值

            scalar = preprocessing.StandardScaler().fit(X_curr_day) # 标准化
            X_curr_day = scalar.transform(X_curr_day)

            X_curr_day = PCA_algorithm.pca(X_curr_day) # pca

            # 预测
            y_score_1st_layer = np.zeros((y_curr_day.shape[0], len(models_1st_layer)))
            for i in range(len(models_1st_layer)):
                y_a_model_1st_layer = models_1st_layer[i].predict(X_curr_day)
                y_score_1st_layer[:,i]  = y_a_model_1st_layer
            y_score_curr_day = meta_model.predict(y_score_1st_layer)

            # 保存结果到csv文件
            result_curr_day = pd.DataFrame(y_curr_day.index)
            result_curr_day['date_pred'] = np.nan
            result_curr_day['return_true'] = np.nan
            result_curr_day['return_pred'] = y_score_curr_day
            result_curr_day = result_curr_day.sort_values(by='return_pred', ascending=False)
            if os.path.exists(para.path_results + "ave_stacking") == False:
                os.mkdir(para.path_results + "meta_stacking")
            store_path = para.path_results + "meta_stacking\\"+str(n_days_in_test) + ".csv"
            result_curr_day.to_csv(store_path, sep=',', header=True, index=False)

            # 计算r2, mse
            r2_curr_day =  metrics.r2_score(y_curr_day, y_score_curr_day)
            mse_curr_day = metrics.mean_squared_error(y_curr_day, y_score_curr_day)
            r2_all_tests.append(r2_curr_day)
            mse_all_tests.append(mse_curr_day)
            print("day #%d, r2 = %6f, MSE = %6f" %(n_days_in_test,r2_curr_day, mse_curr_day))
    print("average r2 on all test days = %6f" % np.mean(r2_all_tests))
    print("average MSE on all test days = %6f" % np.mean(mse_all_tests))

    return n_days_in_test

def train_1st_layer(models_1st_layer_inits, X_in_sample, y_in_sample):
    models_1st_layer = []
    kf = KFold(n_splits=len(models_1st_layer_inits), random_state=para.seed, shuffle=True)
    for i, (train_index, cv_index) in enumerate(kf.split(X_in_sample)):
        X_train, X_cv = X_in_sample[train_index], X_in_sample[cv_index]
        y_train, y_cv = y_in_sample[train_index], y_in_sample[cv_index]
        model_name = models_1st_layer_inits[i][1]
        models_1st_layer.append(
            train.train_regress(clone(models_1st_layer_inits[i][0]), model_name, X_train, X_cv, y_train, y_cv))
    return models_1st_layer

def first_layer_predict(models_1st_layer, X_in_sample, y_in_sample):
    X_all_meta = np.zeros((y_in_sample.shape[0], len(models_1st_layer)))
    y_all_meta = y_in_sample
    for i in range(len(models_1st_layer)):
        X_all_meta[:,i] = models_1st_layer[i].predict(X_in_sample)  # 第一层模型的预测值存贮在X_all_meta的列中
        # print("first layer model #%d r2 on all sample data = %6f" %(i,metrics.r2_score(X_all_meta[:,i], y_in_sample)))
        # print("first layer model #%d mse on all sample data = %6f" %(i,metrics.mean_squared_error(X_all_meta[:,i], y_in_sample)))
    X_train_meta, X_cv_meta, y_train_meta, y_cv_meta = train_test_split(X_all_meta, y_all_meta, test_size=para.seed,
                                                                        random_state=para.seed)
    # y_train_meta, y_cv_meta = y_train_meta.values.ravel(), y_cv_meta.values.ravel()
    return X_train_meta, X_cv_meta, y_train_meta, y_cv_meta


if __name__ == '__main__':

    # 1. 加载train/cv set数据
    X_in_sample, y_in_sample = load_sample_data.load_regress()

    scalar = preprocessing.StandardScaler().fit(X_in_sample)
    X_in_sample = scalar.transform(X_in_sample)
    X_in_sample = PCA_algorithm.pca(X_in_sample)
    y_in_sample = y_in_sample.values.ravel()
    print("X_in_sample shape, y_in_sample shape:", X_in_sample.shape, y_in_sample.shape)

    # 2. 初始化第一、第二层模型
    models_1st_layer_inits = [Ridge_init.init(), SVR_init.init()]
    model_2nd_layer, *arg= RFR_init.init()

    # ---------- 训练第一层模型 ------------
    # 3. 训练模型,保存模型
    models_1st_layer = train_1st_layer(models_1st_layer_inits, X_in_sample, y_in_sample)

    # ---------- Meta-model Stacking --------------
    # 4. 将第一层的预测值作为第二层的输入
    # models_1st_layer = [] # 也可以直接从已训练好的模型中加载第一层模型
    # models_1st_layer.append(joblib.load(r"D:\Meiying\data\result\RFR\RFR_model.m"))  # 加载第一层的模型
    # models_1st_layer.append(joblib.load(r"D:\Meiying\data\result\Ridge\Ridge_model.m"))
    X_train_meta, X_cv_meta, y_train_meta, y_cv_meta = first_layer_predict(models_1st_layer, X_in_sample, y_in_sample)

    # 5. 训练第二层模型
    model_name = 'meta_stacking'
    meta_model = train.train_regress(model_2nd_layer, model_name, X_train_meta, X_cv_meta, y_train_meta, y_cv_meta)
    # ------------ staking结束 ------------

    # 6. 预测,保存结果
    n_days_in_test = meta_stack_predict(models_1st_layer, meta_model)

    # 7. 策略构建
    build_strategy.add_next_day_return(model_name)
    strategy = build_strategy.build(n_days_in_test, model_name)

    # 8. 策略评价
    evaluate_strategy.evaluate(strategy, n_days_in_test)

    # 其他
    # print(svm.SVC().get_params().keys()) # 查看模型需要的参数
    # model = joblib.load( para.path_results  + "model.m") # 模型加载


