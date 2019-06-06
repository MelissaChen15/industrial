# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/6/4  15:40
desc:
'''

from sql.dbsynchelper2 import dbsynchelper
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


class dbData_weekly_datetime(object):

    def __init__(self,date_tablename,start_date,end_date):
        '''
        :param auxiliary_name: # 辅助数据字段名  type:list   may not just one
        :param auxiliary_tablename: # 辅助数据所在表名
        :param start_date: # 数据开始日期 ,与factordata保持一致
        '''
        self.sql_sentence_auxiliary = ''  # 初始化辅助数据sql，比如涨跌幅，流通市值等
        self.date_tablename = date_tablename
        self.start_date = start_date
        self.end_date = end_date

    def create_sql_sentence(self):
        part1 = 'select TradingDate'
        part1_2 ='  from '
        part2 = ' where SecuMarket = 83 and IfWeekEnd = 1 and IfTradingDay = 1  '
        adding1 = ' and TradingDate >= to_date(\''+self.start_date+' 00:00:00'+'\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'
        adding2 = ' and TradingDate <= to_date(\''+self.end_date+' 00:00:00'+'\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'
        self.sql_sentence_auxiliary = part1+part1_2+self.date_tablename+part2 +adding1+adding2
        # print(self.sql_sentence_auxiliary)

    def InputDataPreprocess(self):
        data1 = dbsynchelper()

        # 从数据库提取出数据，注意输出格式是list
        # ValuationDataset = []
        auxiliary_data = data1.select_detail(ip='192.168.1.187', user='jydb', pwd='jydb', database='JYDB', sql=self.sql_sentence_auxiliary)
        auxiliary_data = pd.DataFrame(auxiliary_data)

        return auxiliary_data