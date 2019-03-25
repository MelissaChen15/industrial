# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/25 9:40

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
color = sns.color_palette()
sns.set_style('darkgrid')
import warnings
from scipy import stats
from scipy.stats import norm, skew
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn #ignore annoying warning (from sklearn and seaborn)
pd.set_option('display.float_format', lambda x: '{:.3f}'.format(x)) #Limiting floats output to 3 decimal points





# 导入数据
file_path = r'D:\Meiying\data\Kaggle_house_price\\'
train = pd.read_csv(file_path + 'train.csv') # 数据中同时含有数值和标签型的数据
test = pd.read_csv(file_path + 'test.csv')

# --------- 数据预处理 ----------

# 可视化
# print(train.head(5)) # 1. pd前五行
# print(test.head(5))
# plt.figure(figsize=(15,8)) # 2. sns散点图
# sns.boxplot(train.GrLivArea, train.SalePrice)
# fig, ax = plt.subplots() # 3. plt散点图
# ax.scatter(x = train['GrLivArea'], y = train['SalePrice'])
# plt.ylabel('SalePrice', fontsize=13)
# plt.xlabel('GrLivArea', fontsize=13)
# sns.distplot(train['SalePrice'] , fit=norm) # 4. 正态概率图 ：如果和正态分布有偏离，需要做log变换恢复正态性
# # Get the fitted parameters used by the function
# (mu, sigma) = norm.fit(train['SalePrice'])
# print( '\n mu = {:.2f} and sigma = {:.2f}\n'.format(mu, sigma))
# #Now plot the distribution
# plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu, sigma)],
#             loc='best')
# plt.ylabel('Frequency')
# plt.title('SalePrice distribution')
# fig = plt.figure()#Get also the QQ-plot
# res = stats.probplot(train['SalePrice'], plot=plt)

# 按照参考文献的说法，此时正态分布明显属于右态分布，整体峰值向左偏离，并且skewness较大，需要对目标值做log转换，以恢复目标值的正态性。
train["SalePrice"] = np.log1p(train["SalePrice"]) #We use the numpy fuction log1p which  applies log(1+x) to all elements of the column
# sns.distplot(train['SalePrice'] , fit=norm) #Check the new distribution
(mu, sigma) = norm.fit(train['SalePrice']) # Get the fitted parameters used by the function
# print( '\n mu = {:.2f} and sigma = {:.2f}\n'.format(mu, sigma))
# plt.legend(['Normal dist. ($\mu=$ {:.2f} and $\sigma=$ {:.2f} )'.format(mu, sigma)],#Now plot the distribution
            # loc='best')
# plt.ylabel('Frequency')
# plt.title('SalePrice distribution')
# fig = plt.figure() #Get also the QQ-plot
# res = stats.probplot(train['SalePrice'], plot=plt)
# plt.show()

# 为了特征工程处理方便，把train和test数据合在一起
all_data = train.append(test)

# ------- 特征工程 ----------
# 缺失值处理
# 首先使用热力图看一下变量之间的相关性
corrmat = train.corr() # 热力图：变量之间的相关性
plt.subplots(figsize=(12,9))
sns.heatmap(corrmat, vmax=0.9, square=True)
# plt.show()
#这代表全部建筑面积TotaLBsmtSF与一层建筑面积1stFlrSF成强正相关，车库区域GarageAreas和车库车辆GarageCars成强正相关，
# 那么在填补缺失值的时候就有了依据，我们可以直接删掉一个多余的特征或者使用一个填补另一个。
# n_null = all_data.isnull().sum() # 查看各特征缺失值的数量
# print(n_null[n_null>0].sort_values(ascending=False))

cols1 = ["PoolQC" , "MiscFeature", "Alley", "Fence", "FireplaceQu",  # 用none来填补
         "GarageQual", "GarageCond", "GarageFinish", "GarageYrBlt", "GarageType",
         "BsmtExposure", "BsmtCond", "BsmtQual", "BsmtFinType2", "BsmtFinType1", "MasVnrType","Electrical",
         "MSZoning","Utilities","Functional","SaleType","KitchenQual",'KitchenQual','Exterior1st','Exterior2nd']
for col in cols1:
    all_data[col].fillna("None", inplace=True)

cols=["MasVnrArea", "BsmtUnfSF", "TotalBsmtSF", "GarageCars","BsmtHalfBath","BsmtFullBath", # 用0来填补
      "BsmtFinSF2", "BsmtFinSF1", "GarageArea"]
for col in cols:
    all_data[col].fillna(0, inplace=True)
# 阅读材料可知，LotFrontage这个特征与LotAreaCut和Neighborhood有比较大的关系，所以这里用这两个特征分组后的中位数进行插补
all_data["LotFrontage"] = all_data.groupby("Neighborhood")["LotFrontage"].transform( lambda x: x.fillna(x.median()))



