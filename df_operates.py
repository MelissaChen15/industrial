# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/12 10:42

# 返回所在的行数
# row = df2[df2['trade_date'].isin([str(k)])]

# 返回列=某个值所在的那一行
# table1.loc[table1['TRADINGDAY'] == report_day]

# 快速迭代
# for row in df.itertuples(index=True, name='Pandas'):
#     getattr(row, 'a'), getattr(row, 'b')


# 合并
# https://jingyan.baidu.com/article/91f5db1b79205a1c7f05e3ae.html


# 自定义函数操作
# daily_data['STARTDAY'] = daily_data['TRADINGDAY'].apply(lambda v: first_day_this_month(v))

# 显示所有的行/列
# pd.set_option('display.max_columns', None) #显示所有列
# pd.set_option('display.max_rows', None) #显示所有行
# pd.set_option('max_colwidth',100) #设置value的显示长度为100，默认为50


# 判断是不是nan
# a = pd.DataFrame(np.array([np.nan, 1, None, 1, 1]))
# b = pd.DataFrame(np.array([1, np.nan, 1,None, 1]))
#
# c = a/b
# print(c)
#
# print(c == None)
# print(c == np.nan)
# print(c == c)
# print(pd.isnull(c))


# 快速从数据库中读表
# from sqlalchemy import create_engine
# engine = create_engine('oracle+cx_oracle://jydb:jydb@192.168.1.187/JYDB')
# df = pd.DataFrame(engine.execute("SELECT * FROM DailyValueFactor").fetchall())
# print(df.shape)