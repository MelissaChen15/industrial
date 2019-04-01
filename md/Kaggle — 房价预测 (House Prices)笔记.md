# Kaggle — 房价预测 (House Prices)笔记

## Part 1 数据特征

train shape: **(1457, 81)**  test shape: **(1459, 80)**

80个特征，预测目标**Sale Price** 

11个连续变量，69个离散变量。18个特征较为稀疏。

![HousePrices1](D:\Meiying\data\kaggle\HousePrices1.svg)

![HousePrices2](D:\Meiying\data\kaggle\HousePrices2.svg)

![HousePrices3](D:\Meiying\data\kaggle\HousePrices3.svg)

## Part 2 特征工程

### 1. 异常数据清洗

观察散点图，手工删除离群点

### 2.  数据预处理

#### 2.1 缺失值处理

- 大部分填充为none或者0

- 有变量间相关关系的，直接删掉一个或者用其中一个填补另外一个

#### 2.2 离散型数据编码

- 手工编码

按特征进行分组，计算该特征每个取值下SalePrice的平均数和中位数，按特征进行分组，计算该特征每个取值下SalePrice的平均数和中位数，再以此为基准排序赋值

- 无序多分类变量：get_dummies 函数 one-hot编码

#### 2.3 特征组合

先用Lasso进行特征筛选，选出较重要的一些特征，观察特征间的关系，手工组合。比如：

```python
X["TotalHouse"] = X["TotalBsmtSF"] + X["1stFlrSF"] + X["2ndFlrSF"]   
X["+_TotalHouse_OverallQual"] = X["TotalHouse"] * X["OverallQual"]
X["+_oMSZoning_TotalHouse"] = X["oMSZoning"] * X["TotalHouse"]
```

#### 2.4 PCA去相关性

新增特征与原来的高度相关，PCA降为到和原来一样的维度

#### 2.5 归一化

RobustScaler()  如果你的数据包含**许多异常值**，使用均值和方差缩放可能并不是一个很好的选择。这种情况下，你可以使用 robust_scale 以及 RobustScaler 作为替代品。它们对你的数据的中心和范围使用更有鲁棒性的估计。

## Part 3 模型构建

#### 1. 定义评价指标

rmse_cv

#### 2. 单一模型

["LR", "Ridge", "Lasso", "RF", "GBR", "SVR", "LinSVR", "Ela","SGD","Bay","Ker","Extra","Xgb"]

训练，grid_search调参，选择几个最佳模型

#### 3. 集成模型

- 加权平均

  权重按照单个模型的表现赋值，不要选择过多模型

  for every data point, single model prediction times weight, then add them together

- Staking

  第一层模型的作用是训练得到一个nxm的特征矩阵来用于输入第二层模型训练，其中n为训练数据行数，m为第一层模型个数
