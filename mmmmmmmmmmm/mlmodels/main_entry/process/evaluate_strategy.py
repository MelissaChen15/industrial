# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 13:46


import numpy as np
import matplotlib.pyplot as plt
from main_entry.process.Para import Para
para = Para()

# 策略评价
def evaluate(strategy, n_days_in_test):
    ann_excess_return = float(np.mean(strategy['return'])) * 252  # 年化超额收益
    ann_excess_vol = float(np.std(strategy['return'])) * np.sqrt(252)  # 年化超额收益波动率
    info_ratio = ann_excess_return / ann_excess_vol  # 信息比率
    print("ann excess return = %6f" % ann_excess_return)
    print("ann excess vol = %6f" % ann_excess_vol)
    print("info ratio = %6f" % info_ratio)
    # plt.plot(range(1, n_days_in_test + 1), strategy.loc[range(n_days_in_test), 'value'], 'r-') # 净值图像
    # plt.show()



