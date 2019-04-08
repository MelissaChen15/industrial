# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 10:22


from factors.BasicFactor import BasicFactor
import pandas as pd

"""
因子类型类
"""

# 价值类因子
class ValueFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = 'value factor'


