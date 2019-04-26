# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

from factors.Frequency import SeasonalFrequency
from factors.Category import CapitalStructureFactor
from factors.sql import pl_sql_oracle

import pandas as pd

"""
季频资本结构类因子

代码表：
    1101	DebtAssetsRatio
    1102	CurrentAssetsToTA
    1103	NonCurrentAssetsToTA
    1104	FixAssetRatio
    1105	IntangibleAssetRatio
    1106	LongDebtToAsset
    1107	BondsPayableToAsset
    1108	SEWithoutMIToTotalCapital
    1109	InteBearDebtToTotalCapital
    1110	NonCurrentLiabilityToTL
    1111	EquityToAsset
    1112	EquityMultipler
    1113	WorkingCapital
    1114	LongDebtToEquity
    1115	LongAssetFitRate


"""

class SeasonalCapitalStructureFactor(SeasonalFrequency, CapitalStructureFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频资本结构类'

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # DebtAssetsRatio 资产负债率(%)
        DebtAssetsRatio = SeasonalCapitalStructureFactor(factor_code='1101',
                                                         name='DebtAssetsRatio',
                                                         describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['DebtAssetsRatio'] = DebtAssetsRatio

        # CurrentAssetsToTA 流动资产/总资产(%)
        CurrentAssetsToTA = SeasonalCapitalStructureFactor(factor_code='1102',
                                                           name='CurrentAssetsToTA',
                                                           describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['CurrentAssetsToTA'] = CurrentAssetsToTA

        # NonCurrentAssetsToTA 非流动资产/总资产(%)
        NonCurrentAssetsToTA = SeasonalCapitalStructureFactor(factor_code='1103',
                                                              name='NonCurrentAssetsToTA',
                                                              describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NonCurrentAssetsToTA'] = NonCurrentAssetsToTA

        # FixAssetRatio 固定资产比率(%)
        FixAssetRatio = SeasonalCapitalStructureFactor(factor_code='1104',
                                                       name='FixAssetRatio',
                                                       describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['FixAssetRatio'] = FixAssetRatio

        # IntangibleAssetRatio 无形资产比率(%)
        IntangibleAssetRatio = SeasonalCapitalStructureFactor(factor_code='1105',
                                                              name='IntangibleAssetRatio',
                                                              describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['IntangibleAssetRatio'] = IntangibleAssetRatio

        # LongDebtToAsset 长期借款/总资产(%)
        LongDebtToAsset = SeasonalCapitalStructureFactor(factor_code='1106',
                                                         name='LongDebtToAsset',
                                                         describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['LongDebtToAsset'] = LongDebtToAsset

        # BondsPayableToAsset 应付债券/总资产(%)
        BondsPayableToAsset = SeasonalCapitalStructureFactor(factor_code='1107',
                                                             name='BondsPayableToAsset',
                                                             describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['BondsPayableToAsset'] = BondsPayableToAsset

        # SEWithoutMIToTotalCapital 归属母公司股东的权益/全部投入资本(%)
        SEWithoutMIToTotalCapital = SeasonalCapitalStructureFactor(factor_code='1108',
                                                                   name='SEWithoutMIToTotalCapital',
                                                                   describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['SEWithoutMIToTotalCapital'] = SEWithoutMIToTotalCapital

        # InteBearDebtToTotalCapital 带息债务/全部投入资本(%)
        InteBearDebtToTotalCapital = SeasonalCapitalStructureFactor(factor_code='1109',
                                                                    name='InteBearDebtToTotalCapital',
                                                                    describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['InteBearDebtToTotalCapital'] = InteBearDebtToTotalCapital

        # NonCurrentLiabilityToTL 非流动负债/负债合计(%)
        NonCurrentLiabilityToTL = SeasonalCapitalStructureFactor(factor_code='1110',
                                                                 name='NonCurrentLiabilityToTL',
                                                                 describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NonCurrentLiabilityToTL'] = NonCurrentLiabilityToTL

        # EquityToAsset 股东权益比率(%)
        EquityToAsset = SeasonalCapitalStructureFactor(factor_code='1111',
                                                       name='EquityToAsset',
                                                       describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['EquityToAsset'] = EquityToAsset

        # EquityMultipler 权益乘数(%)
        EquityMultipler = SeasonalCapitalStructureFactor(factor_code='1112',
                                                         name='EquityMultipler',
                                                         describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['EquityMultipler'] = EquityMultipler

        # WorkingCapital 营运资金(元)
        WorkingCapital = SeasonalCapitalStructureFactor(factor_code='1113',
                                                        name='WorkingCapital',
                                                        describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['WorkingCapital'] = WorkingCapital

        # LongDebtToEquity 长期负债/股东权益合计
        LongDebtToEquity = SeasonalCapitalStructureFactor(factor_code='1114',
                                                          name='LongDebtToEquity',
                                                          describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['LongDebtToEquity'] = LongDebtToEquity

        # LongAssetFitRate 长期资产适合率
        LongAssetFitRate = SeasonalCapitalStructureFactor(factor_code='1115',
                                                          name='LongAssetFitRate',
                                                          describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['LongAssetFitRate'] = LongAssetFitRate

        return factor_entities

    def find_components(self, file_path, table_name,secucode = ''):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, table_name, secucode )

        # TODO: 读取时需要按时间排序
        components['LC_MainIndexNew'] = components['LC_MainIndexNew'].sort_values(by='ENDDATE')
        # 如果需要转换
        components['LC_MainIndexNew_monthly'] = self.seasonal_to_monthly(components['LC_MainIndexNew'],['DEBTASSETSRATIO', 'CURRENTASSETSTOTA', 'NONCURRENTASSETSTOTA', 'FIXASSETRATIO', 'INTANGIBLEASSETRATIO', 'LONGDEBTTOASSET', 'BONDSPAYABLETOASSET', 'SEWITHOUTMITOTOTALCAPITAL', 'INTEBEARDEBTTOTOTALCAPITAL', 'NONCURRENTLIABILITYTOTL', 'EQUITYTOASSET', 'EQUITYMULTIPLER', 'WORKINGCAPITAL', 'LONGDEBTTOEQUITY', 'LONGASSETFITRATE'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值
        factor_values['DebtAssetsRatio'] = components['LC_MainIndexNew_monthly']['DEBTASSETSRATIO']
        factor_values['CurrentAssetsToTA'] = components['LC_MainIndexNew_monthly']['CURRENTASSETSTOTA']
        factor_values['NonCurrentAssetsToTA'] = components['LC_MainIndexNew_monthly']['NONCURRENTASSETSTOTA']
        factor_values['FixAssetRatio'] = components['LC_MainIndexNew_monthly']['FIXASSETRATIO']
        factor_values['IntangibleAssetRatio'] = components['LC_MainIndexNew_monthly']['INTANGIBLEASSETRATIO']
        factor_values['LongDebtToAsset'] = components['LC_MainIndexNew_monthly']['LONGDEBTTOASSET']
        factor_values['BondsPayableToAsset'] = components['LC_MainIndexNew_monthly']['BONDSPAYABLETOASSET']
        factor_values['SEWithoutMIToTotalCapital'] = components['LC_MainIndexNew_monthly']['SEWITHOUTMITOTOTALCAPITAL']
        factor_values['InteBearDebtToTotalCapital'] = components['LC_MainIndexNew_monthly'][
            'INTEBEARDEBTTOTOTALCAPITAL']
        factor_values['NonCurrentLiabilityToTL'] = components['LC_MainIndexNew_monthly']['NONCURRENTLIABILITYTOTL']
        factor_values['EquityToAsset'] = components['LC_MainIndexNew_monthly']['EQUITYTOASSET']
        factor_values['EquityMultipler'] = components['LC_MainIndexNew_monthly']['EQUITYMULTIPLER']
        factor_values['WorkingCapital'] = components['LC_MainIndexNew_monthly']['WORKINGCAPITAL']
        factor_values['LongDebtToEquity'] = components['LC_MainIndexNew_monthly']['LONGDEBTTOEQUITY']
        factor_values['LongAssetFitRate'] = components['LC_MainIndexNew_monthly']['LONGASSETFITRATE']

        return factor_values



    def write_values_to_DB(self,mode,  code_sql_file_path, data_sql_file_path):
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(code_sql_file_path,
                                            ['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path= data_sql_file_path,
                                           table_name=['LC_MainIndexNew'],
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
                factor_values = self.get_factor_values(data)


                from sqlalchemy import String, Integer
                # print(factor_values)
                pl_sql_oracle.df_to_DB(factor_values,'seasonalcapitalstructurefactor',if_exists= mode,data_type={'SECUCODE': String(20)})

                print(getattr(row, 'SECUCODE'),' done')


            except Exception as e:
                print('write to database failed, error:',getattr(row, 'SECUCODE'), e)



if __name__ == '__main__':
    scsf = SeasonalCapitalStructureFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_capital_structure_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    scsf.write_values_to_DB(mode = 'append',data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)

    # # 修改报错：
    # # 000008 x and y arrays must have at least 2 entries
    # sql = pl_sql_oracle.dbData_import()
    # s = sql.InputDataPreprocess(code_sql_file_path, ['secucodes'])
    # data = scsf.find_components(file_path=data_sql_file_path,
    #                            table_name=['LC_MainIndexNew'],
    #                            secucode='and t2.Secucode = \'000008\'')
    # factor_values = scsf.get_factor_values(data)
    # print(factor_values)

