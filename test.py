import pandas as pd
import numpy as np
import datetime
import time
import parser

pd.set_option('display.max_columns', None)

df = pd.read_excel(r'C:\Users\Kww\Desktop\数据库索引.xlsx', sheet_name = '因子')
df = df[['factor_code','英文简写','因子名称','说明']].iloc[100:,:]


# for init
for row in df.itertuples(index=True, name='Pandas'):
    print('# ' + str(getattr(row, '英文简写')) + ' '+ getattr(row, '因子名称') )
    print('     '+ getattr(row, '英文简写')  + ' = SeasonalCashFactor(factor_code=\'' + str(getattr(row, 'factor_code')) + '\',')
    print('                                 name= \'' + getattr(row, '英文简写') + '\',')
    print('                                 describe= \'' + getattr(row, '说明') + '\')')
    print('     factor_entities[\''+ getattr(row, '英文简写') + '\'] = ' +getattr(row, '英文简写'))
    print()
    print()


# for sql
for row in df.itertuples(index=True, name='Pandas'):
    print('t1.'+ str(getattr(row, '英文简写')) + ', ',end="" )
print()
print()

# for find components
for row in df.itertuples(index=True, name='Pandas'):
    print('\''+ str(getattr(row, '英文简写')).upper() + '\', ',end="" )
print()
print()


# for get factor values
for row in df.itertuples(index=True, name='Pandas'):
    print('factor_values[\''+ str(getattr(row, '英文简写')) + '\'] = components[\'LC_MainIndexNew_monthly\'][\''+ str(getattr(row, '英文简写')).upper() + '\']')
print()
print()



# 测试数据库读取
# sql = pl_sql_oracle.dbData_import()
# s = sql.InputDataPreprocess(code_sql_file_path,
#                             ['secucodes'])
# for row in s['secucodes'].itertuples(index=True, name='Pandas'):
#     pd.set_option('display.max_columns', None)
#     data = .find_components(file_path=data_sql_file_path,
#                                 table_name=['LC_MainIndexNew'],
#                                 secucode='and t2.Secucode = \'' + getattr(row, 'SECUCODE') + '\'')
#     print(data)



