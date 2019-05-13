 -- 注意：取2005-01-01及之后的数据，要设置date >= 2004-12-31, 否则季度数据无法插值就会有缺失的情况

--表1 ：LC_DIndicesForValuation
select t2.SecuCode,t1.TradingDay,t1.PE,t1.PELYR,t1.PB,t1.PCFTTM,t1.PCFSTTM,t1.PS,t1.PSTTM,t1.DividendRatio,t1.TotalMV
 from LC_DIndicesForValuation t1 
inner join SecuMain t2
on t1.InnerCode=t2.InnerCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t1.tradingday >= to_date( '2004-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') )
