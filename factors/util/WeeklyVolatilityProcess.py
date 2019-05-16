# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/9  17:03
desc:
'''
from util import VolatilityFunc


class WeeklyVolatilityProcess(VolatilityFunc):

    def __init__(self,ClosePrice,high,low,ChangePCT,periodcoef, window,TurnoverVolume,turnover):
        super().__init__(ClosePrice,high,low,ChangePCT,periodcoef, window,TurnoverVolume,turnover)
        self.frequency = 2