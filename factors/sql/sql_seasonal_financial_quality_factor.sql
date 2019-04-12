

--表1： LC_MainIndexNew
select t2.SecuCode,t1.EndDate,t1.ROEAvg,t1.ROA,t1.GrossIncomeRatio,t1.TotalProfitCostRatio,t1.ROIC,t1.OperatingNIToTP,t1.CashRateOfSales,t1.NOCFToOperatingNITTM,t1.CurrentLiabilityToTL,t1.CurrentRatio,t1.TotalAssetTRate,t1.NetProfitCut, t1. NetProfit
 from LC_MainIndexNew t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t2.SecuCode='000001' or t2.SecuCode='000002')order by SecuCode


