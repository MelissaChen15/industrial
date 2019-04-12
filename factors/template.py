# # __author__ = Chen Meiying
# # -*- coding: utf-8 -*-
# # 2019/4/11 13:17
#
#
# from factors.Frequency import SeasonalFrequency
# from factors.Category import GrowthFactor
# from factors.sql import pl_sql_oracle
#
# import pandas as pd
#
# """
# 季频、成长类因子
#
# 代码表：
#
# """
#
# class (, ):
#
#     def __init__(self, factor_code, name, describe):
#         super().__init__(factor_code, name, describe)
#         self.type = ''
#
#
#     def find_components(self, file_path, table_name):
#         """
#         在数据库中查询计算本类因子需要的数据
#
#         :return: pandas.DataFrame, sql语句执行后返回的数据
#         """
#         sql = pl_sql_oracle.dbData_import()
#         components = sql.InputDataPreprocess(file_path, table_name)
#
#         return components
#
#
#
#
#     def get_factor_values(self, components):
#         """
#         计算本类所有的因子
#
#         :param components: pandas.DataFrame,计算需要的数据
#         :return:
#             factor_values： pandas.DataFrame, 因子值
#             factor_entities： dict, 实例化的因子，可以用于获取因子的代码、名称、描述等数据
#         """
#
#         factor_values = pd.DataFrame(components[''][['SECUCODE','ENDDATE']]) # 存储因子值
#         factor_entities = dict() # 存储实例化的因子
#
#         #
#          = SeasonalGrowthFactor(factor_code='',
#                                            name='',
#                                            describe='')
#         factor_entities[''] =
#         factor_values[''] = components['']['']
#
#
#         return factor_values, factor_entities
#
#
#
# if __name__ == '__main__':
#      = SeasonalGrowthFactor(factor_code = '', name = '', describe = '')
#     sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\.sql'
#     data = .find_components(file_path = sql_file_path, table_name = ['='])
#     # print(data)
#     factor_values, factor_entities = .get_factor_values(data)
#     factor_list = .get_factor_list(factor_entities)
#     print(factor_values)
#     pd.set_option('display.max_columns', None)
#     print(factor_list)
#
#
#
#
#
#
#
#
