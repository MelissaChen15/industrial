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

from factors.sql.dbsynchelper2 import dbsynchelper
from factors.sql.GetSQLsentence import GetSQLsentence
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

import datetime



class dbData_import(object):
    def __init__(self):
        pass
    # def InputDataPreprocess(self,filepath,table_name, secucode = ''):
    #     # FactorName=['ROE_ttm','ROE_q','ROA_ttm','ROA_q','GrossProfitMargin_ttm','GrossProfitMargin_ttm_q','AssetTurnover_ttm','AssetTurnover_q']
    #     result = {}
    #     # 1.将sql语句执行得到数据
    #     data1 = dbsynchelper()
    #     Getdata1 = GetSQLsentence()
    #     sql_sentence = Getdata1.readsql(filepath)  # 输入文件的路径,得到整个sql文件里面的语句
    #     # print(sql_sentence)
    #     sentence_length=int(len(sql_sentence)/len(table_name))
    #
    #     # 一条完整的sql语句换行，将语句进行拼接
    #     Newsql_sentence=[]
    #     for i in range(len(table_name)):
    #         tempsentence2 = sql_sentence[sentence_length * i].decode('utf-8')
    #         for j in range(sentence_length*i+1,sentence_length*(i+1),1):
    #             tempsentence2=tempsentence2+ ' '+sql_sentence[j].decode('utf-8')
    #         Newsql_sentence.append(tempsentence2 + secucode) # 可以设置按股票代码读取
    #     # print(Newsql_sentence)
    #
    #     # 从数据库提取出数据，注意输出格式是list
    #     ValuationDataset = []
    #     for i in range(len(Newsql_sentence)):  #如果只有一条sql语句 len(sql_sentence)不会返回1
    #         temp = data1.select_detail(ip='192.168.1.187', user='jydb', pwd='jydb', database='JYDB', sql=Newsql_sentence[i])
    #         ValuationDataset.append(temp)
    #
    #     # 将数据赋给某个变量名
    #     for i in range(len(ValuationDataset)):
    #         exec("%s=%s" % (table_name[i],ValuationDataset[i]))
    #         result[table_name[i]] = pd.DataFrame(eval(table_name[i])).replace([None],np.nan)# 转换成df,并且把None转换为np.nan
    #
    #     return result

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
