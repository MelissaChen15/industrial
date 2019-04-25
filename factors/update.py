# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/25 9:36

import  pandas as pd
import numpy as np
from factors.sql import pl_sql_oracle
from factors.SeasonalValueFactor import SeasonalValueFactor
from factors.SeasonalFinancialQualityFactor import SeasonalFinancialQualityFactor
from factors.SeasonalGrowthFactor import SeasonalGrowthFactor
from factors.DailyValueFactor import DailyValueFactor
from factors.SeasonalSecuIndexFactor import SeasonalSecuIndexFactor
from factors.SeasonalDebtpayingAbilityFactor import  SeasonalDebtpayingAbilityFactor
from factors.SeasonalProfitabilityFactor import SeasonalProfitabilityFactor
from factors.SeasonalOperatingFactor import  SeasonalOperatingFactor
from factors.SeasonalCashFactor import SeasonalCashFactor


def update():
    # TODO: 写入数据表之前检查写入方式是replace还是append
    # TODO: 写入数据表之前检查时间戳

    factor_list = pd.DataFrame()


    # 日频价值类
    dvf = DailyValueFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_daily_value_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # dvf.write_values_to_DB(mode = 'append',data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = dvf.get_factor_list()
    factor_list = factor_list.append(curr_list,ignore_index=True)


    # 季频价值类
    svf = SeasonalValueFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_value_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # svf.write_values_to_DB(mode = 'append',data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = svf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 季频财务质量类
    sfqf = SeasonalFinancialQualityFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_financial_quality_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # sfqf.write_values_to_DB(mode = 'append',data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = sfqf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 季频成长类 未写入
    sgv = SeasonalGrowthFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_growth_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # sgv.write_values_to_DB(mode = 'append',data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)
    curr_list = sgv.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 季频每股指标 未写入
    ssif = SeasonalSecuIndexFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_secu_index_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # ssif.write_values_to_DB(mode = 'append',,data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = ssif.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 季频偿债能力 未写入
    sdaf = SeasonalDebtpayingAbilityFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_debtpaying_ability_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # sdaf.write_values_to_DB(mode = 'append',data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = sdaf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 季频盈利能力 未写入
    spf = SeasonalProfitabilityFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_profitability_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # spf.write_values_to_DB(mode='append', data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = spf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)

    # 季频营运能力 未写入
    sof = SeasonalOperatingFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_operating_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # sof.write_values_to_DB(mode='append', data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = sof.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 季频现金状况 未写入
    scf = SeasonalCashFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_cash_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # scf.write_values_to_DB(mode='append', data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = scf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 将因子表写入数据库
    print(factor_list)
    from sqlalchemy import String, Integer
    pl_sql_oracle.df_to_DB(df=factor_list, table_name='factorlist',if_exists= 'replace',
                               data_type={'FactorCode': String(16), '简称': String(64), '频率': Integer(),
                                '类别': String(128), '描述': String(512)})


if __name__ == '__main__':
    update()
    # from sqlalchemy import create_engine
    # engine = create_engine('oracle+cx_oracle://jydb:jydb@192.168.1.187/JYDB')
    # df = pd.DataFrame(engine.execute("SELECT * FROM DailyValueFactor").fetchall())
    # print(df.shape)
