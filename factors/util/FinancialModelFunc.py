# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/8  11:04
desc:
'''
import pandas as pd
from util.StockIndexGroup import StockIndexGroup
from util.FinancialCAPMModelCal import CAPM_ModelCal
from  util.FinancialFF3ModelCal import FF3_ModelCal
from util.ClassicalFactorcal import TimeseriesFactorCal
from util.ClassicalFactorcal_weekly import TimeseriesFactorCal_weekly
import numpy as np


# input_y = pd.DataFrame(np.random.random(200))
# data1 = pd.DataFrame(np.arange(200))
# mad = lambda x: (x[-1]-x[0])/x[0]
# input_y = input_y.rolling(5)
#
# pd.DataFrame(data1)

# 对于周频信号，那么输入数据本身也是周频。
class FinancialModel_statsFunc(StockIndexGroup):

    def __init__(self,TradingDay,ChangePCT,flag,
                 data_sql_file_path,code_sql_file_path1,code_sql_file_path2):
        # 三类指数的涨跌幅带时间序列索引，个股的涨幅必须也带
        # 三类指数既可以是日频的涨跌幅，也可以是周频的涨跌幅
        super().__init__(flag,code_sql_file_path1)  # path1是指数数据的路径
        ChangePCT.index = TradingDay
        self.ChangePCT = ChangePCT  # 涨跌幅
        self.data_sql_file_path = data_sql_file_path  # 计算SMB,HML使用，ClassicalFactorcal类的参数
        self.code_sql_file_path = code_sql_file_path2  # 计算SMB,HML使用，ClassicalFactorcal类的参数

    def CAPM_model_stats(self,marketindex):
        if marketindex == 'IF':
            if self.flag == 1:
                finance_model = CAPM_ModelCal(self.HS300ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
            elif self.flag == 2:
                finance_model = CAPM_ModelCal(self.HS300ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量

        elif marketindex == 'IC':
            if self.flag == 1:
                finance_model = CAPM_ModelCal(self.ZZ500ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
            elif self.flag == 2:
                finance_model = CAPM_ModelCal(self.ZZ500ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量

        elif marketindex == 'IH':
            if self.flag == 1:
                finance_model = CAPM_ModelCal(self.SZ50ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
            elif self.flag == 2:
                finance_model = CAPM_ModelCal(self.SZ50ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量

        return beta_all,residuals_stats


    def FF3_model_stats(self,marketindex):
        if marketindex == 'IF':
            if self.flag == 1:
                factors_exm = TimeseriesFactorCal(self.data_sql_file_path,self.code_sql_file_path)
                SMB_and_HML = factors_exm.get_data_cal()  # 注意得到的日期序列顺序与self.HS300ChangePCT不匹配！！！
                finance_model = FF3_ModelCal(self.HS300ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
            elif self.flag == 2:
                factors_exm = TimeseriesFactorCal_weekly(self.data_sql_file_path,self.code_sql_file_path)
                SMB_and_HML = factors_exm.get_data_cal()
                finance_model = FF3_ModelCal(self.HS300ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量

        elif marketindex == 'IC':
            if self.flag == 1:
                factors_exm = TimeseriesFactorCal(self.data_sql_file_path,self.code_sql_file_path)
                SMB_and_HML = factors_exm.get_data_cal()
                finance_model = FF3_ModelCal(self.ZZ500ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
            elif self.flag == 2:
                factors_exm = TimeseriesFactorCal_weekly(self.data_sql_file_path,self.code_sql_file_path)
                SMB_and_HML = factors_exm.get_data_cal()
                finance_model = FF3_ModelCal(self.ZZ500ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量

        elif marketindex == 'IH':
            if self.flag == 1:
                factors_exm = TimeseriesFactorCal(self.data_sql_file_path,self.code_sql_file_path)
                SMB_and_HML = factors_exm.get_data_cal()
                finance_model = FF3_ModelCal(self.SZ50ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
            elif self.flag == 2:
                factors_exm = TimeseriesFactorCal_weekly(self.data_sql_file_path,self.code_sql_file_path)
                SMB_and_HML = factors_exm.get_data_cal()
                finance_model = FF3_ModelCal(self.SZ50ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量

        return beta_all,residuals_stats




