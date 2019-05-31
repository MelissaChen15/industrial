# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/17  17:44
desc:
'''

# 引用frequency.py文件中相应的频率类
from factors.Frequency import WeeklyFrequency
# 引用category.py文件中相应的类别类
from factors.Category import FinancialModelFactor
from factors.sql import pl_sql_oracle
from factors.util.FinancialModelFuncProcess import FinancialModelFuncProcess
from factors.util.FinancialModelFunc import FinancialModel_statsFunc
import pandas as pd

"""
周频金融模型_FF3类因子

"""


class WeeklyFinancialModelFactor1(WeeklyFrequency,FinancialModelFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '周频金融模型_FF3类因子'
        self.target_methods,self.nameGroup = FinancialModelFuncProcess()  # 生成因子代码和因子名称，进行初始化
        self.code_sql_file_path_index = r'.\sql\sql_StockIndex.sql'
        self.SMB_HML_file_path_daily = r'.\sql\sql_daily_timeseries_factor.sql'
        self.SMB_HML_file_path_weekly = r'.\sql\sql_weekly_timeseries_factor.sql'
        self.data_sql_file_path = r'.\sql\sql_weekly_financialmodel_factor.sql'  # 读取数据库数据的sql代码文件路径
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'  # 查询股票代码的sql文件路径
        self.weeklyday_file_path = r'.\sql\sql_get_last_trading_weekday.sql'

    def init_factors(self):
        """
        初始化因子的基础特征,包括factor name, factor code和description

        :return: dict, key为因子名,value为因子类的一个实例
        """
        factor_entities = dict()
        count = 0000
        columns_name = ['alpha','beta_index','beta_HML','beta_SMB','波动率', '上行波动率', '下行波动率', '上下波动率之差', '偏度']
        marketindex = ['IF','IC','IH']
        window = [3,6]

        for i in columns_name:
            for j in marketindex:
                for w in window:
                    name = i + '_' + j + '_'+ str(w) + '_m'
                    entity = WeeklyFinancialModelFactor1(factor_code='WFA%04d' % count,
                                            name=name,
                                            describe='')
                    factor_entities[name] = entity
                    count += 1

        return factor_entities

    def find_components(self, file_path ,secucode, date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(self.data_sql_file_path,  ['QT_Performance'],secucode,date )
        WeeklyTradingDay = sql.InputDataPreprocess(self.weeklyday_file_path, ['QT_TradingDayNew'])
        components['QT_Performance'] = components['QT_Performance'].sort_values(by='TRADINGDAY')
        WeeklyTradingDay['QT_TradingDayNew'] = WeeklyTradingDay['QT_TradingDayNew'].sort_values(by='TRADINGDATE')  # 周频交易日期
        # 匹配周频交易日期
        components['QT_Performance'] = components['QT_Performance'][components['QT_Performance']['TRADINGDAY'].isin(WeeklyTradingDay['QT_TradingDayNew']['TRADINGDATE'])]
        components['QT_Performance'] = components['QT_Performance'].reset_index(drop=True)  # 重设索引是必须的，否则会出错

        # print(components)
        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """
        # factor_values['SECUCODE'] = pd.DataFrame(components['QT_Performance']['SECUCODE']) # 'secucode'因子的长度与后面的数据要保持一致

        TO_cal = FinancialModel_statsFunc(components['QT_Performance']['TRADINGDAY'],components['QT_Performance']['CHANGEPCTRW'],
                                          flag=2,code_sql_file_path1=self.code_sql_file_path_index)

        # columns_name1 = ['alpha','beta','波动率', '上行波动率', '下行波动率', '上下波动率之差', '偏度','上行beta','下行beta','上下行beta差']
        columns_name2 = ['alpha','beta_index','beta_HML','beta_SMB','波动率', '上行波动率', '下行波动率', '上下波动率之差', '偏度']
        marketindex = ['IF','IC','IH']

        datagroup_FF3 = pd.DataFrame()
        for i in marketindex:
            alpha1_all, beta_all, residuals_stats = TO_cal.FF3_model_stats(i,self.SMB_HML_file_path_daily,self.SMB_HML_file_path_weekly)
            index_datagroup = pd.DataFrame()
            for j in alpha1_all.keys():
                temp_datagroup = pd.concat([alpha1_all[j],beta_all[j],residuals_stats[j]],axis=1)
                columns_name_temp = [k+'_'+i+'_'+j[-1]+'m' for k in columns_name2 ]
                temp_datagroup.columns = columns_name_temp
                index_datagroup = pd.concat([index_datagroup,temp_datagroup],axis=1)
            datagroup_FF3 = pd.concat([datagroup_FF3,index_datagroup],axis=1)

        factor_values = pd.DataFrame()
        factor_values[list(datagroup_FF3.columns)] = datagroup_FF3
        factor_values['TRADINGDAY'] = datagroup_FF3.index
        factor_values['SECUCODE'] = components['QT_Performance']['SECUCODE'].values[:len(datagroup_FF3)]
        return factor_values