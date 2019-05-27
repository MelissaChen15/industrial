# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/6  8:56
desc:
'''
import pandas as pd
import numpy as np


# 对于周频信号，那么输入数据本身也是周频。
class IdiosyncrasticFunc(object):

    def __init__(self,TotalMV,NegotiableMV,TurnoverVolume,ChangePCT,window,periodcoef):

        self.TotalMV = TotalMV  # 总市值
        self.NegotiableMV = NegotiableMV # 自由流通市值
        self.ChangePCT = ChangePCT  # 涨跌幅
        self.TurnoverVolume = TurnoverVolume  # 成交额
        self.window = window  # [1,3,6], [3,6,12]
        self.periodcoef = periodcoef # 20, 4

    def TotalMV_stock(self):  #  属性名和方法名不能相同，否则调用会出现混乱
        '''
        :return: 总市值
        '''
        return self.TotalMV

    def NegotiableMV_stock(self):
        '''
        :return: 流通市值
        '''
        return self.NegotiableMV

    def logNegotiableMV(self):
        '''
        :return: 对数流通市值
        '''
        return np.log(1+self.NegotiableMV)

    def rootNegotiableMV(self):
        '''
        :return: 流通市值平方根
        '''
        return np.sqrt(self.NegotiableMV)

    def return_skew(self):
        from scipy import stats
        res1 = pd.DataFrame(index=[])
        for i in self.window:
            res1 = pd.concat([res1,self.ChangePCT.rolling(self.periodcoef*i).apply(stats.skew) ],axis=1)
        return res1  # 会有NaN

    def max_return(self):
        res1 = pd.DataFrame(index=[])
        for i in self.window:
            res1 = pd.concat([res1,self.ChangePCT.rolling(self.periodcoef*i).apply(max) ],axis=1)
        return res1  # 会有NaN

    def illqurisk(self):
        return np.abs(self.ChangePCT)/self.TurnoverVolume
