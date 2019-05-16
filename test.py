import pandas as pd
import numpy as np
import datetime
import time
import parser

pd.set_option('display.max_columns', None)
#
#
# # # import os
# # #
# # # path = './factors/'
# # #
# # # for fpathe, dirs, fs in os.walk(path):
# # #     for f in fs:
# # #         print(os.path.join(fpathe, f))
# #
# # # 组合基本面因子
# # numerator = pd.read_excel(r'C:\Users\Kww\Desktop\Description2.xlsx', sheet_name = '分子')
# # numerator = numerator[['英文简写','描述','聚源表名','聚源字段','表编号']].iloc[0:33,:]
# #
# # denominator = pd.read_excel(r'C:\Users\Kww\Desktop\Description2.xlsx', sheet_name = '分母')
# # denominator = denominator[['英文简写','描述','聚源表名','聚源字段','表编号']].iloc[0:11,:]
# #
# # # print(numerator,denominator)
# #
# # # # for sql
# # # print('分子sql')
# # # for row1 in numerator.itertuples(index=True, name='Pandas'):
# # #     print(str(getattr(row1, '表编号'))+ '.'+str(getattr(row1, '聚源字段')) + ', ',end="" )
# # # print()
# # # print('分母sql')
# # # for row2 in denominator.itertuples(index=True, name='Pandas'):
# # #     print(str(getattr(row2, '表编号'))+'.'+ str(getattr(row2, '聚源字段')) + ', ',end="" )
# # # print()
# # # print()
# #
# #
# # # for csv
# # count = 0
# # for n in numerator.itertuples(index=True, name='Pandas'): #分子
# #     for d in denominator.itertuples(index=True, name='Pandas2'):  # 分母
# #         dict = {
# #         'factor_code' : str('CB%04d') % count,
# #         'factor_name':   str(getattr(n, '英文简写')) + 'to' + str(getattr(d, '英文简写')),
# #         'factor_des': str(getattr(n, '描述')) + '/' + str(getattr(d, '描述')),
# #         '字段': str(getattr(n, '聚源表名')) + '.' + str(getattr(n, '聚源字段')) +', '+ str(getattr(d, '聚源表名')) + '.' + str(getattr(d, '聚源字段'))
# #         }
# #         if count == 0:
# #             csv = pd.DataFrame(dict,index=[0])
# #         else:
# #             mel = pd.DataFrame(dict,index=[0])
# #             csv = csv.append(mel,ignore_index=True)
# #         count += 1
# # # print(csv)A
# # c
# #
# # # 形式1： X/AT
# # # factor_code = 0
# # # for n in numerator.itertuples(index=True, name='Pandas'): #分子
# # #     for d in denominator.itertuples(index=True, name='Pandas2'):  # 分母
# # #         factor_name  = str(getattr(n, '英文简写')) + 'to' + str(getattr(d, '英文简写'))
# # #         factor_des = str(getattr(n, '描述')) + '/' + str(getattr(d, '描述'))
# # #         print('# ' + factor_name+ ' '+factor_des)
# # #         print('     '+ factor_name + ' = SeasonalComposedBasicFactorForm1(factor_code=\'CB%04d\',' %factor_code)
# # #         print('                                 name= \'' + factor_name + '\',')
# # #         print('                                 describe= \'' +  factor_des+ '\')')
# # #         print('     factor_entities[\''+ factor_name + '\'] = ' +factor_name)
# # #         factor_code += 1
# # #         print()
# # #         print()
# #
# #
# #
# # # for find components
# # # print('分子findcomponants')
# # # for row1 in numerator.itertuples(index=True, name='Pandas'):
# # #     print('\''+ str(getattr(row1, '聚源字段')).upper() + '\', ',end="" )
# # # print()
# # # print('分母findcomponants')
# # # for row2 in denominator.itertuples(index=True, name='Pandas'):
# # #     print('\''+ str(getattr(row2, '聚源字段')).upper() + '\', ',end="" )
# # # print()
# # # print()
# #
# #
# #
# # # for get factor values
# #
# # # 形式1： X/AT
# # for n in numerator.itertuples(index=True, name='Pandas'): #分子
# #     for d in denominator.itertuples(index=True, name='Pandas2'):  # 分母
# #         factor_name  = str(getattr(n, '英文简写')) + '/' + str(getattr(d, '英文简写'))
# #         print('factor_values[\'' + factor_name + '\'] = components[\''+str(getattr(n,'聚源表名'))+'_monthly\'][\'' + getattr(n, '英文简写').upper() + '\']'
# #               +'/components[\''+str(getattr(d,'聚源表名'))+'_monthly\'][\'' + getattr(d, '英文简写').upper() + '\']')
# # print()
# # print()
# #
# # # # 形式2 ： %X_change/AT
# # # for n in numerator.itertuples(index=True, name='Pandas'): #分子
# # #     for d in denominator.itertuples(index=True, name='Pandas2'):  # 分母
# # #         factor_name  = str(getattr(n, '英文简写')) + '/' + str(getattr(d, '英文简写'))
# # #         print('factor_values[\'' + factor_name + '\'] = components[\''+str(getattr(n,'聚源表名'))+'_monthly\'][\'' + getattr(n, '英文简写').upper() + '\']'
# # #               +'/components[\''+str(getattr(d,'聚源表名'))+'_monthly\'][\'' + getattr(d, '英文简写').upper() + '\']')
# # # print()
# # # print()
# #
#
# # sr = pd.Series([1,2,3])
# # print(sr.shape)
#
# import pandas as pd
#
# def InputDataPreprocess(filepath,table_name, secucode = ''):
#     # 获取 sql 代码， 存入sql_sentences中
#     sql_sentences = []
#     sentence = ''
#     file = open(filepath, 'r', encoding='utf-8')
#     for line in file:
#         if 'select' in line:
#             sentence = ''
#         sentence += line
#         if 'where' in line:
#             sql_sentences.append(sentence + secucode)
#
#     # 循环执行 sql 代码
#     data = {}
#     from sqlalchemy import create_engine
#     import os
#     os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8' # 中文编码问题
#     engine = create_engine('oracle+cx_oracle://jydb:jydb@192.168.1.187/JYDB') #  数据库连接串
#     # with管理安全
#     with engine.connect() as conn, conn.begin():
#         for i in range(len(sql_sentences)):
#             res = engine.execute(sql_sentences[i])
#             data[table_name[i]] = pd.DataFrame(data=res.fetchall(), columns=[key.upper() for key in res.keys()]).replace([None], np.nan) # 将None替换为np.nan
#     return data
#
#
#
#
# if __name__ == '__main__':
#     filepath = './factors/sql/sql_seasonal_composed_basic_factor_f1.sql'
#     table_name=['LC_BalanceSheetAll', 'LC_IncomeStatementAll', 'LC_MainDataNew',
#                                             'LC_CashFlowStatementAll', 'LC_DerivativeData', 'LC_BalanceSheet',
#                                             'LC_Staff']
#     secucode = 'and SecuCode = \'000002\''
#     print(InputDataPreprocess(filepath, table_name,secucode))
#

