# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/11 13:17


from factors.Frequency import SeasonalFrequency
from factors.Category import GrowthFactor
from factors.sql import pl_sql_oracle

import pandas as pd

"""
季频、成长类因子

代码表：
    0013	NetProfitGrowRate
    0014	ROETTM
    0015	TotalAssetGrowRate
    0016	BasicEPSYOY
    0017	GrossIncomeRatioTTM
    0018	NetProfitRatioTTM


"""

class SeasonalGrowthFactor(SeasonalFrequency, GrowthFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = 'seasonal growth vector'


    def find_components(self, file_path, table_name):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, table_name)

        return components




    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
            factor_entities： dict, 实例化的因子，可以用于获取因子的代码、名称、描述等数据
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew'][['SECUCODE','ENDDATE']]) # 存储因子值
        factor_entities = dict() # 存储实例化的因子

        # NetProfitGrowRate	净利润同比增长(%)
        NetProfitGrowRate = SeasonalGrowthFactor(factor_code='0013',
                                           name='NetProfitGrowRate',
                                           describe='（本期数据－去年同期数据）/︱去年同期数据︱*100%')
        factor_entities['NetProfitGrowRate'] =NetProfitGrowRate
        factor_values['NetProfitGrowRate'] = components['LC_MainIndexNew']['NETPROFITGROWRATE']



        # ROETTM 净资产收益率(摊薄)(%)
        ROETTM = SeasonalGrowthFactor(factor_code='0014',
                                           name='ROETTM',
                                           describe='净资产收益率_TTM（ROETTM）＝（归属于母公司的净利润（TTM）*2/（期初归属于母公司的股东权益+期末归属于母公司的股东权益）*100%')
        factor_entities['ROETTM'] = ROETTM
        factor_values['ROETTM'] = components['LC_MainIndexNew']['ROETTM']



        # TotalAssetGrowRate	总资产同比增长(%)
        TotalAssetGrowRate = SeasonalGrowthFactor(factor_code='0015',
                                           name='TotalAssetGrowRate',
                                           describe='（本期数据－去年同期数据）/︱去年同期数据︱*100%')
        factor_entities['TotalAssetGrowRate'] =TotalAssetGrowRate
        factor_values['TotalAssetGrowRate'] = components['LC_MainIndexNew']['TOTALASSETGROWRATE']



        # BasicEPSYOY	基本每股收益同比增长(%)
        BasicEPSYOY = SeasonalGrowthFactor(factor_code='0016',
                                           name='BasicEPSYOY',
                                           describe='')
        factor_entities['BasicEPSYOY'] = BasicEPSYOY
        factor_values['BasicEPSYOY'] = components['LC_MainIndexNew']['BASICEPSYOY']



        # GrossIncomeRatioTTM	销售毛利率_TTM(%)
        GrossIncomeRatioTTM = SeasonalGrowthFactor(factor_code='0017',
                                           name='GrossIncomeRatioTTM',
                                           describe='销售毛利率_TTM（GrossIncomeRatioTTM）＝[营业收入（TTM）-营业成本（TTM）]/营业收入（TTM）*100%，金融类企业不计算。')
        factor_entities['GrossIncomeRatioTTM'] = GrossIncomeRatioTTM
        factor_values['GrossIncomeRatioTTM'] = components['LC_MainIndexNew']['GROSSINCOMERATIOTTM']



        # NetProfitRatioTTM	销售净利率_TTM(%)
        NetProfitRatioTTM = SeasonalGrowthFactor(factor_code='0018',
                                           name='NetProfitRatioTTM',
                                           describe='销售净利率_TTM（NetProfitRatioTTM）＝含少数股东损益的净利润（TTM）/营业收入（TTM）*100%')
        factor_entities['NetProfitRatioTTM'] =NetProfitRatioTTM
        factor_values['NetProfitRatioTTM'] = components['LC_MainIndexNew']['NETPROFITRATIOTTM']


        return factor_values, factor_entities



if __name__ == '__main__':
    sgv = SeasonalGrowthFactor(factor_code = '0013-0018', name = 'NetProfitGrowRate,ROETTM,TotalAssetGrowRate,BasicEPSYOY,GrossIncomeRatioTTM,NetProfitRatioTTM', describe = 'seasonal growth vector')
    sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_growth_factor.sql'
    data = sgv.find_components(file_path = sql_file_path, table_name = ['LC_MainIndexNew'])
    # print(data)
    factor_values, factor_entities =sgv .get_factor_values(data)
    factor_list =sgv .get_factor_list(factor_entities)
    print(factor_values)
    pd.set_option('display.max_columns', None)
    print(factor_list)

