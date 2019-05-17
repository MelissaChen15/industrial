# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

import pandas as pd

from factors.Category import CashFactor
from factors.Frequency import SeasonalFrequency
from factors.sql import pl_sql_oracle

"""
季频现金状况类因子

代码表：
    9001	SaleServiceCashToORTTM
    9002	CashRateOfSalesTTM
    9003	CapitalExpenditureToDM
    9004	CashEquivalentIncrease
    9005	NetOperateCashFlow
    9006	GoodsSaleServiceRenderCash
    9007	FreeCashFlow
    9008	NetProfitCashCover
    9009	OperatingRevenueCashCover
    9010	OperCashInToAsset


"""

class SeasonalCashFactor(SeasonalFrequency, CashFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频现金状况类因子'
        self.data_sql_file_path = r'.\sql\sql_seasonal_cash_factor.sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'
        self.table_name = ['LC_MainIndexNew']

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # SaleServiceCashToORTTM 销售商品提供劳务收到的现金/营业收入_TTM(%)
        SaleServiceCashToORTTM = SeasonalCashFactor(factor_code='9001',
                                                    name='SaleServiceCashToORTTM',
                                                    describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['SaleServiceCashToORTTM'] = SaleServiceCashToORTTM

        # CashRateOfSalesTTM 经营活动产生的现金流量净额/营业收入_TTM(%)
        CashRateOfSalesTTM = SeasonalCashFactor(factor_code='9002',
                                                name='CashRateOfSalesTTM',
                                                describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['CashRateOfSalesTTM'] = CashRateOfSalesTTM

        # CapitalExpenditureToDM 资本支出/折旧和摊销
        CapitalExpenditureToDM = SeasonalCashFactor(factor_code='9003',
                                                    name='CapitalExpenditureToDM',
                                                    describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['CapitalExpenditureToDM'] = CapitalExpenditureToDM

        # CashEquivalentIncrease 现金及现金等价物净增加额(元)
        CashEquivalentIncrease = SeasonalCashFactor(factor_code='9004',
                                                    name='CashEquivalentIncrease',
                                                    describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['CashEquivalentIncrease'] = CashEquivalentIncrease

        # NetOperateCashFlow 经营活动产生的现金流量净额(元)
        NetOperateCashFlow = SeasonalCashFactor(factor_code='9005',
                                                name='NetOperateCashFlow',
                                                describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NetOperateCashFlow'] = NetOperateCashFlow

        # GoodsSaleServiceRenderCash 销售商品提供劳务收到的现金(元)
        GoodsSaleServiceRenderCash = SeasonalCashFactor(factor_code='9006',
                                                        name='GoodsSaleServiceRenderCash',
                                                        describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['GoodsSaleServiceRenderCash'] = GoodsSaleServiceRenderCash

        # FreeCashFlow 自由现金流量(元)
        FreeCashFlow = SeasonalCashFactor(factor_code='9007',
                                          name='FreeCashFlow',
                                          describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['FreeCashFlow'] = FreeCashFlow

        # NetProfitCashCover 净利润现金含量(%)
        NetProfitCashCover = SeasonalCashFactor(factor_code='9008',
                                                name='NetProfitCashCover',
                                                describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NetProfitCashCover'] = NetProfitCashCover

        # OperatingRevenueCashCover 营业收入现金含量(%)
        OperatingRevenueCashCover = SeasonalCashFactor(factor_code='9009',
                                                       name='OperatingRevenueCashCover',
                                                       describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['OperatingRevenueCashCover'] = OperatingRevenueCashCover

        # OperCashInToAsset 总资产现金回收率(%)
        OperCashInToAsset = SeasonalCashFactor(factor_code='9010',
                                               name='OperCashInToAsset',
                                               describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['OperCashInToAsset'] = OperCashInToAsset

        return factor_entities

    def find_components(self, file_path,secucode, date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, self.table_name, secucode, date)

        components['LC_MainIndexNew']  = components['LC_MainIndexNew'].sort_values(by='ENDDATE')
        components['LC_MainIndexNew_monthly'] = self.seasonal_to_monthly(components['LC_MainIndexNew'],['SALESERVICECASHTOORTTM', 'CASHRATEOFSALESTTM', 'CAPITALEXPENDITURETODM', 'CASHEQUIVALENTINCREASE', 'NETOPERATECASHFLOW', 'GOODSSALESERVICERENDERCASH', 'FREECASHFLOW', 'NETPROFITCASHCOVER', 'OPERATINGREVENUECASHCOVER', 'OPERCASHINTOASSET'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值
        factor_values['SaleServiceCashToORTTM'] = components['LC_MainIndexNew_monthly']['SALESERVICECASHTOORTTM']
        factor_values['CashRateOfSalesTTM'] = components['LC_MainIndexNew_monthly']['CASHRATEOFSALESTTM']
        factor_values['CapitalExpenditureToDM'] = components['LC_MainIndexNew_monthly']['CAPITALEXPENDITURETODM']
        factor_values['CashEquivalentIncrease'] = components['LC_MainIndexNew_monthly']['CASHEQUIVALENTINCREASE']
        factor_values['NetOperateCashFlow'] = components['LC_MainIndexNew_monthly']['NETOPERATECASHFLOW']
        factor_values['GoodsSaleServiceRenderCash'] = components['LC_MainIndexNew_monthly']['GOODSSALESERVICERENDERCASH']
        factor_values['FreeCashFlow'] = components['LC_MainIndexNew_monthly']['FREECASHFLOW']
        factor_values['NetProfitCashCover'] = components['LC_MainIndexNew_monthly']['NETPROFITCASHCOVER']
        factor_values['OperatingRevenueCashCover'] = components['LC_MainIndexNew_monthly']['OPERATINGREVENUECASHCOVER']
        factor_values['OperCashInToAsset'] = components['LC_MainIndexNew_monthly']['OPERCASHINTOASSET']

        return factor_values


if __name__ == '__main__':
    # scf = SeasonalCashFactor()
    # scf.write_values_to_DB(mode = 'append',data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)
    pass
