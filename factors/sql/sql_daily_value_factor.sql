

--表1 ：LC_DIndicesForValuation
select t2.SecuCode,t1.TradingDay,t1.PE,t1.PELYR,t1.PB,t1.PCFTTM,t1.PCFSTTM,t1.PS,t1.PSTTM,t1.DividendRatio,t1.TotalMV
 from LC_DIndicesForValuation t1 
inner join SecuMain t2
on t1.InnerCode=t2.InnerCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t2.SecuCode='000001' or t2.SecuCode='000002')order by SecuCode



--表2：LC_MainIndexNew，注意主键是CompanyCode
select t2.SecuCode,t1.EndDate,t1.NetProfitGrowRate
 from LC_MainIndexNew t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t2.SecuCode='000001' or t2.SecuCode='000002')order by SecuCode
