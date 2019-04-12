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

    def get_factor_list(self, factor_entities):
        """
        获取本类的因子列表

        :param factor_entities: dict, 因子实例
        :return: pandas.DataFrame 因子列表，包括FactorCode、简称、频率、类别、描述
        """
        factor_list = pd.DataFrame(columns=['FactorCode', '简称', '频率', '类别', '描述'])
        for k in factor_entities.keys():
            row = {'FactorCode': factor_entities.get(k).factor_code, '简称': factor_entities.get(k).name,
                   '频率': factor_entities.get(k).frequency, '类别': factor_entities.get(k).type,
                   '描述': factor_entities.get(k).describe}
            factor_list = factor_list.append(row, ignore_index=True)
        return factor_list

