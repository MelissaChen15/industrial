# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

from factors.Frequency import DailyFrequency
from factors.Category import ValueFactor
from factors.sql import pl_sql_oracle

import pandas as pd

"""
日频、价值类因子
"""

class DailyValueFactor(DailyFrequency, ValueFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = 'daily value factor'


    def find_components(self, file_path, factor_name):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, factor_name)

        return components



    def get_daily_value_factors(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
            factor_entities： dict, 实例化的因子，可以用于获取因子的代码、名称、描述等数据
        """

        factor_values = pd.DataFrame(components[['SECUCODE','TRADINGDAY']]) # 存储因子值
        factor_entities = dict() # 存储实例化的因子

        # PE 滚动市盈率
        PE = DailyValueFactor(factor_code = '0001',
                              name = 'PE',
                              describe = '滚动市盈率（PE）＝股票市值/最近四个季度的净利润之和。其中，股票市值=A股价格×总股本')
        factor_entities['PE'] = PE
        factor_values['PE'] = components['PE']

        # PB 市净率
        PB = DailyValueFactor(factor_code='0002',
                              name='PB',
                              describe='市净率（PB）＝股票市值/净资产。其中，股票市值=A股价格×总股本；净资产为最新定期报告公布的净资产。')
        factor_entities['PB'] = PB
        factor_values['PB'] = components['PB']


        return factor_values, factor_entities




if __name__ == '__main__':
    dvf = DailyValueFactor(factor_code = '0001-0002', name = 'PE, PB', describe = 'hhhhh')
    factor_name = ['just_need_to_read_database_once']
    sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_sentence_template.sql'
    data = dvf.find_components(file_path = sql_file_path, factor_name = factor_name)
    print(data)
    factor_values, factor_entities = dvf.get_daily_value_factors(data)
    print(factor_values)
    print(factor_entities)






