# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/5 17:01

import numpy as np
import pandas as pd
from factors.sql import pl_sql_oracle
import datetime
from factors.util import datetime_ops

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
        self.data_sql_file_path = '' # string, 读取数据库数据的文件相对路径
        self.code_sql_file_path = '' # string,  读取股票代码的sql文件的相对路径
        self.table_name = [] # list, 需要读取的数据库中的表名

    def init_factors(self):
        """
        初始化因子的基础特征,包括factor name, factor code和description

        :return: dict, key为因子名,value为因子类的一个实例
        """
        factor_entities = {}

        return factor_entities

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

    def write_values_to_DB(self, date, mode = 'print'):
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(self.code_sql_file_path,['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path=self.data_sql_file_path,
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'',
                                            date = date)
                factor_values = self.get_factor_values(data)

                from sqlalchemy import String, Integer
                if mode == 'print':
                    print(factor_values)
                if mode == 'write':
                    pl_sql_oracle.df_to_DB(factor_values, self.__class__.__name__.lower(),if_exists= 'append',data_type={'SECUCODE': String(20)})
                print(self.type,'secucode' ,getattr(row, 'SECUCODE'),' done')


            except Exception as e:
                print(getattr(row, 'SECUCODE'), e)


    def find_components(self, file_path,secucode,date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        components = {}


        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """
        factor_values = pd.DataFrame()

        return factor_values

    def seasonal_to_monthly(self, seasonal_data: pd.DataFrame, seasonal_factor_name: list):
        # 插值法会导致尾部没有数据，目前使用的解决方法是取最近一期报告的值
        """
        应用cubic spline或者线性插值法，将季频数据转换成月频数据
        可以同时处理多个特征；多支股票需要将同一支股票的数据放在一起，上下拼接

        :param seasonal_data:  pandas.DataFrame, 列包含 'ENDDATE''SECUCODE'和需要转换的因子
        :param seasonal_factor_name: list of string，需要转换的因子的名称
        :return: pandas.DataFrame, 列包含 'ENDDATE''SECUCODE'和需要转换的因子
        """
        from factors.util.datetime_ops import months_next_season
        a_stock_monthly_data = pd.DataFrame()
        seasonal_data = seasonal_data.sort_values(by='ENDDATE') # 排序
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
        # 如果插值的日期超过了今日, 则删除
        a_stock_monthly_data = a_stock_monthly_data.drop(a_stock_monthly_data[a_stock_monthly_data.STARTDAY > datetime.date.today()].index)
        # 最后一个报告日至现在日期, 无法插值, 沿用最后一个报告日的数据
        a_stock_monthly_data = a_stock_monthly_data.fillna(method='ffill')
        return a_stock_monthly_data

    def monthly_to_daily(self, monthly_data: pd.DataFrame, daily_data: pd.DataFrame, seasonal_factor_name: list,date:list):
        """
        将seasonal_to_monthly转换之后的月频数据转换为日频数据

        :param monthly_data:  pd.DataFrame seasonal_to_monthly转换之后的月频数据，必须有[['SECUCODE', 'TRADINGDAY']两列
        :param daily_data: pd.DataFrame 必须有[['SECUCODE', 'TRADINGDAY']两列
        :param seasonal_factor_name: list of string，需要转换的因子的名称
        :param date: list of string，转换后需要的日期范围
        :return: pd.DataFrame 转换好的日频数据，列包含 'ENDDATE''SECUCODE'和需要转换的因子
        """
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
        #
        # # 如果日期超过了限定的日期范围, 则删除
        # daily_data = daily_data.drop(daily_data[daily_data.TRADINGDAY > datetime_ops.next_day(date[1])].index)
        # daily_data = daily_data.drop(daily_data[daily_data.TRADINGDAY < datetime_ops.next_day(date[0])].index)
        # 处理数据尾部空值，目前解决方案是全部等于最近一期报告披露的数值
        daily_data = daily_data.fillna(method='ffill')


        return daily_data


