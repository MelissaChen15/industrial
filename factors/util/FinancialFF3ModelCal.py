# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/8  10:31
desc:
'''
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
# T注意SMB,HML的时间区间与设定的因子值的时间段不一样，保守起见，计算得到的SMB等数据时间从2002年初开始，需进行日期匹配。


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

class FF3_ModelCal(object):
    # 计算常用因子模型的alpha ,beta,以及残差序列
    def __init__(self,StockIndex,SMB,HML,ChangePCT,flag,rolling_window=[[3,6],[6,12]]):
        if flag == 1:
            self.StockIndex = StockIndex
            self.SMB = SMB
            self.HML = HML
            self.rolling_window = rolling_window[0]
            self.ChangePCT = ChangePCT
            self.periodcoef = 20  # 日频
        elif flag == 2:
            self.StockIndex = StockIndex
            self.SMB = SMB
            self.HML = HML
            self.rolling_window = rolling_window[1]
            self.ChangePCT = ChangePCT
            self.periodcoef = 4  # 周频

    #  残差单独拿出来算，这里没法滚动直接得出
    def data_align(self):
        index_list = [self.StockIndex.index, self.HML.index, self.SMB.index, self.ChangePCT.index]
        common_index = list(set(index_list[0]).intersection(*index_list[1:]))  # 时间序列对齐
        common_index.sort()
        self.data_x = pd.concat([self.StockIndex[common_index], self.HML[common_index], self.SMB[common_index]], axis=1)  # 拼接自变量
        self.data_y = self.ChangePCT[common_index]

    def FF3_cal(self):
        alpha1_all = dict()
        beta_all = dict()

        for j in self.rolling_window:
            model = pyfinance.ols.PandasRollingOLS(self.data_y, self.data_x, window=self.periodcoef * j)  # 注意y必须在前面
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
            alpha = alpha1_all[i]
            beta = beta_all[i]
            window_length = self.periodcoef*int(i[-1])  # 不同的数据加窗长度的初始索引不同

            std_resids = []
            upsideSTD_resids = []
            downsideSTD_resids = []
            diff_twosidesSTD = []
            skew_resids = []  # 偏度，三阶矩
            for j in range(len(alpha.index)):
                data_y = self.data_y[j:j+window_length]  # 取前不取后的
                data_x = self.data_x[j:j+window_length]
                alpha_j = alpha[alpha.index == alpha.index[j]].values
                beta_j = beta[beta.index == alpha.index[j]].values  # 转换成array进行矩阵运算
                residuals = data_y.values - (np.dot(beta_j,data_x.values.reshape((beta_j.shape[1]),len(data_x)))+alpha_j[0])   # 计算残差序列,type为array,shape必须是(1,数据长度)
                std_resids.append(dataSTD(residuals))  # 计算波动率
                up = upsideSTD(residuals)
                down = downsideSTD(residuals)
                upsideSTD_resids.append(up)  # 计算上行波动率
                downsideSTD_resids.append(down)  # 计算下行波动率
                diff_twosidesSTD.append(up-down)  # 上下波动率之差
                skew_resids.append(pd.DataFrame(residuals).transpose().skew()[0])  # 计算偏度
            residuals_stats[i] = pd.DataFrame([std_resids, upsideSTD_resids,downsideSTD_resids,diff_twosidesSTD,skew_resids]).transpose()
            residuals_stats[i].columns = ['波动率','上行波动率','下行波动率','上下波动率之差','偏度']
            residuals_stats[i].index = alpha.index

        return residuals_stats












