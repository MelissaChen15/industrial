# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/4/30  8:59
desc:
'''

from util.TurnoverFunc import TurnoverFunc


class WeeklyTurnoverProcess(TurnoverFunc):
    def __init__(self, turnover, dailypct, periodcoef, window):
        super().__init__(turnover, dailypct, periodcoef, window)
        self.frequency = 2  # weekly index
