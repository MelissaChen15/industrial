# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

date: 2019/5/13  13:30
desc:
'''
# 得到因子名称，以及因子方法名
from factors.util.TurnoverFunc import TurnoverFunc


def TurnoverFuncProcess():
    target_methods = [x for x in dir(TurnoverFunc) if not x.startswith('_')]  # 返回非内置方法
    nameGroup = [x+'_' for x in target_methods]  # 生成的FactorCode，

    return target_methods,nameGroup