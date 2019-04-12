import pandas as pd
import numpy as np
import datetime
import time
import parser

df1 = pd.DataFrame({'a':[1,2],'b':[3,4]})





# df = pd.DataFrame({'a':[0]*100000,'b':[1]*100000})
# # print(df)
# # df1 = df.interpolate(method='cubic',axis=0)
# # print(df1)
# import time
# tic = time.time()
# for row in df.itertuples(index=True, name='Pandas'):
#     getattr(row, 'a'), getattr(row, 'b')
# tok = time.time()
# for index, row in df.iterrows():
#     a = row['a']
#     b = row['b']
# tok2 = time.time()
# print(tok-tic, tok2-tok)

#
# #显示所有列
# pd.set_option('display.max_columns', None)
# #显示所有行
# pd.set_option('display.max_rows', None)
# #设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth',100)

# d1 = '2019-04-04'
# # dt1 = datetime.datetime.strptime(d1,'%Y-%m-%d')
#
#
# # 返回传入日期的上季度报告日
# def last_season_report_day(date_now):
#     x = datetime.datetime.strptime(date_now, '%Y-%m-%d')
#     y = x + pd.tseries.offsets.DateOffset(months=-((x.month - 1) % 3), days= - x.day)  # 上季第一天
#     return y.strftime("%Y-%m-%d")
#
# # https://www.jb51.net/article/138085.htm
# # print(last_season_report_day(d1))
# # print(type(last_season_report_day(d1)))
#
# # print(1/np.nan)
#
#
# # df1 = pd.DataFrame({'a':1,'b':2})
# # print(df1.iloc['a':])

dt1 = datetime.datetime.strptime('2019-04-04','%Y-%m-%d')
dt2 = datetime.datetime.strptime('2019-03-01','%Y-%m-%d')
dt3 = datetime.datetime.strptime('2019-01-01','%Y-%m-%d')

print(dt1 >= dt2 and dt2 >= dt3)