#-*- coding: UTF-8 -*-
from queue import Queue
import threading,sys
from time import ctime,sleep
import time
import datetime
from  decimal import Decimal
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import math

def performance_calculation(Inputdata,dateseries):
    Inputdata=pd.DataFrame(Inputdata)
    interval_days= len(Inputdata)
    fund_number = Inputdata.columns.size
    interval_return = (Inputdata.iloc[-1, :] - Inputdata.iloc[0, :]) / Inputdata.iloc[0, :]  # 全区间累计收益率
    interval_return_year = (1 + interval_return) ** (12 / interval_days) - 1  # 全区间年化收益率

    max_drawback = []  # 最大回撤
    position_M = []
    position_N = []
    for i in range(fund_number):
        tempdata = []
        tempdata_index = np.zeros((len(dateseries), len(dateseries)))
        for j in range(interval_days):
            for k in range(interval_days):
                if k < j:
                    tempdata.append((Inputdata.iloc[j, i] - Inputdata.iloc[k, i]) / Inputdata.iloc[k, i])
                    tempdata_index[j][k] = (Inputdata.iloc[j, i] - Inputdata.iloc[k, i]) / Inputdata.iloc[k, i]
        raw, column = tempdata_index.shape
        position_m, position_n = divmod(tempdata_index.argmin(), column)  # 找到最大回撤对应的j，k
        position_M.append(position_m)
        position_N.append(position_n)
        max_drawback.append(min(tempdata))
    # max_drawback_recover_interval = []
    # for i in range(fund_number):
    #     store_index = []
    #     tempdata8 = Inputdata_original['ParentFund'][Inputdata_original['Date'].isin(dateseries)]
    #     tempdata8 = tempdata8.reset_index(drop=True)
    #     for j in range(interval_days):
    #         if (tempdata8[j] >= tempdata8[position_N[i]]) & (j > position_M[i]):  # 注意这里的减去1
    #             store_index.append(j)
    #     if store_index == []:
    #         recoverdays = 'NaN'
    #     else:
    #         recoverdays = min(store_index) - position_M[i]
    #     max_drawback_recover_interval.append(recoverdays)  # 最大回撤回补天数

    annual_volatility = Inputdata.std() * (math.sqrt(12 / interval_days))  # 年化波动率
    Sharpe = interval_return_year / annual_volatility  # 夏普比率

    # latter_data = Inputdata.iloc[1:, :]
    # former_data = Inputdata.iloc[0:-1, :]
    # latter_data = latter_data.reset_index(drop=True)
    # former_data = former_data.reset_index(drop=True)
    # yield_day = (latter_data - former_data) / former_data  # 日收益率数据；日单位净值增长率
    # yield_day4 = yield_day
    # yield_day4[yield_day4 >= 0] = 0
    # downside_std_interval = (((yield_day4 ** 2).apply(lambda x: x.sum(), axis=0)) / (len(yield_day4) - 1)) ** 0.5 * (250 ** 0.5)  # 下行标准差

    # yield_day2 = (latter_data - former_data) / former_data  # 日收益率数据；日单位净值增长率
    # yield_day3 = yield_day2 - ((0.015 + 0.02 + 1) ** (1 / 250) - 1)
    # yield_day3[yield_day3 >= 0] = 0
    # downside_risk = (((yield_day3 ** 2).apply(lambda x: x.sum(), axis=0)) / (len(yield_day3) - 1)) ** 0.5 * (250 ** 0.5)
    # sortino = (yield_day2.mean() - ((0.015 + 0.02 + 1) ** (1 / 250) - 1)) / downside_risk
    calmar = interval_return_year / abs(np.array(max_drawback))  # calmar

    Output_data_interval = pd.DataFrame([interval_return, interval_return_year, annual_volatility, Sharpe, pd.Series(max_drawback[0],index=Sharpe.index),calmar],
        index=['全区间累计收益率', '全区间年化收益率', '全区间年化波动率', '夏普比率', '最大回撤', 'Calmar' ])

    return Output_data_interval

def performance_cal_all(NetValue_combin1):
    asset_num=(NetValue_combin1.columns.size)-1
    asset_name2=list(NetValue_combin1.columns)[1:]
    for i in range(1,asset_num+1):
        Inputdata=NetValue_combin1.iloc[:,i]
        dateseries=NetValue_combin1['Date']
        Output_data_interval=performance_calculation(Inputdata,dateseries)
        writer = pd.ExcelWriter(asset_name2[i-1]+'绩效指标.xlsx')
        Output_data_interval.to_excel(writer, sheet_name=asset_name2[i-1], float_format='%.5f')  # float_format 控制精度
        writer.save()