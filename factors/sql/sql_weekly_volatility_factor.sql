select t2.SecuCode,t1.TradingDay,t1.HighestClosePriceRW,t1.HighPriceRW,t1.LowPriceRW,t1.TurnoverVolumeRW,t1.TurnoverRateRW,t1.ChangePCTRW
from QT_Performance t1
inner join SecuMain t2
on t1.InnerCode=t2.InnerCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t2.SecuCategory = 1)
