模型评价指标（改公式呀~~~）

考察：不同类别的重要性；样本不平衡时，指标对于各种类别的敏感性

part 1: 回归模型

1. ###### MSE/RMSE

   ![img](https://images2018.cnblogs.com/blog/1036486/201803/1036486-20180301212750947-1184937029.png)

   优点：RMSE与原数据同一量纲

   缺点：平均值指标假设数据满足**高斯分布**；**异常点**敏感：放大了较大误差与均值之间的差距，如果某个异常点误差大，整个MSE/RMSE就会比较大

2. MAE(平均绝对误差)

   ![img](https://images2018.cnblogs.com/blog/1036486/201803/1036486-20180301212932425-2060601307.png)

   优点：同量纲；真实误差

   缺点：绝对数

3.  R2 （R Squared）

   ![img](https://images2018.cnblogs.com/blog/1036486/201803/1036486-20180302155715312-1898824494.png)

   ![img](https://images2018.cnblogs.com/blog/1036486/201803/1036486-20180302160827654-1176272029.png)

R2 <=  1

越大越好，当R2 = 0时，预测模型表现 = 基准模型

当R2 < 0时, 预测模型表现不如基准模型，说明数据可能不存在任何线性关系

part 2: 分类模型

无所谓几分类：

1.  准确率

######  

$$
accurancy = n_correct/N_total
$$

优点：简单

缺点：**不区分样本的重要性**；数据不平衡的时候，**样本多**的类别主导了准确率的计算

2. 平均准确率

   公式：

   <https://blog.csdn.net/shine19930820/article/details/78335550>

缺点：**样本少**的类别，不同模型的准确率的方差可能会比较大

二分类：

输出类别概率的分类器：

3. 对数损失（Log-loss/Cross-entropy）

<https://blog.csdn.net/shine19930820/article/details/78335550>

输出0/1的分类器：

4.  基于混淆矩阵的各类指标

   | predict:0                        | predict:1                        |
   | -------------------------------- | -------------------------------- |
   | actual:0 -- true positive -- TP  | actual:0 -- false negative -- FN |
   | actual:1 -- false positive -- FP | actual:1 -- true negative -- TN  |

**查准率 Precision** = TP/(TP+FP)

**查全率 Recall** = TP/(TP+FN)

一般情况下，两者存在trade off

**PR曲线**：以P作为横坐标，R作为纵坐标，就可以画出P-R曲线。

**F1-score** = (2*Recall**Precision) / (Recall + Precision)， Precision和Recall加权调和平均数，假设两者一样重要

**TPR**（True Positive Rate） = TP/(TP+FN)

**FPR**（False Positive Rate） = FP/(TN+FP)

**ROC曲线**：横轴FPR，纵轴TPR

AUC即为ROC曲线下的面积，表示一种概率：假设AUC=0.7，则表示给定一个正样本和一个负样本，在70%的情况下，模型对正样本的打分高于对负样本的打分。

![img](https://img2018.cnblogs.com/blog/1479233/201810/1479233-20181014234000689-2045856494.png)

part 3: sklearn

sklearn.metrics

| Scoring                     | Function                                                     | Comment                          |
| --------------------------- | ------------------------------------------------------------ | -------------------------------- |
| **Classification**          |                                                              |                                  |
| ‘accuracy’                  | [`metrics.accuracy_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html#sklearn.metrics.accuracy_score) |                                  |
| ‘average_precision’         | [`metrics.average_precision_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.average_precision_score.html#sklearn.metrics.average_precision_score) |                                  |
| ‘f1’                        | [`metrics.f1_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score) | for binary targets               |
| ‘f1_micro’                  | [`metrics.f1_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score) | micro-averaged                   |
| ‘f1_macro’                  | [`metrics.f1_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score) | macro-averaged                   |
| ‘f1_weighted’               | [`metrics.f1_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score) | weighted average                 |
| ‘f1_samples’                | [`metrics.f1_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html#sklearn.metrics.f1_score) | by multilabel sample             |
| ‘neg_log_loss’              | [`metrics.log_loss`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html#sklearn.metrics.log_loss) | requires `predict_proba` support |
| ‘neg_log_loss’              | [`metrics.log_loss`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html#sklearn.metrics.log_loss) | requires `predict_proba` support |
| ‘recall’ etc.               | [`metrics.recall_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html#sklearn.metrics.recall_score) | suffixes apply as with ‘f1’      |
| ‘roc_auc’                   | [`metrics.roc_auc_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html#sklearn.metrics.roc_auc_score) |                                  |
| **Clustering**              |                                                              |                                  |
| ‘adjusted_rand_score’       | [`metrics.adjusted_rand_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html#sklearn.metrics.adjusted_rand_score) |                                  |
| **Regression**              |                                                              |                                  |
| ‘neg_mean_absolute_error’   | [`metrics.mean_absolute_error`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_absolute_error.html#sklearn.metrics.mean_absolute_error) |                                  |
| ‘neg_mean_squared_error’    | [`metrics.mean_squared_error`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html#sklearn.metrics.mean_squared_error) |                                  |
| ‘neg_median_absolute_error’ | [`metrics.median_absolute_error`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.median_absolute_error.html#sklearn.metrics.median_absolute_error) |                                  |
| ‘r2’                        | [`metrics.r2_score`](http://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html#sklearn.metrics.r2_score) |                                  |

感谢

<https://blog.csdn.net/shine19930820/article/details/78335550>