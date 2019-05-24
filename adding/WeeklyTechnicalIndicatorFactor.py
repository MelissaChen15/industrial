# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/22  15:20
desc:
'''

from Frequency import WeeklyFrequency
from Category import TechnicalIndicatorFactor
from sql import pl_sql_oracle

from util.TechnicalIndicatorProcess import TechnicalIndicatorProcess
from util.TechnicalIndicatorFunc import TechnicalIndicatorFunc
import pandas as pd


# 开盘价和收盘价取的当天周最后交易日数据，最高价和最低价取整个周的，成交量为整个周的。
class WeeklyTechnicalIndicatorFactor(WeeklyFrequency,TechnicalIndicatorFactor ):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '周频技术指标类'
        self.target_methods, self.nameGroup = TechnicalIndicatorProcess()

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子
        for i in range(len(self.target_methods)):
            factor_entities[self.target_methods[i]] = WeeklyTechnicalIndicatorFactor(factor_code=self.nameGroup[i],name = self.target_methods[i],describe='')

        return factor_entities

    def find_components(self, file_path,file_path2, table_name,secucode = ''):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, table_name, secucode )

        WeeklyTradingDay = sql.InputDataPreprocess(file_path2,['QT_TradingDayNew'],'')  # 这个secucode的''不能省去！

        # TODO: 读取时需要按时间排序
        components['QT_Performance'] = components['QT_Performance'].sort_values(by='TRADINGDAY')
        WeeklyTradingDay['QT_TradingDayNew'] = WeeklyTradingDay['QT_TradingDayNew'].sort_values(by='TRADINGDATE')  # 周频交易日期
        # TODO: 匹配周频交易日期
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

    def write_values_to_DB(self,  code_sql_file_path, data_sql_file_path,weeklyday_file_path):
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(code_sql_file_path,['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path= data_sql_file_path,file_path2= weeklyday_file_path,
                                           table_name=['QT_Performance'],
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
                factor_values = self.get_factor_values(data)
                print(factor_values)

                from sqlalchemy import String, Integer
                # pl_sql_oracle.df_to_DB(factor_values, 'weeklytechnicalindicatorfactor',if_exists= 'append',data_type={'SECUCODE': String(20)})

                print(getattr(row, 'SECUCODE'),' done')


            except Exception as e:
                print(getattr(row, 'SECUCODE'), e)




if __name__ == '__main__':
    dtif = WeeklyTechnicalIndicatorFactor()
    data_sql_file_path =  r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver4\StockFactorsCreating\factors\sql\sql_weekly_technicalIndicator_factor.sql'
    code_sql_file_path =  r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver4\StockFactorsCreating\factors\sql\sql_get_secucode.sql'
    weeklyday_file_path = r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver4\StockFactorsCreating\factors\sql\sql_get_last_trading_weekday.sql'

    dtif.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path,weeklyday_file_path=weeklyday_file_path)