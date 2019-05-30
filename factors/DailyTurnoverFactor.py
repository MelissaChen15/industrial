# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/13  13:06
desc:
'''

# 引用frequency.py文件中相应的频率类
from factors.Frequency import DailyFrequency

# 引用category.py文件中相应的类别类
from factors.Category import TurnoverFactor
from factors.sql import pl_sql_oracle
from factors.util.TurnoverFuncProcess import TurnoverFuncProcess
from factors.util.TurnoverFunc import TurnoverFunc
import pandas as pd

"""
日频换手率类因子

"""


class DailyTurnoverFactor(DailyFrequency,TurnoverFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '日频换手率类因子'
        self.target_methods,self.nameGroup = TurnoverFuncProcess()  # 生成因子代码和因子名称，进行初始化
        self.data_sql_file_path = r'.\sql\sql_daily_turnover_factor.sql'  # 读取数据库数据的sql代码文件路径
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'  # 查询股票代码的sql文件路径
        self.table_name = ['QT_Performance']

    def init_factors(self):
        """
        初始化因子的基础特征,包括factor name, factor code和description

        :return: dict, key为因子名,value为因子类的一个实例
        """
        factor_entities = dict()
        count = 0000
        TO_cal = TurnoverFunc(pd.DataFrame(), pd.DataFrame(),
                              periodcoef=20, window=[1, 3, 6])
        for i in self.target_methods:
            name = [i + '_' + str(TO_cal.window[0]) + '_' + str(self.frequency),
                    i + '_' + str(TO_cal.window[1]) + '_' + str(self.frequency),
                    i + '_' + str(TO_cal.window[2]) + '_' + str(self.frequency)]
            for n in name:
                # print(n) expwgtTurnover_1_1
                entity = DailyTurnoverFactor(factor_code='TF%04d' % count,
                                        name=n,
                                        describe='')
                factor_entities[n] = entity
                count += 1

        return factor_entities

    def find_components(self, file_path,secucode,date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, self.table_name, secucode,date )

        components['QT_Performance'] = components['QT_Performance'].sort_values(by='TRADINGDAY')

        return components


    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['QT_Performance'][['SECUCODE','TRADINGDAY']]) # 存储因子值
        TO_cal = TurnoverFunc(components['QT_Performance']['TURNOVERRATE'],components['QT_Performance']['CHANGEPCT'],
                              periodcoef=20,window=[1,3,6])

        for i in self.target_methods:
            temp_str = 'TO_cal.'+i+'()'
            # 注意.values的操作并不多余，生成的dataframe的列名均为0，重新设置成pd.DF后列名会重置成1,2,3..
            name = [i+'_'+str(TO_cal.window[0])+'_'+str(self.frequency),i+'_'+str(TO_cal.window[1])+'_'+str(self.frequency),i+'_'+str(TO_cal.window[2])+'_'+str(self.frequency)]
            temp = pd.DataFrame(eval(temp_str).values,columns=name)
            factor_values = pd.concat([factor_values,temp],axis=1 )

        return factor_values

