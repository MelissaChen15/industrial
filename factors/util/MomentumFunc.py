# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/4/30  9:06
desc:
'''
import pandas as pd
from util.StockIndexGroup import StockIndexGroup

# np.average(input_y, weights=data1)
# input_y = pd.DataFrame(np.random.random(200))
# data1 = pd.DataFrame(np.arange(200))
# mad = lambda x: (x[-1]-x[0])/x[0]
# input_y = input_y.rolling(5)
#
# pd.DataFrame(np.average(input_y,weights=data1))
#
# input_y.rolling(20).apply(funcavr,args=data1.rolling(20))


class MomentumFunc(StockIndexGroup):
    # TODO :注意数据单位
    # TODO :注意flag变量
    # TODO :回归时出现NaN会报错
    def __init__(self,closePrice,TurnoverVolume,TurnoverRate,ChangePCT,flag,code_sql_file_path,
                 window,periodcoef):
        '''
        # 对于日频，window = [1,3,6,12]
        :param closePrice:
        :param TurnoverVolume:
        :param TurnoverRate:
        :param flag: 指示标志，日频==1；周频==2；
        '''
        super().__init__(flag,code_sql_file_path)
        self.closePrice = closePrice  # 股票收盘价
        self.TurnoverVolume = TurnoverVolume  # 成交量（万股）
        self.TurnoverRate = TurnoverRate  # 换手率（%）
        self.window = window  # 月份数
        self.periodcoef = periodcoef  # 周期系数，一个月20个交易日
        self.ChangePCT = ChangePCT  # 日涨跌幅

    def PriceMomentum(self):
        res1 = pd.DataFrame(index=[])
        func1 = lambda x: (x[-1] - x[0]) / x[0]
        for j in self.window:
            temp = self.closePrice.rolling(j*self.periodcoef).apply(func1)
            res1 = pd.concat([res1, temp],axis=1)
        return res1

    def volumneMomentum(self,short_per = 1,long_per = 3):
        res1 = pd.DataFrame(index=[])
        part1 = self.TurnoverVolume.rolling(short_per*self.periodcoef).mean()
        part2 = self.TurnoverVolume.rolling(long_per*self.periodcoef).mean()
        res1 = pd.concat([res1,part1/part2],axis=1)
        return res1

    def TurnoverRateMomentum(self,short_per = 1,long_per = 3):
        res1 = pd.DataFrame(index=[])
        part1 = self.TurnoverRate.rolling(short_per*self.periodcoef).mean()
        part2 = self.TurnoverRate.rolling(long_per*self.periodcoef).mean()
        res1 = pd.concat([res1,part1/part2],axis=1)
        return res1

    def HLPriceMomentum(self,window_short = [0.25, 1, 3, 6],window_long = [3, 3, 3, 6]):
        # 高低价动量
        res1 = pd.DataFrame(index=[])
        for j in range(len(window_short)):
            part1 = self.closePrice.rolling(window_short[j]*self.periodcoef).max()
            part2 = self.closePrice.rolling(window_long[j]*self.periodcoef).min()
            res1 = pd.concat([res1,part1/part2],axis=1)
        return res1

    def alpha_create(self,window_alpha = 6):

        res1 = pd.DataFrame(index=[])
        import pyfinance
        input_y = [self.HS300ChangePCT,self.ZZ500ChangePCT,self.SZ50ChangePCT,self.SZZZChangePCT]
        for i in input_y:
            model = pyfinance.ols.PandasRollingOLS(self.ChangePCT,i, window=self.periodcoef*window_alpha)  # 注意y必须在前面
            alpha1 = model.alpha
            alpha1 = alpha1.reset_index(drop=True)  # 注意索引重置
            res1 = pd.concat([res1,alpha1],axis=1)

    def momentumchg(self,window_short=[0.25,1,3,6]):
        #  动量变化
        res1 = pd.DataFrame(index=[])
        func1 = lambda x: (x[-1] - x[0]) / x[0]
        for j in window_short:
            part1 = self.closePrice.rolling(j*self.periodcoef).apply(func1)
            part2 = self.closePrice.rolling(j*self.periodcoef*2).apply(func1)
            res1 = pd.concat([res1,((part1+1)-(part2+1/(part1+1)))])
        return res1













