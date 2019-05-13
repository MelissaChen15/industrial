# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/4/8  10:13
desc:
'''

# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/4/8  10:12
desc:
'''

import pandas as pd
import numpy as np
from sqlalchemy import create_engine

class dbData_import(object):
    def __init__(self):
        pass

    def InputDataPreprocess(self, filepath, table_name, secucode=''):
        # 获取 sql 代码， 存入sql_sentences中
        sql_sentences = []
        sentence = ''
        file = open(filepath, 'r', encoding='utf-8')
        for line in file:
            if 'select' in line:
                sentence = ''
            sentence += line
            if 'where' in line:
                sql_sentences.append(sentence + secucode)

        # for sentence in sql_sentences:
        #     print(sentence)

        # 循环执行 sql 代码
        data = {}
        from sqlalchemy import create_engine
        import os
        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 中文编码问题
        engine = create_engine('oracle+cx_oracle://jydb:jydb@192.168.1.187/JYDB')  # 数据库连接串
        # with管理安全
        with engine.connect() as conn, conn.begin():
            for i in range(len(sql_sentences)):
                res = engine.execute(sql_sentences[i])
                # print(sql_sentences[i])
                data[table_name[i]] = pd.DataFrame(data=res.fetchall(),
                                                   columns=[key.upper() for key in res.keys()])
                # 将None替换为np.nan
                data[table_name[i]] = data[table_name[i]].replace([None],np.nan)
                # 将非float格式的数据转换为float
                if table_name[i] != 'secucodes':
                    temp = data[table_name[i]]['SECUCODE']
                    data[table_name[i]] = data[table_name[i]].drop(columns='SECUCODE').convert_objects(convert_numeric=True)
                    data[table_name[i]]['SECUCODE'] = temp
                    # print(data[table_name[i]].sort_values(by='ENDDATE'))

        # print(data)
        return data


def df_to_DB(df:pd.DataFrame, table_name, if_exists, data_type):
    """
    将DataFrame存储到数据库
    :param df: pd.DataFrame, 需要存储的DataFrame
    :param table_name: string， 表名
    :param if_exists: string, 当表已存在的时候如何处理：
        fail: Raise a ValueError.
        replace: Drop the table before inserting new values.
        append: Insert new values to the existing table.
    :param data_type: dict, 格式{"A": Integer()}；数据类型参考https://blog.csdn.net/aimill/article/details/81531499
    """
    # oracle+cx_oracle://user:pass@host:port/dbname[?key=value&key=value...]

    assert(table_name.islower()) #数据库要求写入时表名必须是小写
    conn_string = 'oracle+cx_oracle://jydb:jydb@192.168.1.187/JYDB'
    engine = create_engine(conn_string, echo=False)
    df.to_sql(name=table_name, if_exists= if_exists, con=engine,index=False,dtype=data_type)
    # print(engine.execute("SELECT * FROM Test").fetchall())



if __name__ == '__main__':
    pass
    # df = pd.DataFrame({
    #     'a':[0.1,1.2,3.4],
    #     'b':['I','am','Melissa']
    # })
    # from sqlalchemy import Float, String
    # df_to_DB(df, 'aaa','replace',{'a': Float,'b': String(150)})
