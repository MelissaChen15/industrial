# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37
# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

from factors.Frequency import DailyFrequency
from factors.Category import ValueFactor
from factors.sql import pl_sql_oracle

import pandas as pd

"""
日频、价值类因子, 因为日频/季频而做特殊处理

代码表：
    1010	PEG
"""

class DailyDivideSeasonalFactor(DailyFrequency, ValueFactor):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '日频价值类特殊处理'

    def init_factors(self):
        factor_entities = dict()  # 存储实例化的因子

        # PEG 市盈率增长率
        # 注意，此因子为日频数据/季频数据，分母取上个季度最后一天的数据
        PEG = DailyDivideSeasonalFactor(factor_code='1010',
                               name='PEG',
                               describe='市盈率增长率 = 市盈率(PE)/净利润同比增长率(NetProfitGrowRate)')
        factor_entities['PEG'] = PEG

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
        components['LC_DIndicesForValuation'] = components['LC_DIndicesForValuation'].sort_values(by='TRADINGDAY')

        monthly_data = self.seasonal_to_monthly(components['LC_MainIndexNew'],['NETPROFITGROWRATE'])
        components['LC_MainIndexNew_daily'] = self.monthly_to_daily(monthly_data, components['LC_DIndicesForValuation'],['NETPROFITGROWRATE'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """
        factor_values = pd.DataFrame(components['LC_DIndicesForValuation'][['SECUCODE', 'TRADINGDAY']])  # 存储因子值
        factor_values['PEG'] = components['LC_DIndicesForValuation']['PE'] / (components['LC_MainIndexNew_daily']['NETPROFITGROWRATE'])

        return factor_values.drop(axis=0, index=0)

    def write_values_to_DB(self, code_sql_file_path,data_sql_file_path, daterange):
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(code_sql_file_path,['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path=data_sql_file_path,
                                           table_name=['LC_DIndicesForValuation', 'LC_MainIndexNew'],
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
                factor_values = self.get_factor_values(data)


                from sqlalchemy import String, Integer
                print(factor_values)
                pl_sql_oracle.df_to_DB(factor_values, 'dailydivideseasonalfacor',if_exists= 'append',data_type={'SECUCODE': String(20)})

                print(getattr(row, 'SECUCODE'),' done')

            except Exception as e:

                print(getattr(row, 'SECUCODE'), e)


if __name__ == '__main__':
    pass
    # dvf = DailyDivideSeasonalFactor()
    # data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_daily_divide_seasonal_factor.sql'
    # code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # dvf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)

