import pandas as pd
import numpy as np

new = pd.DataFrame([
 [np.nan],
 [4],
 [np.nan]
])

old = pd.DataFrame()

a = new.isna() & ~old.isna()
b = a.mask(a.isna(),False)

new = new.mask(b.astype('bool'),old)
print(new)

# for i in range(old.shape[0]):
#  if b.iloc[i,0] == True:
#   new.iloc[i,0] = old.iloc[i,0]
#
# print(b)
# print(new)







df1 = pd.DataFrame([['a', 10, '男'],
                 ['b', 11, '男'],
                 ['c', 11, '女'],
                 ['a', 10, '女'],
                 ['c', 11, '男']],
                columns=['name', 'age', 'sex'])
df2 = pd.DataFrame([['a', 10, '男'],
                 ['b', 11, '女']],
                columns=['name', 'age', 'sex'])
# print(df1)
# print(df2)
# # 取交集
# # print(pd.merge(df1,df2,on=['name', 'age', 'sex']))
#
# # 取并集
# print( pd.merge(df1,df2,on=['name', 'age', 'sex'], how='outer'))

# 从df1中过滤df1在df2中存在的行，也就是取补集
# df1 = df1.append(df2)
# df1 = df1.append(df2)
# print(df1.drop_duplicates(subset=['name', 'age', 'sex'],keep=False))
