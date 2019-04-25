 -- 注意：取2005-01-01及之后的数据，要设置date >= 2004-12-31, 否则季度数据无法插值就会有缺失的情况

--表1： LC_MainIndexNew
select t2.SecuCode,t1.EndDate, t1.QuickRatio, t1.DebtEquityRatio, t1.SEWithoutMIToTL, t1.SEWMIToInterestBearDebt, t1.DebtTangibleEquityRatio, t1.TangibleAToNetDebt, t1.EBITDAToTLiability, t1.NOCFToTLiability, t1.NOCFToInterestBearDebt, t1.NOCFToCurrentLiability, t1.NOCFToNetDebt, t1.InterestCover, t1.LongDebtToWorkingCapital, t1.OperCashInToCurrentDebt
 from LC_MainIndexNew t1
inner join SecuMain t2
on t1.CompanyCode=t2.CompanyCode
where (t2.SecuMarket='83' or t2.SecuMarket='90') and (t1.enddate >= to_date( '2004-12-31 00:00:00','yyyy-mm-dd hh24:mi:ss') )


