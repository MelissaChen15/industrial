# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/10  8:55
desc:
'''
import pandas as pd
from factors.util.StockIndexGroup import StockIndexGroup
import numpy as np


def DateAlignment(ChangePCT,HS300ChangePCT,ZZ500ChangePCT,SZ50ChangePCT):
    datagroup = [ChangePCT.index, HS300ChangePCT.index, ZZ500ChangePCT.index, SZ50ChangePCT.index]
    common_index = list(set(datagroup[0]).intersection(*datagroup[1:]))
    common_index.sort()
    ChangPCT_com = ChangePCT[common_index]
    HS300ChangePCT_com = HS300ChangePCT[common_index]
    ZZ500ChangePCT_com = ZZ500ChangePCT[common_index]
    SZ50ChangePCT_com = SZ50ChangePCT[common_index]

    return common_index,ChangPCT_com, HS300ChangePCT_com, ZZ500ChangePCT_com, SZ50ChangePCT_com


class CorrelationFunc(StockIndexGroup):

    def __init__(self,ChangePCT,Tradingday,periodcoef,window,flag,code_sql_file_path,weekday_sql_file_path):
        # Tradingday指示个股数据的时间戳，用于与指数时间戳进行匹配
        super().__init__(flag,code_sql_file_path,weekday_sql_file_path)  # path是指数数据的路径
        self.periodcoef = periodcoef  # 周期系数，一个月20个交易日
        self.window = window
        self.ChangePCT = ChangePCT
        self.ChangePCT.index = Tradingday

    def _common_dateIndex(self):
        datagroup = [self.ChangePCT.index, self.HS300ChangePCT.index, self.ZZ500ChangePCT.index, self.SZ50ChangePCT.index]
        common_index = list(set(datagroup[0]).intersection(*datagroup[1:]))
        common_index.sort()
        return common_index

    def CorrelationToIndex(self):
        common_index,ChangPCT_com, HS300ChangePCT_com, ZZ500ChangePCT_com, SZ50ChangePCT_com = \
            DateAlignment(self.ChangePCT,self.HS300ChangePCT,self.ZZ500ChangePCT,self.SZ50ChangePCT)
        # print(len(common_index))
        correaltion_all = pd.DataFrame()
        for j in self.window:
            rolling_length = j * self.periodcoef
            correaltion_cal = pd.DataFrame()
            for i in range(len(ChangPCT_com)):
                if (i+1) < rolling_length:
                    res_all = [np.nan, np.nan, np.nan]
                    correaltion_cal = correaltion_cal.append(pd.DataFrame(res_all).transpose())
                elif (i+1) >= rolling_length:
                    stockPCT = ChangPCT_com[i+1-rolling_length:i+1]
                    indexPCT1 = HS300ChangePCT_com[i+1-rolling_length:i+1]
                    indexPCT2 = SZ50ChangePCT_com[i+1-rolling_length:i+1]
                    indexPCT3 = ZZ500ChangePCT_com[i+1-rolling_length:i+1]
                    res_all = [stockPCT.corr(indexPCT1), stockPCT.corr(indexPCT2), stockPCT.corr(indexPCT3)]
                    correaltion_cal = correaltion_cal.append(pd.DataFrame(res_all).transpose())
            correaltion_cal.columns = ['corrIF'+'_'+str(j)+'m','corrIH'+'_'+str(j)+'m','corrIC'+'_'+str(j)+'m']
            correaltion_all = pd.concat([correaltion_all,correaltion_cal],axis=1)
        correaltion_all.index = common_index
        return correaltion_all

    def CorrelationDiffToIndex(self):
        common_index,ChangPCT_com, HS300ChangePCT_com, ZZ500ChangePCT_com, SZ50ChangePCT_com = \
            DateAlignment(self.ChangePCT,self.HS300ChangePCT,self.ZZ500ChangePCT,self.SZ50ChangePCT)
        correaltiondiff_all = pd.DataFrame()
        for j in self.window:
            rolling_length = j * self.periodcoef * 2  # 计算差值，所需数据是原来的两倍
            correaltiondiff_cal = pd.DataFrame()
            for i in range(len(ChangPCT_com)):
                if (i+1) <rolling_length:
                    res_all = [np.nan, np.nan, np.nan]
                    correaltiondiff_cal = correaltiondiff_cal.append(pd.DataFrame(res_all).transpose())
                elif (i+1) >= rolling_length:
                    stockPCT_1 = ChangPCT_com[i+1-rolling_length:i+1-int(rolling_length*0.5)]
                    stockPCT_2 = ChangPCT_com[i+1-int(rolling_length*0.5):i+1]

                    indexPCT1_1 = HS300ChangePCT_com[i+1-rolling_length:i+1-int(rolling_length*0.5)]
                    indexPCT1_2 = HS300ChangePCT_com[i+1-int(rolling_length*0.5):i+1]
                    indexPCT2_1 = SZ50ChangePCT_com[i+1-rolling_length:i+1-int(rolling_length*0.5)]
                    indexPCT2_2 = SZ50ChangePCT_com[i+1-int(rolling_length*0.5):i+1]
                    indexPCT3_1 = ZZ500ChangePCT_com[i+1-rolling_length:i+1-int(rolling_length*0.5)]
                    indexPCT3_2 = ZZ500ChangePCT_com[i+1-int(rolling_length*0.5):i+1]

                    res1 = abs(stockPCT_2.corr(indexPCT1_2) -stockPCT_1.corr(indexPCT1_1))
                    res2 = abs(stockPCT_2.corr(indexPCT2_2) -stockPCT_1.corr(indexPCT2_1))
                    res3 = abs(stockPCT_2.corr(indexPCT3_2) -stockPCT_1.corr(indexPCT3_1))
                    res_all = [res1,res2,res3]
                    correaltiondiff_cal = correaltiondiff_cal.append(pd.DataFrame(res_all).transpose())
            correaltiondiff_cal.columns = ['corrIFchg' + '_' + str(j) + 'm', 'corrIHchg' + '_' + str(j) + 'm', 'corrICchg' + '_' + str(j) + 'm']
            correaltiondiff_all = pd.concat([correaltiondiff_all, correaltiondiff_cal], axis=1)
        correaltiondiff_all.index = common_index
        return correaltiondiff_all


# # # if __name__ == '__main__':
#     code_sql_file_path_index = r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver4\StockFactorsCreating\factors\sql\sql_StockIndex.sql'
#     weekday_sql_file_path = r'D:\项目\FOF相关资料\wind研报\工具性代码\Chen\industrial\factors_ver4\StockFactorsCreating\factors\sql\sql_get_last_trading_weekday.sql'
#     ex = CorrelationFunc(components['QT_Performance']['CHANGEPCT'],components['QT_Performance']['TRADINGDAY'], periodcoef=20,window=[1,3,6],
#                                 flag=1,code_sql_file_path=code_sql_file_path_index,weekday_sql_file_path=weekday_sql_file_path)


























