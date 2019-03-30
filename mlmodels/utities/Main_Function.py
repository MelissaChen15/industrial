# from cross_sectional_Extraction import CrossSectional_Extr
# from FactorYield_Cal_New import FactorYield_Cal
# from FactorCorr import FactorCorr
# from StockSelection_Testing import Stratified_stock_backtest
import pandas as pd
import numpy as np
# from StockSlection_FiveGroups import Stratified_stock_backtestnew
# from PerformanceIndicator import PerformanceIndicator
#
# from DataInput_Valuation import InputData_Valuation
# from DataInput_TurnoverRate import InputData_TurnoverRate
# from DataInput_Fluctuation import InputData_Fluctuation
# from DataInput_Financial import InputData_financial
# from DataInput_Growth import InputData_Growth
# from DataInput_Leverage import InputData_Leverage
# from DataInput_Momentum import InputData_Momentum
# from excess_return import InputData_excess_return
# from PCA_algorithm import pca
# import matplotlib.pyplot as plt
# class all_factor_assemble(object):
#     def __init__(self):
#         pass
#     def factor_process_integrated(self):
#         #1.数据输入，数据预处理，输出需要的所有数据
#         filepath1 = r"F:\wind研报\研究\多因子\机器学习量化选股\Project\20180628-人工智能选股之SVM\code\Valuation_Factor.sql"
#         filepath2 = r"F:\wind研报\研究\多因子\机器学习量化选股\Project\20180628-人工智能选股之SVM\code\Fluctuation_Factor.sql"
#         filepath3 = r"F:\wind研报\研究\多因子\机器学习量化选股\Project\20180628-人工智能选股之SVM\code\Financial_Factor.sql"
#         filepath4 = r"F:\wind研报\研究\多因子\机器学习量化选股\Project\20180628-人工智能选股之SVM\code\Growth_Factor.sql"
#         filepath5 = r"F:\wind研报\研究\多因子\机器学习量化选股\Project\20180628-人工智能选股之SVM\code\Leverage_Factor.sql"
#         filepath6 = r"F:\wind研报\研究\多因子\机器学习量化选股\Project\20180628-人工智能选股之SVM\code\Momentum_Factor.sql"
#         filepath7 = r"F:\wind研报\研究\多因子\机器学习量化选股\Project\20180628-人工智能选股之SVM\code\TurnoverRate_Factor.sql"
#         filepath8 = r"F:\wind研报\研究\多因子\机器学习量化选股\Project\20180628-人工智能选股之SVM\code\month_excess_yield.sql"
#
#
#         InputData_ex1 = InputData_Valuation()
#         InputData_ex2 = InputData_Fluctuation()
#         InputData_ex3=InputData_financial()
#         InputData_ex4 = InputData_Growth()
#         InputData_ex5 = InputData_Leverage()
#         InputData_ex6 = InputData_Momentum()
#         InputData_ex7 = InputData_TurnoverRate()
#         InputData_ex8 = InputData_excess_return()
#
#
#         FactorCombData_1, DateSeries_1, FactorValueNameOnly_1, secucode_combin_new_1=InputData_ex1.InputDataPreprocess(filepath1)
#         FactorCombData_2, DateSeries_2, FactorValueNameOnly_2, secucode_combin_new_2=InputData_ex2.InputDataPreprocess(filepath2)
#         FactorCombData_3, DateSeries_3, FactorValueNameOnly_3, secucode_combin_new_3=InputData_ex3.InputDataPreprocess(filepath3)
#         FactorCombData_4, DateSeries_4, FactorValueNameOnly_4, secucode_combin_new_4=InputData_ex4.InputDataPreprocess(filepath4)
#         FactorCombData_5, DateSeries_5, FactorValueNameOnly_5, secucode_combin_new_5=InputData_ex5.InputDataPreprocess(filepath5)
#         FactorCombData_6, DateSeries_6, FactorValueNameOnly_6, secucode_combin_new_6=InputData_ex6.InputDataPreprocess(filepath6)
#         FactorCombData_7, DateSeries_7, FactorValueNameOnly_7, secucode_combin_new_7=InputData_ex7.InputDataPreprocess(filepath7)
#         excess_return, DateSeries_8, FactorValueNameOnly_8, secucode_combin_new_8=InputData_ex8.InputDataPreprocess(filepath8)
#
#         DateSeries_all=[DateSeries_1,DateSeries_2,DateSeries_3,DateSeries_4,DateSeries_5,DateSeries_6,DateSeries_7]
#         common_dateseries=list(set(DateSeries_all[0]).intersection(*DateSeries_all[1:]))
#         common_dateseries.sort()
#         final_factor=dict()
#         seccode_all=dict()#每个时间戳下的共同股票代码
#         for i in common_dateseries:
#             temp_combin= pd.concat([FactorCombData_1[str(i)], FactorCombData_2[str(i)], FactorCombData_3[str(i)],FactorCombData_4[str(i)],FactorCombData_5[str(i)],FactorCombData_6[str(i)],FactorCombData_7[str(i)]],axis=1,join='outer')# ,FactorCombData_5,FactorCombData_6,FactorCombData_7
#             temp_combin = temp_combin.dropna(axis=0, how='any', thresh=None, subset=None, inplace=False)  # 删除存在None的行数
#             temp_combin=temp_combin.reset_index(drop=True)
#             DataSet_Seccode=temp_combin.loc[:, 'SecuCode']
#             common_secucode=list(set(DataSet_Seccode.values.transpose().tolist()[0]).intersection(*DataSet_Seccode.values.transpose().tolist()[1:]))
#             common_secucode.sort()
#             seccode_all[i]=common_secucode
#             final_factor[str(i)]=pd.DataFrame()
#             for j in range(int(temp_combin.columns.size/2)):
#                 temp2=temp_combin.iloc[:,(j*2):(j+1)*2]
#                 temp3=temp2[temp2['SecuCode'].isin(common_secucode)]
#                 temp3 = temp3.reset_index(drop=True)
#                 final_factor[str(i)].insert(j,list(temp3.columns)[1],temp3.iloc[:,1])#插入第二列的因子值的数据
#
#         factor_name_assemble=list(final_factor[str(common_dateseries[0])].columns)#第一个是股票代码
#         #1.数据处理，标准化，去极值，根据IC值，因子收益，T检验等确定因子得有效性，去掉重因子等
#         FactorYield_Cal_ex = FactorYield_Cal()
#         result = FactorYield_Cal_ex.FactorData_Process(final_factor, common_dateseries, factor_name_assemble)#去极值
#         factor_standard = FactorYield_Cal_ex.Standardization(result, common_dateseries)#标准化
#
#         factor_decomp=dict()#旋转后的数据
#         for i in common_dateseries:
#             input_data_pca=factor_standard[str(i)]
#             if not (input_data_pca.empty):#有一个日期的数据集为空
#                 reconMat=pca(input_data_pca,percentage=0.9)
#                 factor_decomp[i]=reconMat
#         #训练数据的确定，label的确定
#         positive_y=dict()#
#         negative_y=dict()
#         positive_x=dict()
#         negative_x=dict()
#         combin_x=dict()#样本合并
#         combin_y=dict()
#         label_y=dict()
#         common_dateseries_new=list(set(common_dateseries) ^ set([np.datetime64('2008-04-30T00:00:00.000000000')]))#存在数据缺失
#         common_dateseries_new.sort()
#         for j in common_dateseries_new:
#             temp_data1=excess_return[str(j)]
#             temp_data2=temp_data1.sort_values(by = 'excess_yield_Modi_Value',axis = 0,ascending = False)
#             temp_data2=temp_data2.reset_index(drop=True)
#             train_num=int(len(temp_data2)*0.1)
#             positive_y_temp=temp_data2.iloc[0:train_num,:]#这个只是收益率数据，真正的训练数据需要与因子数据的股票代码取交集
#             common_stock_posi=list(set(seccode_all[j]).intersection(positive_y_temp['SecuCode']))
#             index_data1=[seccode_all[j].index(x) for x in common_stock_posi]
#             positive_x[j]=pd.DataFrame(factor_decomp[j]).iloc[index_data1,:]
#             positive_x[j]=positive_x[j].reset_index(drop=True)
#             positive_y[j]=positive_y_temp[positive_y_temp['SecuCode'].isin(common_stock_posi)]['excess_yield_Modi_Value']
#             positive_y[j]=positive_y[j].reset_index(drop=True)
#             positive_label=pd.DataFrame(np.repeat(1,len(common_stock_posi)))
#
#             negative_y_temp=temp_data2.iloc[-(train_num):,:]
#             common_stock_negat = list(set(seccode_all[j]).intersection(negative_y_temp['SecuCode']))
#             index_data2 = [seccode_all[j].index(x) for x in common_stock_negat]
#             negative_x[j] = pd.DataFrame(factor_decomp[j]).iloc[index_data2, :]
#             negative_x[j] = negative_x[j].reset_index(drop=True)
#             negative_y[j] = negative_y_temp[negative_y_temp['SecuCode'].isin(common_stock_negat)]['excess_yield_Modi_Value']
#             negative_y[j] = negative_y[j].reset_index(drop=True)
#             negative_label=pd.DataFrame(np.repeat(-1,len(common_stock_negat)))
#
#             combin_x[j]=positive_x[j].append(negative_x[j])
#             combin_y[j]=positive_y[j].append(negative_y[j])
#             combin_x[j]=combin_x[j].reset_index(drop=True)
#             combin_y[j]=combin_y[j].reset_index(drop=True)
#             label_y[j]=positive_label.append(negative_label)
#             label_y[j]=label_y[j].reset_index(drop=True)
#
#         train_set=pd.DataFrame()
#         train_target=pd.DataFrame()
#         train_regression_target=pd.DataFrame()
#         for j in range(84):#84个月数据作为样本内数据，其他数据进行样本外回测
#             train_set=train_set.append(combin_x[common_dateseries_new[j]])
#             train_set=train_set.reset_index(drop=True)
#             train_target=train_target.append(pd.DataFrame(label_y[common_dateseries_new[j]]))
#             train_target = train_target.reset_index(drop=True)
#             train_regression_target=train_regression_target.append(pd.DataFrame(combin_y[common_dateseries_new[j]]))
#             train_regression_target = train_regression_target.reset_index(drop=True)
#         train_set=pd.DataFrame(train_set,dtype='float')
#         train_target=pd.DataFrame(train_target,dtype='float')
#         train_regression_target=pd.DataFrame(train_regression_target,dtype='float')
#
#         from sklearn.model_selection import train_test_split
#         from sklearn import model_selection
#         train_x, test_x, train_y, test_y = model_selection.train_test_split(train_set, train_target, test_size=0.2,random_state=27)  #
#     # SVM Classifier using cross validation
#     from sklearn import svm, datasets
#     C_range = [1e-3, 1e-2, 1e-1, 0.3,1,3, 5, 10]
#     gamma_range = [1e-4,3e-4,1e-3,3e-3,0.01,0.03,0.1,0.3,1,5,10]
def svm_cross_validation(train_x, train_y,C_range,gamma_range):
    from sklearn.model_selection import GridSearchCV #应用超参数
    from sklearn.model_selection import StratifiedShuffleSplit
    from sklearn.svm import SVR
    model = SVR(kernel='rbf')#'C': [1e-3, 1e-2, 1e-1, 0.3,1,3, 5, 10], 'gamma': [1e-4,3e-4,1e-3,3e-3,0.01,0.03,0.1,0.3,1,5,10]
    cv = StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=42)
    param_grid = {'C': C_range, 'epsilon':gamma_range }#gamma值越小，分类界面越连续；gamma值越大，分类界面越“散”，分类效果越好，但有可能会过拟合
    grid_search = GridSearchCV(model, param_grid, n_jobs=8,cv=cv, verbose=1,scoring=['accuracy','roc_auc'],refit='accuracy')#进行分层抽样
    grid_search.fit(np.array(train_x), np.array(train_y).transpose()[0])#注意这里的格式
    best_parameters = grid_search.best_estimator_.get_params()#z最优的参数
    best_model=grid_search.best_estimator_
    scores_cross = grid_search.cv_results_['mean_test_accuracy'].reshape(len(C_range),len(gamma_range))#返回交叉验证的平均测试值,准确度
    auc_cross= grid_search.cv_results_['mean_test_roc_auc'].reshape(len(C_range),len(gamma_range))##返回交叉验证的平均测试值,准确度

    output_accuracy1=pd.DataFrame(scores_cross)
    output_accuracy1.index=[str(x) for x in C_range]
    output_accuracy1.columns=[str(x) for x in gamma_range]

    output_auc1=pd.DataFrame(auc_cross)
    output_auc1.index=[str(x) for x in C_range]
    output_auc1.columns=[str(x) for x in gamma_range]
    writer = pd.ExcelWriter('sigmoid交叉验证集数据.xlsx')  #
    output_accuracy1.to_excel(writer,  'sigmoid交叉验证集准确率', float_format='%.5f')  # float_format 控制精度
    output_auc1.to_excel(writer,  'sigmoid交叉验证集AUC', float_format='%.5f')  # float_format 控制精度
    writer.save()
    return scores_cross,auc_cross,best_model #返回最优的模型

