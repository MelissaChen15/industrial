# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/4/25  19:51
desc:
'''


from factors.Frequency import DailyFrequency
from factors.Category import TechnicalIndicatorFactor
from factors.sql import pl_sql_oracle

from factors.util.TechnicalIndicatorProcess import TechnicalIndicatorProcess
from factors.util.TechnicalIndicatorFunc import TechnicalIndicatorFunc
import pandas as pd

"""
日频技术指标类因子

代码表：
    TI0000	ADLine
    TI0001	ADOscillator
    TI0002	ADX
    TI0003	APO
    TI0004	AveragePrice
    TI0005	BOP
    TI0006	CCI
    TI0007	CDL2CROWS
    TI0008	CDL3BLACKCROWS
    TI0009	CDL3INSIDE
    TI0010	CDL3LINESTRIKE
    TI0011	CDL3STARSINSOUTH
    TI0012	CDL3WHITESOLDIERS
    TI0013	CDLABANDONEDBABY
    TI0014	CDLADVANCEBLOCK
    TI0015	CDLBELTHOLD
    TI0016	CDLBREAKAWAY
    TI0017	CDLCLOSINGMARUBOZU
    TI0018	CDLCONCEALBABYSWALL
    TI0019	CDLCOUNTERATTACK
    TI0020	CDLDARKCLOUDCOVER
    TI0021	CDLDOJI
    TI0022	CDLDOJISTAR
    TI0023	CDLDRAGONFLYDOJI
    TI0024	CDLENGULFING
    TI0025	CDLEVENINGDOJISTAR
    TI0026	CDLGAPSIDESIDEWHITE
    TI0027	CDLHAMMER
    TI0028	CDLHARAMI
    TI0029	CDLHARAMICROSS
    TI0030	CDLHIKKAKE
    TI0031	CDLHIKKAKEMOD
    TI0032	CDLIDENTICAL3CROWS
    TI0033	CDLINVERTEDHAMMER
    TI0034	CDLKICKING
    TI0035	CDLLADDERBOTTOM
    TI0036	CDLLONGLEGGEDDOJI
    TI0037	CDLLONGLINE
    TI0038	CDLMARUBOZU
    TI0039	CDLMATCHINGLOW
    TI0040	CDLMATHOLD
    TI0041	CDLMORNINGDOJISTAR
    TI0042	CDLONNECK
    TI0043	CDLRICKSHAWMAN
    TI0044	CDLRISEFALL3METHODS
    TI0045	CDLSEPARATINGLINES
    TI0046	CDLSHOOTINGSTAR
    TI0047	CDLSPINNINGTOP
    TI0048	CDLSTICKSANDWICH
    TI0049	CDLTASUKIGAP
    TI0050	CDLTRISTAR
    TI0051	CDLUNIQUE3RIVER
    TI0052	CDLUPSIDEGAP2CROWS
    TI0053	CDLXSIDEGAP3METHODS
    TI0054	CMO
    TI0055	HT_dcperiod
    TI0056	HT_dcphase
    TI0057	HT_trendmode
    TI0058	MACD
    TI0059	MFI
    TI0060	MINUS_DI
    TI0061	MOM
    TI0062	MedianPrice
    TI0063	PPO
    TI0064	ROC
    TI0065	ROCP
    TI0066	RSI
    TI0067	TRIX
    TI0068	TypicalPrice
    TI0069	WILLR
    TI0070	WeightedClosePrice
"""

class DailyTechnicalIndicatorFactor(DailyFrequency,TechnicalIndicatorFactor ):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '日频技术指标类'
        self.target_methods, self.nameGroup, *args = TechnicalIndicatorProcess()
        self.data_sql_file_path = r'.\sql\sql_daily_technicalIndicator_factor.sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'
        self.table_name = ['QT_DailyQuote']

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子
        for i in  range(len(self.target_methods)):
            factor_entities[self.target_methods[i]] = DailyTechnicalIndicatorFactor(factor_code=self.nameGroup[i],name=self.target_methods[i],describe='')

        return factor_entities

    def find_components(self, file_path, secucode, date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, self.table_name, secucode, date)
        components['QT_DailyQuote']  = components['QT_DailyQuote'].sort_values(by='TRADINGDAY') # 计算所需数据在这个表内

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:S
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['QT_DailyQuote'][['SECUCODE','TRADINGDAY']]) # 存储因子值
        cal_TI = TechnicalIndicatorFunc(components['QT_DailyQuote']['HIGHPRICE'],components['QT_DailyQuote']['LOWPRICE'],
                                        components['QT_DailyQuote']['CLOSEPRICE'],components['QT_DailyQuote']['OPENPRICE'],
                                        components['QT_DailyQuote']['TURNOVERVOLUME'])
        for i in self.target_methods:
            temp_str = 'cal_TI.'+i+'()'
            factor_values[i] = eval(temp_str)


        return factor_values



if __name__ == '__main__':
    pass

