import pandas as pd
import numpy as np
import datetime
import time
import parser

# df = pd.DataFrame(columns=['a','b'])
# print(df)
# row = {'a':1,'b':2}
#
# #显示所有列
# pd.set_option('display.max_columns', None)
# #显示所有行
# pd.set_option('display.max_rows', None)
# #设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth',100)

d1 = '2019-04-04'
# dt1 = datetime.datetime.strptime(d1,'%Y-%m-%d')


# 返回传入日期的上季度报告日
def last_season_report_day(date_now):
    x = datetime.datetime.strptime(date_now, '%Y-%m-%d')
    y = x + pd.tseries.offsets.DateOffset(months=-((x.month - 1) % 3), days= - x.day)  # 上季第一天
    return y.strftime("%Y-%m-%d")

# https://www.jb51.net/article/138085.htm
# print(last_season_report_day(d1))
# print(type(last_season_report_day(d1)))

# print(1/np.nan)


# df1 = pd.DataFrame({'a':1,'b':2})
# print(df1.iloc['a':])