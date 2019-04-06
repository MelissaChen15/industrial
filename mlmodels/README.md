# mlmodels

需要修改的地方：

- [x] 数据概览之后，注明一下需要改数据加载的函数（注明模型需要的数据格式）

- [ ] datetime

- [ ] pred和实际值放在一个文件里面

## 1. 文件结构

```bash
mlmodels/
|-- main_entry/ 主程序入口
|   |-- process/
|      |-- train.py
|      |-- predict.py
|      |-- build_strategy.py
|      |-- evaluate_strategy.py
|      |-- load_sample_data.py
|   |
|   |-- Para.py 参数类
|   |-- xgboost.py
|   |-- main_r.py 回归模型主函数
|   |-- main_c.py 分类模型主函数
|   |-- main_ave_stacking.py
|   |-- main_meta_stacking.py
|
|-- classifiers/ 分类模型参数设置
|   |-- DTC_init.py
|   |-- GaussianNB_init .py
|   |-- Logistic_init.py
|   |-- RFC_init.py
|   |-- SVC_init.py
|
|-- regressors/ 回归模型参数设置
|   |-- DTR_init.py
|   |-- ExraTreeR_init.py
|   |-- GBoostR_init.py
|   |-- Lasso_init.py
|   |-- LinearR_init.py
|   |-- RFR_init.py
|   |-- Ridge_init.py
|   |-- SVR_init.py
|
|-- utities/ 工具包
|   |-- PCA_algorithm.py
|   |-- cubic_spline.py
|   |-- data_clear.py
|   |-- Detting_data.py
|   |-- iris.py
|   |-- Main_Function.py
|   |-- performance_index.py
```

## 2. 数据概览

### 笔者使用的数据

**Data Name：1.h5 ~ 180.h5**

**Data range**: 2004年1月 ~ 2018年12月，按数字顺序，每个文件存储一个月的数据。对于每一个文件，按天建表，key为交易日期。

**Demo：**1.h5, key = 20040102, head(5)

| ts_code   | trade_date | close | turnover_rate_f | pe_ttm  | pb     | ps_ttm  | circ_mv    | open | pre_close | change | high | low  | vol      | amount    | pct_chg |
| --------- | ---------- | ----- | --------------- | ------- | ------ | ------- | ---------- | ---- | --------- | ------ | ---- | ---- | -------- | :-------- | ------- |
| 000683.SZ | 20040102   | 4.34  | 0.2848          | NaN     | 4.1233 | 2.3449  | 73346      | 4.32 | 4.34      | 0      | 4.39 | 4.32 | 4813.4   | 2094.8232 | 0       |
| 000729.SZ | 20040102   | 9.37  | 0.3096          | 25.5337 | 1.5789 | 1.8888  | 175406.4   | 9.3  | 9.37      | 0      | 9.44 | 9.29 | 5795.67  | 5410.9105 | 0       |
| 000921.SZ | 20040102   | 6.83  | 0.6433          | 46.8696 | 2.438  | 1.0948  | 132844.183 | 6.61 | 6.68      | 0.15   | 6.88 | 6.61 | 12511.99 | 8503.6234 | 2.25    |
| 600074.SH | 20040102   | 6.5   | 0.7598          | 20.6439 | 1.9852 | 1.7766  | 113724     | 6.47 | 6.52      | -0.02  | 6.64 | 6.42 | 13293.86 | 8650.095  | -0.31   |
| 600159.SH | 20040102   | 2.61  | 2.0099          | NaN     | NaN    | 17.0864 | 22970.0045 | 2.56 | 2.59      | 0.02   | 2.64 | 2.51 | 17688.3  | 4552.642  | 0.77    |

### 使用其他数据时

- 在 main_entry/process/load_sample_data.py中修改或者重写load()、preprocess()函数。

- 为了符合sklearn的运行要求，load()、preprocess() 返回的数据格式可以为pandas.DataFrame、pandas.Series 或 numpy.array，X.shape 必须为 (n_samples, n_features)， y.shape 必须为 (n_samples,)。

  Tips: 2d-array变为1d-array 可以使用y.values.ravel()

- 根据你的数据格式，修改main_entry/process/predict.py、main_entry/process/ build_strategy.add_next_day_return() 中涉及数据读取的代码0。

## 3. 设置参数 

**3.1 全局参数 **：

​	修改文件 /main_entry/Para.py

**3.2 模型参数**：

​	分类模型：修改 /classifiers/ 文件夹下相应文件

​	回归模型：修改 /regressors/ 文件夹下相应文件



## 4. 使用单个模型

**4.1 分类模型：**

​	a. 设置参数（见3） 

​	b.  在 /main_entry/main_c.py 中初始化模型, 如：

```python
inits = [Logistic_init.init(), SVC_init.init()]
```

​	c. 运行main_c.py, 结果存储在para.path_results路径下的文件夹中

**4.2 回归模型**：

​	a. 设置参数（见3） 

​	b.  在 /main_entry/main_r.py 中初始化模型, 如：

```python
    inits = [Ridge_init.init(), RFR_init.init()]
```

​	c. 运行main_r.py, 结果存储在para.path_results路径下的文件夹中

## 5. 使用 average stacking

​	a. 设置参数（见3） 

​	b.  在 /main_entry/main_ave_stacking.py 中初始化模型, 如：

```python
    inits = [SVR_init.init(),Ridge_init.init(), RFR_init.init()]
```

​	设置每个模型的权重，如：

```python
	weights = [0.1,0.1,0.8]
```

​	c. 运行main_ave_stacking.py, 结果存储在para.path_results路径下的文件夹中

## 6. 使用 meta stacking

​	a. 设置参数（见3） 

​	b.  在 /main_entry/main_meta_stacking.py 中初始化模型, 如：

```python
    第一层：     models_1st_layer_inits = [Ridge_init.init(), SVR_init.init()]
	第二层：	 model_2nd_layer, *arg= RFR_init.init()
```

​	c. 运行main_meta_stacking.py, 结果存储在para.path_results路径下的文件夹中

