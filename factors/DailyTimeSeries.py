# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/16  16:25
desc:
'''
from factors.sql import pl_sql_oracle
from sqlalchemy import Float
from factors.util.ClassicalFactorcal import TimeseriesFactorCal
import datetime


def get_name():
    return 'dailytimeseries'

def calculate_SMB_HML(daterange):
    data_sql_file_path = r'.\sql\sql_classical_factor_rawdata.sql'
    code_sql_file_path = r'.\sql\sql_get_tradingday.sql'
    aa = TimeseriesFactorCal(data_sql_file_path, code_sql_file_path, daterange)
    SML_and_HML = aa.get_data_cal()
    SML_and_HML['TradingDay'] = SML_and_HML.index
    return SML_and_HML


def write_UMD_toDB():
    pass

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore')

    # write_SMB_HML_toDB(daterange=['2001-01-01', datetime.date.today()], mode = 'print')
