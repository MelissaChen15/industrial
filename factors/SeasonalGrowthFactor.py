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
    3001	NetProfitGrowRate
    3002	ROETTM
    3003	TotalAssetGrowRate
    3004	BasicEPSYOY
    3005	GrossIncomeRatioTTM
    3006	NetProfitRatioTTM
    3007	DilutedEPSYOY
    3008	OperatingRevenueGrowRate
    3009	ORComGrowRate3Y
    3010	OperProfitGrowRate
    3011	TotalProfeiGrowRate
    3012	NPParentCompanyYOY
    3013	NPParentCompanyCutYOY
    3014	NPPCCGrowRate3Y
    3015	AvgNPYOYPastFiveYear
    3016	NetOperateCashFlowYOY
    3017	OperCashPSGrowRate
    3018	NAORYOY
    3019	NetAssetGrowRate
    3020	EPSGrowRateYTD
    3021	SEWithoutMIGrowRateYTD
    3022	TAGrowRateYTD
    3023	SustainableGrowRate

"""

class SeasonalGrowthFactor(SeasonalFrequency, GrowthFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频成长类'

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # NetProfitGrowRate 净利润同比增长(%)
        NetProfitGrowRate = SeasonalGrowthFactor(factor_code='3001',
                                                 name='NetProfitGrowRate',
                                                 describe='（本期数据－去年同期数据）/︱去年同期数据︱*100%')
        factor_entities['NetProfitGrowRate'] = NetProfitGrowRate

        # ROETTM 净资产收益率_TTM(%)
        ROETTM = SeasonalGrowthFactor(factor_code='3002',
                                      name='ROETTM',
                                      describe='净资产收益率_TTM（ROETTM）＝（归属于母公司的净利润（TTM）*2/（期初归属于母公司的股东权益+期末归属于母公司的股东权益）*100%')
        factor_entities['ROETTM'] = ROETTM

        # TotalAssetGrowRate 总资产同比增长(%)
        TotalAssetGrowRate = SeasonalGrowthFactor(factor_code='3003',
                                                  name='TotalAssetGrowRate',
                                                  describe='（本期数据－去年同期数据）/︱去年同期数据︱*100%')
        factor_entities['TotalAssetGrowRate'] = TotalAssetGrowRate

        # BasicEPSYOY 基本每股收益同比增长(%)
        BasicEPSYOY = SeasonalGrowthFactor(factor_code='3004',
                                           name='BasicEPSYOY',
                                           describe='基本每股收益（BasicEPS）：新会计准则下，取公司的实际披露数；旧会计准则下，取公司披露的每股收益（加权）。')
        factor_entities['BasicEPSYOY'] = BasicEPSYOY

        # GrossIncomeRatioTTM 销售毛利率_TTM(%)
        GrossIncomeRatioTTM = SeasonalGrowthFactor(factor_code='3005',
                                                   name='GrossIncomeRatioTTM',
                                                   describe='销售毛利率_TTM（GrossIncomeRatioTTM）＝[营业收入（TTM）-营业成本（TTM）]/营业收入（TTM）*100%，金融类企业不计算。')
        factor_entities['GrossIncomeRatioTTM'] = GrossIncomeRatioTTM

        # NetProfitRatioTTM 销售净利率_TTM(%)
        NetProfitRatioTTM = SeasonalGrowthFactor(factor_code='3006',
                                                 name='NetProfitRatioTTM',
                                                 describe='销售净利率_TTM（NetProfitRatioTTM）＝含少数股东损益的净利润（TTM）/营业收入（TTM）*100%')
        factor_entities['NetProfitRatioTTM'] = NetProfitRatioTTM

        # DilutedEPSYOY 稀释每股收益同比增长(%)
        DilutedEPSYOY = SeasonalGrowthFactor(factor_code='3007',
                                             name='DilutedEPSYOY',
                                             describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['DilutedEPSYOY'] = DilutedEPSYOY

        # OperatingRevenueGrowRate 营业收入同比增长(%)
        OperatingRevenueGrowRate = SeasonalGrowthFactor(factor_code='3008',
                                                        name='OperatingRevenueGrowRate',
                                                        describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['OperatingRevenueGrowRate'] = OperatingRevenueGrowRate

        # ORComGrowRate3Y 营业收入3年复合增长率(%)
        ORComGrowRate3Y = SeasonalGrowthFactor(factor_code='3009',
                                               name='ORComGrowRate3Y',
                                               describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['ORComGrowRate3Y'] = ORComGrowRate3Y

        # OperProfitGrowRate 营业利润同比增长(%)
        OperProfitGrowRate = SeasonalGrowthFactor(factor_code='3010',
                                                  name='OperProfitGrowRate',
                                                  describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['OperProfitGrowRate'] = OperProfitGrowRate

        # TotalProfeiGrowRate 利润总额同比增长(%)
        TotalProfeiGrowRate = SeasonalGrowthFactor(factor_code='3011',
                                                   name='TotalProfeiGrowRate',
                                                   describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['TotalProfeiGrowRate'] = TotalProfeiGrowRate

        # NPParentCompanyYOY 归属母公司股东的净利润同比增长(%)
        NPParentCompanyYOY = SeasonalGrowthFactor(factor_code='3012',
                                                  name='NPParentCompanyYOY',
                                                  describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NPParentCompanyYOY'] = NPParentCompanyYOY

        # NPParentCompanyCutYOY 归属母公司股东的净利润(扣除)同比增长(%)
        NPParentCompanyCutYOY = SeasonalGrowthFactor(factor_code='3013',
                                                     name='NPParentCompanyCutYOY',
                                                     describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NPParentCompanyCutYOY'] = NPParentCompanyCutYOY

        # NPPCCGrowRate3Y 归属母公司股东的净利润3年复合增长率(%)
        NPPCCGrowRate3Y = SeasonalGrowthFactor(factor_code='3014',
                                               name='NPPCCGrowRate3Y',
                                               describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NPPCCGrowRate3Y'] = NPPCCGrowRate3Y

        # AvgNPYOYPastFiveYear 过去五年同期归属母公司净利润平均增幅(%)
        AvgNPYOYPastFiveYear = SeasonalGrowthFactor(factor_code='3015',
                                                    name='AvgNPYOYPastFiveYear',
                                                    describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['AvgNPYOYPastFiveYear'] = AvgNPYOYPastFiveYear

        # NetOperateCashFlowYOY 经营活动产生的现金流量净额同比增长(%)
        NetOperateCashFlowYOY = SeasonalGrowthFactor(factor_code='3016',
                                                     name='NetOperateCashFlowYOY',
                                                     describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NetOperateCashFlowYOY'] = NetOperateCashFlowYOY

        # OperCashPSGrowRate 每股经营活动产生的现金流量净额同比增长(%)
        OperCashPSGrowRate = SeasonalGrowthFactor(factor_code='3017',
                                                  name='OperCashPSGrowRate',
                                                  describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['OperCashPSGrowRate'] = OperCashPSGrowRate

        # NAORYOY 净资产收益率(摊薄)同比增长(%)
        NAORYOY = SeasonalGrowthFactor(factor_code='3018',
                                       name='NAORYOY',
                                       describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NAORYOY'] = NAORYOY

        # NetAssetGrowRate 净资产同比增长(%)
        NetAssetGrowRate = SeasonalGrowthFactor(factor_code='3019',
                                                name='NetAssetGrowRate',
                                                describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['NetAssetGrowRate'] = NetAssetGrowRate

        # EPSGrowRateYTD 每股净资产相对年初增长率(%)
        EPSGrowRateYTD = SeasonalGrowthFactor(factor_code='3020',
                                              name='EPSGrowRateYTD',
                                              describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['EPSGrowRateYTD'] = EPSGrowRateYTD

        # SEWithoutMIGrowRateYTD 归属母公司股东的权益相对年初增长率(%)
        SEWithoutMIGrowRateYTD = SeasonalGrowthFactor(factor_code='3021',
                                                      name='SEWithoutMIGrowRateYTD',
                                                      describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['SEWithoutMIGrowRateYTD'] = SEWithoutMIGrowRateYTD

        # TAGrowRateYTD 资产总计相对年初增长率(%)
        TAGrowRateYTD = SeasonalGrowthFactor(factor_code='3022',
                                             name='TAGrowRateYTD',
                                             describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['TAGrowRateYTD'] = TAGrowRateYTD

        # SustainableGrowRate 可持续增长率(%)
        SustainableGrowRate = SeasonalGrowthFactor(factor_code='3023',
                                                   name='SustainableGrowRate',
                                                   describe='见聚源数据库，表LC_MainIndexNew')
        factor_entities['SustainableGrowRate'] = SustainableGrowRate

        return factor_entities


    def find_components(self, file_path, table_name,secucode = ''):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """

        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, table_name, secucode)

        # TODO: 读取时需要按时间排序
        components['LC_MainIndexNew'] = components['LC_MainIndexNew'].sort_values(by='ENDDATE')
        # 如果需要转换
        components['LC_MainIndexNew_monthly'] = self.seasonal_to_monthly(components['LC_MainIndexNew'],['NETPROFITGROWRATE', 'ROETTM', 'TOTALASSETGROWRATE', 'BASICEPSYOY', 'GROSSINCOMERATIOTTM', 'NETPROFITRATIOTTM', 'DILUTEDEPSYOY', 'OPERATINGREVENUEGROWRATE', 'ORCOMGROWRATE3Y', 'OPERPROFITGROWRATE', 'TOTALPROFEIGROWRATE', 'NPPARENTCOMPANYYOY', 'NPPARENTCOMPANYCUTYOY', 'NPPCCGROWRATE3Y', 'AVGNPYOYPASTFIVEYEAR', 'NETOPERATECASHFLOWYOY', 'OPERCASHPSGROWRATE', 'NAORYOY', 'NETASSETGROWRATE', 'EPSGROWRATEYTD', 'SEWITHOUTMIGROWRATEYTD', 'TAGROWRATEYTD', 'SUSTAINABLEGROWRATE'])
        return components


    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值

        factor_values['NetProfitGrowRate'] = components['LC_MainIndexNew_monthly']['NETPROFITGROWRATE']
        factor_values['ROETTM'] = components['LC_MainIndexNew_monthly']['ROETTM']
        factor_values['TotalAssetGrowRate'] = components['LC_MainIndexNew_monthly']['TOTALASSETGROWRATE']
        factor_values['BasicEPSYOY'] = components['LC_MainIndexNew_monthly']['BASICEPSYOY']
        factor_values['GrossIncomeRatioTTM'] = components['LC_MainIndexNew_monthly']['GROSSINCOMERATIOTTM']
        factor_values['NetProfitRatioTTM'] = components['LC_MainIndexNew_monthly']['NETPROFITRATIOTTM']
        factor_values['DilutedEPSYOY'] = components['LC_MainIndexNew_monthly']['DILUTEDEPSYOY']
        factor_values['OperatingRevenueGrowRate'] = components['LC_MainIndexNew_monthly']['OPERATINGREVENUEGROWRATE']
        factor_values['ORComGrowRate3Y'] = components['LC_MainIndexNew_monthly']['ORCOMGROWRATE3Y']
        factor_values['OperProfitGrowRate'] = components['LC_MainIndexNew_monthly']['OPERPROFITGROWRATE']
        factor_values['TotalProfeiGrowRate'] = components['LC_MainIndexNew_monthly']['TOTALPROFEIGROWRATE']
        factor_values['NPParentCompanyYOY'] = components['LC_MainIndexNew_monthly']['NPPARENTCOMPANYYOY']
        factor_values['NPParentCompanyCutYOY'] = components['LC_MainIndexNew_monthly']['NPPARENTCOMPANYCUTYOY']
        factor_values['NPPCCGrowRate3Y'] = components['LC_MainIndexNew_monthly']['NPPCCGROWRATE3Y']
        factor_values['AvgNPYOYPastFiveYear'] = components['LC_MainIndexNew_monthly']['AVGNPYOYPASTFIVEYEAR']
        factor_values['NetOperateCashFlowYOY'] = components['LC_MainIndexNew_monthly']['NETOPERATECASHFLOWYOY']
        factor_values['OperCashPSGrowRate'] = components['LC_MainIndexNew_monthly']['OPERCASHPSGROWRATE']
        factor_values['NAORYOY'] = components['LC_MainIndexNew_monthly']['NAORYOY']
        factor_values['NetAssetGrowRate'] = components['LC_MainIndexNew_monthly']['NETASSETGROWRATE']
        factor_values['EPSGrowRateYTD'] = components['LC_MainIndexNew_monthly']['EPSGROWRATEYTD']
        factor_values['SEWithoutMIGrowRateYTD'] = components['LC_MainIndexNew_monthly']['SEWITHOUTMIGROWRATEYTD']
        factor_values['TAGrowRateYTD'] = components['LC_MainIndexNew_monthly']['TAGROWRATEYTD']
        factor_values['SustainableGrowRate'] = components['LC_MainIndexNew_monthly']['SUSTAINABLEGROWRATE']

        return factor_values


    def write_values_to_DB(self, mode, code_sql_file_path,data_sql_file_path):
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(code_sql_file_path,['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path=data_sql_file_path,
                                           table_name=['LC_MainIndexNew'],
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
                factor_values = self.get_factor_values(data)

                from sqlalchemy import String, Integer
                # pl_sql_oracle.df_to_DB(factor_values, 'seasonalgrowthfactor', if_exists= mode,data_type={'SECUCODE': String(20)})
                print(factor_values)

                print(getattr(row, 'SECUCODE'),' done')


            except Exception as e:

                print(getattr(row, 'SECUCODE'), e)




if __name__ == '__main__':
    sgv = SeasonalGrowthFactor(factor_code = '0013-0018', name = 'NetProfitGrowRate,ROETTM,TotalAssetGrowRate,BasicEPSYOY,GrossIncomeRatioTTM,NetProfitRatioTTM', describe = 'seasonal growth vector')
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_growth_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    sgv.write_values_to_DB(mode='append',data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)