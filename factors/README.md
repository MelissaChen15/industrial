# 使用手册 Tutorial

## Part 1： 数据库概览

### 聚源数据库原有数据表（部分）

证券主表 SecuMain 主要字段

| 列名         | 中文名       |
| ------------ | ------------ |
| InnerCode    | 证券内部编码 |
| SecuMarket   | 证券市场     |
| SecuCategory | 证券类别     |

### 因子库数据表

## Part 2： 文件结构

```bash
./factors
|- BasicFactor.py 		基础因子类，定义所有因子应该的有的基本特征和基本操作
|- Category.py 			因子类别类
|- Frequency.py 		因子频率类
|- factor_template.py 	新类别因子模板
|- update.py 			因子写入/更新主入口
|- 因子库索引.xlsx		
|- README.md

|- DailyTechnicalIndicatorFactor.py		日频技术指标类因子
|- DailyValueFactor.py					日频价值类因子
|- SeasonalCapitalStructureFactor.py	季频资本结构类因子
|- SeasonalCashFactor.py				季频现金状况类因子
|- SeasonalDebtpayingAbilityFactor.py	季频偿债能力因子
|- SeasonalDividendFactor.py			季频分红能力类因子
|- SeasonalDuPontFactor.py				季频杜邦分析体系因子
|- SeasonalEarningQualityFactor.py		季频收益质量类因子
|- SeasonalFinancialQualityFactor.py	季频财务质量类因子
|- SeasonalGrowthFactor.py				季频成长类因子
|- SeasonalOperatingFactor.py			季频营运能力类因子
|- SeasonalProfitabilityFactor.py		季频盈利能力因子
|- SeasonalSecuIndexFactor.py			季频每股指标因子
|- SeasonalValueFactor.py				季频价值类因子

|- util				工具类
	|- datetime_ops.py		时间戳操作
	|- TechnicalIndicatorFunc.py	技术指标类因子计算
	|- TechnicalIndicatorProcess.py	技术指标类因子计算

|- sql 				数据库操作
	|- dbsynchelper2.py			数据库读取
	|- GetSQLsentence.py		数据库读取
	|- pl_sql_oracle.py			数据库读取
	|- sql_template.sql			sql查询模板
	|- sql_get_secucode.sql		获取聚源数据库中所有的股票代码
	
	以下是从聚源数据库中查询各类因子的sql代码，文件名与因子类名对应：
	|- sql_daily_technicalIndicator_factor.sql
	|- sql_daily_value_factor.sql
	|- sql_seasonal_capital_structure_factor.sql
	|- sql_seasonal_cash_factor.sql
	|- sql_seasonal_debtpaying_ability_factor.sql
	|- sql_seasonal_dividend_factor .sql
	|- sql_seasonal_dupont_factor.sql
	|- sql_seasonal_earning_quality_factor.sql
	|- sql_seasonal_financial_quality_factor.sql
	|- sql_seasonal_growth_factor.sql
	|- sql_seasonal_operating_factor.sql
	|- sql_seasonal_profitability_factor.sql
	|- sql_seasonal_secu_index_factor.sql
	|- sql_seasonal_value_factor.sql

```

## Part 3： 设计思路

## Part 4： 命名规范

## Part 5： 使用步骤 

添加新类别的因子

在已有的类别中添加新的因子

更新因子主表

更新因子值

## Part 6： 异常处理与其他注意事项



































## 注意事项

### sql文件

取2005-01-01及之后的数据，要设置date >= 2004-12-31, 否则季度数据无法插值就会有缺失的情况

### 数据预处理

季度数据使用插值法之后，临近现在的一个季度没有数据，暂时用上一个季度的报告值代替

### 数据库

同时读写、频繁读写数据库会导致数据表锁死（阀值未知）

数据库有session数上限，多个程序访问可能导致超时

写入时，数据超过数据字段字符数上限不会报错
