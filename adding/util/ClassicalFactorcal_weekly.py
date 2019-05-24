# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/7  15:30
desc:
'''

# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/6  13:17
desc:
'''
# 计算SMB、HML、UMD等指标
# SMB = 1 / 3 * (SH + SM + SL) - 1 / 3 * (BH + BM + BL)
# HML = 1 / 2 * (SH + BH) - 1 / 2 * (SL + BL)
# UMD = 1 / 2 * U - 1 / 2 * D
from sql import pl_sql_oracle
import pandas as pd
import datetime


def GroupingStock_SMB(RawData):
    # TODO:write the logic
    RawData2 = RawData.sort_values(by = 'NEGOTIABLEMV',axis = 0,ascending = True)
    smallsize = RawData2[RawData2['NEGOTIABLEMV']<=RawData2['NEGOTIABLEMV'].quantile(0.5)]
    bigsize = RawData2[RawData2['NEGOTIABLEMV']>RawData2['NEGOTIABLEMV'].quantile(0.5)]
    def calpart(groupdata):
        BL = groupdata[groupdata['PB'] >= groupdata['PB'].quantile(0.7)]  # 注意是BP的前百分之三十
        BN = groupdata[(groupdata['PB'] < groupdata['PB'].quantile(0.7)) & (groupdata['PB'] > groupdata['PB'].quantile(0.3))]
        BH = groupdata[groupdata['PB'] <= groupdata['PB'].quantile(0.3)]  # 注意是BP的后百分之三十
        return BL,BN,BH
    BL, BN, BH = calpart(bigsize)
    SL, SN, SH = calpart(smallsize)

    SMB = ((SL['CHANGEPCTRW'].mean()+SN['CHANGEPCTRW'].mean()+SH['CHANGEPCTRW'].mean())/3)- \
    ((BL['CHANGEPCTRW'].mean()+BN['CHANGEPCTRW'].mean()+BH['CHANGEPCTRW'].mean())/3)  # 简单平均

    HML = (BH['CHANGEPCTRW'].mean()+SH['CHANGEPCTRW'].mean())/2 -(BL['CHANGEPCTRW'].mean()+SL['CHANGEPCTRW'].mean())
    res = pd.DataFrame([SMB ,HML]).transpose()
    res.columns = ['SMB','HML']  # 输出结果为百分数
    return res

# def GroupingStock_UMD(*inputdata):
#     # TODO:write the logic
#
#     res =
#     return res


class TimeseriesFactorCal_weekly(object):
    '''
    计算HML,SMB以及UMD，FF五因子的CMA以及RMW数据涉及财务报表，为季频数据，不采用FF5模型
    '''
    def __init__(self,data_sql_file_path,code_sql_file_path):
        '''
        :param data_sql_file_path: 原始数据sql文件路径
        :param code_sql_file_path: 交易日生成sql文件路径
        '''
        self.data_sql_file_path = data_sql_file_path
        self.code_sql_file_path = code_sql_file_path

    def get_data_cal(self):
        sql = pl_sql_oracle.dbData_import()

        s1 = sql.InputDataPreprocess(self.code_sql_file_path, ['TradingDayWeek'],
                                     secucode='and (t1.TradingDate <= to_date(\''+datetime.datetime.now().date().strftime('%Y-%m-%d')+' 00:00:00'+\
                                     '\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'+')') # TradingDay作为表名会进行变量赋值，必须是合格的变量字符串
        SML_and_HML = pd.DataFrame()
        for row in s1['TradingDayWeek'].itertuples(index=True, name='Pandas'):
            try:
                # sql = pl_sql_oracle.dbData_import()  getattr(row, 'TRADINGDAY')
                s2 = sql.InputDataPreprocess(self.data_sql_file_path, ['RawData'], secucode='and (t1.tradingday = to_date(\''+str(getattr(row, 'TRADINGDATE'))+\
                                                                             '\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'+')')
                SML_and_HML = SML_and_HML.append(GroupingStock_SMB(s2['RawData']))  # s2是一个字典形式
                # print(SML_and_HML)
                print(getattr(row, 'TRADINGDATE'), ' done')

            except Exception as e:

                print(getattr(row, 'TRADINGDATE'), e)
        SML_and_HML = SML_and_HML.reset_index(drop=True)
        SML_and_HML.index = list(s1['TradingDayWeek']['TRADINGDATE'][:len(SML_and_HML)])
        return SML_and_HML


# if __name__ == '__main__':
#     data_sql_file_path = r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver3\factors\sql\sql_classical_factor_rawdata_weekly.sql'
#     code_sql_file_path = r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver3\factors\sql\sql_get_last_trading_weekday.sql'
#     aa = TimeseriesFactorCal(data_sql_file_path,code_sql_file_path)
#     ddd = aa.get_data_cal()
#     print(ddd)
