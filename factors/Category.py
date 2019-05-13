# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/8 10:22


from factors.BasicFactor import BasicFactor
import pandas as pd

"""
因子类型类
"""

# 价值类因子
class ValueFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '价值类'


# 成长类因子
class GrowthFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '成长类'


# 财务质量类因子
class FinancialQualityFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '财务质量类'


# 个股指标因子
class SecuIndexFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '个股指标'

# 偿债能力
class DebtpayingAbilityFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '偿债能力'



# 盈利能力
class ProfitabilityFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '盈利能力'

# 营运能力
class OperatingFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '营运能力'


# 现金状况
class CashFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '现金状况'

# 分红能力
class DividendFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '分红能力'

# 资本结构
class CapitalStructureFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '资本结构'


# 收益质量
class EarningQualityFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '收益质量'


# 杜邦分析体系
class DuPontFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '杜邦分析体系'



# 技术指标类
class TechnicalIndicatorFactor(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '技术指标类'


# 组合基本面因子， Form1, X/AT形式
class ComposedBasicFactorForm1(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '组合基本面因子， Form1, X/AT形式'

# 组合基本面因子， Form2, X/AT形式
class ComposedBasicFactorForm2(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '组合基本面因子，Form2, (X_change/AT)_pct形式'

# 组合基本面因子， Form3, X/AT形式
class ComposedBasicFactorForm3(BasicFactor):

    def __init__(self, factor_code, name, describe):
        super().__init__(factor_code, name, describe)
        self.type = '组合基本面因子, Form3, X_change_pct - AT_change_pct形式'