# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/11 14:54

"""
工具类
"""

import datetime
import pandas as pd

def last_season_report_day(date_now):
    """
    返回传入日期的上季度报告日
    :param date_now: string, 传入日期，格式：2019-01-01
    :return: string，上季度最后一天，格式同传入日期
    """
    x = datetime.datetime.strptime(date_now, '%Y-%m-%d')
    y = x + pd.tseries.offsets.DateOffset(months=-((x.month - 1) % 3), days= - x.day)  # 上季第一天
    return y.strftime("%Y-%m-%d")

# def last_season_value(date_now, factor, dataframe):
#     report_day = last_season_report_day(date_now)
#     return dataframe.iloc[report_day:factor]

