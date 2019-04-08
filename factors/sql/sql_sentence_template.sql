

--因子1：总市值 TotalMV ,涨跌幅 ChangePCT
select t2.SecuCode,t1.TradingDay,t1.PE,t1.PB  from LC_DIndicesForValuation t1 
inner join SecuMain t2
on t1.InnerCode=t2.InnerCode 
where t2.SecuCode='000001' order by TradingDay 

--因子2：

--select SecuCode from Secumain where SecuCategory=1 and SecuMarket in (83,90) and ListedState in (1)


--加一下20050101之后开始算