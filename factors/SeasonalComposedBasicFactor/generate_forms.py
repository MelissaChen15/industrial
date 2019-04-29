# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/4/29 15:07

import pandas as pd
import numpy as np
from  factors.SeasonalComposedBasicFactor.form1 import SeasonalComposedBasicFactorForm1

# 形式1： X/AT
def generate_form1_inits(numerator, denominator):
    factor_code = 0
    factor_entities = {}
    for n in numerator.itertuples(index=True, name='Pandas'): #分子
        for d in denominator.itertuples(index=True, name='Pandas2'):  # 分母
            factor_name  = str(getattr(n, '英文简写')) + 'to' + str(getattr(d, '英文简写'))
            factor_des = str(getattr(n, '描述')) + '/' + str(getattr(d, '描述'))
            # print('# ' + factor_name+ ' '+factor_des)
            factor_entity = SeasonalComposedBasicFactorForm1(factor_code='CB%04d,' %factor_code,
                                                                name= factor_name,
                                                                describe= factor_des)
            factor_entities[factor_name] = factor_entity
            factor_code += 1

    return  factor_entities

if __name__ == '__main__':
    numerator = pd.read_excel(r'./组合基本面因子.xlsx', sheet_name='分子')
    numerator = numerator[['英文简写', '描述', '聚源表名', '聚源字段', '表编号']]

    denominator = pd.read_excel(r'./组合基本面因子.xlsx', sheet_name='分母')
    denominator = denominator[['英文简写', '描述', '聚源表名', '聚源字段', '表编号']]

    print(generate_form1_inits(numerator,denominator))





