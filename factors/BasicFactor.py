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
        self.factor_code = factor_code #  int, 因子代码, 主键，不可空
        self.name = name # string, 因子名, 不可空
        self.describe = describe # string, 因子描述
        self.type = np.nan # string, 因子类型，如：价值类
        self.frequency = np.nan # string, 因子频率

    def init_factors(self):
        pass

    def get_factor_list(self):
        """
        获取本类的因子列表

        :param factor_entities: dict, 因子实例
        :return: pandas.DataFrame 因子列表，包括FactorCode、简称、频率、类别、描述
        """
        factor_entities = self.init_factors()
        factor_list = pd.DataFrame(columns=['FactorCode', '简称', '频率', '类别', '描述'])
        for k in factor_entities.keys():
            row = {'FactorCode': factor_entities.get(k).factor_code, '简称': factor_entities.get(k).name,
                   '频率': factor_entities.get(k).frequency, '类别': factor_entities.get(k).type,
                   '描述': factor_entities.get(k).describe}
            factor_list = factor_list.append(row, ignore_index=True)
        return factor_list


    def seasonal_to_monthly(self, seasonal_data: pd.DataFrame, seasonal_factor_name: list):
        # TODO: 插值法会导致尾部没有数据，目前使用的解决方法是取最近一期报告的值
        """
        应用cubic spline，将季频数据转换成月频数据
        可以同时处理多个特征；多支股票需要将同一支股票的数据放在一起，上下拼接

        :param seasonal_data:  pandas.DataFrame, 列包含 'ENDDATE''SECUCODE'和需要转换的因子
        :param seasonal_factor_name: list of string，需要转换的因子的名称
        :return: pandas.DataFrame, 列包含 'ENDDATE''SECUCODE'和需要转换的因子
        """
        from factors.util.datetime_ops import months_next_season
        a_stock_monthly_data = pd.DataFrame()
        # 循环所有数据
        for row in seasonal_data.itertuples(index=True, name='Pandas'):
            code = getattr(row, 'SECUCODE')

            months_start = months_next_season(getattr(row, 'ENDDATE'))
            row1_dict = {'STARTDAY': months_start[0],
                         'SECUCODE': code,
                         }
            for f in seasonal_factor_name:
                row1_dict[f] = getattr(row, f)
            row2_dict = {'STARTDAY': [months_start[1], months_start[2]],
                         'SECUCODE': [code, code],
                         }
            for f in seasonal_factor_name:
                row2_dict[f] = np.nan
            row1 = pd.DataFrame(row1_dict, index=[0])
            row2 = pd.DataFrame(row2_dict)

            a_stock_monthly_data = pd.concat([a_stock_monthly_data, row1.append(row2)], axis=0, ignore_index=True)
        # 因为cubic spline要求第一个值非空，所以一列一列的插值，输出报错的列
        for c in a_stock_monthly_data.columns:
            try:
                a_stock_monthly_data[c] = a_stock_monthly_data[c].interpolate(method='cubic', axis=0)  # cubic spline 三次样条插值
            except ValueError:
                try:
                    a_stock_monthly_data[c] = a_stock_monthly_data[c].interpolate(method='slinear', axis=0)  # slinear 线性插值
                except Exception as e:
                    print('factor', c, 'error: ',e)
        return a_stock_monthly_data

    def monthly_to_daily(self, monthly_data: pd.DataFrame, daily_data: pd.DataFrame, seasonal_factor_name: list):
        """
        将seasonal_to_monthly转换之后的月频数据转换为日频数据

        :param monthly_data:  pd.DataFrame seasonal_to_monthly转换之后的月频数据，必须有[['SECUCODE', 'TRADINGDAY']两列
        :param daily_data: pd.DataFrame 必须有[['SECUCODE', 'TRADINGDAY']两列
        :param seasonal_factor_name: list of string，需要转换的因子的名称
        :return: pd.DataFrame 转换好的日频数据，列包含 'ENDDATE''SECUCODE'和需要转换的因子
        """
        # TODO: 看一下源码concat_inner 或者 to list之后用binary search
        from factors.util.datetime_ops import first_day_this_month
        daily_data = pd.DataFrame(daily_data[['SECUCODE', 'TRADINGDAY']])
        for f in seasonal_factor_name:
            daily_data[f] = np.nan
        daily_data['STARTDAY'] = daily_data['TRADINGDAY'].apply(lambda v: first_day_this_month(v))

        for row in daily_data.itertuples(index=True, name='Pandas'):
            code = getattr(row, 'SECUCODE')
            start_day = getattr(row, 'STARTDAY')
            for row2 in monthly_data.itertuples(index=True, name='Pandas2'):
                code2 = getattr(row2, 'SECUCODE')
                start_day2 = getattr(row2, 'STARTDAY')
                if (code == code2 and start_day == start_day2): # 如果某日期的上季度报告已经发布
                    for f in seasonal_factor_name:
                        daily_data.loc[row.Index, f] = getattr(row2, f)

        # 处理数据尾部空值，目前解决方案是全部等于最近一期报告披露的数值
        daily_data = daily_data.fillna(method='ffill')


        return daily_data


