# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 11:30

from sklearn import metrics
from sklearn.externals import joblib
from main_entry.process.Para import Para
import os
para = Para()



# 训练回归模型
def train_regress(model, model_name, X_train, X_cv,y_train, y_cv):
    if os.path.exists(para.path_results + model_name) == False:
        os.mkdir(para.path_results + model_name)
    print()
    print("model : ", model_name)
    model.fit(X_train, y_train)
    joblib.dump(model, para.path_results+ model_name+ "\\" + model_name + "_model.m")  # 模型存储
    try:
        print("best params : ", model.best_params_)
        print("best score : ", model.best_score_)
    except:
        print("did not use param grid search")
    y_score_train = model.predict(X_train)
    y_score_cv = model.predict(X_cv)
    print("train set r2 = %6f, MSE = %6f" %(metrics.r2_score(y_train, y_score_train), metrics.mean_squared_error(y_train, y_score_train)) )
    print("cv set r2 = %6f, MSE = %6f" %(metrics.r2_score(y_cv, y_score_cv), metrics.mean_squared_error(y_cv, y_score_cv)) )
    print("model saved")

    return model

# 训练分类模型
def train_class(model, model_name, X_train, X_cv,y_train, y_cv):
    print()
    print("model : ", model_name)
    model.fit(X_train, y_train) # 训练模型
    try:# 如果使用了grid search， 打印最优参数
        print("best params : ", model.best_params_)
        print("best score : ", model.best_score_)
    except:
        print("did not use param grid search")
    # 在train和cv上predict
    y_pred_train = model.predict(X_train)
    y_pred_cv = model.predict(X_cv)
    print("train set accurancy = %6f" % metrics.accuracy_score(y_train, y_pred_train))
    print("cv set accurancy = %6f" % metrics.accuracy_score(y_cv, y_pred_cv))
    try:# 如果是有decision function的模型
        y_score_train = model.decision_function(X_train)
        y_score_cv = model.decision_function(X_cv)
        print("train set auc = %6f" % metrics.roc_auc_score(y_train, y_score_train))
        print("cv set auc = %6f" % metrics.roc_auc_score(y_cv, y_score_cv))
    except:# 如果没有decision function
        print("this classifiers has no decision function")
    joblib.dump(model, para.path_results+ model_name+ "\\" + model_name + "_model.m")  # 模型存储
    print("model saved")

    return model
