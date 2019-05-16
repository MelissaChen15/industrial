# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/4/30  9:02
desc:
'''

from util.TurnoverFunc import TurnoverFunc


class MonthlyTurnoverProcess(TurnoverFunc):
    def __init__(self, turnover, dailypct, periodcoef, window):
        super().__init__(turnover, dailypct, periodcoef, window)
        self.frequency = 3