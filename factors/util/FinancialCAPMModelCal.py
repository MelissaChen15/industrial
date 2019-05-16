# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/6  9:13
desc:
'''
import numpy as np
import pandas as pd
import pyfinance
# TODO: 注意SMB,HML的时间区间与设定的因子值的时间段不一样，保守起见，计算得到的SMB等数据时间从2002年初开始，需进行日期匹配。


def dataSTD(input_data):
    return input_data.std()


def upsideSTD(input_data):
    max_data = np.maximum(input_data,0)  # 小于0的值置为0
    temp1 = (np.sum(np.square(max_data)))/(max_data.shape[1]-1)
    res = (np.sqrt(temp1))
    return res


def downsideSTD(input_data):
    max_data = np.minimum(input_data, 0)  # 大于0的值置为0
    temp1 = (np.sum(np.square(max_data))) / (max_data.shape[1] - 1)
    res = (np.sqrt(temp1))
    return res

# def diff_twosideSTD(input_data):
#     res1 = upsideSTD(input_data)  这种写法太浪费程序运行时间
#     res2 = downsideSTD(input_data)
#
#     return res1

class CAPM_ModelCal(object):
    # 计算常用因子模型的alpha ,beta,以及残差序列
    def __init__(self,StockIndex,ChangePCT,flag,rolling_window=[[3,6],[6,12]]):
        if flag == 1:
            self.StockIndex = StockIndex
            # self.SMB = SMB
            # self.HML = HML
            self.rolling_window = rolling_window[0]
            self.ChangePCT = ChangePCT
            self.periodcoef = 20  # 日频
        elif flag == 2:
            self.StockIndex = StockIndex
            # self.SMB = SMB
            # self.HML = HML
            self.rolling_window = rolling_window[1]
            self.ChangePCT = ChangePCT
            self.periodcoef = 4  # 周频

    def sideBeta(self):
        common_index = list(set(self.ChangePCT.index).intersection(set(self.StockIndex)))
        common_index.sort()
        data_y = self.ChangePCT[common_index]
        data_x = self.StockIndex[common_index]  # 匹配时间序列

        upsidebeta_all = dict()
        downsidebeta_all = dict()
        sidediffbeta_all = dict()
        for j in self.rolling_window:
            mean_data = data_x.rolling(self.periodcoef*j).apply(np.mean())
            # 判断一个数是否为nan,判断自己是否等于自己，注意nan是float
            upsidebeta = pd.DataFrame()
            downsidebeta = pd.DataFrame()
            sidediffbeta = pd.DataFrame()
            for i in range(len(mean_data)):
                if mean_data[i] == mean_data[i]: # 非nan情况
                    data1 = data_x[i-self.periodcoef*j+1:i+1]
                    data2 = data_y[i-self.periodcoef*j+1:i+1]
                    upsidedata1 = data1[data1>mean_data[i]]
                    upside_index = upsidedata1.index
                    upsidedata2 = data2[data2.index.isin(upside_index)]
                    upsidebeta_temp = np.cov(upsidedata1,upsidedata2)[0,1]/np.var(upsidedata1)
                    upsidebeta = upsidebeta.append()

                    downsidedata1 = data1[data1<mean_data[i]]
                    downside_index = downsidedata1.index
                    downsidedata2 = data2[data2.index.isin(downside_index)]
                    downsidebeta_temp = np.cov(downsidedata1,downsidedata2)[0,1]/np.var(downsidedata1)
                    downsidebeta = downsidebeta.append()

                    sidediffbeta = sidediffbeta.append(upsidebeta_temp-downsidebeta_temp)
                elif mean_data[i] != mean_data[i]:
                    upsidebeta = upsidebeta.append(np.nan)
                    downsidebeta = downsidebeta.append(np.nan)
                    sidediffbeta = sidediffbeta.append(np.nan)

                upsidebeta = upsidebeta.reset_index(drop=True)
                upsidebeta.index = list(mean_data.index)

                downsidebeta = downsidebeta.reset_index(drop=True)
                downsidebeta.index = list(mean_data.index)

                sidediffbeta = sidediffbeta.reset_index(drop=True)
                sidediffbeta.index = list(mean_data.index)
            upsidebeta_all['滚动窗口(月)'+str(j)] = upsidebeta
            downsidebeta_all['滚动窗口(月)'+str(j)] = downsidebeta
            sidediffbeta_all['滚动窗口(月)'+str(j)] = sidediffbeta

        return upsidebeta,downsidebeta,sidediffbeta

    #  残差单独拿出来算，这里没法滚动直接得出
    def CAPM_cal(self):
        alpha1_all = dict()
        beta_all = dict()
        import pyfinance
        common_index = list(set(self.ChangePCT.index).intersection(set(self.StockIndex)))
        common_index.sort()
        data_y = self.ChangePCT[common_index]
        data_x = self.StockIndex[common_index]  # 匹配时间序列

        for j in self.rolling_window:
            model = pyfinance.ols.PandasRollingOLS(data_y, data_x, window=self.periodcoef * j)  # 注意y必须在前面
            alpha1 = model.alpha
            beta1 = model.beta
            # alpha1 = alpha1.reset_index(drop=True)  # 注意索引重置
            # beta = beta.reset_index(drop=True)  # 注意索引重置
            alpha1_all['滚动窗口(月)'+str(j)] = alpha1  # 根据alpha1的初始索引可确定滚动的窗口长度
            beta_all['滚动窗口(月)'+str(j)] = beta1
        return alpha1_all, beta_all

    # 对于每个时间点，残差都是一个与窗口长度一致的序列，保存残差太耗内存，这里直接保存计算残差的相关统计量。
    # alpha1_all, beta_all = self.CAPM_cal()
    def residuals_model_cal(self,alpha1_all,beta_all):
        '''
        :param alpha1_all: 根据前面模型计算得到的alpha和beta
        :param beta_all:   模型可以是CAPM或者FF3等，carhart模型在此方法上面添加即可
        :return:
        '''
        periods = list(alpha1_all.keys())
        residuals_stats = dict()  # 存储不同窗口长度下的残差统计量
        for i in periods:
            alpha = alpha1_all[periods[i]]
            beta = beta_all[periods[i]]
            window_length = alpha.index[0] + 1  # 不同的数据加窗长度的初始索引不同

            std_resids = []
            upsideSTD_resids = []
            downsideSTD_resids = []
            diff_twosidesSTD = []
            skew_resids = []  # 偏度，三阶矩
            for j in alpha.index:
                data_y = self.ChangePCT[j-window_length+1:j+1]  # 取前不取后的
                data_x = self.StockIndex[j-window_length+1:j+1]
                alpha_j = alpha[alpha.index ==j].values
                beta_j = beta[beta.index ==j].values  # 转换成array进行矩阵运算
                residuals = data_y.values - (np.dot(beta_j,data_x.transpose())+alpha_j)  # 计算残差序列,type为array,shape必须是(1,数据长度)
                std_resids.append(dataSTD(residuals))  # 计算波动率
                up = upsideSTD(residuals)
                down = downsideSTD(residuals)
                upsideSTD_resids.append(up)  # 计算上行波动率
                downsideSTD_resids.append(down)  # 计算下行波动率
                diff_twosidesSTD.append(up-down)  # 上下波动率之差
                skew_resids.append(pd.DataFrame(residuals).skew()[0])  # 计算偏度
            residuals_stats[i] = pd.DataFrame([std_resids, upsideSTD_resids,downsideSTD_resids,diff_twosidesSTD,skew_resids]).transpose()
            residuals_stats[i].columns = ['波动率','上行波动率','下行波动率','上下波动率之差','偏度']
        return residuals_stats