#     def correlation_cal(best_model,combin_x,common_dateseries_new,factor_name_assemble):#尝试检验预测值与因子之间的相关性
#         corr_timeseries=pd.DataFrame()
#         for i in range(len(common_dateseries_new)):
#             predi_y=best_model.predict(np.array(combin_x[common_dateseries_new[i]]))
#             corr_cal=combin_x[common_dateseries_new[i]]
#             corr_cal.insert(0,'预测值',predi_y)
#             corr=(corr_cal.corr()).iloc[0,1:]#只关心预测值与其他因子之间的相关性问题
#             corr_timeseries.insert(i,common_dateseries_new[i],corr)
#         corr_timeseries.index=factor_name_assemble
#         writer = pd.ExcelWriter('sigmoid预测值与本期因子相关系数序列.xlsx')  #
#         corr_timeseries.transpose().to_excel(writer,  '相关系数序列', float_format='%.5f')  # float_format 控制精度
#         writer.save()
#
#
#     def model_evaluation(train_x,train_y,test_x,test_y):#上面得网格搜索可以直接得到最好的模型，下面的循环调参用于可视化，看参数对决策函数得影响
#         from sklearn.svm import SVC
#         from sklearn.metrics import roc_auc_score,auc,accuracy_score #进行auc以及正确率的计算
#         C_2d_range = [1e-3, 1e-2, 1e-1, 0.3,1,3, 5, 10]
#         gamma_2d_range = [1e-4,3e-4,1e-3,3e-3,0.01,0.03,0.1,0.3,1,5,10]
#         classifiers = []
#         test_auc=np.zeros([len(C_2d_range),len(gamma_2d_range)])
#         test_accuracy_score=np.zeros([len(C_2d_range),len(gamma_2d_range)])
#         for C in C_2d_range:
#             for gamma in gamma_2d_range:
#                 clf = SVC(C=C, gamma=gamma,probability=True,kernel='sigmoid')
#                 clf.fit(np.array(train_x), np.array(train_y).transpose()[0])
#                 classifiers.append((C, gamma, clf))
#                 predict_prob_y=clf.predict(test_x)
#                 test_auc[C_2d_range.index(C),gamma_2d_range.index(gamma)] = roc_auc_score(test_y, predict_prob_y)
#                 test_accuracy_score[C_2d_range.index(C),gamma_2d_range.index(gamma)]=accuracy_score(test_y,predict_prob_y)
#         output_accuracy1 = pd.DataFrame(test_accuracy_score)
#         output_accuracy1.index = [str(x) for x in C_2d_range]
#         output_accuracy1.columns = [str(x) for x in gamma_2d_range]
#
#         output_auc1 = pd.DataFrame(test_auc)
#         output_auc1.index = [str(x) for x in C_2d_range]
#         output_auc1.columns = [str(x) for x in gamma_2d_range]
#         writer = pd.ExcelWriter('sigmoid测试集数据.xlsx')  #
#         output_accuracy1.to_excel(writer, 'sigmoid测试集准确率', float_format='%.5f')  # float_format 控制精度
#         output_auc1.to_excel(writer, 'sigmoid测试集AUC', float_format='%.5f')  # float_format 控制精度
#         writer.save()
#         # end svm ,start metrics
#         plt.figure(figsize=(8, 6))
#         xx, yy = np.meshgrid(np.linspace(-2, 2, 200), np.linspace(-2, 2, 200))
#         for (k, (C, gamma, clf)) in enumerate(classifiers):
#             # evaluate decision function in a grid
#             Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
#             Z = Z.reshape(xx.shape)
#             # visualize decision function for these parameters
#             plt.subplot(len(C_2d_range), len(gamma_2d_range), k + 1)
#             plt.title("gamma=10^%d, C=10^%d" % (np.log10(gamma), np.log10(C)),size='medium')
#             # visualize parameter's effect on decision function
#             # 可视化参数对决策函数的影响
#             plt.pcolormesh(xx, yy, -Z, cmap=plt.cm.RdBu)  # 对网格进行画图
#             plt.scatter(X_2d[:, 0], X_2d[:, 1], c=y_2d, cmap=plt.cm.RdBu_r)
#             plt.xticks(())
#             plt.yticks(())
#             plt.axis('tight')
#             # 返回交叉验证的平均测试值，写成（len(C_range),len(gamma_range)）的形式
#     def parameter_visualization(scores=scores_cross,C_range,gamma_range):
#         plt.figure(figsize=(8, 6))  # 创建一个宽8英寸、高6英寸的图 热力图
#         plt.subplots_adjust(left=.2, right=0.95, bottom=0.15, top=0.95)
#         plt.imshow(auc_cross, interpolation='nearest', cmap=plt.cm.hot)#,norm=MidpointNormalize(vmin=0.2, midpoint=0.92))
#         plt.xlabel('gamma')
#         plt.ylabel('C')
#         plt.colorbar()
#         # plt.contourf(C_range, gamma_range, scores)#第三个参数需要展开成一维的
#         plt.xticks(np.arange(len(gamma_range)), gamma_range, rotation=45)
#         plt.yticks(np.arange(len(C_range)), C_range)
#         plt.title('Validation auc')
#         plt.show()
#         #曲面图表示
#         from mpl_toolkits.mplot3d import Axes3D
#         figure = plt.figure()
#         ax = Axes3D(figure)
#         # 网格化数据
#         C_range1=np.log(C_range)
#         gamma_range1=np.log(gamma_range)
#         X, Y = np.meshgrid(C_range1, gamma_range1)
#         ax.plot_surface(X, Y, output_auc1.transpose(), rstride=1, cstride=1, cmap='rainbow')
#         plt.show()
#
#     #SVR以及SVM联合预测并进行回测
#     best_C=5
#     best_gamma=0.003
#     kernel='sigmoid'
#
#     def SVR_model(best_C,best_gamma,kernel,seccode_all):
#         from sklearn.svm import SVR,SVC
#         clf = SVR(C=best_C, gamma=best_gamma, kernel=kernel)
#         clf.fit(np.array(train_set), np.array(train_regression_target).transpose()[0])
#         # predict_prob_y = clf.predict(test_x)
#         clf_svc=SVC(C=best_C, gamma=best_gamma, kernel=kernel)
#         clf_svc.fit(np.array(train_set), np.array(train_target).transpose()[0])
#
#         predict_factor=dict()
#         sccode=dict()
#         common_right=[]
#         for j in common_dateseries_new[84:]:
#             y_svr=clf.predict(factor_decomp[j])#得到预测值
#             y_svc = clf_svc.predict(factor_decomp[j])  # 得到预测值
#             common_index =[]
#             for i in range(len(y_svc)):
#                 if (y_svc[i] * y_svr[i])>0:
#                     common_index.append(i)
#             predict_factor[j]=y_svr[common_index]#筛选出在两个模型中均预测相同符号的股票为候选股票
#             sccode[j]=np.array(seccode_all[j])[common_index]
#             common_right.append(len(common_index)/len(y_svc))#两者预测方向一致的准确率
#         writer = pd.ExcelWriter('SVR与SVC方向一致性准确率时间序列.xlsx')  #
#         pd.DataFrame(common_right).to_excel(writer, '方向一致性准确率', float_format='%.5f')  # float_format 控制精度
#         writer.save()
#
#         DateSeries=common_dateseries_new[84:]
#         FactorCombData=dict()
#         for j in DateSeries:
#             temp1=pd.DataFrame([predict_factor[j],sccode[j]]).transpose()
#             temp1.columns=['value','secCode']
#             FactorCombData[j]=temp1
#
#         #对比组，直接根据SVR进行选择，不管svc结果
#         predict_factor2=dict()
#         for j in common_dateseries_new[84:]:
#             y_svr=clf.predict(factor_decomp[j])#得到预测值
#             predict_factor2[j]=y_svr
#
#         DateSeries=common_dateseries_new[84:]
#         FactorCombData=dict()
#         for j in DateSeries:
#             temp1=pd.DataFrame([predict_factor2[j],seccode_all[j]]).transpose()
#             temp1.columns=['value','secCode']
#             FactorCombData[j]=temp1
#
#
#         Test1 = Stratified_stock_backtestnew()
#         IndustryWeight, IndustryClassification = Test1.Industry300_SecCode()
#         IndustryName = IndustryClassification['中信证券行业'].unique()[0:29]  # 最后面有个0，只有29个行业
#         ExcessEarningGroup1,ExcessEarningGroup2, ExcessEarningGroup3 ,ExcessEarningGroup4, ExcessEarningGroup5 = Test1.StratifiedTest(DataSet_newTemp_Seccode, FactorCombData, DateSeries,IndustryName, IndustryClassification, IndustryWeight)
#
#     def performance_cal(sheetname):
#         import performance_index
#         NetValue_combin1 = pd.read_excel('绩效指标计算-输入数据.xlsx', sheetname=sheetname, header=0)
#         performance_index.performance_cal_all(NetValue_combin1)