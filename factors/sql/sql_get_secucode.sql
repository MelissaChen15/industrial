 -- 注意：取2005-01-01及之后的数据，要设置date >= 2004-12-31, 否则季度数据无法插值就会有缺失的情况


 -- A股代码
select secucode from SecuMain t
where (t.SecuMarket='83' or t.SecuMarket='90') and t.SecuCategory = 1 order by secucode