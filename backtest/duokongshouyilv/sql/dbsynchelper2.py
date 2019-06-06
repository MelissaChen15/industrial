#-*- coding: UTF-8 -*-
from queue import Queue
import threading,sys
from time import ctime,sleep
import time

# from factors.sqlalchemy import create_engine
import pandas as pd
import numpy as np
import cx_Oracle


class dbsynchelper():
    def __init__(self):
        pass

    # 查询
    def select(self,ip,user,pwd,database, sql):
        try:

            res_list = []
            # res_list = pd.DataFrame()
            with cx_Oracle.connect(user+'/'+pwd+'@'+ip+'/'+database) as connect:
                with connect.cursor() as cur:
                    # result = pd.read_sql(sql, con=connect)
                    cur.execute(sql)

                    # for idx,v in cur:
                    #     print(idx)


                    result = cur.fetchall()
                    res_list.extend(result)

                    while len(result) > 0:
                        cur.nextset()


                        result = cur.fetchall()
                        res_list.extend(result)


            # engine = create_engine(connect_string)
            # result = pd.read_sql(sql, con=engine)
            return res_list
        except Exception as e:
            print(e)

    # 查询
    def select_detail(self, ip,user, pwd, database, sql):
        try:

            res_list = []
            # res_list = pd.DataFrame()
            with cx_Oracle.connect(user+'/'+pwd+'@'+ip+'/'+database) as connect:
                with connect.cursor() as cur:
                    # result = pd.read_sql(sql, con=connect)
                    cur.execute(sql)

                    # for idx,v in cur:
                    #     print(idx)

                    index = cur.description
                    result = []
                    for res in cur.fetchall():
                        row = {}
                        for i in range(len(index)):
                            row[index[i][0]] = res[i]
                        result.append(row)
                        # result = cur.fetchall()
                        # res_list.extend(result)

                        #                    while len(result) > 0:
                        #                        cur.nextset()
                        #
                        #
                        #                        result = cur.fetchall()
                        #                        res_list.extend(result)

            # engine = create_engine(connect_string)
            # result = pd.read_sql(sql, con=engine)
            return result
            # return res_list
        except Exception as e:
            print(e)


# if __name__ == '__main__':
#     ins = dbsynchelper()
#     data = ins.select_detail(ip='10.168.20.22',port=1433,user='sas',pwd='111111',database='EBTR',sql='select * from EventMain')
#     print(data)