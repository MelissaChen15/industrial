# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/14  15:28
desc:
'''
# 引用frequency.py文件中相应的频率类
from factors.Frequency import WeeklyFrequency

# 引用category.py文件中相应的类别类
from factors.Category import MomentumFactor
from factors.sql import pl_sql_oracle
from factors.util.MomentumFuncProcess import MomentumFuncProcess
from factors.util.MomentumFunc import MomentumFunc
import pandas as pd

"""
周频动量类因子

"""


class WeeklyMomentumFactor(WeeklyFrequency,MomentumFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '周频动量类因子'
        self.target_methods,self.nameGroup = MomentumFuncProcess()  # 生成因子代码和因子名称，进行初始化
        self.data_sql_file_path = r'.\sql\sql_weekly_momentum_factor.sql'  # 读取数据库数据的sql代码文件路径
        self.weeklyday_file_path = r'.\sql\sql_get_last_trading_weekday.sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'  # 查询股票代码的sql文件路径

    def init_factors(self):
        """
        初始化因子的基础特征,包括factor name, factor code和description

        :return: dict, key为因子名,value为因子类的一个实例
        """
        factor_entities = dict()
        count = 0000
        TO_cal = MomentumFunc(pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),
                              window=[1,3,6,12],periodcoef=4)
        for i in self.target_methods:
            name = [i+'_'+str(TO_cal.window[0])+'_'+str(self.frequency),i+'_'+str(TO_cal.window[1])+'_'+str(self.frequency)
                ,i+'_'+str(TO_cal.window[2])+'_'+str(self.frequency),i+'_'+str(TO_cal.window[3])+'_'+str(self.frequency)]
            for n in name:
                entity = WeeklyMomentumFactor(factor_code='WM%04d' % count,
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
        components = sql.InputDataPreprocess(self.data_sql_file_path, ['QT_Performance'], secucode,date)
        WeeklyTradingDay = sql.InputDataPreprocess(self.weeklyday_file_path,['QT_TradingDayNew'])

        components['QT_Performance'] = components['QT_Performance'].sort_values(by='TRADINGDAY')
        WeeklyTradingDay['QT_TradingDayNew'] = WeeklyTradingDay['QT_TradingDayNew'].sort_values(by='TRADINGDATE')  # 周频交易日期
        #  匹配周频交易日期
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
        TO_cal = MomentumFunc(components['QT_Performance']['HIGHESTCLOSEPRICERW'],components['QT_Performance']['TURNOVERVOLUMERW'],
                              components['QT_Performance']['TURNOVERRATERW'],components['QT_Performance']['CHANGEPCTRW'],
                              window=[1,3,6,12],periodcoef=4)

        for i in self.target_methods:
            temp_str = 'TO_cal.'+i+'()'
            # 注意.values的操作并不多余，生成的dataframe的列名均为0，重新设置成pd.DF后列名会重置成1,2,3..
            factor_values[[i+'_'+str(TO_cal.window[0])+'_'+str(self.frequency),i+'_'+str(TO_cal.window[1])+'_'+str(self.frequency)
                ,i+'_'+str(TO_cal.window[2])+'_'+str(self.frequency),i+'_'+str(TO_cal.window[3])+'_'+str(self.frequency)]] = pd.DataFrame(eval(temp_str).values)
            # print(factor_values)

        return factor_values



