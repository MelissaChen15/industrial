# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 13:41

import pandas as pd
import  h5py
import numpy as np
from main_entry.Para import Para
para = Para()

# 匹配预测值与真实收益
def add_next_day_return(model_name):
    n_days_in_test = 0
    for i_month in para.month_test:  # 按月加载
        file_name = para.path_data + str(i_month) + ".h5"
        f = h5py.File(file_name, 'r')
        # print(file_name)
        for key in f.keys():  # 按天加载，按天预处理数据
            # key是被预测的日期
            n_days_in_test += 1
            if n_days_in_test == 1: continue # 第一天的y不要
            h5 = pd.read_hdf(file_name, key=str(key))
            data_next_day = pd.DataFrame(h5)
            y_next_day = data_next_day.loc[:, 'pct_chg'] # y的实际值
            csv_name = para.path_results + model_name + "\\" + str(n_days_in_test-1)
            csv_curr_day = pd.read_csv(csv_name + ".csv")
            # csv_curr_day = csv.iloc[:para.n_stock_select,:1]# 取前n_stock_select支股票的ts code
            csv_curr_day['date_pred'] = key

            # map对应的股票
            for i in range(csv_curr_day.shape[0]):
                code = csv_curr_day.iloc[i,0]
                try:
                    csv_curr_day.iloc[i,2] = y_next_day[code] * 0.01 # 第2列第return_ture
                except:
                    pass
            # print(csv_curr_day)
            csv_curr_day.to_csv(csv_name + '.csv', sep=',', header=True, index=False)


# 计算每天的平均收益和净值
def build(n_days_in_test,model_name):
    strategy = pd.DataFrame({'date': np.nan * n_days_in_test, 'return': [0] * n_days_in_test, 'value': [1] * n_days_in_test})
    for i_day in range(1, n_days_in_test): # 共n_days_in_test - 1天，因为最后一天的预测没有数据回测
        file_name = para.path_results + model_name +"\\" +str(i_day) + ".csv"
        csv = pd.read_csv(file_name)
        result_csv_day = pd.DataFrame(csv)
        ##### 如果需要修改取股票的方式 ####
        select = result_csv_day.iloc[:para.n_stock_select, 2]  # 取para.n_stock_select,第2列是pred_true
        ############### end #############
        strategy.iloc[i_day, 0] = result_csv_day.iloc[1,1] # strategy第0列是date, result_csv_day[1,1]也是date
        strategy.iloc[i_day, 1] = float(select.mean()) # 日平均收益, strategy第1列是return
    strategy['value'] = (strategy['return'] * (1-para.fee_rate) + 1).cumprod()
    strategy.to_csv(para.path_results + model_name+ "\\" + model_name+ "_performance.csv", sep=',', header=True, index=False)

    return  strategy

if __name__ == '__main__':
    # add_next_day_return("Logistic")
    s = build(20, "Logistic")
    # evaluate_strategy.evaluate(s, 1219)
    pass
