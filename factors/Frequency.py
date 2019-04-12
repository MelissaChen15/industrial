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

    def seasonal_to_monthly(self, seasonal_data: pd.DataFrame, seasonal_factor_name: list):
        # TODO: 插值法会导致收尾没有数据
        """
        应用cubic spline，将季频数据转换成月频数据
        可以同时处理多个特征；多支股票需要将同一支股票的数据放在一起，上下拼接

        :param seasonal_data:  pandas.DataFrame, 列包含 'ENDDATE''SECUCODE'和需要转换的因子
        :param seasonal_factor_name: list of string，需要转换的因子的名称
        :return: pandas.DataFrame, 列包含 'ENDDATE''SECUCODE'和需要转换的因子
        """
        all_monthly_data = pd.DataFrame()

        from factors.util import months_next_season
        # 设立flag，对股票代码循环
        flag = seasonal_data.loc[0, 'SECUCODE']
        a_stock_monthly_data = pd.DataFrame()
        # 循环所有数据
        for row in seasonal_data.itertuples(index=True, name='Pandas'):
            code = getattr(row, 'SECUCODE')
            if flag != code:
                a_stock_monthly_data = a_stock_monthly_data.interpolate(method='cubic', axis=0)  # cubic spline
                all_monthly_data = pd.concat([all_monthly_data, a_stock_monthly_data], axis=0, ignore_index=True)
                flag = code
                a_stock_monthly_data = pd.DataFrame()

            months_start = months_next_season(getattr(row, 'ENDDATE'))
            row1_dict = {'STARTDAY': months_start[0],
                         'SECUCODE': code,
                         }
            for f in seasonal_factor_name:
                row1_dict[f] = getattr(row, f)
            row2_dict = {'STARTDAY': [months_start[1], months_start[2]],
                         'SECUCODE': [code, code],
                         }
            for f in seasonal_factor_name:
                row2_dict[f] = np.nan
            row1 = pd.DataFrame(row1_dict, index=[0])
            row2 = pd.DataFrame(row2_dict)

            a_stock_monthly_data = pd.concat([a_stock_monthly_data, row1.append(row2)], axis=0, ignore_index=True)

        # 因为flag循环没有办法处理列表中最后一只股票，这里手动处理
        a_stock_monthly_data = a_stock_monthly_data.interpolate(method='cubic', axis=0)  # cubic spline
        all_monthly_data = pd.concat([all_monthly_data, a_stock_monthly_data], axis=0, ignore_index=True)

        return all_monthly_data

    def monthly_to_daily(self, monthly_data: pd.DataFrame, daily_data: pd.DataFrame, seasonal_factor_name: list):
        """
        将seasonal_to_monthly转换之后的月频数据转换为日频数据

        :param monthly_data:  pd.DataFrame seasonal_to_monthly转换之后的月频数据，必须有[['SECUCODE', 'TRADINGDAY']两列
        :param daily_data: pd.DataFrame 必须有[['SECUCODE', 'TRADINGDAY']两列
        :param seasonal_factor_name: list of string，需要转换的因子的名称
        :return: pd.DataFrame 转换好的日频数据，列包含 'ENDDATE''SECUCODE'和需要转换的因子
        """
        # TODO: 看一下源码concat_inner 或者 to list之后用binary search
        from factors.util import first_day_this_month
        daily_data = pd.DataFrame(daily_data[['SECUCODE', 'TRADINGDAY']])
        for f in seasonal_factor_name:
            daily_data[f] = np.nan
        daily_data['STARTDAY'] = daily_data['TRADINGDAY'].apply(lambda v: first_day_this_month(v))

        for row in daily_data.itertuples(index=True, name='Pandas'):
            code = getattr(row, 'SECUCODE')
            start_day = getattr(row, 'STARTDAY')
            for row2 in monthly_data.itertuples(index=True, name='Pandas2'):
                code2 = getattr(row2, 'SECUCODE')
                start_day2 = getattr(row2, 'STARTDAY')
                if (code == code2 and start_day == start_day2):
                    for f in seasonal_factor_name:
                        daily_data.loc[row.Index, f] = getattr(row2, f)

        return daily_data


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
    print(table_2_daily.sort_values(by='NETPROFITGROWRATE', ascending=False))





