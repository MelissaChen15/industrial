select TradingDate from QT_TradingDayNew t1 where t1.TradingDate> to_date( '2001-12-31','yyyy-mm-dd') and t1.SecuMarket=83 and t1.IfTradingDay=1 and t1.IfWeekEnd=1
--and t1.TradingDate<= to_date( '2019-05-07 00:00:00','yyyy-mm-dd hh24:mi:ss')
