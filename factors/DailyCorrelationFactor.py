# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/15  9:35
desc:
'''

# 引用frequency.py文件中相应的频率类
from factors.Frequency import DailyFrequency

# 引用category.py文件中相应的类别类
from factors.Category import CorrelationFactor

from factors.sql import pl_sql_oracle
from factors.util.CorrelationFuncProcess import CorrelationFuncProcess
from factors.util.CorrelationFunc import CorrelationFunc
import pandas as pd

"""
日频相关性类因子

代码表：
	见excel

"""


class DailyCorrelationFactor(DailyFrequency,CorrelationFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '日频相关性类因子'
        self.target_methods,self.nameGroup = CorrelationFuncProcess()  # 生成因子代码和因子名称，进行初始化
        self.code_sql_file_path_index = r'.\sql\sql_StockIndex.sql'
        self.weekday_sql_file_path = r'.\sql\sql_get_last_trading_weekday.sql'
        self.data_sql_file_path = r'.\sql\sql_daily_correlation_factor.sql'  # 读取数据库数据的sql代码文件路径
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'  # 查询股票代码的sql文件路径
        self.table_name = ['QT_Performance']

    def init_factors(self):
        """
        初始化因子的基础特征,包括factor name, factor code和description

        :return: dict, key为因子名,value为因子类的一个实例
        """
        factor_entities = dict()
        for i in range(len(self.target_methods)):
            factor_entities[self.target_methods[i]] = DailyCorrelationFactor(factor_code=self.nameGroup[i],name=self.target_methods[i],describe='')

        return factor_entities  # 不止一个因子

    def find_components(self, file_path,secucode,date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(filepath=file_path, table_name=self.table_name, secucode=secucode, date=date)

        components['QT_Performance'] = components['QT_Performance'].sort_values(by='TRADINGDAY')
        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """
        # factor_values = pd.DataFrame(components['QT_Performance'][['SECUCODE','TRADINGDAY']]) # 存储因子值
        TO_cal = CorrelationFunc(components['QT_Performance']['CHANGEPCT'],components['QT_Performance']['TRADINGDAY'] ,periodcoef=20,window=[1,3,6],
                            flag=1,code_sql_file_path=self.code_sql_file_path_index,weekday_sql_file_path=self.weekday_sql_file_path)

        common_dateIndex = TO_cal._common_dateIndex()
        tradingday = components['QT_Performance']['TRADINGDAY'][components['QT_Performance']['TRADINGDAY'].isin(common_dateIndex)]
        tradingday = tradingday.reset_index(drop=True)
        secucode = components['QT_Performance']['SECUCODE'][:len(common_dateIndex)]
        factor_values = pd.DataFrame()
        factor_values['TRADINGDAY'] = tradingday
        factor_values['SECUCODE'] = secucode

        for i in self.target_methods:
            temp_str = 'TO_cal.'+i+'()'
            # 注意.values的操作并不多余，生成的dataframe的列名均为0，重新设置成pd.DF后列名会重置成1,2,3..
            res = eval(temp_str)
            factor_values[list(res.columns)] = pd.DataFrame(res.values)
            # print(factor_values)

        return factor_values
