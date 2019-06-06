# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/20  15:34
desc:
'''


import numpy as np
import pandas as pd


def create_LSreturns(factor_data,auxiliary_data,factor_name):
    '''
    :param factor_tablename: 因子所在表名
    :param factor_name: 因子名称
    :param start_date: 开始日期
    :param auxiliary_tablename: 辅助数据表名
    :param auxiliary_name: 'CHANGEPCT';'NEGOTIABLEMV'  涨跌幅和自由流通市值
    :param weighting_method: 'Equal Weighted';'Value Weighted'
    :return:
    '''
    time_series = factor_data['TRADINGDAY'].unique()
    time_series.sort()  # 时间序列
    EW_LS_returns = dict()  # 等权平均
    VW_LS_returns = dict()  # 自由流通市值加权平均

    for i in np.arange(0,(len(time_series)-1)):
        tempdata = factor_data[factor_data['TRADINGDAY']==time_series[i]]
        tempdata = tempdata.sort_values(by=factor_name,axis=0,ascending=True)
        low_stock = tempdata[tempdata[factor_name]<=tempdata[factor_name].quantile(0.2)]['SECUCODE']
        high_stock = tempdata[tempdata[factor_name]>=tempdata[factor_name].quantile(0.8)]['SECUCODE']

        auxiliarytemp_data = auxiliary_data[auxiliary_data['TRADINGDAY']==time_series[i+1]]  # 得到下期收益率
        returns_low = auxiliarytemp_data[auxiliarytemp_data['SECUCODE'].isin(low_stock)]['CHANGEPCT']
        returns_high = auxiliarytemp_data[auxiliarytemp_data['SECUCODE'].isin(high_stock)]['CHANGEPCT']

        EW_LS_returns[time_series[i+1]] = abs(returns_low.mean() -returns_high.mean())

        weights_low = auxiliarytemp_data[auxiliarytemp_data['SECUCODE'].isin(low_stock)]['NEGOTIABLEMV']
        weights_high = auxiliarytemp_data[auxiliarytemp_data['SECUCODE'].isin(high_stock)]['NEGOTIABLEMV']
        VW_LS_returns[time_series[i+1]] = abs(np.average(returns_low,weights=weights_low)-np.average(returns_high,weights=weights_high))

    EW_LS_frame = pd.DataFrame.from_dict(EW_LS_returns, orient='index')
    EW_LS_frame.columns = ['ew_LS_returns']
    VW_LS_frame = pd.DataFrame.from_dict(VW_LS_returns, orient='index')
    VW_LS_frame.columns = ['vw_LS_returns']

    res = pd.concat([EW_LS_frame,VW_LS_frame],axis=1)
    return res


# if __name__ == '__main__':
#     import time
#     time_start = time.time()
#     res = create_LSreturns('dailyvaluefactor', 'PE', '2018-01-01', 'QT_Performance', ['CHANGEPCT','NEGOTIABLEMV'], 'Equal Weighted')
#
#     time_end = time.time()
#     print('time cost', time_end - time_start, 's')