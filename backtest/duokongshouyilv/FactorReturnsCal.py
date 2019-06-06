# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/6/3  13:14
desc:
'''
import pandas as pd
from sql.get_factordata_DB import dbData_import_factor
from sql.get_auxiliarydata_DB import dbData_import_auxiliary
from Long_Short_returns_of_Signals_daily import create_LSreturns
import datetime


class FactorReturnsCal(object):
    def __init__(self,factor_tb,auxiliary_tablename,auxiliary_name,daterange):
        '''
        :param factor_tb: 因子表名称
        :param start_date: 开始日期
        :param frequency: 频率，不同频率的因子对应的数据库涨跌幅字段不同，日涨跌幅，周涨跌幅，月涨跌幅
        '''
        self.factor_tb = factor_tb
        self.frequency = 1  # 1,2,3 日频，周频，月频
        self.factor_data = ''  # 初始化因子数据
        self.auxiliary_tablename = auxiliary_tablename
        self.auxiliary_name = auxiliary_name
        self.auxiliary_data = '' # 初始化辅助数据
        self.daterange = daterange
        for i in [0, 1]:
            if type(self.daterange[i]) == datetime.date: self.daterange[i] = self.daterange[i].strftime("%Y-%m-%d")

    def get_ori_factordata(self,):
        get_data = dbData_import_factor(self.factor_tb,self.frequency,self.daterange)
        get_data.create_sql_sentence()
        self.factor_data = get_data.InputDataPreprocess()
        self.factor_data.dropna(axis=0,how='any',inplace=True)  # 因子数据可能存在空值情形，直接去掉

    def get_auxiliarydata(self):
        auxiliary_import = dbData_import_auxiliary(self.auxiliary_tablename, self.auxiliary_name, self.daterange)
        auxiliary_import.create_sql_sentence()
        self.auxiliary_data = auxiliary_import.InputDataPreprocess()
        self.auxiliary_data.dropna(axis=0,how='any',inplace=True)  # 因子数据可能存在空值情形，直接去掉

    def factor_cal(self):  # 'Equal Weighted';'Value Weighted'
        date_and_code = ['SECUCODE','TRADINGDAY']
        factor_names = list((self.factor_data.columns).drop(date_and_code))  # 所有因子库的前两列均为证券代码和交易日期
        res_part1 = pd.DataFrame()
        for i in factor_names:
            temp1 = date_and_code + [i]
            res1 = create_LSreturns(self.factor_data[temp1], self.auxiliary_data, i)
            res1 = pd.DataFrame(res1)
            colums_name1 = [x+'_'+i for x in list(res1.columns)]
            res_part1[colums_name1] = res1
            print(self.factor_tb,' ', i ,'done')
        # res_part1['TRADINGDAY'] = (self.factor_data['TRADINGDAY']).values[1:]

        return res_part1


# if __name__ == '__main__':
#     import time
#     time_start = time.time()
#     res = FactorReturnsCal('DailyValueFactor','QT_Performance', ['ChangePCT','NEGOTIABLEMV'],['2018-01-01', datetime.date.today()])
#     res.get_ori_factordata()
#     res.get_auxiliarydata()
#     res11 = res.factor_cal()
#     print(res11)
# #     time_end = time.time()
# #     print('time cost', time_end - time_start, 's')
