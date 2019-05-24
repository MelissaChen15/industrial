select t2.SecuCode,t1.TradingDay,t1.ChangePCTRW
from QT_Performance t1
inner join SecuMain t2
on t1.InnerCode=t2.InnerCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t2.SecuCategory = 1) and (t1.tradingday >= to_date( '2001-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') ) 
