# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

import pandas as pd

from factors.Category import OperatingFactor
from factors.Frequency import SeasonalFrequency
from factors.sql import pl_sql_oracle

"""
季频营运能力类因子

代码表：
    8001	OperCycle
    8002	InventoryTRate
    8003	InventoryTDays
    8004	ARTRate
    8005	ARTDays
    8006	AccountsPayablesTRate
    8007	AccountsPayablesTDays
    8008	CurrentAssetsTRate
    8009	FixedAssetTRate
    8010	EquityTRate


"""

class SeasonalOperatingFactor(SeasonalFrequency, OperatingFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频营运能力类'
        self.data_sql_file_path = r'.\sql\sql_seasonal_operating_factor.sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'
        self.table_name = ['LC_MainIndexNew']

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # OperCycle 营业周期(天/次)
        OperCycle = SeasonalOperatingFactor(factor_code='8001',
                                            name='OperCycle',
                                            describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['OperCycle'] = OperCycle

        # InventoryTRate 存货周转率(次)
        InventoryTRate = SeasonalOperatingFactor(factor_code='8002',
                                                 name='InventoryTRate',
                                                 describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['InventoryTRate'] = InventoryTRate

        # InventoryTDays 存货周转天数(天/次)
        InventoryTDays = SeasonalOperatingFactor(factor_code='8003',
                                                 name='InventoryTDays',
                                                 describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['InventoryTDays'] = InventoryTDays

        # ARTRate 应收账款周转率(次)
        ARTRate = SeasonalOperatingFactor(factor_code='8004',
                                          name='ARTRate',
                                          describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['ARTRate'] = ARTRate

        # ARTDays 应收账款周转天数(天/次)
        ARTDays = SeasonalOperatingFactor(factor_code='8005',
                                          name='ARTDays',
                                          describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['ARTDays'] = ARTDays

        # AccountsPayablesTRate 应付账款周转率(次)
        AccountsPayablesTRate = SeasonalOperatingFactor(factor_code='8006',
                                                        name='AccountsPayablesTRate',
                                                        describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['AccountsPayablesTRate'] = AccountsPayablesTRate

        # AccountsPayablesTDays 应付账款周转天数(天/次)
        AccountsPayablesTDays = SeasonalOperatingFactor(factor_code='8007',
                                                        name='AccountsPayablesTDays',
                                                        describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['AccountsPayablesTDays'] = AccountsPayablesTDays

        # CurrentAssetsTRate 流动资产周转率(次)
        CurrentAssetsTRate = SeasonalOperatingFactor(factor_code='8008',
                                                     name='CurrentAssetsTRate',
                                                     describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['CurrentAssetsTRate'] = CurrentAssetsTRate

        # FixedAssetTRate 固定资产周转率(次)
        FixedAssetTRate = SeasonalOperatingFactor(factor_code='8009',
                                                  name='FixedAssetTRate',
                                                  describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['FixedAssetTRate'] = FixedAssetTRate

        # EquityTRate 股东权益周转率(次)
        EquityTRate = SeasonalOperatingFactor(factor_code='8010',
                                              name='EquityTRate',
                                              describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['EquityTRate'] = EquityTRate

        return factor_entities

    def find_components(self, file_path,secucode, date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, self.table_name, secucode, date )

        components['LC_MainIndexNew']  = components['LC_MainIndexNew'].sort_values(by='ENDDATE')
        components['LC_MainIndexNew_monthly'] = self.seasonal_to_monthly(components['LC_MainIndexNew'],['OPERCYCLE', 'INVENTORYTRATE', 'INVENTORYTDAYS', 'ARTRATE', 'ARTDAYS', 'ACCOUNTSPAYABLESTRATE', 'ACCOUNTSPAYABLESTDAYS', 'CURRENTASSETSTRATE', 'FIXEDASSETTRATE', 'EQUITYTRATE'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值
        factor_values['OperCycle'] = components['LC_MainIndexNew_monthly']['OPERCYCLE']
        factor_values['InventoryTRate'] = components['LC_MainIndexNew_monthly']['INVENTORYTRATE']
        factor_values['InventoryTDays'] = components['LC_MainIndexNew_monthly']['INVENTORYTDAYS']
        factor_values['ARTRate'] = components['LC_MainIndexNew_monthly']['ARTRATE']
        factor_values['ARTDays'] = components['LC_MainIndexNew_monthly']['ARTDAYS']
        factor_values['AccountsPayablesTRate'] = components['LC_MainIndexNew_monthly']['ACCOUNTSPAYABLESTRATE']
        factor_values['AccountsPayablesTDays'] = components['LC_MainIndexNew_monthly']['ACCOUNTSPAYABLESTDAYS']
        factor_values['CurrentAssetsTRate'] = components['LC_MainIndexNew_monthly']['CURRENTASSETSTRATE']
        factor_values['FixedAssetTRate'] = components['LC_MainIndexNew_monthly']['FIXEDASSETTRATE']
        factor_values['EquityTRate'] = components['LC_MainIndexNew_monthly']['EQUITYTRATE']

        return factor_values


if __name__ == '__main__':
    pass

