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
    0001	PE
    0002	PELYR
    0003	PB
    0004	PCFTTM
    0005	PCFSTTM
    0006	PS
    0007	PSTTM
    0008	DividendRatio
    0009	TotalMV
    0010    PEG
"""

class DailyValueFactor(DailyFrequency, ValueFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = 'daily value factor'


    def find_components(self, file_path, table_name,secucode = ''):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, table_name, secucode )

        # TODO: 读取时需要按时间排序
        components['LC_MainIndexNew']  = components['LC_MainIndexNew'].sort_values(by='ENDDATE')
        components['LC_DIndicesForValuation'] = components['LC_DIndicesForValuation'].sort_values(by='TRADINGDAY')

        monthly_data = self.seasonal_to_monthly(components['LC_MainIndexNew'],['NETPROFITGROWRATE'])
        components['LC_MainIndexNew_daily'] = self.monthly_to_daily(monthly_data, components['LC_DIndicesForValuation'],['NETPROFITGROWRATE'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
            factor_entities： dict, 实例化的因子，可以用于获取因子的代码、名称、描述等数据
        """

        factor_values = pd.DataFrame(components['LC_DIndicesForValuation'][['SECUCODE','TRADINGDAY']]) # 存储因子值
        factor_entities = dict() # 存储实例化的因子

        # PE 滚动市盈率
        PE = DailyValueFactor(factor_code = '0001',
                                name = 'PE',
                                describe = '滚动市盈率（PE）＝股票市值/最近四个季度的净利润之和。其中，股票市值=A股价格×总股本')
        factor_entities['PE'] = PE
        factor_values['PE'] = components['LC_DIndicesForValuation']['PE']


        # PELYR 市盈率
        PELYR = DailyValueFactor(factor_code = '0002',
                                name = 'PELYR',
                                describe = '市盈率（PELYR）＝股票市值/去年净利润。其中，股票市值=A股价格×总股本')
        factor_entities['PELYR'] = PELYR
        factor_values['PELYR'] = components['LC_DIndicesForValuation']['PELYR']

        # PB 市净率
        PB = DailyValueFactor(factor_code='0003',
                                name='PB',
                                describe='市净率（PB）＝股票市值/净资产。其中，股票市值=A股价格×总股本；净资产为最新定期报告公布的净资产。')
        factor_entities['PB'] = PB
        factor_values['PB'] = components['LC_DIndicesForValuation']['PB']

        # PCFTTM 滚动市现率(经营现金流)
        PCFTTM = DailyValueFactor(factor_code='0004',
                            name='PCFTTM',
                            describe='滚动市现率（经营现金流）（PCFTTM）＝股票市值/最近四个季度的经营现金流量净额。其中，股票市值=A股价格×总股本。')
        factor_entities['PCFTTM'] = PCFTTM
        factor_values['PCFTTM'] = components['LC_DIndicesForValuation']['PCFTTM']

        # PCFSTTM 滚动市现率(现金流净额)
        PCFSTTM = DailyValueFactor(factor_code='0005',
                            name='PCFSTTM',
                            describe='滚动市现率（现金流净额）（PCFSTTM）＝股票市值/最近四个季度现金及现金等价物净增加额。其中，股票市值=A股价格×总股本。')
        factor_entities['PCFSTTM'] = PCFSTTM
        factor_values['PCFSTTM'] = components['LC_DIndicesForValuation']['PCFSTTM']

        # PS 市销率
        PS = DailyValueFactor(factor_code='0006',
                            name='PS',
                            describe='市销率（PS）＝股票市值/去年营业收入。')
        factor_entities['PS'] =PS
        factor_values['PS'] = components['LC_DIndicesForValuation']['PS']

        # PSTTM 滚动市销率
        PSTTM = DailyValueFactor(factor_code='0007',
                            name='PSTTM',
                            describe='滚动市销率（PSTTM）＝股票市值/最近四个季度的营业收入之和。其中，股票市值=A股价格×总股本。')
        factor_entities['PSTTM'] =PSTTM
        factor_values['PSTTM'] = components['LC_DIndicesForValuation']['PSTTM']

        # DividendRatio 滚动股息率
        DividendRatio = DailyValueFactor(factor_code='0008',
                            name='DividendRatio',
                            describe='滚动股息率（DividendRatio）＝公司派现合计/股票市值。其中，公司派现合计是指最近12个月的派现合计累计（整个公司的派现合计）其中，股票市值=A股价格×总股本。')
        factor_entities['DividendRatio'] = DividendRatio
        factor_values['DividendRatio'] = components['LC_DIndicesForValuation']['DIVIDENDRATIO']

        # TotalMV A股总市值
        TotalMV = DailyValueFactor(factor_code='0009',
                                name='TotalMV',
                                describe='A股总市值')
        factor_entities['TotalMV'] = TotalMV
        factor_values['TotalMV'] = components['LC_DIndicesForValuation']['TOTALMV']


        # PEG 市盈率增长率
        # 注意，此因子为日频数据/季频数据，分母取上个季度最后一天的数据
        PEG = DailyValueFactor(factor_code='0010',
                               name='PEG',
                               describe='市盈率增长率 = 市盈率(PE)/净利润同比增长率(NetProfitGrowRate)')
        factor_entities['PEG'] = PEG
        factor_values['PEG'] = components['LC_DIndicesForValuation']['PE'] / (components['LC_MainIndexNew_daily']['NETPROFITGROWRATE'])

        return factor_values, factor_entities

    def write_to_DB(self, code_sql_file_path,data_sql_file_path):
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(code_sql_file_path,['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path=data_sql_file_path,
                                           table_name=['LC_DIndicesForValuation', 'LC_MainIndexNew'],
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
                factor_values, factor_entities = self.get_factor_values(data)


                from sqlalchemy import String, Integer
                if row.Index == 0:
                    factor_list = self.get_factor_list(factor_entities)
                    pl_sql_oracle.df_to_DB(factor_list, 'factorlist', 'append',
                                           {'FactorCode': String(4), '简称': String(32), '频率': Integer(),
                                            '类别': String(64), '描述': String(512)})
                pl_sql_oracle.df_to_DB(factor_values, 'dailyvaluefactor','append',{'SECUCODE': String(20)})

                print(getattr(row, 'SECUCODE'),' done')


            except Exception as e:

                print(getattr(row, 'SECUCODE'), e)



if __name__ == '__main__':
    dvf = DailyValueFactor(factor_code = '0001-0009', name = 'PE,PELYR,PB,PCFTTM,PCFSTTM,PS,PSTTM,DividendRatio,TotalMV', describe = 'daily value factor')
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_daily_value_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    dvf.write_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)

