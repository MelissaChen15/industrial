# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/25 9:36

import  pandas as pd
import numpy as np
import time, datetime
from factors.sql import pl_sql_oracle
from factors.util import datetime_ops
from factors.SeasonalValueFactor import SeasonalValueFactor
from factors.SeasonalFinancialQualityFactor import SeasonalFinancialQualityFactor
from factors.SeasonalGrowthFactor import SeasonalGrowthFactor
from factors.DailyValueFactor import DailyValueFactor
from factors.SeasonalSecuIndexFactor import SeasonalSecuIndexFactor
from factors.SeasonalDebtpayingAbilityFactor import  SeasonalDebtpayingAbilityFactor
from factors.SeasonalProfitabilityFactor import SeasonalProfitabilityFactor
from factors.SeasonalOperatingFactor import  SeasonalOperatingFactor
from factors.SeasonalCashFactor import SeasonalCashFactor
from factors.SeasonalDividendFactor import  SeasonalDividendFactor
from factors.SeasonalCapitalStructureFactor import  SeasonalCapitalStructureFactor
from factors.SeasonalEarningQualityFactor import SeasonalEarningQualityFactor
from factors.SeasonalDuPontFactor import SeasonalDuPontFactor
from  factors.DailyDivideSeasonalFactor import DailyDivideSeasonalFactor
from factors.DailyTechnicalIndicatorFactor import DailyTechnicalIndicatorFactor
from factors.SeasonalComposedBasicFactor.form1 import SeasonalComposedBasicFactorF1
from factors.SeasonalComposedBasicFactor.form2 import SeasonalComposedBasicFactorF2
from factors.SeasonalComposedBasicFactor.form3 import SeasonalComposedBasicFactorF3


def update_factor_list(factor_classes:list):
    """
    更新因子主表
    :param factor_classes: list, 包含所有的因子类
    """

    factor_list = pd.DataFrame()
    for c in factor_classes:
        factor_list = factor_list.append(c.get_factor_list(), ignore_index=True)
    # print(factor_list)

    # 将因子表写入数据库
    print('updating factor list')
    from sqlalchemy import String, Integer
    pl_sql_oracle.df_to_DB(df=factor_list, table_name='factorlist',if_exists= 'replace',
                               data_type={'FactorCode': String(16), '简称': String(64), '频率': Integer(),
                                '类别': String(128), '描述': String(512)})
    print('factor list is up to date')


def multidays_write_to_DB(daterange:list, factor_classes:list, mode = 'print'):
    """
    第一次将因子写入数据库
    为了加快速度, 因为单只股票的数据较大, 所以数据库读写按照股票代码循环, 每次只读写一只股票
    :param daterange: list, 时间范围
    :param factor_classes:list, 因子类别
    """
    # 格式转换
    for i in [0,1]:
        if type(daterange[i]) == datetime.date: daterange[i] = daterange[i].strftime("%Y-%m-%d")
    start = daterange[0]
    end = daterange[1]

    # 循环因子类
    for c in factor_classes:
        print('start writing ',c.type,'to DB, date range: ', daterange)
        date_symbol = 'TradingDay' # 日频时间标识符
        if 'Seasonal' in c.__class__.__name__:
            date_symbol = 'EndDate' # 季频时间标识符
        # 其他频率时间标识符加在这里
        ###########################
        c.write_values_to_DB(date='and t1.'+date_symbol+ '<= to_date( \''+ end + '\',\'yyyy-mm-dd\')  '
                                                                            'and t1.'+date_symbol+'>= to_date( \''+ start + '\',\'yyyy-mm-dd\')',mode = mode)
        print(c.type,' is up to date')


def update_ordinary_daily_factors(daterange:list, factor_classes:list, mode = 'print'):
    """
    更新将日频非rolling和非interpolation因子
    为了加快速度, 因为日期范围小, 单只股票的数据不多, 所以每次读写所有的股票在整个datarange上的数据
    如果只需要更新今天的数据, 设置date_range = [datetime.date.today(),datetime.date.today()]
    :param daterange: list, 时间范围
    :param factor_classes:list, 因子类别
    """
    # 格式转换
    for i in [0,1]:
        if type(daterange[i]) == datetime.date: daterange[i] = daterange[i].strftime("%Y-%m-%d")
    start = daterange[0]
    end = daterange[1]

    # 循环因子类
    for c in factor_classes:
        print('start updating ', c.type, '; date range: ', daterange)
        # 因为因子没有做运算,是直接读取的数据库中的某个字段,所以不用write_values_to_DB方法,而是直接加载出所有股票在这一时间段上的值
        try:
            data = c.find_components(file_path=c.data_sql_file_path,
                                        secucode='',
                                        date='and t1.TradingDay = to_date( \''+ end + '\',\'yyyy-mm-dd\')  '
                                                                            'and t1.TradingDay >= to_date( \''+ start + '\',\'yyyy-mm-dd\')'
                                        )
            factor_values = c.get_factor_values(data)
            factor_values = factor_values.reset_index(drop=True) # 重排索引

            from sqlalchemy import String, Integer
            if mode == 'print':
                print(factor_values)
            if mode == 'write':
                pl_sql_oracle.df_to_DB(factor_values,c.__class__.__name__.lower(),if_exists= 'append',data_type={'SECUCODE': String(20)})

        except Exception as e:
            print(e)
        print(c.type,' is up to date')


