# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/10  8:55
desc:
'''
import pandas as pd
from util.StockIndexGroup import StockIndexGroup
import numpy as np

class CorrelationFunc(StockIndexGroup):

    def __init__(self,ChangePCT,periodcoef,window,flag,code_sql_file_path):
        super().__init__(flag,code_sql_file_path)  # path是指数数据的路径
        self.periodcoef = periodcoef  # 周期系数，一个月20个交易日
        self.window = window
        self.ChangePCT = ChangePCT

    def CorrelationToIndex(self):
        correaltion_all = pd.DataFrame()
        for j in self.window:
            rolling_length = j * self.periodcoef
            correaltion_cal = pd.DataFrame()
            for i in range(len(self.ChangePCT)):
                if (i+1) < rolling_length:
                    res_all = [np.nan, np.nan, np.nan]
                    correaltion_cal = correaltion_cal.append(pd.DataFrame(res_all).transpose())
                elif (i+1) >= rolling_length:
                    stockPCT = self.ChangePCT[i+1-rolling_length:i+1]
                    indexPCT1 = self.HS300ChangePCT[i+1-rolling_length:i+1]
                    indexPCT2 = self.SZ50ChangePCT[i+1-rolling_length:i+1]
                    indexPCT3 = self.ZZ500ChangePCT[i+1-rolling_length:i+1]
                    res_all = [stockPCT.corr(indexPCT1), stockPCT.corr(indexPCT2), stockPCT.corr(indexPCT3)]
                    correaltion_cal = correaltion_cal.append(pd.DataFrame(res_all).transpose())
            correaltion_cal.columns = ['corrIF'+'_'+str(j)+'m','corrIH'+'_'+str(j)+'m','corrIC'+'_'+str(j)+'m']
            correaltion_all = pd.concat([correaltion_all,correaltion_cal],axis=1)
        return correaltion_all

    def CorrelationDiffToIndex(self):
        correaltiondiff_all = pd.DataFrame()
        for j in self.window:
            rolling_length = j * self.periodcoef * 2  # 计算差值，所需数据是原来的两倍
            correaltiondiff_cal = pd.DataFrame()
            for i in range(len(self.ChangePCT)):
                if (i+1) <rolling_length:
                    res_all = [np.nan, np.nan, np.nan]
                    correaltiondiff_cal = correaltiondiff_cal.append(pd.DataFrame(res_all).transpose())
                elif (i+1) >= rolling_length:
                    stockPCT_1 = self.ChangePCT[i+1-rolling_length:i+1-rolling_length*0.5]
                    stockPCT_2 = self.ChangePCT[i+1-rolling_length*0.5:i+1]

                    indexPCT1_1 = self.HS300ChangePCT[i+1-rolling_length:i+1-rolling_length*0.5]
                    indexPCT1_2 = self.HS300ChangePCT[i+1-rolling_length*0.5:i+1]
                    indexPCT2_1 = self.SZ50ChangePCT[i+1-rolling_length:i+1-rolling_length*0.5]
                    indexPCT2_2 = self.SZ50ChangePCT[i+1-rolling_length*0.5:i+1]
                    indexPCT3_1 = self.ZZ500ChangePCT[i+1-rolling_length:i+1-rolling_length*0.5]
                    indexPCT3_2 = self.ZZ500ChangePCT[i+1-rolling_length*0.5:i+1]

                    res1 = abs(stockPCT_2.corr(indexPCT1_2) -stockPCT_1.corr(indexPCT1_1))
                    res2 = abs(stockPCT_2.corr(indexPCT2_2) -stockPCT_1.corr(indexPCT2_1))
                    res3 = abs(stockPCT_2.corr(indexPCT3_2) -stockPCT_1.corr(indexPCT3_1))
                    res_all = [res1,res2,res3]
                    correaltiondiff_cal = correaltiondiff_cal.append(pd.DataFrame(res_all).transpose())
            correaltiondiff_cal.columns = ['corrIFchg' + '_' + str(j) + 'm', 'corrIHchg' + '_' + str(j) + 'm', 'corrICchg' + '_' + str(j) + 'm']
            correaltiondiff_all = pd.concat([correaltiondiff_all, correaltiondiff_cal], axis=1)
        return correaltiondiff_all




























