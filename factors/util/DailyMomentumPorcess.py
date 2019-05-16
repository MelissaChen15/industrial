# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/6  8:46
desc:
'''
from util.MomentumFunc import MomentumFunc


class DailyMomentumProcess(MomentumFunc):
    def __init__(self,closePrice,TurnoverVolume,TurnoverRate,ChangePCT,HS300ChangePCT,SZ50ChangePCT,ZZ500ChangePCT,
                 SZZZChangePCT,flag,window,periodcoef):
        super().__init__(closePrice,TurnoverVolume,TurnoverRate,ChangePCT,HS300ChangePCT,SZ50ChangePCT,ZZ500ChangePCT,
                         SZZZChangePCT,flag,window,periodcoef)
        self.frequency = 1