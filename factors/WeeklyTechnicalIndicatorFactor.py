# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/22  15:20
desc:
'''

from factors.Frequency import WeeklyFrequency
from factors.Category import TechnicalIndicatorFactor
from factors.sql import pl_sql_oracle

from factors.util.TechnicalIndicatorProcess import TechnicalIndicatorProcess
from factors.util.TechnicalIndicatorFunc import TechnicalIndicatorFunc
import pandas as pd


# 开盘价和收盘价取的当天周最后交易日数据，最高价和最低价取整个周的，成交量为整个周的。
class WeeklyTechnicalIndicatorFactor(WeeklyFrequency,TechnicalIndicatorFactor ):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '周频技术指标类'
        self.target_methods, *args , self.nameGroup  = TechnicalIndicatorProcess()
        self.data_sql_file_path = r'.\sql\sql_weekly_technicalIndicator_factor.sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'
        self.weeklyday_file_path = r'.\sql\sql_get_last_trading_weekday.sql'

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子
        for i in range(len(self.target_methods)):
            factor_entities[self.target_methods[i]] = WeeklyTechnicalIndicatorFactor(factor_code=self.nameGroup[i],name = self.target_methods[i],describe='')

        return factor_entities

    def find_components(self, file_path,secucode,date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(self.data_sql_file_path, ['QT_Performance'], secucode )

        WeeklyTradingDay = sql.InputDataPreprocess(self.weeklyday_file_path,['QT_TradingDayNew'])

        components['QT_Performance'] = components['QT_Performance'].sort_values(by='TRADINGDAY')
        WeeklyTradingDay['QT_TradingDayNew'] = WeeklyTradingDay['QT_TradingDayNew'].sort_values(by='TRADINGDATE')  # 周频交易日期
        # 匹配周频交易日期
        components['QT_Performance'] = components['QT_Performance'][components['QT_Performance']['TRADINGDAY'].isin(WeeklyTradingDay['QT_TradingDayNew']['TRADINGDATE'])]
        components['QT_Performance'] = components['QT_Performance'].reset_index(drop=True)  # 重设索引是必须的，否则会出错

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['QT_Performance'][['SECUCODE','TRADINGDAY']]) # 存储因子值
        cal_TI = TechnicalIndicatorFunc(components['QT_Performance']['HIGHPRICERW'],components['QT_Performance']['LOWPRICERW'],
                                        components['QT_Performance']['CLOSEPRICE'],components['QT_Performance']['OPENPRICE'],
                                        components['QT_Performance']['TURNOVERVOLUMERW'])
        for i in self.target_methods:
            temp_str = 'cal_TI.'+i+'()'
            factor_values[i] = eval(temp_str)

        return factor_values
