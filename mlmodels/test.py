# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/15 11:19

import pandas as pd
import h5py

# f = h5py.File(r"D:\Meiying\data\cleaned\1.h5", 'r')  # 打开h5文件
# for k in f.keys():
#     print(k)
#     h = pd.read_hdf(r"D:\Meiying\data\cleaned\1.h5", key=str(k))
#     df = pd.DataFrame(h)
#     print(df)

# k:20140102 - 20181228

# dates = []
# month = ['01','02','03','04','05','06','07','08','09','10','11','12']
# count = 0
# for i in range(2005,2019):
#     for j in range(12):
#         dates.append(str(i) + month[j] + '01')
#         count+=1
# print(dates)
# print(count)

# print(2 ** 1 * 3)

print(range(0, 15)[-1])