# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

from factors.Frequency import SeasonalFrequency
from factors.Category import SecuIndexFactor
from factors.sql import pl_sql_oracle

import pandas as pd

"""
季频每股指标因子

代码表：
    5001	NetAssetPS
    5002	OperatingRevenuePSTTM
    5003	OperProfitPS
    5004	EBITPS
    5005	CapitalSurplusFundPS
    5006	SurplusReserveFundPS
    5007	AccumulationFundPS
    5008	UndividedProfit
    5009	RetainedEarningsPS
    5010	OperCashFlowPSTTM
    5011	CashFlowPSTTM
    5012	ShareHolderFCFPS


"""

class SeasonalSecuIndexFactor(SeasonalFrequency, SecuIndexFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频每股指标'

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # NetAssetPS 每股净资产(元/股)
        NetAssetPS = SeasonalSecuIndexFactor(factor_code='5001',
                                             name='NetAssetPS',
                                             describe='每股净资产（NetAssetPS）：直接取公司定期报告披露数据；若无披露，则，每股净资产=（归属于母公司的所有者权益-其他权益工具）/期末总股本。')
        factor_entities['NetAssetPS'] = NetAssetPS

        # OperatingRevenuePSTTM 每股营业收入_TTM(元/股)
        OperatingRevenuePSTTM = SeasonalSecuIndexFactor(factor_code='5002',
                                                        name='OperatingRevenuePSTTM',
                                                        describe='每股营业收入_TTM（OperatingRevenuePSTTM）＝营业收入（TTM）/期末总股本')
        factor_entities['OperatingRevenuePSTTM'] = OperatingRevenuePSTTM

        # OperProfitPS 每股营业利润(元/股)
        OperProfitPS = SeasonalSecuIndexFactor(factor_code='5003',
                                               name='OperProfitPS',
                                               describe='每股营业利润（OperProfitPS）＝营业利润/期末总股本')
        factor_entities['OperProfitPS'] = OperProfitPS

        # EBITPS 每股息税前利润(元/股)
        EBITPS = SeasonalSecuIndexFactor(factor_code='5004',
                                         name='EBITPS',
                                         describe='每股息税前利润（EBITPS）＝（利润总额+利息费用）/期末总股本其中，利息费用=利息支出-利息收入；若报表附注中未披露利息费用，则用“财务费用”代替；金融类企业不计算。')
        factor_entities['EBITPS'] = EBITPS

        # CapitalSurplusFundPS 每股资本公积金(元/股)
        CapitalSurplusFundPS = SeasonalSecuIndexFactor(factor_code='5005',
                                                       name='CapitalSurplusFundPS',
                                                       describe='每股资本公积金（CapitalSurplusFundPS）＝资本公积/期末总股本')
        factor_entities['CapitalSurplusFundPS'] = CapitalSurplusFundPS

        # SurplusReserveFundPS 每股盈余公积金(元/股)
        SurplusReserveFundPS = SeasonalSecuIndexFactor(factor_code='5006',
                                                       name='SurplusReserveFundPS',
                                                       describe='每股盈余公积金（SurplusReserveFundPS）＝盈余公积/期末总股本')
        factor_entities['SurplusReserveFundPS'] = SurplusReserveFundPS

        # AccumulationFundPS 每股公积金(元/股)
        AccumulationFundPS = SeasonalSecuIndexFactor(factor_code='5007',
                                                     name='AccumulationFundPS',
                                                     describe='每股公积金（AccumulationFundPS）＝（资本公积金+盈余公积金）/期末总股本')
        factor_entities['AccumulationFundPS'] = AccumulationFundPS

        # UndividedProfit 每股未分配利润(元/股)
        UndividedProfit = SeasonalSecuIndexFactor(factor_code='5008',
                                                  name='UndividedProfit',
                                                  describe='每股未分配利润（UndividedProfit）＝未分配利润/期末总股本')
        factor_entities['UndividedProfit'] = UndividedProfit

        # RetainedEarningsPS 每股留存收益(元/股)
        RetainedEarningsPS = SeasonalSecuIndexFactor(factor_code='5009',
                                                     name='RetainedEarningsPS',
                                                     describe='每股留存收益（RetainedEarningsPS）＝（盈余公积+未分配利润）/期末总股本')
        factor_entities['RetainedEarningsPS'] = RetainedEarningsPS

        # OperCashFlowPSTTM 每股经营活动产生的现金流量净额_TTM(元/股)
        OperCashFlowPSTTM = SeasonalSecuIndexFactor(factor_code='5010',
                                                    name='OperCashFlowPSTTM',
                                                    describe='每股经营活动产生的现金流量净额_TTM（OperCashFlowPSTTM）=经营活动产生的现金流量净额（TTM）/期末总股本')
        factor_entities['OperCashFlowPSTTM'] = OperCashFlowPSTTM

        # CashFlowPSTTM 每股现金流量净额_TTM(元/股)
        CashFlowPSTTM = SeasonalSecuIndexFactor(factor_code='5011',
                                                name='CashFlowPSTTM',
                                                describe='每股现金流量净额_TTM（CashFlowPSTTM）=现金及现金等价物净增加额（TTM）/期末总股本')
        factor_entities['CashFlowPSTTM'] = CashFlowPSTTM

        # ShareHolderFCFPS 每股股东自由现金流量(元/股)
        ShareHolderFCFPS = SeasonalSecuIndexFactor(factor_code='5012',
                                                   name='ShareHolderFCFPS',
                                                   describe='每股股东自由现金流量（ShareholderFCFPS）=[归属于母公司的净利润+资产减值准备+固定资产折旧+无形资产摊销+长期待摊费用摊销-（本期固定资产-上期固定资产+固定资产折旧）-营运资本变动额+净债务增加]/期末总股本其中，营运资本变动额＝期末[（流动资产合计－货币资金）－(流动负债合计-应付票据－一年内到期的非流动负债）]－期初[（流动资产合计－货币资金）－(流动负债合计-应付票据－一年内到期的非流动负债）]；净债务增加＝期末（短期借款+长期借款+应付债券）－期初（短期借款+长期借款+应付债券）；金融类企业不计算。')
        factor_entities['ShareHolderFCFPS'] = ShareHolderFCFPS

        return factor_entities

    def find_components(self, file_path, table_name,secucode = ''):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, table_name, secucode )

        # TODO: 读取时需要按时间排序
        components['LC_MainIndexNew']  = components['LC_MainIndexNew'].sort_values(by='ENDDATE')

        # 季频数据转为月频
        components['LC_MainIndexNew_monthly'] = self.seasonal_to_monthly(components['LC_MainIndexNew'],['NETASSETPS', 'OPERATINGREVENUEPSTTM', 'OPERPROFITPS', 'EBITPS', 'CAPITALSURPLUSFUNDPS', 'SURPLUSRESERVEFUNDPS', 'ACCUMULATIONFUNDPS', 'UNDIVIDEDPROFIT', 'RETAINEDEARNINGSPS', 'OPERCASHFLOWPSTTM', 'CASHFLOWPSTTM', 'SHAREHOLDERFCFPS'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值

        factor_values['NetAssetPS'] = components['LC_MainIndexNew_monthly']['NETASSETPS']
        factor_values['OperatingRevenuePSTTM'] = components['LC_MainIndexNew_monthly']['OPERATINGREVENUEPSTTM']
        factor_values['OperProfitPS'] = components['LC_MainIndexNew_monthly']['OPERPROFITPS']
        factor_values['EBITPS'] = components['LC_MainIndexNew_monthly']['EBITPS']
        factor_values['CapitalSurplusFundPS'] = components['LC_MainIndexNew_monthly']['CAPITALSURPLUSFUNDPS']
        factor_values['SurplusReserveFundPS'] = components['LC_MainIndexNew_monthly']['SURPLUSRESERVEFUNDPS']
        factor_values['AccumulationFundPS'] = components['LC_MainIndexNew_monthly']['ACCUMULATIONFUNDPS']
        factor_values['UndividedProfit'] = components['LC_MainIndexNew_monthly']['UNDIVIDEDPROFIT']
        factor_values['RetainedEarningsPS'] = components['LC_MainIndexNew_monthly']['RETAINEDEARNINGSPS']
        factor_values['OperCashFlowPSTTM'] = components['LC_MainIndexNew_monthly']['OPERCASHFLOWPSTTM']
        factor_values['CashFlowPSTTM'] = components['LC_MainIndexNew_monthly']['CASHFLOWPSTTM']
        factor_values['ShareHolderFCFPS'] = components['LC_MainIndexNew_monthly']['SHAREHOLDERFCFPS']

        return factor_values


    def write_values_to_DB(self, code_sql_file_path, data_sql_file_path):
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(code_sql_file_path,
                                            ['secucodes'])


        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path= data_sql_file_path,
                                           table_name=['LC_MainIndexNew'],
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
                factor_values = self.get_factor_values(data)
                # print(factor_values)


                from sqlalchemy import String, Integer
                pl_sql_oracle.df_to_DB(factor_values, 'seasonalsecuindexfactor',if_exists= 'append',data_type={'SECUCODE': String(20)})
                print(self.type, getattr(row, 'SECUCODE'),' done')


            except Exception as e:
                print("write to database failed, error: ", getattr(row, 'SECUCODE'), e)



if __name__ == '__main__':
    ssif = SeasonalSecuIndexFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_secu_index_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'

    # 查看插值后的数据
    # sql = pl_sql_oracle.dbData_import()
    # s = sql.InputDataPreprocess(code_sql_file_path,['secucodes'])
    #
    # for row in s['secucodes'].itertuples(index=True, name='Pandas'):
    #     data = ssif.find_components(file_path=data_sql_file_path,
    #                                     table_name=['LC_MainIndexNew'],
    #                                     secucode='and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
    #     print(data)


    ssif.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)



