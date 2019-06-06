# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/6/4  16:49
desc:
'''
import datetime
from sql import pl_sql_oracle
from FactorReturnsCal import FactorReturnsCal
from FactorReturnCal_weekly import FactorReturnsCal_Weekly
from FactorReturnCal_Monthly import FactorReturnsCal_Monthly


def update_time_series(daterange:list, factor_classes:list, table_name,frequency,mode = 'print'):
    """
    首次写入 或者 更新日频和周频的time_series文件
    :param daterange: [str, datetime.date] 更新的时间range, 第二项一般设为datetime.date.today()
    :param factor_classes: list, 类别
    :param mode: str, default = 'print'. 函数模式,  'print'表示将计算结果打印到terminal, 'write'表示将计算结果写入数据库
    """
    # 转换为string
    for i in [0,1]:
        if type(daterange[i]) == datetime.date: daterange[i] = daterange[i].strftime("%Y-%m-%d")
    start = daterange[0]
    end = daterange[1]

    if frequency == 1:
        cal_method = FactorReturnsCal
        auxiliary_tablename ='QT_Performance'
        auxiliary_name = ['ChangePCT','NEGOTIABLEMV']
    elif frequency == 2:
        cal_method = FactorReturnsCal_Weekly
        auxiliary_tablename ='QT_Performance'
        auxiliary_name = ['ChangePCTRW','NEGOTIABLEMV']
    elif frequency == 3:
        cal_method = FactorReturnsCal_Monthly
        auxiliary_tablename = 'QT_Performance'
        auxiliary_name = ['ChangePCTRM', 'NEGOTIABLEMV']

    # 循环因子类
    for c in factor_classes:
        table_name_temp = table_name[table_name.index ==factor_classes.index(c)]  # 生成的或者需要更新的对应因子多空收益率表
        print('start updating ',table_name_temp, '; date range: ', daterange)
        # 因为因子没有做运算,是直接读取的数据库中的某个字段,所以不用write_values_to_DB方法,而是直接加载出所有股票在这一时间段上的值
        try:
            inst_cal1 = cal_method(c,auxiliary_tablename,auxiliary_name,daterange)
            inst_cal1.get_ori_factordata()
            inst_cal1.get_auxiliarydata()
            factor_values = inst_cal1.factor_cal()

            factor_values['TRADINGDAY'] = factor_values.index
            factor_values = factor_values.reset_index(drop=True) # 重排索引

            # 将原有记录删掉, 以防重复写入
            delete_sql = 'delete from ' + table_name_temp.lower() +  ' where TRADINGDAY <= to_date( \'' + end + '\',\'yyyy-mm-dd\')' \
                         + 'and TRADINGDAY >= to_date( \'' + start + '\',\'yyyy-mm-dd\')'

            print(factor_values)
            if mode == 'print':
                print(factor_values)
            if mode == 'write':
                from sqlalchemy import Float,String
                # try:
                #     pl_sql_oracle.delete_existing_records(delete_sql)
                # except Exception as e: print(e)
                print(type(factor_values))
                # print(table_name)
                pl_sql_oracle.df_to_DB(factor_values, table_name_temp, if_exists='append', data_type={'PE': Float()})

        except Exception as e:
            print(e)
        print(table_name_temp ,' is up to date')


if __name__ == '__main__':
    all_classes = ['DailyValueFactor', 'DailyTechnicalIndicatorFactor', 'SeasonalValueFactor',
                   'SeasonalFinancialQualityFactor', 'SeasonalGrowthFactor',
                   'SeasonalDebtpayingAbilityFactor', 'SeasonalProfitabilityFactor', 'SeasonalOperatingFactor',
                   'SeasonalCashFactor', 'SeasonalDividendFactor', 'SeasonalSecuIndexFactor',
                   'SeasonalCapitalStructureFactor', 'SeasonalEarningQualityFactor',
                   'SeasonalDuPontFactor', 'SeasonalComposedBasicFactorF1', 'SeasonalComposedBasicFactorF2',
                   'SeasonalComposedBasicFactorF3', 'DailyVolatilityFactor', 'DailyPEG', 'DailyTurnoverFactor',
                   'DailyCorrelationFactor', 'DailyIdiosyncrasticFactor','DailyMomentumFactor', 'MonthlyTurnoverFactor',
                   'WeeklyCorrelationFactor','WeeklyIdiosyncrasticFactor','WeeklyMomentumFactor()', 'WeeklyTurnoverFactor',
                   'WeeklyVolatilityFactor','WeeklyTechnicalIndicatorFactor',
                   'DailyFinancialModelFactor2','WeeklyFinancialModelFactor1', 'WeeklyFinancialModelFactor2', 'DailyFinancialModelFactor1']

    # 日频因子多空收益率计算与更新,# # 更新或者首次写入都是使用下面这个函数
    frequency = 1
    # dailyseries_all = ['DailyCorrelationFactor','DailyMomentumFactor','DailyIdiosyncrasticFactor','DailyTurnoverFactor',
    #                    'DailyTechnicalIndicatorFactor','DailyVolatilityFactor','DailyValueFactor','DailyFinancialModelFactor1','DailyFinancialModelFactor2']
    series = ['DailyValueFactor']  # 只是举例
    table_name = [x+'LSreturns' for x in series]  # 对应因子的因子多空收益率表格名称
    update_time_series(daterange = ['2019-01-01', datetime.date.today()], table_name=table_name,frequency=frequency,factor_classes = series, mode = 'write')


    # 周频因子多空收益率计算与更新,# # 更新或者首次写入都是使用下面这个函数
    # frequency = 2
    # weeklyseries_all = ['WeeklyCorrelationFactor', 'WeeklyIdiosyncrasticFactor','WeeklyMomentumFactor()', 'WeeklyTurnoverFactor',
    #                     'WeeklyVolatilityFactor', 'WeeklyTechnicalIndicatorFactor', 'WeeklyFinancialModelFactor1', 'WeeklyFinancialModelFactor2']
    # # series = ['WeeklyTurnoverFactor']  # 只是举例
    # table_name = [x + 'LSreturns' for x in series]
    # update_time_series(daterange=['2016-01-01', datetime.date.today()], table_name=table_name, frequency=frequency,
    #                    factor_classes=series, mode='print')

    # 月频因子多空收益率计算与更新,# # 更新或者首次写入都是使用下面这个函数
    # frequency = 3
    # monthlyseries_all = ['SeasonalValueFactor','SeasonalFinancialQualityFactor', 'SeasonalGrowthFactor','SeasonalDebtpayingAbilityFactor', 'SeasonalProfitabilityFactor', 'SeasonalOperatingFactor',
    #            'SeasonalCashFactor', 'SeasonalDividendFactor', 'SeasonalSecuIndexFactor', 'SeasonalCapitalStructureFactor', 'SeasonalEarningQualityFactor',
    #            'SeasonalDuPontFactor', 'SeasonalComposedBasicFactorF1', 'SeasonalComposedBasicFactorF2', 'SeasonalComposedBasicFactorF3']
    #
    # series = ['SeasonalFinancialQualityFactor']  # 只是举例
    # table_name = [x + 'LSreturns' for x in series]
    # update_time_series(daterange=['2016-01-01', datetime.date.today()], table_name=table_name, frequency=frequency,
    #                    factor_classes=series, mode='print')
