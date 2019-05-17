# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

import pandas as pd

from factors.Category import EarningQualityFactor
from factors.Frequency import SeasonalFrequency
from factors.sql import pl_sql_oracle

"""
季频收益质量类因子

代码表：
    1201	OperatingMIToTPTTM
    1202	InvestRAssociatesToTP
    1203	InvestRAssociatesToTPTTM
    1204	ValueChangeNIToTP
    1205	ValueChangeNIToTPTTM
    1206	NetNonOperatingIncomeToTP
    1207	NetNonOIToTPTTM
    1208	TaxesToTP
    1209	NPCutToTP


"""

class SeasonalEarningQualityFactor(SeasonalFrequency, EarningQualityFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频收益质量类'
        self.table_name = ['LC_MainIndexNew']
        self.data_sql_file_path = r'.\sql\sql_seasonal_earning_quality_factor.sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'


    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # OperatingMIToTPTTM 经营活动净收益/利润总额_TTM(%)
        OperatingMIToTPTTM = SeasonalEarningQualityFactor(factor_code='1201',
                                                          name='OperatingMIToTPTTM',
                                                          describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['OperatingMIToTPTTM'] = OperatingMIToTPTTM

        # InvestRAssociatesToTP 对联营合营公司投资收益/利润总额(%)
        InvestRAssociatesToTP = SeasonalEarningQualityFactor(factor_code='1202',
                                                             name='InvestRAssociatesToTP',
                                                             describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['InvestRAssociatesToTP'] = InvestRAssociatesToTP

        # InvestRAssociatesToTPTTM 对联营合营公司投资收益/利润总额_TTM(%)
        InvestRAssociatesToTPTTM = SeasonalEarningQualityFactor(factor_code='1203',
                                                                name='InvestRAssociatesToTPTTM',
                                                                describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['InvestRAssociatesToTPTTM'] = InvestRAssociatesToTPTTM

        # ValueChangeNIToTP 价值变动净收益/利润总额(%)
        ValueChangeNIToTP = SeasonalEarningQualityFactor(factor_code='1204',
                                                         name='ValueChangeNIToTP',
                                                         describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['ValueChangeNIToTP'] = ValueChangeNIToTP

        # ValueChangeNIToTPTTM 价值变动净收益/利润总额_TTM(%)
        ValueChangeNIToTPTTM = SeasonalEarningQualityFactor(factor_code='1205',
                                                            name='ValueChangeNIToTPTTM',
                                                            describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['ValueChangeNIToTPTTM'] = ValueChangeNIToTPTTM

        # NetNonOperatingIncomeToTP 营业外收支净额/利润总额(%)
        NetNonOperatingIncomeToTP = SeasonalEarningQualityFactor(factor_code='1206',
                                                                 name='NetNonOperatingIncomeToTP',
                                                                 describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NetNonOperatingIncomeToTP'] = NetNonOperatingIncomeToTP

        # NetNonOIToTPTTM 营业外收支净额/利润总额_TTM(%)
        NetNonOIToTPTTM = SeasonalEarningQualityFactor(factor_code='1207',
                                                       name='NetNonOIToTPTTM',
                                                       describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NetNonOIToTPTTM'] = NetNonOIToTPTTM

        # TaxesToTP 所得税/利润总额(%)
        TaxesToTP = SeasonalEarningQualityFactor(factor_code='1208',
                                                 name='TaxesToTP',
                                                 describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['TaxesToTP'] = TaxesToTP

        # NPCutToTP 扣除非经常损益后的净利润/净利润(%)
        NPCutToTP = SeasonalEarningQualityFactor(factor_code='1209',
                                                 name='NPCutToTP',
                                                 describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NPCutToTP'] = NPCutToTP

        return factor_entities

    def find_components(self, file_path, secucode, date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, self.table_name, secucode,date)

        components['LC_MainIndexNew']  = components['LC_MainIndexNew'].sort_values(by='ENDDATE')
        components['LC_MainIndexNew_monthly'] = self.seasonal_to_monthly(components['LC_MainIndexNew'],['OPERATINGMITOTPTTM', 'INVESTRASSOCIATESTOTP', 'INVESTRASSOCIATESTOTPTTM', 'VALUECHANGENITOTP', 'VALUECHANGENITOTPTTM', 'NETNONOPERATINGINCOMETOTP', 'NETNONOITOTPTTM', 'TAXESTOTP', 'NPCUTTOTP'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值
        factor_values['OperatingMIToTPTTM'] = components['LC_MainIndexNew_monthly']['OPERATINGMITOTPTTM']
        factor_values['InvestRAssociatesToTP'] = components['LC_MainIndexNew_monthly']['INVESTRASSOCIATESTOTP']
        factor_values['InvestRAssociatesToTPTTM'] = components['LC_MainIndexNew_monthly']['INVESTRASSOCIATESTOTPTTM']
        factor_values['ValueChangeNIToTP'] = components['LC_MainIndexNew_monthly']['VALUECHANGENITOTP']
        factor_values['ValueChangeNIToTPTTM'] = components['LC_MainIndexNew_monthly']['VALUECHANGENITOTPTTM']
        factor_values['NetNonOperatingIncomeToTP'] = components['LC_MainIndexNew_monthly']['NETNONOPERATINGINCOMETOTP']
        factor_values['NetNonOIToTPTTM'] = components['LC_MainIndexNew_monthly']['NETNONOITOTPTTM']
        factor_values['TaxesToTP'] = components['LC_MainIndexNew_monthly']['TAXESTOTP']
        factor_values['NPCutToTP'] = components['LC_MainIndexNew_monthly']['NPCUTTOTP']

        return factor_values




