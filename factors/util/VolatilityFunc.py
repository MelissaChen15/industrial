# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/9  15:43
desc:
'''
import pandas as pd
import numpy as np


class VolatilityFunc(object):
    def __init__(self,ClosePrice,high,low,ChangePCT,periodcoef, window,TurnoverVolume,turnover):
        self.ClosePrice = ClosePrice  # 收盘价
        self.high = high  # 最高价
        self.low = low  # 最低价
        self.periodcoef = periodcoef  # 周期系数，一个月20个交易日
        self.window = window
        self.TurnoverVolume = TurnoverVolume  # 成交额
        self.turnover = turnover  # 换手率
        self.ChangePCT = ChangePCT

    def return_std(self):
        res = pd.DataFrame(index=[])
        for j in self.window:
            res = pd.concat([res,self.ChangePCT.rolling(self.periodcoef*j).apply(np.std)],axis=1)
        return res

    def turnover_std(self):
        res = pd.DataFrame(index=[])
        for j in self.window:
            res = pd.concat([res,self.turnover.rolling(self.periodcoef*j).apply(np.std)],axis=1)
        return res

    def turnover_volume_std(self):
        res = pd.DataFrame(index=[])
        for j in self.window:
            res = pd.concat([res,self.TurnoverVolume.rolling(self.periodcoef*j).apply(np.std)],axis=1)
        return res

    def high_low_std_part1(self):
        j = self.window[0]
        ChangePrice1 = (self.high-self.ClosePrice.shift())/self.ClosePrice.shift()
        ChangePrice2 = (self.low-self.ClosePrice.shift())/self.ClosePrice.shift()
        std1 = ChangePrice1.rolling(j*self.periodcoef).apply(np.std)
        std2 = ChangePrice2.rolling(j*self.periodcoef).apply(np.std)
        diff_std1 = std1-std2
        diff_std2 = std1+std2
        res1 = pd.concat([std1,std2,diff_std1,diff_std2],axis=1)
        return res1

    def high_low_std_part2(self):
        j = self.window[1]
        ChangePrice1 = (self.high-self.ClosePrice.shift())/self.ClosePrice.shift()
        ChangePrice2 = (self.low-self.ClosePrice.shift())/self.ClosePrice.shift()
        std1 = ChangePrice1.rolling(j*self.periodcoef).apply(np.std)
        std2 = ChangePrice2.rolling(j*self.periodcoef).apply(np.std)
        diff_std1 = std1-std2
        diff_std2 = std1+std2
        res1 = pd.concat([std1,std2,diff_std1,diff_std2],axis=1)
        return res1

    def high_low_std_part3(self):
        j = self.window[2]
        ChangePrice1 = (self.high-self.ClosePrice.shift())/self.ClosePrice.shift()
        ChangePrice2 = (self.low-self.ClosePrice.shift())/self.ClosePrice.shift()
        std1 = ChangePrice1.rolling(j*self.periodcoef).apply(np.std)
        std2 = ChangePrice2.rolling(j*self.periodcoef).apply(np.std)
        diff_std1 = std1-std2
        diff_std2 = std1+std2
        res1 = pd.concat([std1,std2,diff_std1,diff_std2],axis=1)
        return res1