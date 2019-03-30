# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/7 22:56

import numpy as np
import pandas as pd
from sklearn.datasets.samples_generator import make_classification



def SFFS(n, data):
    '''
    Sequential Forward Floating Selection method

    :param n: Integer number, number of features
    :param data: Set of original training data
    :return: Set B, selected variables
    '''
    S = np.zeros(n)
    B = np.zeros([n,n])
    k = 0
    result = {}
    while k < n:
        R = np.zeros(n)
        for j in range(n):
            if S[j] == 0:
                SS = S.copy()
                SS[j] = 1
                R[j] = J(SS, data)
        j = R.argmax()
        if R[j] <= J(B[k],data):
            S = B[k]

        else:
            S[j] = 1
            B[k] = S
            t = 1
            while k > 2 and t == 1:
                R = np.zeros(n)
                for j in range(n):
                    if S[j] == 1:
                        SS = S.copy()
                        SS[j] = 0
                        R[j] = J(SS, data)
                j = R.argmax()
                if R[j] > J(B[k-1], data):
                    k = k - 1
                    S[j] = 0
                    B[k] = S
                else:
                    t = 0
        result[J(S, data)] = B[k]
        print(J(B[k], data))
        k += 1
    return result


def J(feature_select, dataset_orig):
    n = feature_select.shape[0]# K=特征数量=pd的列数-1
    k = 0
    for i in range(n):
        if feature_select[i] != 0:
            k += 1
    if(k == 0): return 0
    y_label = np.array([1])
    dataset = np.insert(feature_select, n, values = y_label) * dataset_orig
    df = pd.DataFrame(dataset)
    corr = df.corr().abs() # 相关系数矩阵取绝对值
    r_ky = corr.iloc[:n,n:].mean(skipna = True) # 相关系数矩阵最后一列的平均值
    r_kk = (corr.iloc[:n,:n].sum().sum() - k)/(2*k)
    # print(corr)
    # print("r_ky ",r_ky)
    # print("r_kk ",r_kk )
    j = float(k * r_ky / np.sqrt(k + (k-1) * r_kk))
    return j


if __name__ == '__main__':
    # generate features and labels data
    features, labels = make_classification(n_samples=500,n_features=10,n_redundant=0,n_informative=10,random_state=1,n_clusters_per_class=2)
    generated_data = np.c_[features,labels]
    B = (SFFS(10,generated_data))
    print(B)
