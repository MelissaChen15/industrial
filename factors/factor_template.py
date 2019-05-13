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

class !因子类名(!继承的频率类名, !继承的经济类别类名):

    def __init__(self, factor_code= '', name= '', describe= ''):
        super().__init__(factor_code, name, describe)
        self.type = '!中文, 如日频价值类因子'
        self.data_sql_file_path = r'.\sql\!sql名.sql'
        self.code_sql_file_path = r'.\sql\sql_get_secucode.sql'
        self.table_name = ['!聚源表名1','!聚源表名2','!聚源表名3']

    def init_factors(self):
        factor_entities = dict()

        # !因子简称 !因子中文名
         !因子简称 = !因子类名(factor_code='!因子代码',
                              name='!因子英文简称',
                              describe='!中文描述, 如何计算因子等内容')
        factor_entities['!因子简称'] = !因子简称

        return factor_entities

    def find_components(self, file_path, secucode, date):
        """
        在数据库中查询计算本类因子需要的数据

        :return: pandas.DataFrame, sql语句执行后返回的数据
        """
        sql = pl_sql_oracle.dbData_import()
        components = sql.InputDataPreprocess(filepath=file_path, table_name=self.table_name, secucode=secucode,
                                             date=date)

        # TODO: 需要按时间排序
        components['!表1名, 同聚源数据库'] = components['!表1名, 同聚源数据库'].sort_values(by='!表1时间标识符(全大写)')
        components['!表2名, 同聚源数据库'] = components['!表2名, 同聚源数据库'].sort_values(by='!表2时间标识符(全大写)'')

        # 如果需要插值转换
        components['!表1名_monthly'] = self.seasonal_to_monthly(components['!表1名, 同聚源数据库'],
                                                              ['!需要转换的字段1(全大写)', '!需要转换的字段2(全大写)'])
        # components['!LC_MainIndexNew_daily'] = self.monthly_to_daily(!monthly_data, !components['LC_DIndicesForValuation'],['NETPROFITGROWRATE'])

        return components

    def get_factor_values(self, components):
        """
        计算本类所有的因子

        :param components: pandas.DataFrame,计算需要的数据
        :return:
            factor_values： pandas.DataFrame, 因子值
        """
        factor_values = pd.DataFrame(components['!表1名, 同聚源数据库, 如果经过插值转换,则为转换后的表名'][['SECUCODE', '!表1的时间标识(全大写)']])  # 存储因子值
        factor_values['!因子简称1'] = components['!表名']['!字段名(全大写)'] + components['!表名']['!字段名(全大写)']
        factor_values['!因子简称2'] = components['!表名']['!字段名(全大写)'] / components['!表名']['!字段名(全大写)']

        return factor_values


if __name__ == '__main__':
    !因子类名的initials = !因子类名()
    !因子类名的initials.write_values_to_DB(可以设置date和secucode的范围)

