# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/20 10:40

from mlmodels.classificators import load_sample_data,SVC_init,train, predict, build_strategy,evaluate_strategy
from mlmodels.classificators.Para import Para
para = Para()

# 1. 加载train/cv set数据
X_train, X_cv, y_train, y_cv, *args = load_sample_data.load()
print("X_train shape :", X_train.shape)
print("X_cv shape :", X_cv.shape)

# 2. 初始化模型
model, model_name= SVC_init.init()

# 3. 训练模型,保存模型
model = train.train(model, model_name, X_train, X_cv, y_train, y_cv)

# 4. 模型预测,保存预测结果
n_days_in_test = predict.predict(model,model_name)

# 5. 策略构建
strategy = build_strategy.build(n_days_in_test, model_name)

# 6. 策略评价
evaluate_strategy.evaluate(strategy,n_days_in_test)


# 其他
# print(svm.SVC().get_params().keys()) # 查看模型需要的参数
# model = joblib.load( para.path_results  + "model.m") # 模型加载