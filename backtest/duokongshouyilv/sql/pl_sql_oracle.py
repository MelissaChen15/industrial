# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/4/8  10:13
desc:
'''

# coding=utf-8

import cx_Oracle
import numpy as np
import pandas as pd
from sqlalchemy import create_engine


class dbData_import(object):
    def __init__(self):
        pass

    def InputDataPreprocess(self, filepath, table_name, secucode='',date = ''):
        # 获取 sql 代码， 存入sql_sentences中
        sql_sentences = []
        sentence = ''
        file = open(filepath, 'r', encoding='utf-8')
        for line in file:
            # sql语句需要以select开头, 以where或order by结尾; 但是不能同时存在where 和 order by
            if 'select' in line:
                sentence = ''
            sentence += line
            if 'where' in line:
                sql_sentences.append(sentence + secucode + date)
            if 'order' in line:
                sql_sentences.append(sentence + secucode + date)

        # for sentence in sql_sentences:
        #     print(sentence)
        #
        # for name in table_name:
        #     print(name)

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
                # print(table_name[i])
                # print(sql_sentences[i])
                data[table_name[i]] = pd.DataFrame(data=res.fetchall(),
                                                   columns=[key.upper() for key in res.keys()])
                # 将None替换为np.nan
                data[table_name[i]] = data[table_name[i]].replace([None],np.nan)
                # 排序
                if table_name[i] == 'secucodes':
                    data[table_name[i]] = data[table_name[i]].sort_values(by='SECUCODE')
                # 将非float格式的数据转换为float
                if table_name[i] != 'secucodes':
                    if 'SECUCODE' in data[table_name[i]].columns:
                        try:
                            temp = data[table_name[i]]['SECUCODE']
                            data[table_name[i]] = data[table_name[i]].drop(columns='SECUCODE').convert_objects(convert_numeric=True)
                            data[table_name[i]]['SECUCODE'] = temp
                            # print(data[table_name[i]].sort_values(by='ENDDATE'))
                        except :  pass
                    else:
                        try:
                            data[table_name[i]] = data[table_name[i]].convert_objects(convert_numeric=True)

                        except: pass


        # print(data)
        return data


def delete_existing_records(sql: str):
    """
    执行sql,  删除原数据表中已有的记录
    :param sql:
    :return:
    """
    conn = cx_Oracle.connect('jydb/jydb@192.168.1.187/JYDB')
    cur = conn.cursor()
    # sql = "delete from seasonalvaluefactor where secucode = '000001' and startday = to_date( '2019-05-01','yyyy-mm-dd')"
    cur.execute(sql)
    conn.commit()
    cur.close()


def execute_inquery(sql:str):
    """
    执行单条查询语句
    :param sql: str, sql语句
    :return: pandas.DataFrame, 查询结果
    """
    conn_string = 'oracle+cx_oracle://jydb:jydb@192.168.1.187/JYDB'
    engine = create_engine(conn_string, echo=False)

    with engine.connect() as conn, conn.begin():
        res = engine.execute(sql)
        res = pd.DataFrame(data=res.fetchall(),columns=[key.upper() for key in res.keys()]) # 赋列名
        res = res.replace([None], np.nan) # 将None替换为np.nan
        try: # 将非float格式的数据转换为float
            temp =res['SECUCODE']
            res = res.drop(columns='SECUCODE').convert_objects(convert_numeric=True)
            res['SECUCODE'] = temp
        except: pass

    return res


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

    # assert(table_name.islower()) #数据库要求写入时表名必须是小写
    conn_string = 'oracle+cx_oracle://jydb:jydb@192.168.1.187/JYDB'
    engine = create_engine(conn_string, echo=False)
    df.to_sql(name=table_name.lower(), if_exists= if_exists, con=engine,index=False,dtype=data_type)
    # print(engine.execute("SELECT * FROM Test").fetchall())



# if __name__ == '__main__':
#     sql = 'delete from dailyvaluefactor where TRADINGDAY <= to_date( \'2019-05-23\',\'yyyy-mm-dd\')and TRADINGDAY >= to_date(\'2019-05-01\',\'yyyy-mm-dd\')'
#     delete_existing_records(sql)
