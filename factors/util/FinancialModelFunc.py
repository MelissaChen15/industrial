# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/8  11:04
desc:
'''
import pandas as pd
from factors.util.StockIndexGroup import StockIndexGroup
from factors.util.FinancialCAPMModelCal import CAPM_ModelCal
from factors.util.FinancialFF3ModelCal import FF3_ModelCal
from factors.sql import pl_sql_oracle

import numpy as np


# 对于周频信号，那么输入数据本身也是周频。
class FinancialModel_statsFunc(StockIndexGroup):

    def __init__(self,TradingDay,ChangePCT,flag,
                 code_sql_file_path1):
        # 三类指数的涨跌幅带时间序列索引，个股的涨幅必须也带
        # 三类指数既可以是日频的涨跌幅，也可以是周频的涨跌幅
        if flag == 1:
            super().__init__(flag,code_sql_file_path1,weekday_sql_file_path='')  # path1是指数数据的路径
            ChangePCT.index = TradingDay
            self.ChangePCT = ChangePCT  # 涨跌幅
            self.ChangePCT = self.ChangePCT.astype('float')
            # self.data_sql_file_path = data_sql_file_path_classic  # 计算SMB,HML使用，ClassicalFactorcal类的参数
            # self.code_sql_file_path = code_sql_file_path2_tradingday  # 计算SMB,HML使用，ClassicalFactorcal类的参数
            self.flag = flag
        elif flag==2:
            weeklyday_file_path = r'.\sql\sql_get_last_trading_weekday.sql'
            super().__init__(flag,code_sql_file_path1,weekday_sql_file_path=weeklyday_file_path)  # path1是指数数据的路径
            ChangePCT.index = TradingDay
            self.ChangePCT = ChangePCT  # 涨跌幅
            self.ChangePCT = self.ChangePCT.astype('float')

        self.ChangePCT = self.ChangePCT * 0.01
        self.HS300ChangePCT = self.HS300ChangePCT * 0.01
        self.ZZ500ChangePCT = self.ZZ500ChangePCT * 0.01
        self.SZ50ChangePCT = self.SZ50ChangePCT * 0.01
            # self.data_sql_file_path = data_sql_file_path_classic  # 计算SMB,HML使用，ClassicalFactorcal类的参数
            # self.code_sql_file_path = code_sql_file_path2_tradingday  # 计算SMB,HML使用，ClassicalFactorcal类的参数
        self.flag = flag

    def CAPM_model_stats(self,marketindex):
        if marketindex == 'IF':
            if self.flag == 1:
                finance_model = CAPM_ModelCal(self.HS300ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
                upsidebeta_all, downsidebeta_all, sidediffbeta_all = finance_model.sideBeta()
            elif self.flag == 2:
                finance_model = CAPM_ModelCal(self.HS300ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
                upsidebeta_all, downsidebeta_all, sidediffbeta_all = finance_model.sideBeta()

        elif marketindex == 'IC':
            if self.flag == 1:
                finance_model = CAPM_ModelCal(self.ZZ500ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
                upsidebeta_all, downsidebeta_all, sidediffbeta_all = finance_model.sideBeta()

            elif self.flag == 2:
                finance_model = CAPM_ModelCal(self.ZZ500ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
                upsidebeta_all, downsidebeta_all, sidediffbeta_all = finance_model.sideBeta()

        elif marketindex == 'IH':
            if self.flag == 1:
                finance_model = CAPM_ModelCal(self.SZ50ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
                upsidebeta_all, downsidebeta_all, sidediffbeta_all = finance_model.sideBeta()

            elif self.flag == 2:
                finance_model = CAPM_ModelCal(self.SZ50ChangePCT,self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                alpha1_all, beta_all = finance_model.CAPM_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
                upsidebeta_all, downsidebeta_all, sidediffbeta_all = finance_model.sideBeta()

        return alpha1_all,beta_all,residuals_stats,upsidebeta_all, downsidebeta_all, sidediffbeta_all

    def FF3_model_stats(self,marketindex,SMB_HML_file_path_daily,SMB_HML_file_path_weekly):
        sql = pl_sql_oracle.dbData_import()
        if self.flag == 1:
            SMB_and_HML_dict = sql.InputDataPreprocess(SMB_HML_file_path_daily, table_name = ['dailytimeseries'])  # 字典格式
            # print(SMB_and_HML_dict)
            SMB_and_HML_dict['dailytimeseries'].index = SMB_and_HML_dict['dailytimeseries']['TradingDay'.upper()]  # dailytimeseries表中的字段名
            SMB_and_HML = SMB_and_HML_dict['dailytimeseries']

        elif self.flag == 2:
            SMB_and_HML_dict = sql.InputDataPreprocess(SMB_HML_file_path_weekly, table_name = ['weeklytimeseries'])
            SMB_and_HML_dict['weeklytimeseries'].index = SMB_and_HML_dict['weeklytimeseries']['TradingDay'.upper()]  # weeklytimeseries表中的字段名
            SMB_and_HML = SMB_and_HML_dict['weeklytimeseries']
        # print(SMB_and_HML)
        # self.ChangePCT = self.ChangePCT*0.01
        # self.HS300ChangePCT = self.HS300ChangePCT*0.01
        # self.ZZ500ChangePCT = self.ZZ500ChangePCT*0.01
        # self.SZ50ChangePCT = self.SZ50ChangePCT*0.01
        SMB_and_HML[['SMB','HML']] = SMB_and_HML[['SMB','HML']]*0.01  # 量纲统一成国际单位制 #注意这里
        # print(SMB_and_HML)
        if marketindex == 'IF':
            if self.flag == 1:
                # factors_exm = TimeseriesFactorCal(self.data_sql_file_path,self.code_sql_file_path)
                # SMB_and_HML = factors_exm.get_data_cal()  # 注意得到的日期序列顺序与self.HS300ChangePCT不匹配！！！
                finance_model = FF3_ModelCal(self.HS300ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                finance_model.data_align()
                alpha1_all, beta_all = finance_model.FF3_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
            elif self.flag == 2:
                finance_model = FF3_ModelCal(self.HS300ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                finance_model.data_align()
                alpha1_all, beta_all = finance_model.FF3_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量

        elif marketindex == 'IC':
            if self.flag == 1:
                finance_model = FF3_ModelCal(self.ZZ500ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                finance_model.data_align()
                alpha1_all, beta_all = finance_model.FF3_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
            elif self.flag == 2:
                finance_model = FF3_ModelCal(self.ZZ500ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                finance_model.data_align()
                alpha1_all, beta_all = finance_model.FF3_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量

        elif marketindex == 'IH':
            if self.flag == 1:
                finance_model = FF3_ModelCal(self.SZ50ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                finance_model.data_align()
                alpha1_all, beta_all = finance_model.FF3_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量
            elif self.flag == 2:
                finance_model = FF3_ModelCal(self.SZ50ChangePCT,SMB_and_HML['SMB'],SMB_and_HML['HML'],self.ChangePCT,self.flag,rolling_window=[[3,6],[6,12]])
                finance_model.data_align()
                alpha1_all, beta_all = finance_model.FF3_cal()  # 注意输出是字典，包含不同时间窗口的数据
                residuals_stats = finance_model.residuals_model_cal(alpha1_all,beta_all)  # 残差统计量，5个统计量

        return alpha1_all,beta_all,residuals_stats

