# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 10:40

# 参数类
class Para:
    percent_select = [0.3,0.3] # 标记分类模型的数据时，收益率前30%标记为1，收益率后30%标记为0
    percent_cv = 0.1 # cv集占样本的比例
    path_data = r"D:\Meiying\data\cleaned\\" # 原始数据路径
    path_results = r"D:\Meiying\data\result\\"  # 模型训练、预测结果存储路径
    seed = 7 # random seed
    month_in_sample = range(1, 1+1) # 样本中包含的月数
    month_test = range(2, 2+1) # 测试集包含的月数
    n_stock_select = 100 # 策略选择的股票数量
    fee_rate = 0.001 # 交易费、佣金等的比率



