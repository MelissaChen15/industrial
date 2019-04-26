# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

from factors.Frequency import
from factors.Category import
from factors.sql import pl_sql_oracle

import pandas as pd

"""
类因子

代码表：

"""

class (, ):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = ''

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        #
         = (factor_code='',
                              name='',
                              describe='')
        factor_entities[''] =

        return factor_entities

    def find_components(self, file_path, table_name,secucode = ''):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, table_name, secucode )

        # TODO: 读取时需要按时间排序
        components['']  = components[''].sort_values(by='')
        components[''] = components[''].sort_values(by='')

        # 如果需要转换
        # monthly_data = self.seasonal_to_monthly(components['LC_MainIndexNew'],['NETPROFITGROWRATE'])
        # components['LC_MainIndexNew_daily'] = self.monthly_to_daily(monthly_data, components['LC_DIndicesForValuation'],['NETPROFITGROWRATE'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components[''][['SECUCODE','TRADINGDAY']]) # 存储因子值
        factor_values[''] = components['']['']
        factor_values[''] = components['']['']

        return factor_values



    def write_values_to_DB(self,  code_sql_file_path, data_sql_file_path):
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(code_sql_file_path,
                                            ['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path= data_sql_file_path,
                                           table_name=['', ''],
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
                factor_values = self.get_factor_values(data)


                from sqlalchemy import String, Integer
                print(factor_values)
                # TODO: 表名必须是小写
                # pl_sql_oracle.df_to_DB(factor_values, '',if_exists= mode,data_type={'SECUCODE': String(20)})

                print(self.type, getattr(row, 'SECUCODE'),' done')


            except Exception as e:
                print("write to database failed, error: ", getattr(row, 'SECUCODE'), e)



if __name__ == '__main__':
     = ()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    .write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)

