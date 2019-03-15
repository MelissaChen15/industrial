import pandas as pd
import tushare as ts
import numpy as np
import math
import h5py
import time

'''
修改 start_date,end_date的日期来更新数据
目前只提取2004-2018年底的数据
'''

def DataImport():
    ts.set_token('0debea0090cfed963f42b574666f6cc990f101dc6c1531d0fe52497c')
    pro = ts.pro_api()
    pro = ts.pro_api('0debea0090cfed963f42b574666f6cc990f101dc6c1531d0fe52497c')

    dateseries=pro.trade_cal(exchange='', start_date='20040101', end_date='20181231')
    trade_date=dateseries[dateseries['is_open']==1]['cal_date']
    trade_date=trade_date.reset_index(drop=True)

    #财务指标数据-tushares
    name_file=pd.read_excel('新建 Microsoft Excel 工作表.xlsx')
    data_stock = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    fin_data=dict()
    for i in data_stock['ts_code']:
        fin_data[str(i)]=pro.fina_indicator(ts_code=i,start_date='20040101', end_date='20181231',fields=list(name_file['名称']))
        time.sleep(5)

    h5 = pd.HDFStore('dataset_part2.h5', 'w', complevel=4, complib='blosc')
    for j in fin_data.keys():
        h5[j] = fin_data[j]
    h5.close()

    #资产负债表 -tushares
    name_file1=pd.read_excel('Tushare数据字段查询.xlsx',sheetname='资产负债表')
    data_stock = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

    balancesheet_data = dict()
    for i in data_stock['ts_code']:
        balancesheet_data[str(i)] = pro.balancesheet(ts_code=i, start_date='20040101', end_date='20181231',fields=list(name_file1['名称']))
        time.sleep(1)










    '''
    dataset1 数据提取字段：    fields=['close','turnover_rate_f','trade_date','pe_ttm','pb','ps_ttm','circ_mv']
    '''
    dataset1=dict()
    for i in trade_date:
        dataset1[str(i)]=pro.daily_basic(ts_code='',trade_date=str(i),fields='ts_code,close,turnover_rate_f,trade_date,pe_ttm,pb,ps_ttm,circ_mv')
        time.sleep(1)  # sleep 5 秒


    h5 = pd.HDFStore('dataset_part1.h5', 'w', complevel=4, complib='blosc')
    for j in dataset1.keys():
        h5[j] = dataset1[j]
    h5.close()


    h5.close()
    h5s = pd.HDFStore('dataset_part1.h5', 'r')
    h5s.keys()
    h5s.close()


    fields=['close','turnover_rate_f','trade_date','pe_ttm','pb','ps_ttm','circ_mv']

    pro.fina_indicator(ts_code='',fields='end_date,eps',start_date='20170101', end_date='20180801')
    df = pro.cashflow(ts_code='600000.SH', fields='end_date,free_cashflow	',start_date='20180101', end_date='20180730')

    ZZ100 = pd.read_excel('中证1000成分股证券代码.xlsx', sheetname='中证1000成分股证券代码', header=0)#中证1000股票证券代码
    def ExtractData():#由于访问下载限制，分段下载每分钟最多访问该接口200次
        dataset1 = dict()
        for i in ZZ100['证券代码'][0:200]:
            dataset1[str(i)]=pro.weekly(ts_code=str(i), start_date='20100101', end_date='20181214')
        dataset2=dict()
        for i in ZZ100['证券代码'][200:400]:
            dataset2[str(i)] = pro.weekly(ts_code=str(i), start_date='20100101', end_date='20181214')
        dataset3=dict()
        for i in ZZ100['证券代码'][400:600]:
            dataset3[str(i)] = pro.weekly(ts_code=str(i), start_date='20100101', end_date='20181214')
        dataset4=dict()
        for i in ZZ100['证券代码'][600:800]:
            dataset4[str(i)] = pro.weekly(ts_code=str(i), start_date='20100101', end_date='20181214')
        dataset5=dict()
        for i in ZZ100['证券代码'][800:]:
            dataset5[str(i)] = pro.weekly(ts_code=str(i), start_date='20100101', end_date='20181214')
        dataset={}
        dataset.update(dataset1)
        dataset.update(dataset2)
        dataset.update(dataset3)
        dataset.update(dataset4)
        dataset.update(dataset5)

        # 写入HDF5
        # f = h5py.File('zz1000daily.h5', 'w-')#中证1000股票日行情数据存储
        h5 = pd.HDFStore('zz1000_weekly.h5', 'w', complevel=4, complib='blosc')
        for j in dataset.keys():
            h5[j]=dataset[j]
        h5.close()

        h5s = pd.HDFStore('dataset_part1.h5', 'r')

        h5s.close()