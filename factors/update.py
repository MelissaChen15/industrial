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
from factors.SeasonalDividendFactor import  SeasonalDividendFactor
from factors.SeasonalCapitalStructureFactor import  SeasonalCapitalStructureFactor
from factors.SeasonalEarningQualityFactor import SeasonalEarningQualityFactor
from factors.SeasonalDuPontFactor import SeasonalDuPontFactor
from factors.DailyTechnicalIndicatorFactor import DailyTechnicalIndicatorFactor


def update():
    # TODO: 写入数据表之前检查写入方式是replace还是append
    # TODO: 写入数据表之前检查时间戳

    factor_list = pd.DataFrame()


    # 1. 日频价值类
    dvf = DailyValueFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_daily_value_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # dvf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = dvf.get_factor_list()
    factor_list = factor_list.append(curr_list,ignore_index=True)


    # 2. 季频价值类
    svf = SeasonalValueFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_value_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # svf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = svf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 3. 季频财务质量类
    sfqf = SeasonalFinancialQualityFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_financial_quality_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # sfqf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = sfqf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 4. 季频成长类 未写入
    sgv = SeasonalGrowthFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_growth_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # sgv.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)
    curr_list = sgv.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 5. 季频每股指标 未写入
    ssif = SeasonalSecuIndexFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_secu_index_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # ssif.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = ssif.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 6. 季频偿债能力 未写入
    sdaf = SeasonalDebtpayingAbilityFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_debtpaying_ability_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # sdaf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = sdaf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 7. 季频盈利能力 未写入
    spf = SeasonalProfitabilityFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_profitability_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # spf.write_values_to_DB( data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = spf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)

    # 8. 季频营运能力 未写入
    sof = SeasonalOperatingFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_operating_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # sof.write_values_to_DB( data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = sof.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)


    # 9. 季频现金状况 未写入
    scf = SeasonalCashFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_cash_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # scf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = scf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)

    # 10. 季频分红能力 未写入
    sdf = SeasonalDividendFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_dividend_factor .sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # sdf.write_values_to_DB( data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = sdf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)

    # 11. 季频资本结构 未写入
    scsf = SeasonalCapitalStructureFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_capital_structure_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # scsf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = scsf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)

    # 12. 季频收益质量 未写入
    seqf = SeasonalEarningQualityFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_earning_quality_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # seqf.write_values_to_DB( data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = seqf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)

    # 13. 季频杜邦分析体系 未写入
    sdpf = SeasonalDuPontFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_seasonal_dupont_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # sdpf.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path = code_sql_file_path)
    curr_list = sdpf.get_factor_list()
    factor_list = factor_list.append(curr_list, ignore_index=True)

    # 14. 日频技术指标
    dtif = DailyTechnicalIndicatorFactor()
    data_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_daily_technicalIndicator_factor.sql'
    code_sql_file_path = r'D:\Meiying\codes\industrial\factors\sql\sql_get_secucode.sql'
    # dtif.write_values_to_DB(data_sql_file_path=data_sql_file_path, code_sql_file_path=code_sql_file_path)
    curr_list = dtif.get_factor_list()
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
