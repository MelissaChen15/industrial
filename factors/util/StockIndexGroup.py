# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/4/30  9:22
desc:
'''
# InnerCode 沪深300:3145
# InnerCode 中证500:4978
# InnerCode 上证50 : 46
from factors.sql import pl_sql_oracle
import datetime
import pandas as pd
# 计算日频或者周频的指数收益率


def StockIndexdataCal(code_sql_file_path):
    '''
    :param code_sql_file_path: 股票指数相关数据的sql语句路径
    :return:
    '''
    sql = pl_sql_oracle.dbData_import()
    s1 = sql.InputDataPreprocess(code_sql_file_path, ['StockIndexIF','StockIndexIC','StockIndexIH'], )  # 指数数据
    return s1

def getWeekTradingDay(code_sql_file_path):
    sql = pl_sql_oracle.dbData_import()
    s1 = sql.InputDataPreprocess(code_sql_file_path, ['TradingDayWeek'],secucode='and (t1.TradingDate <= to_date(\'' + datetime.datetime.now().date().strftime(
                    '%Y-%m-%d') + ' 00:00:00' + '\'' + ',' + '\'yyyy-mm-dd hh24:mi:ss\'' + ')' + ')')  #  作为表名会进行变量赋值，必须是合格的变量字符串
    return s1

def dailyToweek(dailydata,weekday_sql_file_path):
    '''
    :param dailydata: 指数日频数据
    :param code_sql_file_path: 周频交易日序列的sql语句路径
    :return:
    '''
    s1 = getWeekTradingDay(weekday_sql_file_path)  # s1 is a dict which keys equal to tablename in pl_sql_oracle
    weekdata = dailydata[dailydata['TRADINGDAY'].isin(s1['TradingDayWeek']['TRADINGDATE'])]
    weekdata = weekdata.reset_index(drop=True)
    weeklyreturn = ((weekdata['CLOSEPRICE']-weekdata['CLOSEPRICE'].shift())/weekdata['CLOSEPRICE'].shift())*100  # 保持单位与聚源数据一致
    weeklyreturn.index = weekdata['TRADINGDAY']
    return weeklyreturn

class StockIndexGroup(object):

    def __init__(self,flag,code_sql_file_path,weekday_sql_file_path):
        '''
        :param HS300ChangePCT: 沪深300指数日涨跌幅
        :param SZ50ChangePCT: 上证50
        :param ZZ500ChangePCT: 中证500
        '''
        if flag ==1:
            self.indexdata = StockIndexdataCal(code_sql_file_path)
            self.HS300ChangePCT = self.indexdata['StockIndexIF']['CHANGEPCT']
            self.HS300ChangePCT.index = self.indexdata['StockIndexIF']['TRADINGDAY']

            self.SZ50ChangePCT = self.indexdata['StockIndexIH']['CHANGEPCT']
            self.SZ50ChangePCT.index = self.indexdata['StockIndexIH']['TRADINGDAY']

            self.ZZ500ChangePCT = self.indexdata['StockIndexIC']['CHANGEPCT']
            self.ZZ500ChangePCT.index = self.indexdata['StockIndexIC']['TRADINGDAY']

            # self.SZZZChangePCT = SZZZChangePCT
            self.frequency = 1  #日频
        elif flag ==2:
            self.indexdata = StockIndexdataCal(code_sql_file_path)
            self.HS300ChangePCT = dailyToweek(self.indexdata['StockIndexIF'][['TRADINGDAY','CLOSEPRICE']],weekday_sql_file_path)  # 输出为周频
            self.SZ50ChangePCT = dailyToweek(self.indexdata['StockIndexIH'][['TRADINGDAY','CLOSEPRICE']],weekday_sql_file_path)
            self.ZZ500ChangePCT = dailyToweek(self.indexdata['StockIndexIC'][['TRADINGDAY','CLOSEPRICE']],weekday_sql_file_path)
            # self.SZZZChangePCT = dailyToweek(SZZZIndex)
            self.frequency = 2  # 周频


# if __name__ == '__main__':
#     code_sql_file_path = r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver3\factors\sql\sql_StockIndex.sql'
#     code_sql_file_path = r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver3\factors\sql\sql_get_last_trading_weekday.sql'
#
#     filepath = r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver3\factors\sql\sql_StockIndex.sql'
#