# a = pd.DataFrame(np.array([np.nan, 1, None, 1, 1]))
# b = pd.DataFrame(np.array([1, np.nan, 1,None, 1]))
#
# c = a/b
# print(c)
#
# print(c == None)
# print(c == np.nan)
# print(c == c)
# print(pd.isnull(c))

# df = pd.DataFrame({
#     'a':[1,2,3],
#     'b':[2,2,2]
# })
# print(df)
#
# df['c'] = df['a'] * df['b']
# print( df['a'] * df['b'])

# print(pd.DataFrame(np.random.random(200),columns=['a']))
# print(pd.DataFrame(np.random.random(200),columns=['b']))

# pd.DataFrame(np.random.random(200),columns=['a'])['a']*pd.DataFrame(np.random.random(200),columns=['b'])['b']

# print(pd.Series(np.random.random(200))*pd.Series(np.random.random(200)))

# df = pd.DataFrame([
#     [1,2,3],
#     [4,5,6]
# ]
# )
# print(df)
#
# df = df.reset_index(drop=True)
#
# print(df)
#
# df.index = df[0]
#
# print(df)

# 验证cubic spline的插值要求
# df1 = pd.DataFrame([
#     [1.0],
#     [np.nan],
#     [np.nan],
#     [2.0],
#     [np.nan],
#     [np.nan],
#     [3.0]
# ])
#
# print(df1)
# try:
#     print(df1.interpolate(method='linear'))
#     print(df1.interpolate(method='cubic'))
# except Exception as e:
#     print(e)
#
# df2 = pd.DataFrame([[0.0],
#     [np.nan],
#     [np.nan],
#     [1.0],
#     [np.nan],
#     [np.nan],
#     [2.0],
#     [np.nan],
#     [np.nan],
#     [3.0]
# ])
#
# print(df2)
# try:
#     print(df2.interpolate(method='linear'))
#     print(df2.interpolate(method='cubic'))
# except Exception as e:
#     print(e)


print(str(1e-3))