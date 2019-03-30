# __author__ = goldfish
# -*- coding: utf-8 -*-
# 2019/3/4 10:26
#
# |\____╭╭╭____/|
# |               | ╭---------╮
# |    ●     ●    | < Welcome~ |
# |  ≡    o    ≡  | ╰---------╯
# ╰--┬Ｏ◤▽◥Ｏ┬--╯
# 

import tushare as ts
import time

pro = ts.pro_api("71ee26cfb1418f61c26da0fdc2588e50d7aa7d1287ad51307e08c81f")
df = pro.trade_cal(exchange='', start_date='20180901',
                   end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date',
                   is_open='0')
time.sleep(1)

print(df)

