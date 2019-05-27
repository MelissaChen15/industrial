 -- 注意：取2005-01-01及之后的数据，要设置date >= 2004-12-31, 否则季度数据无法插值就会有缺失的情况

--表1： QT_TradingDayNew
select t1.TradingDate,  t1.IfTradingDay, t1.IfWeekEnd, t1.IfMonthEnd, t1.IfQuarterEnd, t1.IfYearEnd
from QT_TradingDayNew t1
where (t1.SecuMarket='83' or t1.SecuMarket='90')
