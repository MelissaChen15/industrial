# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/20  16:53
desc:
'''

from sql.dbsynchelper2 import dbsynchelper
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

import datetime


class dbData_import_factor(object):

    def __init__(self,factor_tablename,frequency,daterange):
        '''
        :param factor_tablename: 因子所在表名
        :param factor_name: 表内因子字段名
        :param start_date:  初始日期
        '''
        self.factor_tablename = factor_tablename  # 因子所在表名
        self.sql_sentence_factor = ''  # 初始化因子sql
        # self.start_date = start_date  # 数据开始日期
        self.frequency = frequency
        self.daterange = daterange

    def create_sql_sentence(self):
        if self.frequency == 1 or self.frequency == 2:
            adding1 = ' where tradingday >= to_date(\''+self.daterange[0]+' 00:00:00'+'\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'
            adding2 = ' and tradingday <= to_date(\''+self.daterange[1]+' 00:00:00'+'\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'
            self.sql_sentence_factor = 'select *'+'from '+self.factor_tablename +adding1+adding2  #不加order by，拖慢速度
        elif self.frequency == 3:
            adding1 = ' where STARTDAY >= to_date(\''+self.daterange[0]+' 00:00:00'+'\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'
            adding2 = ' and STARTDAY <= to_date(\''+self.daterange[1]+' 00:00:00'+'\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'

            self.sql_sentence_factor = 'select *'+'from '+self.factor_tablename +adding1+adding2  # 不加order by，拖慢速度

    def InputDataPreprocess(self):
        data1 = dbsynchelper()

        # 从数据库提取出数据，注意输出格式是list
        # ValuationDataset = []
        factor_data = data1.select_detail(ip='192.168.1.187', user='jydb', pwd='jydb', database='JYDB', sql=self.sql_sentence_factor)
        factor_data = pd.DataFrame(factor_data)

        return factor_data


# if __name__ == '__main__':
#     import time
#     aa = dbData_import('dailyvaluefactor','PE','2018-01-01')
#     aa.create_sql_sentence()
#     time_start = time.time()
#     res = aa.InputDataPreprocess()
#     time_end = time.time()
#     print('time cost', time_end - time_start, 's')
#     aa.sql_sentence