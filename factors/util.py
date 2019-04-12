# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/11 14:54

"""
工具类
"""

import datetime
import pandas as pd
import calendar

def last_day_last_season(date_now):
    """
    返回传入日期的上季度报告日
    :param date_now: Timestamp, 传入日期，格式：2019-01-01
    :return: Timestamp，上季度最后一天，格式同传入日期
    """
    # x = datetime.datetime.strptime(date_now, '%Y-%m-%d')
    y = date_now + pd.tseries.offsets.DateOffset(months=-((date_now.month - 1) % 3), days= - date_now.day)  # 上季最后一天
    # return y.strftime("%Y-%m-%d")
    return y

def first_day_this_season(date_now):
    """
    返回传入日期的本季度的第一天
    :param date_now: Timestamp, 传入日期，格式：2019-01-01
    :return: Timestamp，本季度的第一天，格式同传入日期
    """
    y = date_now + pd.tseries.offsets.DateOffset(months=-((date_now.month - 1) % 3), days=1 - date_now.day)
    return y

def last_day_this_season(date_now):
    """
    返回传入日期的本季度的报告日
    :param date_now: Timestamp, 传入日期，格式：2019-01-01
    :return: Timestamp，本季度的最后一天，格式同传入日期
    """
    y = date_now + pd.tseries.offsets.DateOffset(months=3 - ((date_now.month - 1) % 3), days= - date_now.day)
    return y

def months_next_season(date_now):
    """
    返回输入报告日接下来一季度的每月第一天
    :param date_now: Timestamp, 季度报告日，即季末最后一天，格式：2019-01-01
    :return: list[3], 接下来一季度的每月第一天
    """
    x =  date_now + datetime.timedelta(days=1)
    y = x + pd.tseries.offsets.DateOffset(months=1)# 后一个月
    z = y + pd.tseries.offsets.DateOffset(months=1)# 后一个月
    return [x,y,z]

def first_day_this_month(date_now):
    y = date_now+pd.tseries.offsets.DateOffset(days=1-date_now.day)
    return y

if __name__ == '__main__':
    # https://www.jb51.net/article/138085.htm
    date = datetime.datetime.strptime('2019-03-31', '%Y-%m-%d')
    # print(last_day_last_season(date))
    # print(first_day_this_season(date))
    # print(last_day_this_season(date))
    print(first_day_this_month(date))
