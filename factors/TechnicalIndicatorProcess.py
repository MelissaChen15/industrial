# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/4/26  8:44
desc:
'''
import numpy as np
from factors.TechnicalIndicatorFunc import TechnicalIndicatorFunc

def TechnicalIndicatorProcess():
    target_methods = [x for x in dir(TechnicalIndicatorFunc) if not x.startswith('_')]  # 返回非内置方法
    nameGroup = ['TI'+str(x).zfill(4) for x in range(len(target_methods))]  # 生成TI的FactorCode

    return target_methods,nameGroup
