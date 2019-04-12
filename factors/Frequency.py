# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 10:10

from factors.BasicFactor import BasicFactor

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
    def __init__(self, factor_code, name,  describe):
        BasicFactor.__init__(self, factor_code, name, describe)
        self.frequency = 5
