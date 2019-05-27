# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/14  16:33
desc:
'''
from factors.Frequency import DailyFrequency

# 引用category.py文件中相应的类别类
from factors.Category import VolatilityFactor
from factors.sql import pl_sql_oracle
from factors.util.VolatilityFuncProcess import VolatilityFuncProcess
from factors.util.VolatilityFunc import VolatilityFunc
import pandas as pd

"""
日频波动类因子

"""


class DailyVolatilityFactor(DailyFrequency,VolatilityFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '日频波动类因子'
        self.target_methods,self.nameGroup = VolatilityFuncProcess()  # 生成因子代码和因子名称，进行初始化
        self.data_sql_file_path = r'.\sql\sql_daily_volatility_factor.sql'  # 读取数据库数据的sql代码文件路径
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'  # 查询股票代码的sql文件路径
        self.table_name = ['QT_Performance']

    def init_factors(self):
        """
        初始化因子的基础特征,包括factor name, factor code和description

        :return: dict, key为因子名,value为因子类的一个实例
        """
        factor_entities = dict()
        for i in range(len(self.target_methods)):
            factor_entities[self.target_methods[i]] = DailyVolatilityFactor(factor_code=self.nameGroup[i],name=self.target_methods[i],describe='')

        return factor_entities  # 不止一个因子

    def find_components(self, file_path, secucode,date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, self.table_name, secucode,date)
        components['QT_Performance'] = components['QT_Performance'].sort_values(by='TRADINGDAY')
        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """
        # code_sql_file_path_index = r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver4\StockFactorsCreating\factors\sql\sql_StockIndex.sql'

        factor_values = pd.DataFrame(components['QT_Performance'][['SECUCODE','TRADINGDAY']]) # 存储因子值
        TO_cal = VolatilityFunc(components['QT_Performance']['CLOSEPRICE'],components['QT_Performance']['HIGHPRICE'],
                              components['QT_Performance']['LOWPRICE'],components['QT_Performance']['CHANGEPCT'],20,
                                [1, 3, 6],components['QT_Performance']['TURNOVERVOLUME'],components['QT_Performance']['TURNOVERRATE'])

        for i in self.target_methods:
            temp_str = 'TO_cal.'+i+'()'
            # 注意.values的操作并不多余，生成的dataframe的列名均为0，重新设置成pd.DF后列名会重置成1,2,3..
            if i.startswith('high_low_std_part'):  # 这个函数的生成结果的shape与其他函数不一致
                factor_values[[i+'_'+'highcloseSTD'+'_'+str(self.frequency),i+'_'+'lowcloseSTD'+'_'+str(self.frequency)
                    ,i+'_'+'highlowdiffSTD1'+'_'+str(self.frequency),i+'_'+'highlowdiffSTD2'+'_'+str(self.frequency)]] = pd.DataFrame(eval(temp_str).values)
            else:
                factor_values[[i+'_'+str(TO_cal.window[0])+'_'+str(self.frequency),i+'_'+str(TO_cal.window[1])+'_'+str(self.frequency)
                    ,i+'_'+str(TO_cal.window[2])+'_'+str(self.frequency)]] = pd.DataFrame(eval(temp_str).values)
        return factor_values

