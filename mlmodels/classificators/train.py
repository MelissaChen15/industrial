# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 11:30


from sklearn import metrics
from sklearn.externals import joblib
from mlmodels.classificators.Para import Para
para = Para()

def train(model, model_name, X_train, X_cv,y_train, y_cv):
    print()
    print("model : ", model_name)
    model.fit(X_train, y_train)
    print("best params : ", model.best_params_)
    print("best score : ", model.best_score_)
    y_pred_train = model.predict(X_train)
    y_score_train = model.decision_function(X_train)
    y_pred_cv = model.predict(X_cv)
    y_score_cv = model.decision_function(X_cv)
    print("train set accurancy = %6f" % metrics.accuracy_score(y_train, y_pred_train))
    print("train set auc = %6f" % metrics.roc_auc_score(y_train, y_score_train))
    print("cv set accurancy = %6f" % metrics.accuracy_score(y_cv, y_pred_cv))
    print("cv set auc = %6f" % metrics.roc_auc_score(y_cv, y_score_cv))
    joblib.dump(model, para.path_results+ model_name+ "\\" + model_name + "_model.m")  # 模型存储
    print("model saved")

    return model


