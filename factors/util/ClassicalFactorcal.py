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
from factors.sql import pl_sql_oracle
import pandas as pd
import datetime


def GroupingStock_SMB(RawData,Changpct_data):
    RawData2 = RawData.sort_values(by = 'NEGOTIABLEMV',axis = 0,ascending = True)
    smallsize = RawData2[RawData2['NEGOTIABLEMV']<=RawData2['NEGOTIABLEMV'].quantile(0.5)]
    bigsize = RawData2[RawData2['NEGOTIABLEMV']>RawData2['NEGOTIABLEMV'].quantile(0.5)]

    def calpart(groupdata):
        BL = groupdata[groupdata['PB'] >= groupdata['PB'].quantile(0.7)]  # 注意是BP的从小到大前百分之三十
        BN = groupdata[(groupdata['PB'] < groupdata['PB'].quantile(0.7)) & (groupdata['PB'] > groupdata['PB'].quantile(0.3))]
        BH = groupdata[groupdata['PB'] <= groupdata['PB'].quantile(0.3)]  # 注意是BP的后百分之三十
        return BL,BN,BH
    BL, BN, BH = calpart(bigsize)
    SL, SN, SH = calpart(smallsize)

    # SMB = ((SL['CHANGEPCT'].mean()+SN['CHANGEPCT'].mean()+SH['CHANGEPCT'].mean())/3)- \
    # ((BL['CHANGEPCT'].mean()+BN['CHANGEPCT'].mean()+BH['CHANGEPCT'].mean())/3)  # 简单平均

    target_data_SL = Changpct_data[Changpct_data['SECUCODE'].isin(SL['SECUCODE'])]['CHANGEPCT']
    target_data_SN = Changpct_data[Changpct_data['SECUCODE'].isin(SN['SECUCODE'])]['CHANGEPCT']
    target_data_SH = Changpct_data[Changpct_data['SECUCODE'].isin(SH['SECUCODE'])]['CHANGEPCT']
    target_data_BL = Changpct_data[Changpct_data['SECUCODE'].isin(BL['SECUCODE'])]['CHANGEPCT']
    target_data_BN = Changpct_data[Changpct_data['SECUCODE'].isin(BN['SECUCODE'])]['CHANGEPCT']
    target_data_BH = Changpct_data[Changpct_data['SECUCODE'].isin(BH['SECUCODE'])]['CHANGEPCT']

    SMB = ((target_data_SL.mean()+target_data_SN.mean()+target_data_SH.mean())/3) - \
    ((target_data_BL.mean()+target_data_BN.mean()+target_data_BH.mean())/3)  # 简单平均

    HML = (target_data_BH.mean()+target_data_SH.mean())/2 -(target_data_BL.mean()+target_data_SL.mean())/2
    res = pd.DataFrame([SMB ,HML]).transpose()
    res.columns = ['SMB','HML']  # 输出结果为百分数
    return res

# def GroupingStock_UMD(*inputdata):
#
#     res =
#     return res


class TimeseriesFactorCal(object):
    '''
    计算HML,SMB以及UMD，FF五因子的CMA以及RMW数据涉及财务报表，为季频数据，不采用FF5模型
    '''
    def __init__(self,data_sql_file_path,code_sql_file_path, daterange):
        '''
        :param data_sql_file_path: 原始数据sql文件路径
        :param code_sql_file_path: 交易日生成sql文件路径
        '''
        self.data_sql_file_path = data_sql_file_path
        self.code_sql_file_path = code_sql_file_path
        self.daterange = daterange
        for i in [0, 1]:
            if type(self.daterange[i]) == datetime.date: self.daterange[i] = self.daterange[i].strftime("%Y-%m-%d")

    def get_data_cal(self):
        sql = pl_sql_oracle.dbData_import()
        date =  ' TRADINGDAY <= to_date( \'' + self.daterange[1] + '\',\'yyyy-mm-dd\')' \
                         + 'and TRADINGDAY >= to_date( \'' + self.daterange[0] + '\',\'yyyy-mm-dd\')'
        s1 = sql.InputDataPreprocess(self.code_sql_file_path, ['TradingDay'],date=date)

        SML_and_HML = pd.DataFrame()

        s1['TradingDay'] = s1['TradingDay'].sort_values(by='TRADINGDAY')
        # print(s1['TradingDay'])
        for row in s1['TradingDay'].itertuples(index=True, name='Pandas'):
            try:
                if getattr(row,'Index') == s1['TradingDay'].index[0]:
                    continue
                else:
                    # sql = pl_sql_oracle.dbData_import()  getattr(row, 'TRADINGDAY')
                    s2 = sql.InputDataPreprocess(self.data_sql_file_path, ['RawData'], date='and (t1.tradingday = to_date(\''+str(getattr(row, 'TRADINGDAY'))+\
                                                                                 '\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'+')')

                    last_data = s1['TradingDay'][s1['TradingDay'].index == (getattr(row, 'Index') - 1)]['TRADINGDAY']  # 取下一期的日期

                    s2_2 = sql.InputDataPreprocess(self.data_sql_file_path, ['RawData'], date='and (t1.tradingday = to_date(\''+str(last_data.values)[2:12]+' 00:00:00'+\
                                                                                 '\''+','+'\'yyyy-mm-dd hh24:mi:ss\''+')'+')')

                    s2['RawData'][['CLOSEPRICE','NEGOTIABLEMV', 'CHANGEPCT','PB']] = s2['RawData'][['CLOSEPRICE','NEGOTIABLEMV', 'CHANGEPCT','PB']].astype('float')

                    s2_2['RawData'][['CLOSEPRICE','NEGOTIABLEMV', 'CHANGEPCT','PB']] = s2_2['RawData'][['CLOSEPRICE','NEGOTIABLEMV', 'CHANGEPCT','PB']].astype('float')

                    # s2['RawData'] = s2['RawData'].astype('float')
                    SML_and_HML = SML_and_HML.append(GroupingStock_SMB(s2_2['RawData'],s2['RawData']))  # s2是一个字典形式

                print(getattr(row, 'TRADINGDAY'), ' done')  # 查看
            #
            except Exception as e:

                print(getattr(row, 'TRADINGDAY'), e)
        SML_and_HML = SML_and_HML.reset_index(drop=True)
        SML_and_HML.index = list(s1['TradingDay']['TRADINGDAY'][1:(len(SML_and_HML)+1)])  # s1是一个字典
        return SML_and_HML
