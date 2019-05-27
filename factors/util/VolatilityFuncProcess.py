# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/14  16:39
desc:
'''
from factors.util.VolatilityFunc import VolatilityFunc

def VolatilityFuncProcess():
    target_methods = [x for x in dir(VolatilityFunc) if not x.startswith('_')]  # 返回非内置方法
    nameGroup = [x+'_' for x in target_methods]  # 生成的FactorCode，

    return target_methods,nameGroup