def update_interpolation_seasonal_factors(date:datetime.date, factor_classes:list, mode = 'print'):

    for c in factor_classes:
        print('start updating ', c.type, '; date: ', date)
        # 为了满足三次样条插值的要求, 从最近的报告日算起, 向前回滚三个报告期, 也就是9个月. e.g. 今天是19.4.5, 读取19.3.31, 18.12.31/9.30/6.30 的数据, 为中间没有数据的月份插值
        start = datetime_ops.last_4th_report_day(date).strftime("%Y-%m-%d")
        end = date.strftime("%Y-%m-%d") # 格式转换
        # print(earliest_report_day, now)

        # 因为必须一只一只股票的插值, 所以虽然速度很慢, 但是只能循环股票代码
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(c.code_sql_file_path, ['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = c.find_components(file_path=c.data_sql_file_path,
                                            secucode='and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'',
                                            date='and t1.EndDate<= to_date( \''+ end + '\',\'yyyy-mm-dd\')  '
                                                                                'and t1.EndDate>= to_date( \''+ start + '\',\'yyyy-mm-dd\')')
                factor_values = c.get_factor_values(data)
                from sqlalchemy import String, Integer

                # 生成删除已有数据的sql
                delete_sql = 'delete from '+c.__class__.__name__.lower() + ' where secucode = \''+ getattr(row, 'SECUCODE') \
                             + '\''+'and startday <= to_date( \''+ end + '\',\'yyyy-mm-dd\')'\
                             +'and startday >= to_date( \''+ start + '\',\'yyyy-mm-dd\')'


                # print(factor_values)
                # print(delete_sql)

                if mode == 'print':
                    print(factor_values)
                    print(delete_sql)
                if mode == 'write':
                    pl_sql_oracle.delete_existing_records(delete_sql)
                    pl_sql_oracle.df_to_DB(factor_values,c.__class__.__name__.lower(),if_exists= 'append',data_type={'SECUCODE': String(20)})


                print(c.type, 'secucode', getattr(row, 'SECUCODE'), ' done')


            except Exception as e:
                print(getattr(row, 'SECUCODE'), e)


        print(c.type,' is up to date')




if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")

    # all_classes = [DailyValueFactor(),SeasonalValueFactor(),SeasonalFinancialQualityFactor(),SeasonalGrowthFactor(),SeasonalSecuIndexFactor(),
    # SeasonalDebtpayingAbilityFactor(),SeasonalProfitabilityFactor(),SeasonalOperatingFactor(),SeasonalCashFactor(),SeasonalDividendFactor(),
    # SeasonalCapitalStructureFactor(),SeasonalEarningQualityFactor(),SeasonalDuPontFactor(),DailyTechnicalIndicatorFactor(),
    # SeasonalComposedBasicFactorF1(),SeasonalComposedBasicFactorF2(),SeasonalComposedBasicFactorF3(),DailyDivideSeasonalFactor()]

    # 更新 因子主表
    # update_factor_list(factor_classes=all_classes)

    # 更新日频非rolling非interpolation
    # ordinary_daily_classes = [DailyValueFactor(),DailyTechnicalIndicatorFactor()]
    # multidays_write_to_DB(daterange = ['2005-01-01', datetime.date.today()], factor_classes= ordinary_daily_classes, mode = 'print') # 日频直接使用05-01-01的数据即可
    # update_ordinary_daily_factors(daterange = ['2019-05-01', datetime.date.today()], factor_classes= ordinary_daily_classes, mode = 'print')


    interpolation_seasonal_classes = [SeasonalValueFactor(),SeasonalFinancialQualityFactor(),SeasonalGrowthFactor(),SeasonalSecuIndexFactor()
        ,SeasonalDebtpayingAbilityFactor()]
    temp = []
    multidays_write_to_DB(daterange = ['2004-12-31', datetime.date.today()], factor_classes= temp, mode='print') # 因为需要插值, 要使用2004-12-31开始的数据
    update_interpolation_seasonal_factors(date = datetime.date.today(), factor_classes= temp, mode='print')





