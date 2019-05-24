# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/14  11:07
desc:
'''
from factors.util.MomentumFunc import MomentumFunc

def MomentumFuncProcess():
    target_methods = [x for x in dir(MomentumFunc) if not x.startswith('_')]  # 返回非内置方法
    nameGroup = [x+'_' for x in target_methods]  # 生成的FactorCode，

    return target_methods,nameGroup