 -- 注意：取2005-01-01及之后的数据，要设置date >= 2004-12-31, 否则季度数据无法插值就会有缺失的情况

--表1： LC_MainIndexNew
select t2.SecuCode,t1.EndDate,t1.ROECut,t1.ROA_EBITTTM, t1.ROATTM, t1.SalesCostRatio, t1.PeriodCostsRateTTM, t1.NPToTORTTM, t1.OperatingProfitToTORTTM, t1.EBITToTORTTM, t1.TOperatingCostToTORTTM, t1.OperatingExpenseRateTTM, t1.AdminiExpenseRateTTM, t1.FinancialExpenseRateTTM, t1.AssetImpaLossToTORTTM, t1.NetProfitCut, t1.EBIT, t1.EBITDA, t1.OperatingProfitRatio
 from LC_MainIndexNew t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t1.enddate >= to_date( '2004-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') )


