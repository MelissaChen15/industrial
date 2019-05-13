# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

from factors.Frequency import DailyFrequency
from factors.Category import ValueFactor
from factors.sql import pl_sql_oracle

import pandas as pd

"""
日频、价值类因子

代码表：
    1001	PE
    1002	PELYR
    1003	PB
    1004	PCFTTM
    1005	PCFSTTM
    1006	PS
    1007	PSTTM
    1008	DividendRatio
    1009	TotalMV
    
    1010	PEG  特殊处理, 见文件DailyDivideSeasonalFactor
"""

class DailyValueFactor(DailyFrequency, ValueFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '日频价值类'
        self.data_sql_file_path = r'.\sql\sql_daily_value_factor.sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'
        self.table_name = ['LC_DIndicesForVaaluation']

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # PE 滚动市盈率
        PE = DailyValueFactor(factor_code='1001',
                              name='PE',
                              describe='滚动市盈率（PE）＝股票市值/最近四个季度的净利润之和。其中，股票市值=A股价格×总股本')
        factor_entities['PE'] = PE

        # PELYR 市盈率
        PELYR = DailyValueFactor(factor_code='1002',
                                 name='PELYR',
                                 describe='市盈率（PELYR）＝股票市值/去年净利润。其中，股票市值=A股价格×总股本')
        factor_entities['PELYR'] = PELYR

        # PB 市净率
        PB = DailyValueFactor(factor_code='1003',
                              name='PB',
                              describe='市净率（PB）＝股票市值/净资产。其中，股票市值=A股价格×总股本；净资产为最新定期报告公布的净资产。')
        factor_entities['PB'] = PB

        # PCFTTM 滚动市现率(经营现金流)
        PCFTTM = DailyValueFactor(factor_code='1004',
                                  name='PCFTTM',
                                  describe='滚动市现率（经营现金流）（PCFTTM）＝股票市值/最近四个季度的经营现金流量净额。其中，股票市值=A股价格×总股本。')
        factor_entities['PCFTTM'] = PCFTTM

        # PCFSTTM 滚动市现率(现金流净额)
        PCFSTTM = DailyValueFactor(factor_code='1005',
                                   name='PCFSTTM',
                                   describe='滚动市现率（现金流净额）（PCFSTTM）＝股票市值/最近四个季度现金及现金等价物净增加额。其中，股票市值=A股价格×总股本。')
        factor_entities['PCFSTTM'] = PCFSTTM

        # PS 市销率
        PS = DailyValueFactor(factor_code='1006',
                              name='PS',
                              describe='市销率（PS）＝股票市值/去年营业收入。')
        factor_entities['PS'] = PS

        # PSTTM 滚动市销率
        PSTTM = DailyValueFactor(factor_code='1007',
                                 name='PSTTM',
                                 describe='滚动市销率（PSTTM）＝股票市值/最近四个季度的营业收入之和。其中，股票市值=A股价格×总股本。')
        factor_entities['PSTTM'] = PSTTM

        # DividendRatio 滚动股息率
        DividendRatio = DailyValueFactor(factor_code='1008',
                                         name='DividendRatio',
                                         describe='滚动股息率（DividendRatio）＝公司派现合计/股票市值。其中，公司派现合计是指最近12个月的派现合计累计（整个公司的派现合计）其中，股票市值=A股价格×总股本。')
        factor_entities['DividendRatio'] = DividendRatio

        # TotalMV A股总市值
        TotalMV = DailyValueFactor(factor_code='1009',
                                   name='TotalMV',
                                   describe='A股总市值')
        factor_entities['TotalMV'] = TotalMV


        return factor_entities

    def find_components(self, file_path,secucode,date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(filepath=file_path, table_name = self.table_name, secucode = secucode,date=date)

        # TODO: 需要按时间排序
        components['LC_DIndicesForValuation'] = components['LC_DIndicesForValuation'].sort_values(by='TRADINGDAY')


        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """
        factor_values = pd.DataFrame(components['LC_DIndicesForValuation'][['SECUCODE', 'TRADINGDAY']])  # 存储因子值
        factor_values['PE'] = components['LC_DIndicesForValuation']['PE']
        factor_values['PELYR'] = components['LC_DIndicesForValuation']['PELYR']
        factor_values['PB'] = components['LC_DIndicesForValuation']['PB']
        factor_values['PCFTTM'] = components['LC_DIndicesForValuation']['PCFTTM']
        factor_values['PCFSTTM'] = components['LC_DIndicesForValuation']['PCFSTTM']
        factor_values['PS'] = components['LC_DIndicesForValuation']['PS']
        factor_values['PSTTM'] = components['LC_DIndicesForValuation']['PSTTM']
        factor_values['DividendRatio'] = components['LC_DIndicesForValuation']['DIVIDENDRATIO']
        factor_values['TotalMV'] = components['LC_DIndicesForValuation']['TOTALMV']

        return factor_values


if __name__ == '__main__':
    pass

