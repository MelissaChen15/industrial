# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/21  10:06
desc:
'''

from sql.dbsynchelper2 import dbsynchelper
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


class dbData_import_auxiliary(object):

    def __init__(self,auxiliary_tablename,auxiliary_name,daterange):
        '''
        :param auxiliary_name: # 辅助数据字段名  type:list   may not just one
        :param auxiliary_tablename: # 辅助数据所在表名
        :param start_date: # 数据开始日期 ,与factordata保持一致
        '''
        self.sql_sentence_auxiliary = ''  # 初始化辅助数据sql，比如涨跌幅，流通市值等
        self.auxiliary_tablename = auxiliary_tablename
        self.auxiliary_name = auxiliary_name
        self.daterange = daterange

    def create_sql_sentence(self):
        part1 = 'select t2.SecuCode, t1.TradingDay,'
        part1_2 ='  from '
        part2 = ' t1 inner join SecuMain t2 on t1.InnerCode = t2.InnerCode where(t2.SecuMarket = \'83\' or t2.SecuMarket = \'90\') and (t2.SecuCategory = 1) '
        adding1 = ' and tradingday >= to_date(\''+self.daterange[0]+' 00:00:00'+'\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'
        adding2 = ' and tradingday <= to_date(\''+self.daterange[1]+' 00:00:00'+'\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'
        strilize_aux = ','.join(self.auxiliary_name)
        self.sql_sentence_auxiliary = part1+strilize_aux+part1_2+self.auxiliary_tablename+part2 +adding1+adding2
        # print(self.sql_sentence_auxiliary)

    def InputDataPreprocess(self):
        data1 = dbsynchelper()

        # 从数据库提取出数据，注意输出格式是list
        # ValuationDataset = []
        auxiliary_data = data1.select_detail(ip='192.168.1.187', user='jydb', pwd='jydb', database='JYDB', sql=self.sql_sentence_auxiliary)
        auxiliary_data = pd.DataFrame(auxiliary_data)

        return auxiliary_data


# if __name__ == '__main__':
#     import time
#     aa = dbData_import_auxiliary('QT_Performance',['NegotiableMV','ChangePCT'],'2018-01-01')
#     aa.create_sql_sentence()
#     time_start = time.time()
#     res_aux = aa.InputDataPreprocess()
#     time_end = time.time()
#     print('time cost', time_end - time_start, 's')
