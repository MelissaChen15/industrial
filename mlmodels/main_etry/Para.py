# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 10:40

# 参数类
class Para:
    percent_select = [0.3,0.3] # 收益率前30%标记为1，后30%标记为0
    percent_cv = 0.1 # 0.1
    path_data = r"D:\Meiying\data\cleaned\\"
    path_results = r"D:\Meiying\data\result\\"
    seed = 7 # random seed
    month_in_sample = range(1, 12+1)
    month_test = range(13, 20+1)
    n_stock_select = 100 # 策略选择的股票数量
    fee_rate = 0.9986 # 交易费、佣金等
