# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/8  20:25
desc:
'''
from util.FinancialModelFunc import FinancialModel_statsFunc


class weeklyFinancialModelFactorProcess(FinancialModel_statsFunc):
    def __init__(self, TradingDay, ChangePCT, HS300ChangePCT, SZ50ChangePCT, ZZ500ChangePCT,
                 data_sql_file_path, code_sql_file_path,flag=2):
        super().__init__(TradingDay, ChangePCT, HS300ChangePCT, SZ50ChangePCT, ZZ500ChangePCT, flag,
                         data_sql_file_path, code_sql_file_path)
        self.frequency = 2
