# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/4/29  16:53
desc:
'''
import pandas as pd


class TurnoverFunc(object):
    """
     window等窗口数据为月份数，每个月交易日为20
     注意检查数据类型,满足足够的数据长度
    日频的window=[1,3,6]
    """

    def __init__(self,turnover,dailypct, periodcoef, window):
        '''
        :param turnover: 日换手率序列
        :param dailypct: 日收益率序列
        '''
        self.turnover = turnover
        self.dailypct = dailypct
        self.window = window  # 月份数
        self.periodcoef = periodcoef  # 周期系数，一个月20个交易日

    def meanTurnover(self):  # 月份数
        '''
        :param window: 滚动窗口
        :return: 日均换手率
        '''
        res1 = pd.DataFrame(index=[])
        for i in self.window:
            # res1 = pd.concat([res1, pd.rolling_mean(self.turnover,i*self.periodcoef)],axis=1)  # 前i*20-1的数据为NaN
            res1 = pd.concat([res1, pd.DataFrame(self.turnover).rolling(window=i*self.periodcoef).mean()],axis=1)  # 前i*20-1的数据为NaN
        return res1

    def meanchgTurnover(self):  # 月份数
        '''
        :param short_win:
        :param long_win: 长窗口周期
        :return: 换手率相对变化
        '''
        if self.periodcoef == 20 or self.periodcoef==4:
            long_win = 12
        elif self.periodcoef ==1:
            long_win = 24

        res1 =pd.DataFrame(index=[])
        for i in self.window:
            # temp = (pd.rolling_mean(self.turnover, i*self.periodcoef)/pd.rolling_mean(self.turnover,long_win*self.periodcoef))-1
            temp = (pd.DataFrame(self.turnover).rolling(window=i*self.periodcoef).mean()/pd.DataFrame(self.turnover).rolling(window=long_win*self.periodcoef).mean())-1
            res1 = pd.concat([res1, temp], axis=1)
        return res1

    def stdTurnover(self):
        '''
        :param window:
        :return:滚动标准差
        '''
        res1 = pd.DataFrame(index=[])
        for i in self.window:
            res1 = pd.concat([res1, pd.DataFrame(self.turnover).rolling(window=i*self.periodcoef).std()],axis=1)  # 前i*20-1的数据为NaN
        return  res1

    def stdchgTurnover(self):
        if self.periodcoef ==20 or self.periodcoef==4:
            long_win = 12
        elif self.periodcoef == 1:
            long_win = 24
        res1 =pd.DataFrame(index=[])
        for i in self.window:
            n = pd.Series(self.turnover.values).rolling(window=i*self.periodcoef).std()
            d = pd.Series(self.turnover).rolling(window=long_win*self.periodcoef).std()
            temp = (n/d)-1
            res1 = pd.concat([res1,temp],axis=1)
        return res1

    def expwgtTurnover(self):
        '''
        :param window:
        :return:日换手率乘日收益率指数加权平均
        '''
        res1 = pd.DataFrame(index=[])
        for j in self.window:
            # res1 = pd.concat([res1, pd.DataFrame(pd.ewma(self.turnover.values*self.dailypct.values,span=j*self.periodcoef))],axis=1)  # 前i*20-1的数据为NaN
            res1 = pd.concat([res1, pd.DataFrame(self.turnover.values*self.dailypct.values).ewm(span=j*self.periodcoef).mean()],axis=1)  # 前i*20-1的数据为NaN

        return res1


