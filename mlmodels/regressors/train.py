# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 11:30

import pandas as pd
from sklearn import metrics
from sklearn.externals import joblib
from mlmodels.regressors.Para import Para
para = Para()

def train(model, model_name, X_train, X_cv,y_train, y_cv):
    print()
    print("model : ", model_name)
    model.fit(X_train, y_train)
    try:
        print("best params : ", model.best_params_)
        print("best score : ", model.best_score_)
    except:
        print("did not use param grid search")
    y_score_train = model.predict(X_train)
    y_score_cv = model.predict(X_cv)
    print("train set r2 = %6f, MSE = %6f" %(metrics.r2_score(y_train, y_score_train), metrics.mean_squared_error(y_train, y_score_train)) )
    print("cv set r2 = %6f, MSE = %6f" %(metrics.r2_score(y_cv, y_score_cv), metrics.mean_squared_error(y_cv, y_score_cv)) )
    joblib.dump(model, para.path_results+ model_name+ "\\" + model_name + "_model.m")  # 模型存储
    print("model saved")

    return model


