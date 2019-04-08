# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/5 17:01

import numpy as np
import pandas as pd

"""
基础因子类
"""
class BasicFactor(object):

    def __init__(self, factor_code, name, describe):
        self.factor_code = factor_code #  string, 因子代码, 主键，不可空
        self.name = name # string, 因子名, 不可空
        self.describe = describe # string, 因子描述
        self.type = np.nan # string, 因子类型，如：价值类
        self.frequency = np.nan # string, 因子频率

