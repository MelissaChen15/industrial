# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 13:41

import pandas as pd
import  h5py
import numpy as np
from main_entry.process.Para import Para
para = Para()

# 匹配预测值与真实收益
def add_next_day_return(model_name):
    n_days_in_test = 0
    for i_month in para.month_test:  # 按月加载
        file_name = para.path_data + str(i_month) + ".h5"
        f = h5py.File(file_name, 'r')
        # print(file_name)
        for key in f.keys():  # 按天加载，按天预处理数据
            n_days_in_test += 1
            if n_days_in_test == 1: continue # 第一天的y不要
            ### key!!
            h5 = pd.read_hdf(file_name, key=str(key))
            data_next_day = pd.DataFrame(h5)
            y_next_day = data_next_day.loc[:, 'pct_chg'] # y的实际值
            csv_name = para.path_results + model_name + "\\" + str(n_days_in_test-1)
            csv = pd.read_csv(csv_name + ".csv")
            csv_curr_day = csv.iloc[:para.n_stock_select,:1]# 取前100支股票的ts code
            # print(csv.loc[-1])
            csv_curr_day['return_true'] = np.zeros([para.n_stock_select])
            # map对应的股票
            for i in range(para.n_stock_select):
                code = csv_curr_day.iloc[i,0]
                try:
                    csv_curr_day.iloc[i,1] = y_next_day[code] * 0.01
                except:
                    pass
            # print(csv_curr_day)
            csv_curr_day.loc["predict date:"] = [key,""]
            csv_curr_day.to_csv(csv_name + '_select.csv', sep=',', header=True, index=True)


# 计算每天的平均收益和净值
def build(n_days_in_test,model_name):
    strategy = pd.DataFrame({'return': [0] * n_days_in_test, 'value': [1] * n_days_in_test})
    for i_day in range(1, n_days_in_test): # 共n_days_in_test - 1天，因为最后一天的预测没有数据回测
        file_name = para.path_results + model_name +"\\" +str(i_day) + "_select.csv"
        csv = pd.read_csv(file_name)
        result_csv_day = pd.DataFrame(csv)
        select = result_csv_day.iloc[:100, -1]  # return_true列
        strategy.iloc[i_day, 0] = float(select.mean()) # 日平均收益
    strategy['value'] = (strategy['return'] * (1-para.fee_rate) + 1).cumprod()
    strategy.to_csv(para.path_results + model_name+ "\\" + model_name+ "_performance.csv", sep=',', header=True, index=True)

    return  strategy

if __name__ == '__main__':
    # add_next_day_return("Logistic")
    # s = build(1220, "Logistic")
    # evaluate_strategy.evaluate(s, 1219)
    pass
