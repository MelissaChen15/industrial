# coding=utf-8
'''
Author: Kangchen Wei
Email:  weixk@cifutures.com.cn
Application : machine learning for investment

paper见pad

date: 2019/4/17  9:22
desc: 成熟模型后的
'''
from sklearn.datasets import load_iris  # 自带的样本数据集
from sklearn.neighbors import KNeighborsClassifier  # 要估计的是knn里面的参数，包括k的取值和样本权重分布方式
import matplotlib.pyplot as plt  # 可视化绘图
from sklearn.model_selection import GridSearchCV

import numpy as np


iris = load_iris()
X = iris.data  # 150个样本，4个属性
y = iris.target # 150个类标号


class Combinatorial_purgedCV(object):
    def __init__(self,n_groups,k=2):
        '''
        :param n_groups: 将样本划分为N个小的数据集，不进行shuffle
        :param k: 从N个小的数据集中选取k个作为测试集
        '''
        from scipy.special import comb
        self.n_groups = n_groups
        self.k = k
        self.n_paths = comb(n_groups, k)*k/n_groups

    def data_split(self,sample_index):
        '''
        :param sample_index: 输入样本的索引，对于选股模型这里输入时间序列。
        :return: 组合交叉验证的训练集，测试集的index
        '''
        from itertools import combinations
        partition_T = np.array_split(np.arange(len(sample_index)), self.n_groups)
        groups = set(np.arange(n_groups))
        whole_set = dict()
        for i in combinations(np.arange(self.n_groups),self.k):
            learning_pairs=[]
            test_index = []
            train_index = []
            for j in i:
                test_index.append(list(partition_T[j]))
            learning_pairs.append(test_index)
            for m in (groups-set(i)):
                train_index.append(list(partition_T[m]))
            learning_pairs.append(train_index) # 里面两个list,第一个是test测试集，第二个是训练集
            whole_set[str(i)] = learning_pairs
        return whole_set

    def model_train_test_loop(self,samples, whole_set, model):
        '''
        Attention: TradingDate and SecuCode must be
        :param samples: [X,Y] target in the last column
        :param whole_set: return of func data_split
        :return:
        '''
        predic_set = dict()
        for j in whole_set.keys():
            test_index = np.array(whole_set[j][0])  # contains k list
            train_index = np.array(whole_set[j][1]).ravel()
            # test_data = samples.loc[test_index, :]
            train_data = samples.loc[train_index, :]
            model.fit(train_data.iloc[:, :-1], train_data.iloc[:, -1])
            # 这里需要对应保存日期和股票代码
            temp_predi = []  # just a container, after predicting, timestamp and SecCode must be attached
            for k in test_index:
                test_data = samples.loc[k, :]
                temp_predi.append(model.predict(test_data.iloc[:, :-1]))  # 在训练模型不变的情况下，进行完全部预测后再进行绩效等计算
            predic_set[j]= temp_predi
        return predic_set

    def create_path(self,predic_set):
        '''
        :param predic_set: the result of func:model_train_test_loop
        :return: a whole prediction path created by joining n_groups subset
        '''
        num_sub = self.n_groups

        combina_set = np.array([[float(j) for j in filter(str.isdigit, i)] for i in predic_set.keys()])  # predic_set
        mirroCombine = combina_set.copy()
        index_group = []
        for j in range(num_sub):
            index_group.append(np.argwhere(mirroCombine==j)) # 返回的是mirroCombine的索引
        path_index = dict()

        for k in range(self.n_paths):
            temp1 = []
            for i in range(num_sub):
                temp1.append(index_group[i][k])
            path_index[str(k)] = temp1  # 返回的是属于不同划分区域的索引的集合,且是有序的(时间)

        key_value = list(predic_set.keys())  # predic_set
        path_predict = dict()
        flat = lambda L: sum(map(flat, L), []) if isinstance(L, list) else [L] # 多个嵌套列表压平函数,elegant

        for q in path_index.keys():
            path_data = []
            for p in path_index[q]:  # p[0]给出属于哪个组合的索引，p[1]的值则是这个组合内部的选择
                path_data.extend(predic_set[key_value[p[0]]][p[1]] )
            path_predict[q] = flat(path_data)





k = 2
n_groups = 6
sample_index = np.arange(len(X))
ex1 = Combinatorial_purgedCV(n_groups, k=2)
whole_set = ex1.data_split(sample_index)
for i in whole_set.keys():
    whole_set[i]
    break


k_range = range(1, 31)  # 优化参数k的取值范围
weight_options = ['uniform', 'distance']  # 代估参数权重的取值范围。uniform为统一取权值，distance表示距离倒数取权值
# 下面是构建parameter grid，其结构是key为参数名称，value是待搜索的数值列表的一个字典结构
param_grid = {'n_neighbors':k_range,'weights':weight_options}  # 定义优化参数字典，字典中的key值必须是分类算法的函数的参数名
print(param_grid)

knn = KNeighborsClassifier(n_neighbors=5)  # 定义分类算法。n_neighbors和weights的参数名称和param_grid字典中的key名对应

# ================================网格搜索=======================================
# 这里GridSearchCV的参数形式和cross_val_score的形式差不多，其中param_grid是parameter grid所对应的参数
# GridSearchCV中的n_jobs设置为-1时，可以实现并行计算（如果你的电脑支持的情况下）
grid = GridSearchCV(estimator = knn, param_grid = param_grid, cv=10, scoring='accuracy') #针对每个参数对进行了10次交叉验证。scoring='accuracy'使用准确率为结果的度量指标。可以添加多个度量指标
grid.fit(X, y)


# 使用获取的最佳参数生成模型，预测数据
knn = KNeighborsClassifier(n_neighbors=grid.best_params_['n_neighbors'], weights=grid.best_params_['weights'])  # 取出最佳参数进行建模
knn.fit(X, y)  # 训练模型
print(knn.predict([[3, 5, 4, 2]]))  # 预测新对象

grid.predict([[3, 5, 4, 2],[1,2,4,3]])