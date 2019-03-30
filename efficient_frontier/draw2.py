# __author__ = goldfish
# -*- coding: utf-8 -*-
# 2019/3/4 20:35
#
# |\____╭╭╭____/|
# |               | ╭---------╮
# |    ●     ●    | < Welcome~ |
# |  ≡    o    ≡  | ╰---------╯
# ╰--┬Ｏ◤▽◥Ｏ┬--╯
#

# tushare + matplotlib 绘制有效前沿
# http://f.dataguru.cn/thread-927164-1-1.html

import numpy as np
import pandas as pd
import tushare as ts
import os
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def get_data(code):  # code 为字符串，股票代码
    file = code + '.csv'
    if os.path.exists(file):  # 避免重复下载数据
        df = pd.read_csv(file)
    else:
        df = ts.get_k_data(code, ktype='D')  # 获取指定股票日数据，默认前复权
        df.to_csv(file)  # 将下载的数据保存为 csv 文件，以备下次使用
    return df.set_index('date')['close']  # 返回以日期为索引的收盘价

stocks = [
    '600211',  # 西藏药业
    '002035',  # 华帝股份
    '002695',  # 煌上煌
    '300364',  # 中文在线
    '300404',  # 博济医药
    '300520',  # 科大国创
    '600572']  # 康恩贝
noa = len(stocks)  # 股票数量，后面要用

def get_rtn(codes):  # codes 为股票代码的列表
    df = pd.DataFrame(columns=codes)  # 创建空的 df，并为每个股票代码创建一个空的列
    for code in codes:
        data = get_data(code)
        df[code] = data  # 汇总收盘价到对应列
    # 接上段，建议自备游标卡尺
    df = df.interpolate()  # 线性插值补齐停牌数据
    df = df.dropna()  # 丢弃起始与结尾无法补齐的部分
    return np.log((df/df.shift(1))[1:]) # 对数收益率


rtns = get_rtn(stocks)
rtns[-60:].plot()
plt.show()

exp_rtns = rtns.mean() * 252
exp_cov  = rtns.cov() * 252

def random_weights(noa):
    weights = np.random.random(noa)  # 生成组合中资产种类个随机数
    return weights / np.sum(weights)  # 使其和为 1，即组合中各资产的比重

port_returns = []  # 各组合的期望收益
port_risks = []  # 各组合的标准差
for p in range(10**5):  # 模拟十万次
    weights = random_weights(noa)
    port_returns.append(np.sum(exp_rtns*weights))
    port_risks.append(np.sqrt(np.dot(weights.T, np.dot(exp_cov, weights))))

port_returns = np.array(port_returns)
port_risks = np.array(port_risks)
plt.scatter(port_risks,port_returns,c=port_returns/port_risks,marker='.')
plt.grid(True)
plt.xlabel('excepted volatility')
plt.ylabel('expected return')
plt.colorbar(label = 'Sharpe ratio')
plt.show()







