 -- 注意：取2005-01-01及之后的数据，要设置date >= 2004-12-31, 否则季度数据无法插值就会有缺失的情况

--表1： LC_MainIndexNew
select t2.SecuCode,t1.EndDate, t1.OperCycle, t1.InventoryTRate, t1.InventoryTDays, t1.ARTRate, t1.ARTDays, t1.AccountsPayablesTRate, t1.AccountsPayablesTDays, t1.CurrentAssetsTRate, t1.FixedAssetTRate, t1.EquityTRate
 from LC_MainIndexNew t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90')


