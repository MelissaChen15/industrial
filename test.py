import pandas as pd
import numpy as np
import datetime
import time
import parser

pd.set_option('display.max_columns', None)


# # import os
# #
# # path = './factors/'
# #
# # for fpathe, dirs, fs in os.walk(path):
# #     for f in fs:
# #         print(os.path.join(fpathe, f))
#
# # 组合基本面因子
# numerator = pd.read_excel(r'C:\Users\Kww\Desktop\Description2.xlsx', sheet_name = '分子')
# numerator = numerator[['英文简写','描述','聚源表名','聚源字段','表编号']].iloc[0:33,:]
#
# denominator = pd.read_excel(r'C:\Users\Kww\Desktop\Description2.xlsx', sheet_name = '分母')
# denominator = denominator[['英文简写','描述','聚源表名','聚源字段','表编号']].iloc[0:11,:]
#
# # print(numerator,denominator)
#
# # # for sql
# # print('分子sql')
# # for row1 in numerator.itertuples(index=True, name='Pandas'):
# #     print(str(getattr(row1, '表编号'))+ '.'+str(getattr(row1, '聚源字段')) + ', ',end="" )
# # print()
# # print('分母sql')
# # for row2 in denominator.itertuples(index=True, name='Pandas'):
# #     print(str(getattr(row2, '表编号'))+'.'+ str(getattr(row2, '聚源字段')) + ', ',end="" )
# # print()
# # print()
#
#
# # for csv
# count = 0
# for n in numerator.itertuples(index=True, name='Pandas'): #分子
#     for d in denominator.itertuples(index=True, name='Pandas2'):  # 分母
#         dict = {
#         'factor_code' : str('CB%04d') % count,
#         'factor_name':   str(getattr(n, '英文简写')) + 'to' + str(getattr(d, '英文简写')),
#         'factor_des': str(getattr(n, '描述')) + '/' + str(getattr(d, '描述')),
#         '字段': str(getattr(n, '聚源表名')) + '.' + str(getattr(n, '聚源字段')) +', '+ str(getattr(d, '聚源表名')) + '.' + str(getattr(d, '聚源字段'))
#         }
#         if count == 0:
#             csv = pd.DataFrame(dict,index=[0])
#         else:
#             mel = pd.DataFrame(dict,index=[0])
#             csv = csv.append(mel,ignore_index=True)
#         count += 1
# # print(csv)A
# c
#
# # 形式1： X/AT
# # factor_code = 0
# # for n in numerator.itertuples(index=True, name='Pandas'): #分子
# #     for d in denominator.itertuples(index=True, name='Pandas2'):  # 分母
# #         factor_name  = str(getattr(n, '英文简写')) + 'to' + str(getattr(d, '英文简写'))
# #         factor_des = str(getattr(n, '描述')) + '/' + str(getattr(d, '描述'))
# #         print('# ' + factor_name+ ' '+factor_des)
# #         print('     '+ factor_name + ' = SeasonalComposedBasicFactorForm1(factor_code=\'CB%04d\',' %factor_code)
# #         print('                                 name= \'' + factor_name + '\',')
# #         print('                                 describe= \'' +  factor_des+ '\')')
# #         print('     factor_entities[\''+ factor_name + '\'] = ' +factor_name)
# #         factor_code += 1
# #         print()
# #         print()
#
#
#
# # for find components
# # print('分子findcomponants')
# # for row1 in numerator.itertuples(index=True, name='Pandas'):
# #     print('\''+ str(getattr(row1, '聚源字段')).upper() + '\', ',end="" )
# # print()
# # print('分母findcomponants')
# # for row2 in denominator.itertuples(index=True, name='Pandas'):
# #     print('\''+ str(getattr(row2, '聚源字段')).upper() + '\', ',end="" )
# # print()
# # print()
#
#
#
# # for get factor values
#
# # 形式1： X/AT
# for n in numerator.itertuples(index=True, name='Pandas'): #分子
#     for d in denominator.itertuples(index=True, name='Pandas2'):  # 分母
#         factor_name  = str(getattr(n, '英文简写')) + '/' + str(getattr(d, '英文简写'))
#         print('factor_values[\'' + factor_name + '\'] = components[\''+str(getattr(n,'聚源表名'))+'_monthly\'][\'' + getattr(n, '英文简写').upper() + '\']'
#               +'/components[\''+str(getattr(d,'聚源表名'))+'_monthly\'][\'' + getattr(d, '英文简写').upper() + '\']')
# print()
# print()
#
# # # 形式2 ： %X_change/AT
# # for n in numerator.itertuples(index=True, name='Pandas'): #分子
# #     for d in denominator.itertuples(index=True, name='Pandas2'):  # 分母
# #         factor_name  = str(getattr(n, '英文简写')) + '/' + str(getattr(d, '英文简写'))
# #         print('factor_values[\'' + factor_name + '\'] = components[\''+str(getattr(n,'聚源表名'))+'_monthly\'][\'' + getattr(n, '英文简写').upper() + '\']'
# #               +'/components[\''+str(getattr(d,'聚源表名'))+'_monthly\'][\'' + getattr(d, '英文简写').upper() + '\']')
# # print()
# # print()
#

sr = pd.Series([1,2,3])
print(sr.shape)




