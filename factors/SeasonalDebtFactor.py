# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

from factors.Frequency import SeasonalFrequency
from factors.Category import DebtpayingAbilityFactor
from factors.sql import pl_sql_oracle

import pandas as pd

"""
偿债能力类因子

代码表：
    6001	QuickRatio
    6002	DebtEquityRatio
    6003	SEWithoutMIToTL
    6004	SEWMIToInterestBearDebt
    6005	DebtTangibleEquityRatio
    6006	TangibleAToNetDebt
    6007	EBITDAToTLiability
    6008	NOCFToTLiability
    6009	NOCFToInterestBearDebt
    6010	NOCFToCurrentLiability
    6011	NOCFToNetDebt
    6012	InterestCover
    6013	LongDebtToWorkingCapital
    6014	OperCashInToCurrentDebt


"""

class SeasonalDebtFactor(SeasonalFrequency,DebtpayingAbilityFactor ):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频偿债能力'
        self.data_sql_file_path = r'.\sql\sql_seasonal_debtpaying_ability_factor.sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'
        self.table_name = ['LC_MainIndexNew']

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # QuickRatio 速动比率
        QuickRatio = SeasonalDebtFactor(factor_code='6001',
                                                     name='QuickRatio',
                                                     describe='速动比率（QuickRatio）＝（流动资产合计-存货）／流动负债合计，金融类企业不计算。')
        factor_entities['QuickRatio'] = QuickRatio

        # DebtEquityRatio 产权比率(%)
        DebtEquityRatio = SeasonalDebtFactor(factor_code='6002',
                                                          name='DebtEquityRatio',
                                                          describe='产权比率（DebtEquityRatio）＝负债合计／归属母公司股东的权益*100%')
        factor_entities['DebtEquityRatio'] = DebtEquityRatio

        # SEWithoutMIToTL 归属母公司股东的权益/负债合计(%)
        SEWithoutMIToTL = SeasonalDebtFactor(factor_code='6003',
                                                          name='SEWithoutMIToTL',
                                                          describe='无')
        factor_entities['SEWithoutMIToTL'] = SEWithoutMIToTL

        # SEWMIToInterestBearDebt 归属母公司股东的权益/带息债务(%)
        SEWMIToInterestBearDebt = SeasonalDebtFactor(factor_code='6004',
                                                                  name='SEWMIToInterestBearDebt',
                                                                  describe='归属母公司股东的权益／带息债务（SEWMIToInterestBearDebt）＝归属母公司股东的权益／（负债合计-无息流动负债-无息非流动负债）*100%其中，无息流动负债=应付账款+预收账款+应付职工薪酬+应交税费+其他应付款+预提费用+递延收益+其他流动负债；无息非流动负债=非流动负债合计-长期借款-应付债券。金融类企业不计算。')
        factor_entities['SEWMIToInterestBearDebt'] = SEWMIToInterestBearDebt

        # DebtTangibleEquityRatio 有形净值债务率(%)
        DebtTangibleEquityRatio = SeasonalDebtFactor(factor_code='6005',
                                                                  name='DebtTangibleEquityRatio',
                                                                  describe='有形净值债务率（DebtTangibleEquityRatio）＝负债合计／有形净值*100%其中，有形净值=归属于母公司的股东权益-（无形资产+开发支出+商誉+长期待摊费用+递延所得税资产）。')
        factor_entities['DebtTangibleEquityRatio'] = DebtTangibleEquityRatio

        # TangibleAToNetDebt 有形净值/净债务(%)
        TangibleAToNetDebt = SeasonalDebtFactor(factor_code='6006',
                                                             name='TangibleAToNetDebt',
                                                             describe='有形净值／净债务（TangibleAToNetDebt）＝（有形净值／净债务）*100%其中，有形净值=归属于母公司的股东权益-（无形资产+开发支出+商誉+长期待摊费用+递延所得税资产）；净债务=带息债务-货币资金，“带息债务”的算法如TangibleAToInteBearDebt[有形净值／带息债务（%）]所示。金融类企业不计算。')
        factor_entities['TangibleAToNetDebt'] = TangibleAToNetDebt

        # EBITDAToTLiability 息税折旧摊销前利润/负债合计
        EBITDAToTLiability = SeasonalDebtFactor(factor_code='6007',
                                                             name='EBITDAToTLiability',
                                                             describe='息税折旧摊销前利润／负债合计（EBITDAToTLiability）：“息税折旧摊销前利润”算法见EBITDA[息税折旧摊销前利润（元）]。金融类企业不计算。')
        factor_entities['EBITDAToTLiability'] = EBITDAToTLiability

        # NOCFToTLiability 经营活动产生现金流量净额/负债合计
        NOCFToTLiability = SeasonalDebtFactor(factor_code='6008',
                                                           name='NOCFToTLiability',
                                                           describe='经营活动产生现金流量净额/负债合计(NOCFToTLiability):此指标金融类企业不计算。')
        factor_entities['NOCFToTLiability'] = NOCFToTLiability

        # NOCFToInterestBearDebt 经营活动产生现金流量净额/带息债务
        NOCFToInterestBearDebt = SeasonalDebtFactor(factor_code='6009',
                                                                 name='NOCFToInterestBearDebt',
                                                                 describe='经营活动产生现金流量净额/带息债务（NOCFToInterestBearDebt）：“带息债务”算法见TangibleAToInteBearDebt[有形净值／带息债务（%）]。金融类企业不计算。')
        factor_entities['NOCFToInterestBearDebt'] = NOCFToInterestBearDebt

        # NOCFToCurrentLiability 经营活动产生现金流量净额/流动负债
        NOCFToCurrentLiability = SeasonalDebtFactor(factor_code='6010',
                                                                 name='NOCFToCurrentLiability',
                                                                 describe='经营活动产生现金流量净额/流动负债(NOCFToCurrentLiability):此指标金融类企业不计算。')
        factor_entities['NOCFToCurrentLiability'] = NOCFToCurrentLiability

        # NOCFToNetDebt 经营活动产生现金流量净额/净债务
        NOCFToNetDebt = SeasonalDebtFactor(factor_code='6011',
                                                        name='NOCFToNetDebt',
                                                        describe='经营活动产生现金流量净额/净债务（NOCFToNetDebt）：“净债务”算法见TangibleAToNetDebt[有形净值／净债务（%）]。金融类企业不计算。')
        factor_entities['NOCFToNetDebt'] = NOCFToNetDebt

        # InterestCover 利息保障倍数(倍)
        InterestCover = SeasonalDebtFactor(factor_code='6012',
                                                        name='InterestCover',
                                                        describe='利息保障倍数（InterestCover）＝息税前利润/利息费用。其中，“息税前利润”、“利息费用”均见EBIT[息税前利润（元）]。若“利息费用”小于等于0，则该指标不计算。金融类企业不计算。')
        factor_entities['InterestCover'] = InterestCover

        # LongDebtToWorkingCapital 长期负债与营运资金比率
        LongDebtToWorkingCapital = SeasonalDebtFactor(factor_code='6013',
                                                                   name='LongDebtToWorkingCapital',
                                                                   describe='长期负债与营运资金比率（LongDebtToWorkingCapital）＝长期负债/（流动资产-流动负债），金融类企业不计算。')
        factor_entities['LongDebtToWorkingCapital'] = LongDebtToWorkingCapital

        # OperCashInToCurrentDebt 现金流动负债比
        OperCashInToCurrentDebt = SeasonalDebtFactor(factor_code='6014',
                                                                  name='OperCashInToCurrentDebt',
                                                                  describe='现金流动负债比（OperCashInToCurrentDebt）＝经营现金净流入/流动负债，金融类企业不计算。')
        factor_entities['OperCashInToCurrentDebt'] = OperCashInToCurrentDebt

        return factor_entities

    def find_components(self, file_path, secucode, date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, self.table_name, secucode, date)

        components['LC_MainIndexNew']  = components['LC_MainIndexNew'].sort_values(by='ENDDATE')
        components['LC_MainIndexNew_monthly'] = self.seasonal_to_monthly(components['LC_MainIndexNew'],['QUICKRATIO', 'DEBTEQUITYRATIO', 'SEWITHOUTMITOTL', 'SEWMITOINTERESTBEARDEBT', 'DEBTTANGIBLEEQUITYRATIO', 'TANGIBLEATONETDEBT', 'EBITDATOTLIABILITY', 'NOCFTOTLIABILITY', 'NOCFTOINTERESTBEARDEBT', 'NOCFTOCURRENTLIABILITY', 'NOCFTONETDEBT', 'INTERESTCOVER', 'LONGDEBTTOWORKINGCAPITAL', 'OPERCASHINTOCURRENTDEBT'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值

        factor_values['QuickRatio'] = components['LC_MainIndexNew_monthly']['QUICKRATIO']
        factor_values['DebtEquityRatio'] = components['LC_MainIndexNew_monthly']['DEBTEQUITYRATIO']
        factor_values['SEWithoutMIToTL'] = components['LC_MainIndexNew_monthly']['SEWITHOUTMITOTL']
        factor_values['SEWMIToInterestBearDebt'] = components['LC_MainIndexNew_monthly']['SEWMITOINTERESTBEARDEBT']
        factor_values['DebtTangibleEquityRatio'] = components['LC_MainIndexNew_monthly']['DEBTTANGIBLEEQUITYRATIO']
        factor_values['TangibleAToNetDebt'] = components['LC_MainIndexNew_monthly']['TANGIBLEATONETDEBT']
        factor_values['EBITDAToTLiability'] = components['LC_MainIndexNew_monthly']['EBITDATOTLIABILITY']
        factor_values['NOCFToTLiability'] = components['LC_MainIndexNew_monthly']['NOCFTOTLIABILITY']
        factor_values['NOCFToInterestBearDebt'] = components['LC_MainIndexNew_monthly']['NOCFTOINTERESTBEARDEBT']
        factor_values['NOCFToCurrentLiability'] = components['LC_MainIndexNew_monthly']['NOCFTOCURRENTLIABILITY']
        factor_values['NOCFToNetDebt'] = components['LC_MainIndexNew_monthly']['NOCFTONETDEBT']
        factor_values['InterestCover'] = components['LC_MainIndexNew_monthly']['INTERESTCOVER']
        factor_values['LongDebtToWorkingCapital'] = components['LC_MainIndexNew_monthly']['LONGDEBTTOWORKINGCAPITAL']
        factor_values['OperCashInToCurrentDebt'] = components['LC_MainIndexNew_monthly']['OPERCASHINTOCURRENTDEBT']

        return factor_values





if __name__ == '__main__':
    pass
    sdaf = SeasonalDebtFactor()
    # data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_debtpaying_ability_factor.sql'
    # code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # sdaf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)

