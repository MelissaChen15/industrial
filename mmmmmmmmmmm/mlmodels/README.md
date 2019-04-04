# mlmodels

## 1. 项目结构

mlmodels/
|-- main_entry/ 主程序入口
|   |-- process/
|   	|-- Para.py
|   	|-- train.py
|   	|-- predict.py
|  	 |-- build_strategy.py
|  	 |-- evaluate_strategy.py
|   	|-- load_sample_data.py
|   |
|   |-- xgboost.py
|   |-- main_r.py
|   |-- main_c.py
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



## 2. 设置参数

**2.1 全局参数 **：

​	修改文件/main_entry/process/Para.py

**2.2 模型参数**：

​	分类模型：修改/classifiers/文件夹下相应文件

​	回归模型：修改/regressors/文件夹下相应文件



## 3. 使用单个模型

#####注明一下需要改数据加载的函数

datetime

pred和实际值放在一个文件里面

数据



**3.1 分类模型：**

​	a. 设置参数（见2） 

​	b.  在/main_entry/main_c.py中初始化模型, 如：

```python
inits = [Logistic_init.init(), SVC_init.init()]
```

​	c. 运行main_c.py

**3.2 回归模型**：

​	a. 设置参数（见2） 

​	b.  在/main_entry/main_r.py中初始化模型, 如：

```python
    inits = [Ridge_init.init(), RFR_init.init()]
```

​	c. 运行main_r.py

## 4. 使用 average stacking

​	a. 设置参数（见2） 

​	b.  在/main_entry/main_ave_stacking.py中初始化模型, 如：

```python
    inits = [SVR_init.init(),Ridge_init.init(), RFR_init.init()]
```

​	设置每个模型的权重，如：

```python
	weights = [0.1,0.1,0.8]
```

​	c. 运行main_ave_stacking.py

## 5. 使用 meta stacking

​	a. 设置参数（见2） 

​	b.  在/main_entry/main_meta_stacking.py中初始化模型, 如：

```python
    第一层：     models_1st_layer_inits = [Ridge_init.init(), SVR_init.init()]
	第二层：	 model_2nd_layer, *arg= RFR_init.init()
```

​	c. 运行main_meta_stacking.py

