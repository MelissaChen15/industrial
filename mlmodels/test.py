# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/15 11:19

import pandas as pd
import numpy as np
import h5py
import matplotlib.pyplot as plt


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

# a = np.array([[1,2,3],[4,5,6]])
# df = pd.DataFrame(a)
# print(df)
# print(df.sort_values(by=0,ascending=False))


# df = pd.DataFrame(np.array([[1,0,1],[10,20,5],[10,10,10],[2,2,2]]))
# print(df)
# df = df.mask(df[1] > 10.0, 10.0)
# # df = df.mask(df == 0.0)
#
# # df2 = df.where(m, -df)
# print(df)
#
# df = pd.DataFrame({
# 'SepalLength': [6.5, 7.7, 5.1, 5.8, 7.6, 5.0, 5.4, 4.6,6.7, 4.6],
# 'SepalWidth': [3.0, 3.8, 3.8, 2.7, 3.0, 2.3, 3.0, 3.2,3.3, 3.6],
# 'PetalLength': [5.5, 6.7, 1.9, 5.1, 6.6, 3.3, 4.5, 1.4,5.7, 1.0],
# 'PetalWidth': [1.8, 2.2, 0.4, 1.9, 2.1, 1.0, 1.5, 0.2,2.1, 0.2],
# 'Category': ['virginica', 'virginica', 'setosa',
# 'virginica', 'virginica', 'versicolor',
# 'versicolor', 'setosa', 'virginica',
#  'setosa']
#  })
#
# print(df)

a = [1,2,3]
print(np.mean(a))