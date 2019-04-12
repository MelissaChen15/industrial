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
import datetime



class dbData_import(object):
    def __init__(self):
        pass
    def InputDataPreprocess(self,filepath,table_name):
        # FactorName=['ROE_ttm','ROE_q','ROA_ttm','ROA_q','GrossProfitMargin_ttm','GrossProfitMargin_ttm_q','AssetTurnover_ttm','AssetTurnover_q']
        result = {}
        # 1.将sql语句执行得到数据
        data1 = dbsynchelper()
        Getdata1 = GetSQLsentence()
        sql_sentence = Getdata1.readsql(filepath)  # 输入文件的路径,得到整个sql文件里面的语句
        # print(sql_sentence)
        sentence_length=int(len(sql_sentence)/len(table_name))

        # 一条完整的sql语句换行，将语句进行拼接
        Newsql_sentence=[]
        for i in range(len(table_name)):
            tempsentence2 = sql_sentence[sentence_length * i].decode('utf-8')
            for j in range(sentence_length*i+1,sentence_length*(i+1),1):
                tempsentence2=tempsentence2+ ' '+sql_sentence[j].decode('utf-8')
            Newsql_sentence.append(tempsentence2)

        # 从数据库提取出数据，注意输出格式是list
        ValuationDataset = []
        for i in range(len(Newsql_sentence)):  #如果只有一条sql语句 len(sql_sentence)不会返回1
            temp = data1.select_detail(ip='192.168.1.187', user='jydb', pwd='jydb', database='JYDB', sql=Newsql_sentence[i])
            ValuationDataset.append(temp)

        # 将数据赋给某个变量名
        for i in range(len(ValuationDataset)):
            exec("%s=%s" % (table_name[i],ValuationDataset[i]))
            result[table_name[i]] = pd.DataFrame(eval(table_name[i])).replace([None],np.nan)# 转换成df,并且把None转换为np.nan

        return result



if __name__ == '__main__':
    # pass
    table_name = ['LC_DIndicesForValuation', 'LC_MainIndexNew']
    filepath = r'D:\Meiying\codes\industrial\factors\sql\sql_daily_value_factor.sql'



    data = dbData_import().InputDataPreprocess(filepath, table_name)
    table1 = data['LC_DIndicesForValuation']
    table2 = data['LC_MainIndexNew']
    # pd.set_option('display.max_columns', None)

    # InnerCode是唯一的
    # 一个公司就一个companycode
    # 但是一个公司可以有股票和很多债券，也就有多个SecuCode ，然后每个SecuCode
    # 对应一个InnerCode
    # SECUCODE
    # TRADINGDAY
    # INNERCODE











  # 日频 [7015 rows x 11 columns]
    # 季频 [90 rows x 4 columns]
    # 需要inner join的是 ENDDATE和SECUCODE