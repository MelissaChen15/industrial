select t2.SecuCode,t1.TradingDay,t1.Highprice,t1.Lowprice,t1.Openprice,t1.Closeprice,t1.Turnovervolume
from QT_DailyQuote t1
inner join SecuMain t2
on t1.InnerCode=t2.InnerCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t2.SecuCategory = 1) and (t1.tradingday >= to_date( '2004-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') )
