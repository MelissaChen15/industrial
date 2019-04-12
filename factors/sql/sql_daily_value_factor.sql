

--因子1：总市值 TotalMV ,涨跌幅 ChangePCT
select t2.SecuCode,t1.TradingDay,t1.PE,t1.PELYR,t1.PB,t1.PCFTTM,t1.PCFSTTM,t1.PS,t1.PSTTM,t1.DividendRatio,t1.TotalMV
 from LC_DIndicesForValuation t1 
inner join SecuMain t2
on t1.InnerCode=t2.InnerCode 
where t2.SecuCode='000001' order by TradingDay DESC

--加一下20050101之后开始算

--因子2：
--select SecuCode from Secumain where SecuCategory=1 and SecuMarket in (83,90) and ListedState in (1)
select t2.SecuCode,t1.EndDate,t1.EnterpriseFCFPS,t1.EPSTTM
 from LC_MainIndexNew t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where t2.SecuCode='000001' order by EndDate DESC
