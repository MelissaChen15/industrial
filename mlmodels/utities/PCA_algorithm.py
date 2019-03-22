#coding=utf-8
import numpy as np

'''通过方差的百分比来计算将数据降到多少维是比较合适的，函数传入的参数是特征值和百分比percentage，返回需要降到的维度数num'''
def eigValPct(eigVals,percentage):
    sortArray=np.sort(eigVals) #使用numpy中的sort()对特征值按照从小到大排序
    sortArray=sortArray[-1::-1] #特征值从大到小排序
    arraySum=sum(sortArray) #数据全部的方差arraySum
    tempSum=0
    num=0
    for i in sortArray:
        tempSum+=i
        num+=1
        if tempSum>=arraySum*percentage:
            return num

'''pca函数有两个参数，其中dataMat是已经转换成矩阵matrix形式的数据集，列表示特征；其中的percentage表示取前多少个特征需要达到的方差占比，默认为0.9'''
def pca(dataMat1,percentage=0.9):
    dataMat=np.array(dataMat1)
    meanVals=np.mean(dataMat,axis=0)  #对每一列求平均值，因为协方差的计算中需要减去均值
    meanRemoved=dataMat-meanVals
    covMat=np.cov(meanRemoved,rowvar=0)  #cov()计算方差
    eigVals,eigVects=np.linalg.eig(np.mat(covMat))  #利用numpy中寻找特征值和特征向量的模块linalg中的eig()方法
    k=eigValPct(eigVals,percentage) #要达到方差的百分比percentage，需要前k个向量
    eigValInd=np.argsort(eigVals)  #对特征值eigVals从小到大排序
    eigValInd=eigValInd[:-(k+1):-1] #从排好序的特征值，从后往前取k个，这样就实现了特征值的从大到小排列
    redEigVects=eigVects[:,eigValInd]   #返回排序后特征值对应的特征向量redEigVects（主成分）
    lowDDataMat=meanRemoved*redEigVects #将原始数据投影到主成分上得到新的低维数据lowDDataMat
    reconMat=(lowDDataMat*redEigVects.T)+meanVals   #得到重构数据reconMat
    return reconMat


def PCA_calculation(self,factor_standard,common_dateseries):#画图相关
    data_input=np.array(factor_standard[str(common_dateseries[0])])
    from sklearn.decomposition import PCA
    pca=PCA()
    reduced_factor=pca.fit(data_input)
    var_proportion=pca.explained_variance_ratio_

    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(pca.explained_variance_, 'k', linewidth=2)
    plt.xlabel('n_components', fontsize=16)
    plt.ylabel('explained_variance_', fontsize=16)
    plt.show()

    return reduced_factor,var_proportion
