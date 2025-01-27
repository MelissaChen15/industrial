# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/11 13:17


from factors.Frequency import SeasonalFrequency
from factors.Category import ValueFactor
from factors.sql import pl_sql_oracle

import pandas as pd

"""
季频、价值类因子

代码表：
    2001	EnterpriseFCFPS
    2002	EPSTTM

"""

class SeasonalValueFactor(SeasonalFrequency, ValueFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '季频价值类'
        self.data_sql_file_path = r'.\sql\sql_seasonal_value_factor.sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'
        self.table_name = ['LC_MainIndexNew'] # list, 需要读取的数据库中的表名

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # EnterpriseFCFPS 每股企业自由现金流量(元/股)
        EnterpriseFCFPS = SeasonalValueFactor(factor_code='2001',
                                           name='EnterpriseFCFPS',
                                           describe='每股企业自由现金流量（EnterpriseFCFPS）=[归属于母公司的净利润+资产减值准备+固定资产折旧+无形资产摊销+长期待摊费用摊销+利息费用*（1-所得税/利润总额）-（本期固定资产-上期固定资产+固定资产折旧）-营运资本变动额]/期末总股本其中，利息费用=利息支出-利息收入，如果企业未披露利息收入和利息支出，则“利息费用=财务费用”；营运资本变动额＝期末[（流动资产合计－货币资金）－(流动负债合计－应付票据－一年内到期的非流动负债）]－期初[（流动资产合计－货币资金）－(流动负债合计－应付票据－一年内到期的非流动负债）]；金融类企业不计算。')
        factor_entities['EnterpriseFCFPS'] = EnterpriseFCFPS

        # EPSTTM 每股收益_TTM(元/股)
        EPSTTM = SeasonalValueFactor(factor_code='2002',
                                  name='EPSTTM',
                                  describe='每股收益_TTM（EPSTTM）=归属于母公司的净利润（TTM）/期末总股本')
        factor_entities['EPSTTM'] = EPSTTM
        return factor_entities


    def find_components(self, file_path,secucode, date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(filepath=file_path, table_name=self.table_name,secucode=secucode,date=date)
        components['LC_MainIndexNew'] = components['LC_MainIndexNew'].sort_values(by='ENDDATE')
        components['LC_MainIndexNew_monthly'] = self.seasonal_to_monthly(components['LC_MainIndexNew'],['EnterpriseFCFPS'.upper(),'EPSTTM'])


        return components


    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['LC_MainIndexNew_monthly'][['SECUCODE','STARTDAY']]) # 存储因子值
        factor_values['EnterpriseFCFPS'] = components['LC_MainIndexNew_monthly']['ENTERPRISEFCFPS']
        factor_values['EPSTTM'] = components['LC_MainIndexNew_monthly']['EPSTTM']


        return factor_values


if __name__ == '__main__':
    pass
    # svf = SeasonalValueFactor(factor_code = '0011-0012', name = 'EnterpriseFCFPS,EPSTTM', describe = 'seasonal value factor')
    # data_sql_file_path =  r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_value_factor.sql'
    # code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # svf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)









