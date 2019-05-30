# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

import pandas as pd

from factors.Category import DividendFactor
from factors.Frequency import SeasonalFrequency
from factors.sql import pl_sql_oracle

"""
季频分红能力类因子

代码表：
    1001	CashEquivalentPS
    1002	DividendPS
    1003	DividendCover
    1004	CashDividendCover
    1005	DividendPaidRatio
    1006	RetainedEarningRatio


"""

class SeasonalDividendFactor(SeasonalFrequency,DividendFactor ):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频分红能力类'
        self.table_name = ['LC_MainIndexNew']
        self.data_sql_file_path = r'.\sql\sql_seasonal_dividend_factor .sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # CashEquivalentPS 每股现金及现金等价物余额(元/股)
        CashEquivalentPS = SeasonalDividendFactor(factor_code='1401',
                                                  name='CashEquivalentPS',
                                                  describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['CashEquivalentPS'] = CashEquivalentPS

        # DividendPS 每股股利(元/股)
        DividendPS = SeasonalDividendFactor(factor_code='1402',
                                            name='DividendPS',
                                            describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['DividendPS'] = DividendPS

        # DividendCover 股利保障倍数(倍)
        DividendCover = SeasonalDividendFactor(factor_code='1403',
                                               name='DividendCover',
                                               describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['DividendCover'] = DividendCover

        # CashDividendCover 现金股利保障倍数(倍)
        CashDividendCover = SeasonalDividendFactor(factor_code='1404',
                                                   name='CashDividendCover',
                                                   describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['CashDividendCover'] = CashDividendCover

        # DividendPaidRatio 股利支付率(%)
        DividendPaidRatio = SeasonalDividendFactor(factor_code='1405',
                                                   name='DividendPaidRatio',
                                                   describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['DividendPaidRatio'] = DividendPaidRatio

        # RetainedEarningRatio 留存盈余比率(%)
        RetainedEarningRatio = SeasonalDividendFactor(factor_code='1406',
                                                      name='RetainedEarningRatio',
                                                      describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['RetainedEarningRatio'] = RetainedEarningRatio

        return factor_entities

    def find_components(self, file_path, secucode, date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, self.table_name, secucode, date)
        components['LC_MainIndexNew']  = components['LC_MainIndexNew'].sort_values(by='ENDDATE')
        components['LC_MainIndexNew_monthly'] = self.seasonal_to_monthly(components['LC_MainIndexNew'],['CASHEQUIVALENTPS', 'DIVIDENDPS', 'DIVIDENDCOVER', 'CASHDIVIDENDCOVER', 'DIVIDENDPAIDRATIO', 'RETAINEDEARNINGRATIO'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值
        factor_values['CashEquivalentPS'] = components['LC_MainIndexNew_monthly']['CASHEQUIVALENTPS']
        factor_values['DividendPS'] = components['LC_MainIndexNew_monthly']['DIVIDENDPS']
        factor_values['DividendCover'] = components['LC_MainIndexNew_monthly']['DIVIDENDCOVER']
        factor_values['CashDividendCover'] = components['LC_MainIndexNew_monthly']['CASHDIVIDENDCOVER']
        factor_values['DividendPaidRatio'] = components['LC_MainIndexNew_monthly']['DIVIDENDPAIDRATIO']
        factor_values['RetainedEarningRatio'] = components['LC_MainIndexNew_monthly']['RETAINEDEARNINGRATIO']

        return factor_values



if __name__ == '__main__':
    # sdf = SeasonalDividendFactor()
    # sdf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)
    pass

