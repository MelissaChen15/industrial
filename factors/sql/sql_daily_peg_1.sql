 -- 注意：取2005-01-01及之后的数据，要设置date >= 2004-12-31, 否则季度数据无法插值就会有缺失的情况

 -- PEG计算 日频数据部分
--表1 ：LC_DIndicesForValuation, 日频
select t2.SecuCode,t1.TradingDay,t1.PE
 from LC_DIndicesForValuation t1
inner join SecuMain t2
on t1.InnerCode=t2.InnerCode
where (t2.SecuMarket='83' or t2.SecuMarket='90')