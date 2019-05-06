 -- 表2：SecuMain

--表1： LC_BalanceSheetAll
select t2.SecuCode,t1.EndDate,t1.OtherCurrentAssets,  t1.OtherAssets, t1.ShortTermLoan, t1.CapitalReserveFund, t1.DeferredProceeds, t1.DividendPayable, t1.FixedAssets, t1.GoodWill, t1.OtherCurrentLiability, t1.NotesPayable, t1.IntangibleAssets, t1.MinorityInterests, t1.AccountReceivable, t1.TreasuryStock, t1.AdvancePayment
 from LC_BalanceSheetAll t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t1.enddate >= to_date( '2004-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') )

--表3： LC_IncomeStatementAll
select t2.SecuCode,t3.EndDate,t3.NetProfit, t3.OtherNetRevenue, t3.RAndD, t3.OperatingRevenue, t3.OperatingPayout, t3.AdministrationExpense, t3.OperatingRevenue
 from LC_IncomeStatementAll t3
inner join SecuMain t2
on t3.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t3.enddate >= to_date( '2004-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') )

 --表4： LC_MainDataNew
select t2.SecuCode,t4.EndDate,t4.TotalAssets, t4.TotalCurrentLiability, t4.TotalShareholderEquity, t4.TotalAssets, t4.TotalCurrentAssets, t4.Inventories, t4.TotalLiability, t4.TotalCurrentLiability, t4.TotalShareholderEquity
 from LC_MainDataNew t4
inner join SecuMain t2
on t4.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t4.enddate >= to_date( '2004-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') )

 --表5： LC_CashFlowStatementAll
select t2.SecuCode,t5.EndDate,t5.CashEquivalentIncrease, t5. InventoryDecrease, t5.NetOperateCashFlow, t5.NetInvestCashFlow,t5.IntangibleAssetAmortization
 from LC_CashFlowStatementAll t5
inner join SecuMain t2
on t5.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t5.enddate >= to_date( '2004-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') )

 --表6： LC_DerivativeData
select t2.SecuCode,t6.EndDate,t6.TotalOperatingCostTTM, t6.RetainedEarnings, t6.GrossProfitTTM, t6.NetWorkingCaital,t6.TotalOperatingRevenueTTM, t6.TotalOperatingCostTTM, t6.TotalPaidinCapital
 from LC_DerivativeData t6
inner join SecuMain t2
on t6.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t6.enddate >= to_date( '2004-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') )


 --表7： LC_BalanceSheet
 select t2.SecuCode,t7.EndDate,t7.TotalLongtermLiability
 from LC_BalanceSheet t7
inner join SecuMain t2
on t7.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t7.enddate >= to_date( '2004-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') )

 --表8： LC_Staff
select t2.SecuCode,t8.EndDate,t8.EmployeeSum
 from LC_Staff t8
inner join SecuMain t2
on t8.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t8.enddate >= to_date( '2004-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') )
