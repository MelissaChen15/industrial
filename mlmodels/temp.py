# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/11 17:06


# from sklearn.pipeline import Pipeline
# from sklearn.svm import SVC
# from sklearn.feature_selection import SelectKBest
# from sklearn.feature_selection import f_regression
# from sklearn.datasets import samples_generator
#
# x, y = samples_generator.make_classification(n_informative=5, n_redundant=0, random_state=42)
# anova_filter = SelectKBest(f_regression, k=5)
# clf = SVC(kernel='linear')
# anova_svm = Pipeline([('anova', anova_filter), ('svc', clf)])
# anova_svm.set_params(anova__k=10, svc__C=0.1).fit(x, y)
# # anova__k 下划线是两个，前缀是在pipeline中的名称，后缀是函数中的参数。注意大小写
# score = anova_svm.score(x, y)
# print(score)

# 结果写入文件
fo = open("result.txt", "w")
a = [1,2,3,4,5]
s = ""
for i in a:
    s.join(str(i))
fo.write(s)
fo.close()
# print(y_pred_train,y_score_train,y_pred_cv, y_score_cv)