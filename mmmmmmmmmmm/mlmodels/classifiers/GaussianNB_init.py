# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 16:37


from sklearn import naive_bayes
import os
from main_entry.process.Para import Para
para = Para()

def init():
    # 高斯朴素贝叶斯分类器 参数
    # ['priors'] Prior probabilities of the classes. If specified the priors are not adjusted according to the data.
    # 初始化模型
    model = naive_bayes.GaussianNB()
    # 建立新的文件夹用于存储模型和预测结果
    if os.path.exists(para.path_results + "GaussianNB") == False:
        os.mkdir(para.path_results + "GaussianNB")

    return model, "GaussianNB"