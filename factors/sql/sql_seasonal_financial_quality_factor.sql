 -- 注意：取2005-01-01及之后的数据，要设置date >= 2004-12-31, 否则季度数据无法插值就会有缺失的情况


--表1： LC_MainIndexNew
select t2.SecuCode,t1.EndDate,t1.ROEAvg,t1.ROA,t1.GrossIncomeRatio,t1.TotalProfitCostRatio,t1.ROIC,t1.OperatingNIToTP,t1.CashRateOfSales,t1.NOCFToOperatingNITTM,t1.CurrentLiabilityToTL,t1.CurrentRatio,t1.TotalAssetTRate,t1.NetProfitCut, t1. NetProfit
 from LC_MainIndexNew t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90')


