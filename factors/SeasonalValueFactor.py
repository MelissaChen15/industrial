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
    0011	EnterpriseFCFPS
    0012	EPSTTM
"""

class SeasonalValueFactor(SeasonalFrequency, ValueFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = 'seasonal value factor'


    def find_components(self, file_path, table_name,secucode = ''):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, table_name, secucode)
        components['LC_MainIndexNew'] = components['LC_MainIndexNew'].sort_values(by='ENDDATE')


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

        # EnterpriseFCFPS 每股企业自由现金流量(元/股)
        EnterpriseFCFPS = SeasonalValueFactor(factor_code='0011',
                                           name='EnterpriseFCFPS',
                                           describe='每股企业自由现金流量（EnterpriseFCFPS）=[归属于母公司的净利润+资产减值准备+固定资产折旧+无形资产摊销+长期待摊费用摊销+利息费用*（1-所得税/利润总额）-（本期固定资产-上期固定资产+固定资产折旧）-营运资本变动额]/期末总股本其中，利息费用=利息支出-利息收入，如果企业未披露利息收入和利息支出，则“利息费用=财务费用”；营运资本变动额＝期末[（流动资产合计－货币资金）－(流动负债合计－应付票据－一年内到期的非流动负债）]－期初[（流动资产合计－货币资金）－(流动负债合计－应付票据－一年内到期的非流动负债）]；金融类企业不计算。')
        factor_entities['EnterpriseFCFPS'] = EnterpriseFCFPS
        factor_values['EnterpriseFCFPS'] = components['LC_MainIndexNew']['ENTERPRISEFCFPS']

        # EPSTTM 每股收益_TTM(元/股)
        EPSTTM = SeasonalValueFactor(factor_code='0012',
                                  name='EPSTTM',
                                  describe='每股收益_TTM（EPSTTM）=归属于母公司的净利润（TTM）/期末总股本')
        factor_entities['EPSTTM'] = EPSTTM
        factor_values['EPSTTM'] = components['LC_MainIndexNew']['EPSTTM']


        return factor_values, factor_entities

    def write_to_DB(self, code_sql_file_path,data_sql_file_path):
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(code_sql_file_path,['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path=data_sql_file_path,
                                           table_name=['LC_MainIndexNew'],
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
                factor_values, factor_entities = self.get_factor_values(data)

                # print(factor_values)
                from sqlalchemy import String, Integer
                if row.Index == 0:
                    factor_list = self.get_factor_list(factor_entities)
                    pl_sql_oracle.df_to_DB(factor_list, 'factorlist', 'append',
                                           {'FactorCode': String(4), '简称': String(32), '频率': Integer(),
                                            '类别': String(64), '描述': String(512)})
                pl_sql_oracle.df_to_DB(factor_values, 'seasonalvaluefactor', 'append', {'SECUCODE': String(20)})

                print(getattr(row, 'SECUCODE'),' done')

            except Exception as e:
                print(getattr(row, 'SECUCODE'), e)

if __name__ == '__main__':

    svf = SeasonalValueFactor(factor_code = '0011-0012', name = 'EnterpriseFCFPS,EPSTTM', describe = 'seasonal value factor')
    data_sql_file_path =  r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_value_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    svf.write_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)









