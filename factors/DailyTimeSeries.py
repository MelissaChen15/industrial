# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/16  16:25
desc:
'''
from factors.sql import pl_sql_oracle
from sqlalchemy import FLOAT


def write_SMB_HML_toDB():
    from factors.util.ClassicalFactorcal import TimeseriesFactorCal
    data_sql_file_path = r'.\sql\sql_classical_factor_rawdata.sql'
    code_sql_file_path = r'.\sql\sql_get_tradingday.sql'
    aa = TimeseriesFactorCal(data_sql_file_path, code_sql_file_path)
    SML_and_HML = aa.get_data_cal()
    SML_and_HML['TradingDay'] = SML_and_HML.index
    pl_sql_oracle.df_to_DB(SML_and_HML, 'dailytimeseries', if_exists='append',data_type={'SMB':FLOAT()})

def write_UMD_toDB():
    pass

if __name__ == '__main__':
    write_SMB_HML_toDB()
