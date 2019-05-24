# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/17  9:28
desc:
'''

from sql import pl_sql_oracle
from sqlalchemy import String, Integer,DateTime,FLOAT
import pandas as pd


def write_SMB_HML_toDB():
    from util.ClassicalFactorcal_weekly import TimeseriesFactorCal_weekly
    data_sql_file_path = r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver3\factors\sql\sql_classical_factor_rawdata_weekly.sql'
    code_sql_file_path = r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver3\factors\sql\sql_get_last_trading_weekday.sql'
    aa = TimeseriesFactorCal_weekly(data_sql_file_path, code_sql_file_path)
    SML_and_HML = aa.get_data_cal()
    SML_and_HML['TradingDay'] = SML_and_HML.index
    # TODO: 表名必须是小写
    pl_sql_oracle.df_to_DB(SML_and_HML, 'weeklytimeseries', if_exists='append', data_type={'SMB':FLOAT()})


def write_UMD_toDB():
    pass

if __name__ == '__main__':
    write_SMB_HML_toDB()