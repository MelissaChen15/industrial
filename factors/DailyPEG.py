# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37
# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

import pandas as pd

from factors.Category import ValueFactor
from factors.Frequency import DailyFrequency
from factors.sql import pl_sql_oracle

"""
日频、价值类因子, 因为日频/季频而做特殊处理

代码表：
    1010	PEG
"""

class DailyPEG(DailyFrequency, ValueFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '日频价值类特殊处理'
        self.data_sql_file_path = ['.\sql\sql_daily_peg_1.sql', '.\sql\sql_daily_peg_2.sql']
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'
        self.table_name = ['LC_MainIndexNew','LC_DIndicesForValuation']

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # PEG 市盈率增长率
        # 注意，此因子为日频数据/季频数据，分母为插值成月频的季频数据
        PEG = DailyPEG(factor_code='1010',
                               name='PEG',
                               describe='市盈率增长率 = 市盈率(PE)/净利润同比增长率(NetProfitGrowRate)')
        factor_entities['PEG'] = PEG

        return factor_entities

    def find_components(self, file_path, secucode, date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()

        components = {}
        date_daily = 'and t1.TradingDay >= to_date( \'' + date[0] + '\',\'yyyy-mm-dd\')  ''and t1. TradingDay <= to_date( \'' + date[1] + '\',\'yyyy-mm-dd\')'
        date_seasonal =  'and t1.EndDate >= to_date( \'' + date[0] + '\',\'yyyy-mm-dd\')  ''and t1. EndDate <= to_date( \'' + date[1] + '\',\'yyyy-mm-dd\')'
        c_daily = sql.InputDataPreprocess(file_path[0],['LC_DIndicesForValuation'] , secucode, date_daily)
        c_seasonal = sql.InputDataPreprocess(file_path[1], ['LC_MainIndexNew'], secucode, date_seasonal)

        components['LC_MainIndexNew']  = c_seasonal['LC_MainIndexNew'].sort_values(by='ENDDATE')
        components['LC_DIndicesForValuation'] = c_daily['LC_DIndicesForValuation'].sort_values(by='TRADINGDAY')


        components['LC_MainIndexNew_monthly'] = self.seasonal_to_monthly(components['LC_MainIndexNew'],['NETPROFITGROWRATE']) # 季频插值为月频
        components['LC_MainIndexNew_daily'] = self.monthly_to_daily(components['LC_MainIndexNew_monthly'], components['LC_DIndicesForValuation'],['NETPROFITGROWRATE'],date = date) # 月频转换为日频

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """
        factor_values = pd.DataFrame(components['LC_DIndicesForValuation'][['SECUCODE', 'TRADINGDAY']])  # 存储因子值
        factor_values['PEG'] = components['LC_DIndicesForValuation']['PE'] / (components['LC_MainIndexNew_daily']['NETPROFITGROWRATE'])

        return factor_values.drop(axis=0, index=0)


