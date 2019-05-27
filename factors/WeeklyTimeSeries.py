# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/17  9:28
desc:
'''

from factors.sql import pl_sql_oracle
from sqlalchemy import String, Integer,DateTime,FLOAT
from factors.util.ClassicalFactorcal_weekly import TimeseriesFactorCal_weekly

import pandas as pd

def get_name():
    return 'weeklytimeseries'

def calculate_SMB_HML(daterange):
    data_sql_file_path = r'.\sql\sql_classical_factor_rawdata_weekly.sql'
    code_sql_file_path = r'.\sql\sql_get_last_trading_weekday.sql'
    aa = TimeseriesFactorCal_weekly(data_sql_file_path, code_sql_file_path, daterange)
    SML_and_HML = aa.get_data_cal()
    SML_and_HML['TradingDay'] = SML_and_HML.index
    return SML_and_HML


def write_UMD_toDB():
    pass

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore')

    # write_SMB_HML_toDB()