import tensorflow as tf
from tensorflow_core.examples.tutorials.mnist import input_data

# 导入数据集
mnist = input_data.read_data_sets("/MNIST_data/", one_hot=True)
# 设置训练数据集一批 batch_size 个
batch_size = 100
n_batch = mnist.train.num_examples // batch_size

# 输入层 传入数据集接口
x = tf.compat.v1.placeholder(tf.float32, [None, 784])
y = tf.compat.v1.placeholder(tf.float32, [None, 10])


train_epochs = 21                           # 训练次数
H1_NN = 50                                  # 神经元个数
lr = tf.Variable(0.001, dtype=tf.float32)   # 学习率

# 建立输入-输出神经网络
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
prediction = tf.nn.softmax(tf.matmul(x, W) + b)

# loss = tf.reduce_mean(tf.square(prediction - y))    # 二次损失函数，
# 使用交叉熵，使得距离目标远的更快速，距离目标近的慢速
loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y,logits=prediction))
# 最小梯度法训练
train_step = tf.train.GradientDescentOptimizer(0.2).minimize(loss)
# 求准确率
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(prediction, 1))    # argmax()返回最大值所在序列，prediction返回最大概率序列，
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))          # y则返回1所在序列 ；当前后序列相等，则返回1，最终返回01列表
                                                                            # 对列表值求平均，即正确率
with tf.Session() as sess:
    # 初始化变量
    sess.run(tf.global_variables_initializer())
    for epoch in range(train_epochs):
        for batch in range(n_batch):
            # 读取训练数据并喂入
            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
            sess.run(train_step, feed_dict={x: batch_xs, y: batch_ys})
        # 使用测试样本计算正确率
        acc = sess.run(accuracy, feed_dict={x: mnist.test.images, y: mnist.test.labels})
        print("Iter" + str(epoch) + ",Test Accuracy" + str(acc))
