# __author__ = Chen Meiying
# -*- coding: utf-8 -*-
# 2019/3/25 14:49

import tensorflow as tf
import matplotlib.pyplot as plt
from random import randint
import numpy as np
import math
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('./',one_hot=True)

# 1.------------------------------- setting configuration parameters--------------------------------------------------
logs_path = 'log_simple_stats_5_layers_relu_softmax'
batchsize = 100
learning_rate = 0.003
training_epochs = 10
X = tf.placeholder(tf.float32, [None,28,28,1],name='input')
XX = tf.reshape(X,[-1,784])
# XX = tf.placeholder(tf.float32,[None,784])
Y_ = tf.placeholder(tf.float32, [None, 10],name='output')
# lr = tf.placeholder(tf.float32,[],name='learning_rate')
L = 200
M = 100
N = 60
O = 30
# 2. first layer---------------------------define the NN----------------------------------------------------------------
W1 = tf.Variable(tf.truncated_normal([784,L],stddev=0.1))
B1 = tf.Variable(tf.zeros([L])) # 怀疑维度问题？
Y1 = tf.nn.sigmoid(tf.matmul(XX,W1)+B1)
# 3. second layer
W2 = tf.Variable(tf.truncated_normal([L,M],stddev=0.1))
B2 = tf.Variable(tf.zeros([M]))
Y2 = tf.nn.sigmoid(tf.matmul(Y1,W2)+B2)
# 4. third layer
W3 = tf.Variable(tf.truncated_normal([M,N],stddev=0.1))
B3 = tf.Variable(tf.zeros([N]))
Y3 = tf.nn.sigmoid(tf.matmul(Y2,W3)+B3)
# 5. forth layer
W4 = tf.Variable(tf.truncated_normal([N,O],stddev=0.1))
B4 = tf.Variable(tf.zeros([O]))
Y4 = tf.nn.sigmoid(tf.matmul(Y3, W4) + B4)
# 5. fifth layer
W5 = tf.Variable(tf.truncated_normal([O, 10], stddev=0.1))
B5 = tf.Variable(tf.zeros([10]))
Ylogits = tf.matmul(Y4, W5) + B5
Y = tf.nn.softmax(Ylogits)
# --------------------------loss function---------------------------------------------------------------------
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=Ylogits,labels=Y_)
cross_entropy = cross_entropy
train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy)
# ----------------------------------accuracy--------------------------------------------------------------------------
correct_prediction = tf.equal(tf.argmax(Y,1),tf.argmax(Y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
# -----------------------------------training----------------------------------------------------------------
train_step = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy)
tf.summary.scalar("cost", cross_entropy)
tf.summary.scalar("accuracy", accuracy)
summary_op = tf.summary.merge_all()
# -----------------------------初始化------------------------------------------------------------------------
# init = tf.global_variables_initializer()
# sess = tf.Session()
# sess.run(init)
# ------------------训练-----------------------------------------------------------------------------------
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter(logs_path,graph=tf.get_default_graph())
    for epoch in range(training_epochs):
        batch_count = int(mnist.train.num_examples/batchsize)
        for i in range(batch_count):
            batch_x, batch_y = mnist.train.next_batch(batchsize)
            _,summary = sess.run(train_step,feed_dict={XX:batch_x,Y_:batch_y})
            writer.add_summary(summary, epoch*batch_count+i)
        print("Epoch:",epoch)
    print("Accuracy: ", accuracy.eval(feed_dict={XX: mnist.test.images, Y_: mnist.test.labels}))



