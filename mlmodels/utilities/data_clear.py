# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/15 9:39

# 整理数据：在dataset1中加上涨跌幅
# 记住要改三个地方！！

import numpy as np
import pandas as pd
import h5py

dates = [ '20050401','20050501', '20050601', '20050701', '20050801', '20050901', '20051001', '20051101', '20051201', '20060101', '20060201', '20060301', '20060401', '20060501', '20060601', '20060701', '20060801', '20060901', '20061001', '20061101', '20061201', '20070101', '20070201', '20070301', '20070401', '20070501', '20070601', '20070701', '20070801', '20070901', '20071001', '20071101', '20071201', '20080101', '20080201', '20080301', '20080401', '20080501', '20080601', '20080701', '20080801', '20080901', '20081001', '20081101', '20081201', '20090101', '20090201', '20090301', '20090401', '20090501', '20090601', '20090701', '20090801', '20090901', '20091001', '20091101', '20091201', '20100101', '20100201', '20100301', '20100401', '20100501', '20100601', '20100701', '20100801', '20100901', '20101001', '20101101', '20101201', '20110101', '20110201', '20110301', '20110401', '20110501', '20110601', '20110701', '20110801', '20110901', '20111001', '20111101', '20111201', '20120101', '20120201', '20120301', '20120401', '20120501', '20120601', '20120701', '20120801', '20120901', '20121001', '20121101', '20121201', '20130101', '20130201', '20130301', '20130401', '20130501', '20130601', '20130701', '20130801', '20130901', '20131001', '20131101', '20131201', '20140101', '20140201', '20140301', '20140401', '20140501', '20140601', '20140701', '20140801', '20140901', '20141001', '20141101', '20141201', '20150101', '20150201', '20150301', '20150401', '20150501', '20150601', '20150701', '20150801', '20150901', '20151001', '20151101', '20151201', '20160101', '20160201', '20160301', '20160401', '20160501', '20160601', '20160701', '20160801', '20160901', '20161001', '20161101', '20161201', '20170101', '20170201', '20170301', '20170401', '20170501', '20170601', '20170701', '20170801', '20170901', '20171001', '20171101', '20171201', '20180101', '20180201', '20180301', '20180401', '20180501', '20180601', '20180701', '20180801', '20180901', '20181001', '20181101', '20181201']
# k:20150102 - 20181228
# for i in range(165):
    # f = h5py.File("D:\Meiying\data\part1_modified.h5", 'r')  # 打开h5文件
    # store_path = r"D:\Meiying\data\cleaned\\" + dates[i][:6] + ".h5"
    # store = pd.HDFStore(store_path, 'w', complevel=4, complib='blosc')
    # for k in f.keys():
    #     if k < dates[i]: continue
    #     if k  >=  dates[i+1]: break #每一个月写一个文件
    #     # 对于某一天
    #     # count = 0
    #     h = pd.read_hdf("D:\Meiying\data\part1_modified.h5", key=str(k))
    #     df = pd.DataFrame(h)
    #     df['open'] = np.nan
    #     df['close'] = np.nan
    #     df['pre_close'] = np.nan
    #     df['change'] = np.nan
    #     df['high'] = np.nan
    #     df['low'] = np.nan
    #     df['vol'] = np.nan
    #     df['amount'] = np.nan
    #     df['pct_chg'] = np.nan
    #     df.index = df['ts_code'] # 用股票代码重命名行
    #     for code in df['ts_code']:
    #         f2 = h5py.File("D:\Meiying\data\dataset_part5.h5", 'r')  # 打开h5文件
    #         for key in f2.keys():
    #             if code == key:
    #                 h2 = pd.read_hdf("D:\Meiying\data\dataset_part5.h5", key=str(key))
    #                 df2 = pd.DataFrame(h2)
    #                 # print(df2)
    #                 for date in df2["trade_date"]:
    #                     if date == str(k):
    #                         row = df2[df2['trade_date'].isin([str(k)])]
    #                         # index = code # index是在1中的索引
    #                         # index = row.index.values[0] # index是在5中的索引
    #                         df.at[code, "open"] = float(row["open"])
    #                         df.at[code, "close"] = float(row["close"])
    #                         df.at[code, "pre_close"] = float(row["pre_close"])
    #                         df.at[code, "change"] = float(row["change"])
    #                         df.at[code, "high"] = float(row["high"])
    #                         df.at[code, "low"] = float(row["low"])
    #                         df.at[code, "vol"] = float(row["vol"])
    #                         df.at[code, "amount"] = float(row["amount"])
    #                         df.at[code,"pct_chg"] = float(row["pct_chg"])
    #                         # print(code)
    #                         # print(df)
    #     df.drop("ts_code", axis=1,inplace=True) # 删除多余的ts_code列
    #     # 把每天的数据写入一个h5表
    #     store[k] = df
    #     print(str(k) + " done")
    # store.close()
    # print(dates[i][:6] + " done")

f = h5py.File("D:\Meiying\data\part1_modified.h5", 'r')  # 打开h5文件
store_path = r"D:\Meiying\data\cleaned\labeled.h5"
store = pd.HDFStore(store_path, 'w', complevel=4, complib='blosc')
for k in f.keys():
    if k < '20181201': continue
    if k  >=  '20190101': break #每一个月写一个文件
    # 对于某一天
    # count = 0
    h = pd.read_hdf("D:\Meiying\data\part1_modified.h5", key=str(k))
    df = pd.DataFrame(h)
    df['open'] = np.nan
    df['close'] = np.nan
    df['pre_close'] = np.nan
    df['change'] = np.nan
    df['high'] = np.nan
    df['low'] = np.nan
    df['vol'] = np.nan
    df['amount'] = np.nan
    df['pct_chg'] = np.nan
    df.index = df['ts_code']  # 用股票代码重命名行
    for code in df['ts_code']:
        f2 = h5py.File("D:\Meiying\data\dataset_part5.h5", 'r')  # 打开h5文件
        for key in f2.keys():
            if code == key:
                h2 = pd.read_hdf("D:\Meiying\data\dataset_part5.h5", key=str(key))
                df2 = pd.DataFrame(h2)
                # print(df2)
                for date in df2["trade_date"]:
                    if date == str(k):
                        row = df2[df2['trade_date'].isin([str(k)])]
                        # index = code # index是在1中的索引
                        # index = row.index.values[0] # index是在5中的索引
                        df.at[code, "open"] = float(row["open"])
                        df.at[code, "close"] = float(row["close"])
                        df.at[code, "pre_close"] = float(row["pre_close"])
                        df.at[code, "change"] = float(row["change"])
                        df.at[code, "high"] = float(row["high"])
                        df.at[code, "low"] = float(row["low"])
                        df.at[code, "vol"] = float(row["vol"])
                        df.at[code, "amount"] = float(row["amount"])
                        df.at[code, "pct_chg"] = float(row["pct_chg"])
                        # print(code)
                        # print(df)
    df.drop("ts_code", axis=1, inplace=True)  # 删除多余的ts_code列
    # 把每天的数据写入一个h5表
    store[k] = df
    print(str(k) + " done")
store.close()
print("201812 done")

# 删除数据缺失值，把表拼接起来