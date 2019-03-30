# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 13:41

import pandas as pd
from mlmodels.regressors.Para import Para
para = Para()

def build(n_days_in_test,model_name):

    strategy = pd.DataFrame({'return': [0] * n_days_in_test, 'value': [1] * n_days_in_test})
    for i_day in range(1, n_days_in_test + 1):
        file_name = para.path_results + model_name +"\\" +str(i_day) + ".csv"
        csv = pd.read_csv(file_name)
        result_csv_day = pd.DataFrame(csv)
        select = result_csv_day.iloc[:100, 1:2]  # return_true列
        strategy.iloc[i_day - 1, 0] = float(select.mean())
    strategy['value'] = (strategy['return'] * 0.9986 + 1).cumprod()
    strategy.to_csv(para.path_results + model_name+ "\\" + model_name+ "_performance.csv", sep=',', header=True, index=True)

    return  strategy



