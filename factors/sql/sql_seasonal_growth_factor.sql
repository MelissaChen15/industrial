 -- 注意：取2005-01-01及之后的数据，要设置date >= 2004-12-31, 否则季度数据无法插值就会有缺失的情况


--表1： LC_MainIndexNew
select t2.SecuCode,t1.EndDate,t1.NetProfitGrowRate, t1.ROETTM, t1.TotalAssetGrowRate, t1.BasicEPSYOY, t1.GrossIncomeRatioTTM, t1.NetProfitRatioTTM, t1.DilutedEPSYOY, t1.OperatingRevenueGrowRate, t1.ORComGrowRate3Y, t1.OperProfitGrowRate, t1.TotalProfeiGrowRate, t1.NPParentCompanyYOY, t1.NPParentCompanyCutYOY, t1.NPPCCGrowRate3Y, t1.AvgNPYOYPastFiveYear, t1.NetOperateCashFlowYOY, t1.OperCashPSGrowRate, t1.NAORYOY, t1.NetAssetGrowRate, t1.EPSGrowRateYTD, t1.SEWithoutMIGrowRateYTD, t1.TAGrowRateYTD, t1.SustainableGrowRate
 from LC_MainIndexNew t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90')


