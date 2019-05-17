# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

import pandas as pd

from factors.Category import ProfitabilityFactor
from factors.Frequency import SeasonalFrequency
from factors.sql import pl_sql_oracle

"""
盈利能力类因子

代码表：
    7001	ROECut
    7002	ROA_EBITTTM
    7003	ROATTM
    7004	SalesCostRatio
    7005	PeriodCostsRateTTM
    7006	NPToTORTTM
    7007	OperatingProfitToTORTTM
    7008	EBITToTORTTM
    7009	TOperatingCostToTORTTM
    7010	OperatingExpenseRateTTM
    7011	AdminiExpenseRateTTM
    7012	FinancialExpenseRateTTM
    7013	AssetImpaLossToTORTTM
    7014	NetProfitCut
    7015	EBIT
    7016	EBITDA
    7017	OperatingProfitRatio
"""

class SeasonalProfitabilityFactor(SeasonalFrequency, ProfitabilityFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频盈利能力'
        self.data_sql_file_path = r'.\sql\sql_seasonal_profitability_factor.sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'
        self.table_name = ['LC_MainIndexNew']


    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # ROECut 净资产收益率_扣除,摊薄(%)
        ROECut = SeasonalProfitabilityFactor(factor_code='7001',
                                             name='ROECut',
                                             describe='净资产收益率_扣除,摊薄（ROECut）：直接取公司定期报告披露数据；若无披露值，则ROE（摊薄）=扣除非经常性损益后归属于母公司的净利润/该报告期期末归属于母公司的股东权益*100%。')
        factor_entities['ROECut'] = ROECut

        # ROA_EBITTTM 总资产报酬率_TTM(%)
        ROA_EBITTTM = SeasonalProfitabilityFactor(factor_code='7002',
                                                  name='ROA_EBITTTM',
                                                  describe='总资产报酬率_TTM（ROA_EBITTTM）＝息税前利润（TTM）/总资产（MRQ）*100%其中，息税前利润（TTM）＝利润总额（TTM）+利息费用（TTM）]，利息费用=利息支出（TTM）-利息收入（TTM），若报表附注中未披露利息费用，则用“财务费用”代替；金融类企业不计算。')
        factor_entities['ROA_EBITTTM'] = ROA_EBITTTM

        # ROATTM 总资产净利率_TTM(%)
        ROATTM = SeasonalProfitabilityFactor(factor_code='7003',
                                             name='ROATTM',
                                             describe='总资产净利率_TTM（ROATTM）＝含少数股东损益的净利润（TTM）/总资产（MRQ）*100%')
        factor_entities['ROATTM'] = ROATTM

        # SalesCostRatio 销售成本率(%)
        SalesCostRatio = SeasonalProfitabilityFactor(factor_code='7004',
                                                     name='SalesCostRatio',
                                                     describe='销售成本率（SalesCostRatio）＝营业成本/营业收入*100%，金融类企业不计算。')
        factor_entities['SalesCostRatio'] = SalesCostRatio

        # PeriodCostsRateTTM 销售期间费用率_TTM(%)
        PeriodCostsRateTTM = SeasonalProfitabilityFactor(factor_code='7005',
                                                         name='PeriodCostsRateTTM',
                                                         describe='销售成本率（SalesCostRatio）＝营业成本/营业收入*100%，金融类企业不计算。')
        factor_entities['PeriodCostsRateTTM'] = PeriodCostsRateTTM

        # NPToTORTTM 净利润/营业总收入_TTM(%)
        NPToTORTTM = SeasonalProfitabilityFactor(factor_code='7006',
                                                 name='NPToTORTTM',
                                                 describe='净利润／营业总收入_TTM（NPToTORTTM）＝净利润（TTM）／营业总收入（TTM）*100%')
        factor_entities['NPToTORTTM'] = NPToTORTTM

        # OperatingProfitToTORTTM 营业利润/营业总收入_TTM(%)
        OperatingProfitToTORTTM = SeasonalProfitabilityFactor(factor_code='7007',
                                                              name='OperatingProfitToTORTTM',
                                                              describe='营业利润／营业总收入_TTM（OperatingProfitToTORTTM）＝营业利润（TTM）／营业总收入（TTM）*100%')
        factor_entities['OperatingProfitToTORTTM'] = OperatingProfitToTORTTM

        # EBITToTORTTM 息税前利润/营业总收入_TTM(%)
        EBITToTORTTM = SeasonalProfitabilityFactor(factor_code='7008',
                                                   name='EBITToTORTTM',
                                                   describe='息税前利润／营业总收入_TTM（EBITToTORTTM）＝息税前利润（TTM）／营业总收入（TTM）*100%，金融类企业不计算。')
        factor_entities['EBITToTORTTM'] = EBITToTORTTM

        # TOperatingCostToTORTTM 营业总成本/营业总收入_TTM(%)
        TOperatingCostToTORTTM = SeasonalProfitabilityFactor(factor_code='7009',
                                                             name='TOperatingCostToTORTTM',
                                                             describe='营业总成本／营业总收入_TTM（TOperatingCostToTORTTM）＝营业总成本（TTM）／营业总收入（TTM）*100%，金融类企业不计算。')
        factor_entities['TOperatingCostToTORTTM'] = TOperatingCostToTORTTM

        # OperatingExpenseRateTTM 销售费用/营业总收入_TTM(%)
        OperatingExpenseRateTTM = SeasonalProfitabilityFactor(factor_code='7010',
                                                              name='OperatingExpenseRateTTM',
                                                              describe='销售费用／营业总收入_TTM（OperatingExpenseRateTTM）＝销售费用（TTM）／营业总收入（TTM）*100%，金融类企业不计算。')
        factor_entities['OperatingExpenseRateTTM'] = OperatingExpenseRateTTM

        # AdminiExpenseRateTTM 管理费用/营业总收入_TTM(%)
        AdminiExpenseRateTTM = SeasonalProfitabilityFactor(factor_code='7011',
                                                           name='AdminiExpenseRateTTM',
                                                           describe='管理费用／营业总收入_TTM（AdminiExpenseRateTTM）＝管理费用（TTM）／营业总收入（TTM）*100%，金融类企业不计算。')
        factor_entities['AdminiExpenseRateTTM'] = AdminiExpenseRateTTM

        # FinancialExpenseRateTTM 财务费用/营业总收入_TTM(%)
        FinancialExpenseRateTTM = SeasonalProfitabilityFactor(factor_code='7012',
                                                              name='FinancialExpenseRateTTM',
                                                              describe='财务费用／营业总收入_TTM（FinancialExpenseRateTTM）＝财务费用（TTM）／营业总收入（TTM）*100%，金融类企业不计算。')
        factor_entities['FinancialExpenseRateTTM'] = FinancialExpenseRateTTM

        # AssetImpaLossToTORTTM 资产减值损失/营业总收入_TTM(%)
        AssetImpaLossToTORTTM = SeasonalProfitabilityFactor(factor_code='7013',
                                                            name='AssetImpaLossToTORTTM',
                                                            describe='资产减值损失／营业总收入_TTM（AssetImpaLossToTORTTM）＝资产减值损失（TTM）／营业总收入（TTM）*100%')
        factor_entities['AssetImpaLossToTORTTM'] = AssetImpaLossToTORTTM

        # NetProfitCut 扣除非经常性损益后的净利润(元)
        NetProfitCut = SeasonalProfitabilityFactor(factor_code='7014',
                                                   name='NetProfitCut',
                                                   describe='扣除非经常性损益后的净利润（NetProfitCut）：取公布值。')
        factor_entities['NetProfitCut'] = NetProfitCut

        # EBIT 息税前利润(元)
        EBIT = SeasonalProfitabilityFactor(factor_code='7015',
                                           name='EBIT',
                                           describe='息税前利润（EBIT）＝利润总额+利息费用，其中，利息费用=利息支出-利息收入（若未披露利息费用，则用“财务费用”代替），金融类企业不计算该指标。')
        factor_entities['EBIT'] = EBIT

        # EBITDA 息税折旧摊销前利润(元)
        EBITDA = SeasonalProfitabilityFactor(factor_code='7016',
                                             name='EBITDA',
                                             describe='息税折旧摊销前利润（EBITDA）＝息税前利润EBIT+固定资产折旧+无形资产摊销+长期待摊费用摊销，金融类企业不计算该指标。')
        factor_entities['EBITDA'] = EBITDA

        # OperatingProfitRatio 营业利润率(%)
        OperatingProfitRatio = SeasonalProfitabilityFactor(factor_code='7017',
                                                           name='OperatingProfitRatio',
                                                           describe='营业利润率（OperatingProfitRatio）＝营业利润/营业收入*100%')
        factor_entities['OperatingProfitRatio'] = OperatingProfitRatio

        return factor_entities

    def find_components(self, file_path, secucode, date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, self.table_name, secucode, date )

        components['LC_MainIndexNew']  = components['LC_MainIndexNew'].sort_values(by='ENDDATE')
        components['LC_MainIndexNew_monthly'] = self.seasonal_to_monthly(components['LC_MainIndexNew'],['ROECUT', 'ROA_EBITTTM', 'ROATTM', 'SALESCOSTRATIO', 'PERIODCOSTSRATETTM', 'NPTOTORTTM', 'OPERATINGPROFITTOTORTTM', 'EBITTOTORTTM', 'TOPERATINGCOSTTOTORTTM', 'OPERATINGEXPENSERATETTM', 'ADMINIEXPENSERATETTM', 'FINANCIALEXPENSERATETTM', 'ASSETIMPALOSSTOTORTTM', 'NETPROFITCUT', 'EBIT', 'EBITDA', 'OPERATINGPROFITRATIO'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值

        factor_values['ROECut'] = components['LC_MainIndexNew_monthly']['ROECUT']
        factor_values['ROA_EBITTTM'] = components['LC_MainIndexNew_monthly']['ROA_EBITTTM']
        factor_values['ROATTM'] = components['LC_MainIndexNew_monthly']['ROATTM']
        factor_values['SalesCostRatio'] = components['LC_MainIndexNew_monthly']['SALESCOSTRATIO']
        factor_values['PeriodCostsRateTTM'] = components['LC_MainIndexNew_monthly']['PERIODCOSTSRATETTM']
        factor_values['NPToTORTTM'] = components['LC_MainIndexNew_monthly']['NPTOTORTTM']
        factor_values['OperatingProfitToTORTTM'] = components['LC_MainIndexNew_monthly']['OPERATINGPROFITTOTORTTM']
        factor_values['EBITToTORTTM'] = components['LC_MainIndexNew_monthly']['EBITTOTORTTM']
        factor_values['TOperatingCostToTORTTM'] = components['LC_MainIndexNew_monthly']['TOPERATINGCOSTTOTORTTM']
        factor_values['OperatingExpenseRateTTM'] = components['LC_MainIndexNew_monthly']['OPERATINGEXPENSERATETTM']
        factor_values['AdminiExpenseRateTTM'] = components['LC_MainIndexNew_monthly']['ADMINIEXPENSERATETTM']
        factor_values['FinancialExpenseRateTTM'] = components['LC_MainIndexNew_monthly']['FINANCIALEXPENSERATETTM']
        factor_values['AssetImpaLossToTORTTM'] = components['LC_MainIndexNew_monthly']['ASSETIMPALOSSTOTORTTM']
        factor_values['NetProfitCut'] = components['LC_MainIndexNew_monthly']['NETPROFITCUT']
        factor_values['EBIT'] = components['LC_MainIndexNew_monthly']['EBIT']
        factor_values['EBITDA'] = components['LC_MainIndexNew_monthly']['EBITDA']
        factor_values['OperatingProfitRatio'] = components['LC_MainIndexNew_monthly']['OPERATINGPROFITRATIO']

        return factor_values




if __name__ == '__main__':
    pass
    # spf = SeasonalProfitabilityFactor()
    # data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_profitability_factor.sql'
    # code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'

