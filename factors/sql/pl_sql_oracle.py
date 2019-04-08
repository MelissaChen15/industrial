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
import datetime



class dbData_import(object):
    def __init__(self):
        pass
    def InputDataPreprocess(self,filepath,FactorName):
        # FactorName=['ROE_ttm','ROE_q','ROA_ttm','ROA_q','GrossProfitMargin_ttm','GrossProfitMargin_ttm_q','AssetTurnover_ttm','AssetTurnover_q']
        # 1.将sql语句执行得到数据
        data1 = dbsynchelper()
        Getdata1 = GetSQLsentence()
        sql_sentence = Getdata1.readsql(filepath)  # 输入文件的路径,得到整个sql文件里面的语句
        # print(sql_sentence)
        sentence_length=int(len(sql_sentence)/len(FactorName))

        # 一条完整的sql语句换行，将语句进行拼接
        Newsql_sentence=[]
        for i in range(len(FactorName)):
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
            exec("%s=%s" % (FactorName[i],ValuationDataset[i]))

        # 转换成df
        return pd.DataFrame(eval(FactorName[0]))



if __name__ == '__main__':
    # pass
    FactorName = ['factor1']
    filepath = r'D:\Meiying\codes\industrial\factors\sql\sql_sentence_template.sql'

    data = dbData_import()
    print(data.InputDataPreprocess(filepath, FactorName))

