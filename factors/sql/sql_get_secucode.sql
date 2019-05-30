 -- 注意：取2005-01-01及之后的数据，要设置date >= 2004-12-31, 否则季度数据无法插值就会有缺失的情况


 -- A股代码
select secucode from SecuMain t2
where (t2.SecuMarket='83' or t2.SecuMarket='90') and t2.SecuCategory = 1 and ListedState = 1