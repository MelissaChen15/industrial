 -- 表2：SecuMain

--表1： LC_BalanceSheetAll
select  t2.SecuCode,t1.EndDate,t1.OtherCurrentAssets,  t1.OtherAssets, t1.ShortTermLoan, t1.CapitalReserveFund, t1.DeferredProceeds, t1.DividendPayable, t1.FixedAssets, t1.GoodWill, t1.OtherCurrentLiability, t1.NotesPayable, t1.IntangibleAssets, t1.MinorityInterests, t1.AccountReceivable, t1.TreasuryStock, t1.AdvancePayment
 from LC_BalanceSheetAll t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90')

--表3： LC_IncomeStatementAll
select t2.SecuCode,t1.EndDate,t1.NetProfit, t1.OtherNetRevenue, t1.RAndD, t1.OperatingRevenue, t1.OperatingPayout, t1.AdministrationExpense, t1.OperatingRevenue
 from LC_IncomeStatementAll t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90')

 --表4： LC_MainDataNew
select t2.SecuCode,t1.EndDate,t1.TotalAssets, t1.TotalCurrentLiability, t1.TotalShareholderEquity, t1.TotalAssets, t1.TotalCurrentAssets, t1.Inventories, t1.TotalLiability, t1.TotalCurrentLiability, t1.TotalShareholderEquity
 from LC_MainDataNew t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90')

 --表5： LC_CashFlowStatementAll
select t2.SecuCode,t1.EndDate,t1.CashEquivalentIncrease, t1. InventoryDecrease, t1.NetOperateCashFlow, t1.NetInvestCashFlow,t1.IntangibleAssetAmortization
 from LC_CashFlowStatementAll t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90')

 --表6： LC_DerivativeData
select t2.SecuCode,t1.EndDate,t1.TotalOperatingCostTTM, t1.RetainedEarnings, t1.GrossProfitTTM, t1.NetWorkingCaital,t1.TotalOperatingRevenueTTM, t1.TotalOperatingCostTTM, t1.TotalPaidinCapital
 from LC_DerivativeData t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90')


 --表7： LC_BalanceSheet
 select t2.SecuCode,t1.EndDate,t1.TotalLongtermLiability
 from LC_BalanceSheet t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90')

 --表8： LC_Staff
select t2.SecuCode,t1.EndDate,t1.EmployeeSum
 from LC_Staff t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90')
