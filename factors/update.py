# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/25 9:36

import datetime

import pandas as pd

from factors.SeasonalCapitalStructureFactor import SeasonalCapitalStructureFactor
from factors.SeasonalCashFactor import SeasonalCashFactor
from factors.SeasonalComposedBasicFactor.form1 import SeasonalComposedBasicFactorF1
from factors.SeasonalComposedBasicFactor.form2 import SeasonalComposedBasicFactorF2
from factors.SeasonalComposedBasicFactor.form3 import SeasonalComposedBasicFactorF3
from factors.SeasonalDebtpayingAbilityFactor import SeasonalDebtpayingAbilityFactor
from factors.SeasonalDividendFactor import SeasonalDividendFactor
from factors.SeasonalDuPontFactor import SeasonalDuPontFactor
from factors.SeasonalEarningQualityFactor import SeasonalEarningQualityFactor
from factors.SeasonalFinancialQualityFactor import SeasonalFinancialQualityFactor
from factors.SeasonalGrowthFactor import SeasonalGrowthFactor
from factors.SeasonalOperatingFactor import SeasonalOperatingFactor
from factors.SeasonalProfitabilityFactor import SeasonalProfitabilityFactor
from factors.SeasonalSecuIndexFactor import SeasonalSecuIndexFactor
from factors.SeasonalValueFactor import SeasonalValueFactor
from factors.DailyPEG import DailyPEG
from factors.DailyValueFactor import  DailyValueFactor
from factors.DailyTechnicalIndicatorFactor import DailyTechnicalIndicatorFactor
from factors.WeeklyTurnoverFactor import WeeklyTurnoverFactor
from factors.DailyCorrelationFactor import DailyCorrelationFactor
from factors.DailyMomentumFactor import DailyMomentumFactor
from factors.DailyIdiosyncrasticFactor import  DailyIdiosyncrasticFactor
from factors.DailyTurnoverFactor import DailyTurnoverFactor
from factors.DailyVolatilityFactor import  DailyVolatilityFactor
from factors.MonthlyTurnoverFactor import MonthlyTurnoverFactor
from factors.WeeklyCorrelationFactor import WeeklyCorrelationFactor
from factors.WeeklyIdiosyncrasticFactor import WeeklyIdiosyncrasticFactor
from  factors.WeeklyMomentumFactor import WeeklyMomentumFactor
from factors.WeeklyTechnicalIndicatorFactor import WeeklyTechnicalIndicatorFactor
from factors.WeeklyVolatilityFactor import WeeklyVolatilityFactor
from factors.DailyFinancialModelFactor1 import DailyFinancialModelFactor1
from factors.DailyFinancialModelFactor2 import DailyFinancialModelFactor2
from factors.WeeklyFinancialModelFactor1 import  WeeklyFinancialModelFactor1
from factors.WeeklyFinancialModelFactor2 import  WeeklyFinancialModelFactor2
from factors.sql import pl_sql_oracle
from factors.util import datetime_ops


def update_factor_list(factor_classes:list, mode = 'print'):
    """
    更新因子主表
    :param factor_classes: list, 包含所有的因子类
    :param mode: str, default = 'print'. 函数模式,  'print'表示将计算结果打印到terminal, 'write'表示将计算结果写入数据库

    """
    print('updating factor list')
    factor_list = pd.DataFrame()
    for c in factor_classes:
        factor_list = factor_list.append(c.get_factor_list(), ignore_index=True)

    if mode == 'print':
        print(factor_list)
    if mode == 'write':
        # 将因子表写入数据库
        from sqlalchemy import String, Integer
        pl_sql_oracle.df_to_DB(df=factor_list, table_name='factorlist',if_exists= 'replace',
                                   data_type={'FactorCode': String(16), '表名': String(128),'简称': String(128), '频率': Integer(),
                                    '类别': String(128), '描述': String(512)})
        from factors.util.logger import Logger
        logger = Logger.getLogger()
        logger.info('update factor list')

    print('factor list is up to date')


