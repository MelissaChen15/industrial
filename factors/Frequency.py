# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 10:10

from factors.BasicFactor import BasicFactor
import numpy as np
import pandas as pd

"""
因子频率类

频率代码, int类型：
    daily     -- 1
    weekly    -- 2
    monthly   -- 3
    seasonal  -- 4
    annual    -- 5
"""

# 日频
class DailyFrequency(BasicFactor):
    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.frequency = 1



#  周频
class WeeklyFrequency(BasicFactor):
    def __init__(self, factor_code, name,  describe):
        BasicFactor.__init__(self, factor_code, name, describe)
        self.frequency = 2

# 月频
class MonthlyFrequency(BasicFactor):
    def __init__(self, factor_code, name,  describe):
        BasicFactor.__init__(self, factor_code, name, describe)
        self.frequency = 3


# 季频
class SeasonalFrequency(BasicFactor):
    def __init__(self, factor_code, name,  describe):
        BasicFactor.__init__(self, factor_code, name, describe)
        self.frequency = 4


# 年频
class AnnualFrequency(BasicFactor):
    def __init__(self, factor_code, name, describe):
        BasicFactor.__init__(self, factor_code, name, describe)
        self.frequency = 5


if __name__ == '__main__':
    from factors.sql.pl_sql_oracle import dbData_import
    import numpy as np
    import pandas as pd

    table_name = ['LC_DIndicesForValuation', 'LC_MainIndexNew']
    filepath = r'D:\Meiying\codes\industrial\factors\sql\sql_daily_value_factor.sql'

    data = dbData_import().InputDataPreprocess(filepath, table_name)
    table1_daily = data['LC_DIndicesForValuation']
    table2_seasonal = data['LC_MainIndexNew']
    # # pd.set_option('display.max_columns', None)
    temp = DailyFrequency('0','0','0')
    table2_monthly = temp.seasonal_to_monthly(table2_seasonal,['NETPROFITGROWRATE'])
    print(table2_monthly)
    table_2_daily = temp.monthly_to_daily(table2_monthly, table1_daily,['NETPROFITGROWRATE'] )
    print(table_2_daily.sort_values(by='TRADINGDAY', ascending=True))





