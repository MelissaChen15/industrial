# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 16:37

# 引用frequency.py文件中相应的频率类
from factors.Frequency import !
# 引用category.py文件中相应的类别类
from factors.Category import !
from factors.sql import pl_sql_oracle

import pandas as pd

"""
!xx类因子

!代码表：

"""

class !因子类名(!继承的评率类名, !继承的经济类别类名):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '!修改此处. 中文, 如日频价值类因子'

    def init_factors(self):
        """
        初始化因子的基础特征,包括factor name, factor code和description

        :return: dict, key为因子名,value为因子类的一个实例
        """
        factor_entities = dict()


        ########### 如需添加多个因子, 复制此处的内容 ############
        # !因子简称 !因子中文名
         !因子简称 = !因子类名(factor_code='!因子代码',
                              name='!因子英文简称',
                              describe='!中文描述, 如何计算因子等内容')
        factor_entities['!因子简称'] = !因子简称
        ###################################################

        return factor_entities

    def find_components(self, file_path, table_name,secucode = ''):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(file_path, table_name, secucode )

        # TODO: 读取时需要按时间排序
        components['!表1名, 同聚源数据库']  = components['!表1名, 同聚源数据库'].sort_values(by='!表1时间标识符')
        components['!表2名, 同聚源数据库'] = components['!表2名, 同聚源数据库'].sort_values(by='!表2时间标识符')

        # 如果需要插值转换
        components['!表1名_monthly']  = self.seasonal_to_monthly(components['!表1名, 同聚源数据库'],['!需要转换的字段1','!需要转换的字段2'])
        # components['!LC_MainIndexNew_daily'] = self.monthly_to_daily(!monthly_data, !components['LC_DIndicesForValuation'],['NETPROFITGROWRATE'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """

        factor_values = pd.DataFrame(components['!表1名, 同聚源数据库, 如果经过插值转换,则为转换后的表名'][['SECUCODE','!表1的时间标识符']]) # 存储因子值
        factor_values['!因子简称1'] = components['!表名']['!字段名'] + components['!表名']['!字段名']
        factor_values['!因子简称2'] = components['!表名']['!字段名'] / components['!表名']['!字段名']

        return factor_values



    def write_values_to_DB(self,  code_sql_file_path, data_sql_file_path):
        """
        计算因子值并写入数据库中相应的数据表
        :param code_sql_file_path: str, 查询股票代码的sql文件路径
        :param data_sql_file_path: str, 读取数据库数据的sql代码文件路径
        :return: none
        """
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(code_sql_file_path,['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = self.find_components(file_path= data_sql_file_path,
                                           table_name=['!表1名, 同聚源数据库', '!表2名, 同聚源数据库'],
                                           secucode=  'and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
                factor_values = self.get_factor_values(data)


                from sqlalchemy import String, Integer
                print(factor_values)
                # TODO: 表名必须是小写
                # pl_sql_oracle.df_to_DB(factor_values, '!存入数据库的表名, 必须是连续的小写字符',if_exists='append',data_type={'SECUCODE': String(20)})

                print(self.type, getattr(row, 'SECUCODE'),' done')


            except Exception as e:
                print("write to database failed, error: ", getattr(row, 'SECUCODE'), e)



if __name__ == '__main__':
    !因子类名的initials = !因子类名()
    data_sql_file_path = !r'D:\Meiying\codes\industrial\factors\sql\.sql' # 读取数据库数据的sql代码文件路径
    code_sql_file_path = !r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'  # 查询股票代码的sql文件路径
    !因子类名的initials.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)

