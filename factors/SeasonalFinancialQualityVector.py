# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/11 13:17


from factors.Frequency import SeasonalFrequency
from factors.Category import FinancialQualityFactor
from factors.sql import pl_sql_oracle

import pandas as pd

"""
季频、财务质量类因子

代码表：

    0019	ROEAvg
    0020	ROA
    0021	GrossIncomeRatio
    0022	TotalProfitCostRatio
    0023	ROIC
    0024	OperatingNIToTP
    0025	DPtoP
    0026	CashRateOfSales
    0027	NOCFToOperatingNITTM
    0028	CurrentLiabilityToTL
    0029	CurrentRatio
    0030	TotalAssetTRate

"""

class SeasonalFinancialQualityFactor(SeasonalFrequency, FinancialQualityFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = 'seasonal financial quality factor'


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

        # ROEAvg	净资产收益率_平均,计算值(%)
        ROEAvg = SeasonalFinancialQualityFactor(factor_code='0019',
                                           name='ROEAvg',
                                           describe='净资产收益率_平均,计算值（ROEAvg）==（归属于母公司的净利润*2/（期初归属于母公司的股东权益+期末归属于母公司的股东权益））*100%')
        factor_entities['ROEAvg'] = ROEAvg
        factor_values['ROEAvg'] = components['LC_MainIndexNew']['ROEAVG']

        # ROA	总资产净利率(%)
        ROA = SeasonalFinancialQualityFactor(factor_code='0020',
                               name='ROA',
                               describe='总资产净利率（ROA）＝含少数股东损益的净利润*2/（期初总资产+期末总资产）*100%')
        factor_entities['ROA'] =ROA
        factor_values['ROA'] = components['LC_MainIndexNew']['ROA']

        # GrossIncomeRatio	销售毛利率(%)
        GrossIncomeRatio = SeasonalFinancialQualityFactor(factor_code='0021',
                               name='GrossIncomeRatio',
                               describe=' 销售毛利率（GrossIncomeRatio）＝（营业收入-营业成本）/营业收入*100%，金融类企业不计算。')
        factor_entities['GrossIncomeRatio'] =GrossIncomeRatio
        factor_values['GrossIncomeRatio'] = components['LC_MainIndexNew']['GROSSINCOMERATIO']

        # TotalProfitCostRatio	成本费用利润率
        TotalProfitCostRatio = SeasonalFinancialQualityFactor(factor_code='0022',
                               name='TotalProfitCostRatio',
                               describe='')
        factor_entities['TotalProfitCostRatio'] =TotalProfitCostRatio
        factor_values['TotalProfitCostRatio'] = components['LC_MainIndexNew']['TOTALPROFITCOSTRATIO']

        # ROIC	投入资本回报率(%)
        ROIC = SeasonalFinancialQualityFactor(factor_code='0023',
                               name='ROIC',
                               describe='投入资本回报率ROIC=（息税前利润*（1-所得税/利润总额）*2/（期初全部投入资本+期末全部投入资本））*100%其中，息税前利润=利润总额+(利息支出-利息收入)，若报表附注中未披露利息费用，则用“财务费用”代替；全部投入资本=归属于母公司的股东权益+短期借款+交易性金融负债+一年内到期的非流动负债+长期借款+应付债券，金融类企业不计算。')
        factor_entities['ROIC'] = ROIC
        factor_values['ROIC'] = components['LC_MainIndexNew']['ROIC']

        # OperatingNIToTP	 经营活动净收益/利润总额(%)
        OperatingNIToTP = SeasonalFinancialQualityFactor(factor_code='0024',
                               name='OperatingNIToTP',
                               describe='经营活动净收益／利润总额（OperatingNIToTP）＝经营活动净收益／利润总额*100%')
        factor_entities['OperatingNIToTP'] =OperatingNIToTP
        factor_values['OperatingNIToTP'] = components['LC_MainIndexNew']['OPERATINGNITOTP']

        # DPtoP	单季度扣非净利润/净利润
        DPtoP = SeasonalFinancialQualityFactor(factor_code='0025',
                               name='DPtoP',
                               describe='单季度扣非净利润/净利润')
        factor_entities['DPtoP'] =DPtoP
        factor_values['DPtoP'] = components['LC_MainIndexNew']['NETPROFITCUT'] / components['LC_MainIndexNew']['NETPROFIT']

        # CashRateOfSales	经营活动产生的现金流量净额/营业收入(%)
        CashRateOfSales = SeasonalFinancialQualityFactor(factor_code='0026',
                               name='CashRateOfSales',
                               describe='经营活动产生的现金流量净额/营业收入')
        factor_entities['CashRateOfSales'] = CashRateOfSales
        factor_values['CashRateOfSales'] = components['LC_MainIndexNew']['CASHRATEOFSALES']

        # NOCFToOperatingNITTM	经营活动产生的现金流量净额/经营活动净收益_TTM(%)
        NOCFToOperatingNITTM = SeasonalFinancialQualityFactor(factor_code='0027',
                               name='NOCFToOperatingNITTM',
                               describe='经营活动产生的现金流量净额/经营活动净收益（TTM）=经营活动产生的现金流量净额（TTM）/经营活动净收益（TTM）*100%，“经营活动净收益”的算法见 NOCFToOperatingNI[经营活动产生的现金流量净额/经营活动净收益（%）]。')
        factor_entities['NOCFToOperatingNITTM'] =NOCFToOperatingNITTM
        factor_values['NOCFToOperatingNITTM'] = components['LC_MainIndexNew']['NOCFTOOPERATINGNITTM']

        # CurrentLiabilityToTL	流动负债/负债合计(%)
        CurrentLiabilityToTL = SeasonalFinancialQualityFactor(factor_code='0028',
                               name='CurrentLiabilityToTL',
                               describe='LC_MainIndexNew')
        factor_entities['CurrentLiabilityToTL'] =CurrentLiabilityToTL
        factor_values['CurrentLiabilityToTL'] = components['LC_MainIndexNew']['CURRENTLIABILITYTOTL']

        # CurrentRatio	流动比率
        CurrentRatio = SeasonalFinancialQualityFactor(factor_code='0029',
                               name='CurrentRatio',
                               describe='流动比率（CurrentRatio）＝流动资产合计／流动负债合计，金融类企业不计算。')
        factor_entities['CurrentRatio'] =CurrentRatio
        factor_values['CurrentRatio'] = components['LC_MainIndexNew']['CURRENTRATIO']

        # TotalAssetTRate	总资产周转率(次)
        TotalAssetTRate = SeasonalFinancialQualityFactor(factor_code='0030',
                               name='TotalAssetTRate',
                               describe='总资产周转率（TotalAssetTRate）＝营业总收入*2/（期初资产合计+期末资产合计）')
        factor_entities['TotalAssetTRate'] =TotalAssetTRate
        factor_values['TotalAssetTRate'] = components['LC_MainIndexNew']['TOTALASSETTRATE']


        return factor_values, factor_entities




if __name__ == '__main__':
    sfqf = SeasonalFinancialQualityFactor(factor_code = '0019-0030', name = 'ROEAvg,ROA,GrossIncomeRatio,TotalProfitCostRatio,ROIC,OperatingNIToTP,DPtoP,CashRateOfSales,NOCFToOperatingNITTM,CurrentLiabilityToTL,CurrentRatio,TotalAssetTRate', describe = 'seasonal financial quality factor')
    sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_financial_quality_factor.sql'
    data = sfqf.find_components(file_path = sql_file_path, table_name = ['LC_MainIndexNew'])
    # print(data)
    factor_values, factor_entities = sfqf.get_factor_values(data)
    factor_list = sfqf.get_factor_list(factor_entities)
    print(factor_values)
    pd.set_option('display.max_columns', None)
    print(factor_list)

