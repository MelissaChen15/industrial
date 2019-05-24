select t2.SecuCode,t1.TradingDay,t1.ClosePrice,t1.NegotiableMV,t1.ChangePCT,t3.PB from QT_Performance t1 
inner join SecuMain t2
on t1.InnerCode=t2.InnerCode
inner join LC_DIndicesForValuation t3
on t1.InnerCode=t3.InnerCode and t1.TradingDay=t3.tradingday
where (t2.SecuMarket='83' or t2.SecuMarket='90')

-- and (t1.tradingday = to_date( '2019-04-30 00:00:00','yyyy-mm-dd hh24:mi:ss') )