def multidays_write_to_DB(daterange:list, factor_classes:list, mode = 'print'):
    """
    第一次将因子写入数据库
    为了加快速度, 因为单只股票的数据较大, 所以数据库读写按照股票代码循环, 每次只读写一只股票
    :param daterange: list, 时间范围
    :param factor_classes:list, 因子类别
    :param mode: str, default = 'print'. 函数模式,  'print'表示将计算结果打印到terminal, 'write'表示将计算结果写入数据库
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
        if c.__class__.__name__.startswith(('Seasonal')):
            date_symbol = 'EndDate' # 季频时间标识符
        # 其他频率时间标识符加在这里
        ###########################
        if mode == 'write':
            from factors.util.logger import Logger
            logger = Logger.getLogger()
            info = 'update ' + c.__class__.__name__ + '; date range: from ' + daterange[0] + ' to ' + daterange[1]
            logger.info(info)

        c.write_values_to_DB(date='and t1.'+date_symbol+ '<= to_date( \''+ end + '\',\'yyyy-mm-dd\')  '
                                                                            'and t1.'+date_symbol+'>= to_date( \''+ start + '\',\'yyyy-mm-dd\')',mode = mode)
        print(c.type,' is up to date')


def update_ordinary_daily_factors(daterange:list, factor_classes:list, mode = 'print'):
    """
    更新日频因子, 包括普通的不需要rolling的日频因子
    为了加快速度, 因为日期范围小, 单只股票的数据不多, 所以每次读写所有的股票在整个datarange上的数据
    如果只需要更新今天的数据, 设置date_range = [datetime.date.today(),datetime.date.today()]
    :param daterange: list, 时间范围
    :param factor_classes:list, 因子类别
    :param mode: str, default = 'print'. 函数模式,  'print'表示将计算结果打印到terminal, 'write'表示将计算结果写入数据库
    """
    from factors.util.logger import Logger
    logger = Logger.getLogger()

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
                                        date='and t1.TradingDay <= to_date( \''+ end + '\',\'yyyy-mm-dd\')  '
                                                                            'and t1.TradingDay >= to_date( \''+ start + '\',\'yyyy-mm-dd\')'
                                        )
            # print(data)
            factor_values = c.get_factor_values(data)
            # print(factor_values)
            factor_values = factor_values.reset_index(drop=True) # 重排索引


            # 将原有记录删掉, 以防重复写入
            delete_sql = 'delete from ' + c.__class__.__name__.lower() +  ' where TRADINGDAY <= to_date( \'' + end + '\',\'yyyy-mm-dd\')' \
                         + 'and TRADINGDAY >= to_date( \'' + start + '\',\'yyyy-mm-dd\')'


            from sqlalchemy import String, Integer
            if mode == 'print':
                print(factor_values)
                print(delete_sql)
            if mode == 'write':
                info = 'update ' + c.__class__.__name__ + '; date range: from ' + daterange[0] + ' to ' + daterange[1]
                logger.info(info)

                pl_sql_oracle.delete_existing_records(delete_sql)
                pl_sql_oracle.df_to_DB(factor_values,c.__class__.__name__.lower(),if_exists= 'append',data_type={'SECUCODE': String(20)})

        except Exception as e:
            print(e)
            logger.warning(e)
        print(c.type,' is up to date')


def update_interpolation_seasonal_factors(date:datetime.date, factor_classes:list, mode = 'print'):
    """
    更新需要插值到月频的季频因子
    :param date: datetime.date, 更新至date, 一般设为datetime.date.today()
    :param factor_classes: list, 因子类别
    :param mode: str, default = 'print'. 函数模式,  'print'表示将计算结果打印到terminal, 'write'表示将计算结果写入数据库
    :return:
    """
    from factors.util.logger import Logger
    logger = Logger.getLogger()

    for c in factor_classes:
        print('start updating ', c.type, '; date: ', date)
        # 为了满足三次样条插值的要求, 从最近的报告日算起, 向前回滚三个报告期, 也就是9个月. e.g. 今天是19.4.5, 读取19.3.31, 18.12.31/9.30/6.30 的数据, 为中间没有数据的月份插值
        start = datetime_ops.last_4th_report_day(date).strftime("%Y-%m-%d")
        end = date.strftime("%Y-%m-%d") # 格式转换
        # print(earliest_report_day, now)

        if mode == 'write':
            info = 'update ' + c.__class__.__name__ + '; date range: until ' + end
            logger.info(info)

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

                sql_suffix = c.__class__.__name__.lower() + ' where secucode = \'' + getattr(row, 'SECUCODE') + '\'' \
                             + 'and startday <= to_date( \'' + end + '\',\'yyyy-mm-dd\')'\
                             + 'and startday >= to_date( \'' + start + '\',\'yyyy-mm-dd\')'

                # 首先匹配数据库中已有的数据, 如果原数据不是nan就使用原数据
                match_sql = 'select * from ' + sql_suffix
                match_data = pl_sql_oracle.execute_inquery(match_sql)


                ###### 重要: 两表取各自非nan的值 #######
                for col in factor_values.columns:
                    if factor_values[col].dtype != float: continue
                    cond1 = factor_values[col].isna() & ~match_data[col.upper()].isna()
                    cond2 = cond1.mask(cond1.isna(), False)
                    factor_values[col] = factor_values[col].mask(cond2.astype('bool'), match_data[col.upper()])

                    # factor_values[col] = match_data[col.upper()].mask(match_data[col.upper()].isna() & ~factor_values[col].isna(), factor_values[col])


                # 生成删除已有数据的sql
                delete_sql = 'delete from ' + sql_suffix

                if mode == 'print':
                    print(factor_values)
                    print(delete_sql)
                if mode == 'write':
                    pl_sql_oracle.delete_existing_records(delete_sql)
                    pl_sql_oracle.df_to_DB(factor_values,c.__class__.__name__.lower(),if_exists= 'append',data_type={'SECUCODE': String(20)})

                print(c.type, 'secucode', getattr(row, 'SECUCODE'), ' done')


            except Exception as e:
                logger.warning(getattr(row, 'SECUCODE'), e)
                print(getattr(row, 'SECUCODE'), e)


        print(c.type,' is up to date')


def peg_multidays_to_DB(daterange:list, factor_classes:list, mode = 'print'):
    """
    首次写入 日频价值类特殊处理因子 PEG
    :param daterange: list, 时间范围
    :param factor_classes:list, 因子类别
    :param mode: str, default = 'print'. 函数模式,  'print'表示将计算结果打印到terminal, 'write'表示将计算结果写入数据库
    """
    from factors.util.logger import Logger
    logger = Logger.getLogger()

    # 格式转换
    for i in [0, 1]:
        if type(daterange[i]) == datetime.date: daterange[i] = daterange[i].strftime("%Y-%m-%d")

    # 循环因子类
    for c in factor_classes:
        print('start writing ', c.type, 'to DB, date range: ', daterange)
        if mode == 'write':
            info = 'update ' + c.__class__.__name__ + '; date range: from ' + daterange[0] + ' to ' + daterange[1]
            logger.info(info)
        c.write_values_to_DB(date=daterange, mode=mode)
        print(c.type, ' is up to date')


def update_peg(date:datetime.date, factor_classes:list, mode = 'print'):
    """
    更新peg
    :param date: datetime.date, 更新至date, 一般设为datetime.date.today()
    :param factor_classes: list, 因子类别
    :param mode: str, default = 'print'. 函数模式,  'print'表示将计算结果打印到terminal, 'write'表示将计算结果写入数据库
    """
    from factors.util.logger import Logger
    logger = Logger.getLogger()

    for c in factor_classes:
        print('start updating ', c.type, '; date: ', date)
        # 为了满足三次样条插值的要求, 从最近的报告日算起, 向前回滚三个报告期, 也就是9个月. e.g. 今天是19.4.5, 读取19.3.31, 18.12.31/9.30/6.30 的数据, 为中间没有数据的月份插值
        start = datetime_ops.last_4th_report_day(date).strftime("%Y-%m-%d")
        end = date.strftime("%Y-%m-%d") # 格式转换

        # 因为必须一只一只股票的插值, 所以虽然速度很慢, 但是只能循环股票代码
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(c.code_sql_file_path, ['secucodes'])
        if mode == 'write':
            info = 'update ' + c.__class__.__name__ + '; date range: util ' + end
            logger.info(info)
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = c.find_components(file_path=c.data_sql_file_path,
                                            secucode='and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'',
                                            date=[start, end])
                factor_values = c.get_factor_values(data)

                from sqlalchemy import String, Integer

                sql_suffix = c.__class__.__name__.lower() + ' where secucode = \'' + getattr(row, 'SECUCODE') + '\'' \
                             + 'and tradingday <= to_date( \'' + end + '\',\'yyyy-mm-dd\')'\
                             + 'and tradingday >= to_date( \'' + start + '\',\'yyyy-mm-dd\')'

                # 首先匹配数据库中已有的数据, 如果原数据不是nan就使用原数据
                match_sql = 'select * from ' + sql_suffix
                match_data = pl_sql_oracle.execute_inquery(match_sql)

                ###### 重要: 两表取各自非nan的值 #######
                for col in factor_values.columns:
                    if factor_values[col].dtype != float: continue
                    cond1 = factor_values[col].isna() & ~match_data[col.upper()].isna()
                    cond2 = cond1.mask(cond1.isna(), False)
                    factor_values[col] = factor_values[col].mask(cond2.astype('bool'), match_data[col.upper()])
                    # factor_values[col] = match_data[col.upper()].mask(match_data[col.upper()].isna() & ~factor_values[col].isna(), factor_values[col])


                # 生成删除已有数据的sql
                delete_sql = 'delete from ' + sql_suffix

                if mode == 'print':
                    print(factor_values)
                    print(delete_sql)
                if mode == 'write':
                    pl_sql_oracle.delete_existing_records(delete_sql)
                    pl_sql_oracle.df_to_DB(factor_values,c.__class__.__name__.lower(),if_exists= 'append',data_type={'SECUCODE': String(20)})

                print(c.type, 'secucode', getattr(row, 'SECUCODE'), ' done')


            except Exception as e:
                logger.warning(getattr(row, 'SECUCODE'), e)
                print(getattr(row, 'SECUCODE'), e)


        print(c.type,' is up to date')


def update_rolling_factors(daterange: list, factor_classes:list, mode = 'print'):
    """
    更新不需要插值需要rolling的因子
    注意: 用本函数更新,因子的数据窗口均为向前回滚两年
    :param daterange: [str, datetime.date] 更新的时间range, 第二项一般设为datetime.date.today()
    :param factor_classes: list, 因子类别
    :param mode: str, default = 'print'. 函数模式,  'print'表示将计算结果打印到terminal, 'write'表示将计算结果写入数据库
    """
    from factors.util.logger import Logger
    logger = Logger.getLogger()

    for c in factor_classes:
        print('start updating ', c.type, '; date range: ', daterange)
        # 为了满足rolling的要求, 从最近的报告日算起, 向前回滚两年
        # 格式转换
        start = datetime_ops.last_2nd_year_start(daterange[0]).strftime("%Y-%m-%d")
        end = daterange[1].strftime("%Y-%m-%d")
        for i in [0,1]:
            if type(daterange[i]) == datetime.date :
                daterange[i] = daterange[i].strftime("%Y-%m-%d")
        # print(start, end)

        info = 'update ' + c.__class__.__name__ + '; date range: from ' + daterange[0] + ' to ' + daterange[1]
        logger.info(info)

        # 因为必须一只一只股票的计算相关系数等指标, 所以虽然速度很慢, 但是只能循环股票代码
        sql = pl_sql_oracle.dbData_import()
        s = sql.InputDataPreprocess(c.code_sql_file_path, ['secucodes'])
        for row in s['secucodes'].itertuples(index=True, name='Pandas'):
            try:
                data = c.find_components(file_path=c.data_sql_file_path,
                                            secucode='and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'',
                                            date='and t1.TradingDay<= to_date( \''+ end + '\',\'yyyy-mm-dd\')  '
                                                'and t1.TradingDay>= to_date( \''+ start + '\',\'yyyy-mm-dd\')')
                factor_values = c.get_factor_values(data)

                # 去除不在时间范围内的数据
                factor_values = factor_values.drop(factor_values[factor_values.TRADINGDAY > datetime.date.today()].index)
                factor_values = factor_values.drop(factor_values[factor_values.TRADINGDAY < datetime.datetime.strptime(daterange[0], '%Y-%m-%d') ].index)


                from sqlalchemy import String, Integer

                delete_sql = 'delete from ' + c.__class__.__name__.lower() + ' where secucode = \'' + getattr(row, 'SECUCODE') + '\'' \
                             + 'and TradingDay <= to_date( \'' + end + '\',\'yyyy-mm-dd\')'\
                             + 'and TradingDay >= to_date( \'' + daterange[0] + '\',\'yyyy-mm-dd\')'

                if mode == 'print':
                    print(factor_values)
                    print(delete_sql)
                if mode == 'write':
                    pl_sql_oracle.delete_existing_records(delete_sql)
                    pl_sql_oracle.df_to_DB(factor_values,c.__class__.__name__.lower(),if_exists= 'append',data_type={'SECUCODE': String(20)})

                print(c.type, 'secucode', getattr(row, 'SECUCODE'), ' done')


            except Exception as e:
                logger.warning(getattr(row, 'SECUCODE'), e)
                print(getattr(row, 'SECUCODE'), e)


        print(c.type,' is up to date')


def update_time_series(daterange:list, factor_classes:list, mode = 'print'):
    """
    首次写入 或者 更新日频和周频的time_series文件
    :param daterange: [str, datetime.date] 更新的时间range, 第二项一般设为datetime.date.today()
    :param factor_classes: list, 类别
    :param mode: str, default = 'print'. 函数模式,  'print'表示将计算结果打印到terminal, 'write'表示将计算结果写入数据库
    """
    from factors.util.logger import Logger
    logger = Logger.getLogger()

    # 转换为string
    for i in [0,1]:
        if type(daterange[i]) == datetime.date: daterange[i] = daterange[i].strftime("%Y-%m-%d")
    start = daterange[0]
    end = daterange[1]

    # 循环因子类
    for c in factor_classes:
        print('start updating ',c.get_name(), '; date range: ', daterange)
        # 因为因子没有做运算,是直接读取的数据库中的某个字段,所以不用write_values_to_DB方法,而是直接加载出所有股票在这一时间段上的值
        try:
            factor_values = c.calculate_SMB_HML(daterange=daterange)

            # print(factor_values)
            factor_values = factor_values.reset_index(drop=True) # 重排索引


            # 将原有记录删掉, 以防重复写入
            delete_sql = 'delete from ' + c.get_name() +  ' where "TradingDay" <= to_date( \'' + end + '\',\'yyyy-mm-dd\')' \
                         + 'and "TradingDay" >= to_date( \'' + start + '\',\'yyyy-mm-dd\')'

            if mode == 'print':
                print(factor_values)
                print(delete_sql)
            if mode == 'write':

                info = 'update ' + c.get_name() + '; date range: from ' + daterange[0] + ' to ' + daterange[1]
                logger.info(info)

                from sqlalchemy import Float,String
                try:
                    pl_sql_oracle.delete_existing_records(delete_sql)
                except Exception as e:
                    logger.warning(e)
                    print(e)
                pl_sql_oracle.df_to_DB(factor_values, c.get_name(), if_exists='append', data_type={'SMB': Float()})

        except Exception as e:
            logger.warning(e)
            print(e)
        print(c.get_name() ,' is up to date')



if __name__ == '__main__':
    # 去除warning
    import warnings
    warnings.filterwarnings('ignore')



    ################ 第一次写入数据库之前,请先drop想要写入的数据表 #################


    # 所有的因子类
    all_classes = [DailyValueFactor(),DailyTechnicalIndicatorFactor(),SeasonalValueFactor(),SeasonalFinancialQualityFactor(),SeasonalGrowthFactor(),
    SeasonalDebtpayingAbilityFactor(),SeasonalProfitabilityFactor(),SeasonalOperatingFactor(),SeasonalCashFactor(),SeasonalDividendFactor(),
    SeasonalSecuIndexFactor(),SeasonalCapitalStructureFactor(),SeasonalEarningQualityFactor(),SeasonalDuPontFactor(),
    SeasonalComposedBasicFactorF1(),SeasonalComposedBasicFactorF2(),SeasonalComposedBasicFactorF3(),DailyVolatilityFactor()
    ,DailyPEG(),DailyTurnoverFactor(),DailyCorrelationFactor(),DailyIdiosyncrasticFactor(),DailyMomentumFactor(),
    MonthlyTurnoverFactor(),WeeklyCorrelationFactor(),WeeklyIdiosyncrasticFactor(),WeeklyMomentumFactor(),WeeklyTurnoverFactor(),
    WeeklyVolatilityFactor(),WeeklyTechnicalIndicatorFactor(),DailyFinancialModelFactor1(),DailyFinancialModelFactor2()
    ,WeeklyFinancialModelFactor1(),WeeklyFinancialModelFactor2()]

    # 更新 因子主表
    # update_factor_list(factor_classes=all_classes, mode= 'write')


    # 更新 日频非插值非rolling因子
    # ordinary_daily_classes = [DailyValueFactor()]
    # multidays_write_to_DB(daterange = ['2005-01-01', datetime.date.today()], factor_classes= ordinary_daily_classes, mode = 'print') # 日频直接使用05-01-01的数据即可
    # update_ordinary_daily_factors(daterange = ['2019-05-01', datetime.date.today()], factor_classes= ordinary_daily_classes, mode = 'write')

    # 更新 季频插值因子
    # interpolation_seasonal_classes = [SeasonalValueFactor(),SeasonalFinancialQualityFactor(),SeasonalGrowthFactor(),SeasonalSecuIndexFactor()
    #     ,SeasonalDebtpayingAbilityFactor(),SeasonalProfitabilityFactor(),SeasonalOperatingFactor(),SeasonalCashFactor(),SeasonalDividendFactor(),
    #     SeasonalCapitalStructureFactor(),SeasonalEarningQualityFactor(),SeasonalDuPontFactor(),SeasonalComposedBasicFactorF1(),SeasonalComposedBasicFactorF2(),
    #     SeasonalComposedBasicFactorF3()]
    # multidays_write_to_DB(daterange = ['2004-12-31', datetime.date.today()], factor_classes= interpolation_seasonal_classes, mode='write') # 因为需要插值, 要使用2004-12-31开始的数据
    # update_interpolation_seasonal_factors(date = datetime.date.today(), factor_classes= interpolation_seasonal_classes, mode='write')


    # 更新 日频价值类因子PEG 特殊处理原因: 日频/季频
    # peg = [DailyPEG()]
    # peg_multidays_to_DB(daterange = ['2004-12-31', '2019-04-30'], factor_classes= peg, mode='write') # 因为需要插值, 要使用2004-12-31开始的数据
    # update_peg(date=datetime.date.today(), factor_classes=peg, mode='write')

    # 更新 日频rolling因子
    # rolling_daily_factors = [DailyCorrelationFactor(),DailyTechnicalIndicatorFactor(),
    #                          DailyVolatilityFactor(),DailyMomentumFactor(),DailyIdiosyncrasticFactor(),DailyTurnoverFactor()]
    # multidays_write_to_DB(daterange = ['2002-12-31', '2019-01-01'], factor_classes= rolling_daily_factors, mode = 'print')
    # update_rolling_factors(daterange = ['2019-05-01', datetime.date.today()], factor_classes= rolling_daily_factors, mode = 'write')

    # 更新 月频 非插值rolling因子
    # monthly_rolling_factor = [MonthlyTurnoverFactor()]
    # multidays_write_to_DB(daterange = ['2002-12-31', datetime.date.today()], factor_classes= monthly_rolling_factor, mode = 'write')
    # update_rolling_factors(daterange = ['2019-05-01', datetime.date.today()], factor_classes= monthly_rolling_factor, mode = 'write')


    # 更新 周频 非插值rolling因子
    # weekly_rolling_factors = [WeeklyCorrelationFactor(),WeeklyIdiosyncrasticFactor(),WeeklyMomentumFactor(),WeeklyTechnicalI              ndicatorFactor(),
    #                           WeeklyVolatilityFactor(),WeeklyTurnoverFactor()]
    # multidays_write_to_DB(daterange = ['2002-12-31', datetime.date.today()], factor_classes= weekly_rolling_factors, mode = 'print')
    # update_rolling_factors(daterange = ['2019-05-01', datetime.date.today()], factor_classes= weekly_rolling_factors, mode = 'print')

    # 更新 日频和周频的timeseries
    # from factors import DailyTimeSeries,WeeklyTimeSeries
    # series = [DailyTimeSeries,WeeklyTimeSeries]
    # 更新或者首次写入都是使用下面这个函数
    # update_time_series(daterange=['2019-05-01', datetime.date.today()], factor_classes=[DailyTimeSeries],mode='write')

    # 更新 日频和周频的financial model因子
    # financial_models = [DailyFinancialModelFactor1(),DailyFinancialModelFactor2(),WeeklyFinancialModelFactor1(),WeeklyFinancialModelFactor2()]
    # multidays_write_to_DB(daterange = ['2002-12-31', datetime.date.today()], factor_classes= financial_models, mode = 'print')
    # update_rolling_factors(daterange = ['2019-05-01', datetime.date.today()], factor_classes= financial_models, mode = 'print')










