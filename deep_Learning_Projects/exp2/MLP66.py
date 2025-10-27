#加载MNIST数据集
import tensorflow as tf 
from tensorflow.examples.tutorials.mnist import input_data 
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True) 


#创建占位符,输入节点数为784，隐含层节点数为10
x = tf.placeholder(tf.float32, [None, 784]) 
y_ = tf.placeholder(tf.float32, [None, 10]) 

#初始化隐含层权重W全部初始化为0 
W = tf.Variable(tf.zeros([784, 10]))
#隐含层偏置b全部初始化为0 
b = tf.Variable(tf.zeros([10])) 


#定义模型结构 
y = tf.nn.softmax(tf.matmul(x, W) + b) 
print(y)
  
#训练部分 
#计算交叉熵损失
cross_entropy = -tf.reduce_sum(y_ * tf.log(y))
#定义优化器 
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy) 

#创建会话
with tf.Session() as sess:
    #初始化全部变量
    sess.run(tf.initialize_all_variables()) 

    #评估模型
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1)) 
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) 

    for i in range(1000): 
        #每次迭代都会加载50个样本
        batch = mnist.train.next_batch(50) 
        train_step.run(feed_dict={x: batch[0], y_: batch[1]}) 
        if i % 200 ==0: 
        #训练过程每200步在测试集上验证一下准确率，动态显示训练过程 
            print(i, 'testing_arruracy:', accuracy.eval({x: mnist.test.images, y_: mnist.test.labels})) 
    print('final_accuracy:', accuracy.eval({x: mnist.test.images, y_: mnist.test.labels})) 