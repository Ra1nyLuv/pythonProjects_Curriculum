import tensorflow as tf
from input_data import ImageDataGenerator
import os
import numpy as np
from datetime import datetime

#定位工作路径
#os.chdir(r'.\\flower_cls')
#选择训练文件和测试文件
train_file = r'train_set.txt'
test_file = r'test_set.txt'

batch_size = 16

#初始化训练数据集和测试数据集，训练集要打乱数据，测试集则不用
train_generator = ImageDataGenerator(train_file, shuffle=True)
val_generator = ImageDataGenerator(test_file, shuffle=False)

# Get the number of training/validation steps per epoch
#计算每执行一次epoch训练集和测试集需要几步，测试集的步数要加上1，因为训练时步数向下取整，余数舍去，测试时余数当做一次batch_size
train_batches_per_epoch = np.floor(
    train_generator.data_size / batch_size).astype(np.int32)
val_batches_per_epoch = np.floor(
    val_generator.data_size / batch_size).astype(np.int32) + 1

# 占位符
x = tf.placeholder("float", shape=[None, 227, 227, 3])
y_ = tf.placeholder("float", shape=[None, 5])
keep_prob = tf.placeholder("float")

'''
搭建网络
'''
def AlexNet(images):
  #第一层卷积层
  with tf.name_scope("conv1") as scope:
    #设置卷积核11×11,3通道,64个卷积核
    kernel1 = tf.Variable(tf.truncated_normal([11,11,3,96],mean=0,stddev=0.1,
                                                  dtype=tf.float32),name="weights")
    #卷积,卷积的横向步长和竖向补偿都为4
    conv = tf.nn.conv2d(images,kernel1,[1,4,4,1],padding="VALID")
    #初始化偏置
    biases = tf.Variable(tf.constant(0,shape=[96],dtype=tf.float32),trainable=True,name="biases")
    bias = tf.nn.bias_add(conv,biases)
    #RELU激活函数
    conv1 = tf.nn.relu(bias,name=scope)
    #最大池化
    pool1 = tf.nn.max_pool(conv1,ksize=[1,3,3,1],strides=[1,2,2,1],padding="VALID",name="pool1")
    #lrn处理
    lrn1 = tf.nn.lrn(pool1,5,bias=1,alpha=1e-3/9,beta=0.75,name="lrn1")

  #第二层卷积层
  with tf.name_scope("conv2") as scope:
    #初始化权重
    

    #初始化偏置
    

    #RELU激活
    
    #最大池化
    
    #LRN
    

  #第三层卷积层
  with tf.name_scope("conv3") as scope:
    #初始化权重
    



    #RELU激活层
    

  #第四层卷积层
  with tf.name_scope("conv4") as scope:
    #初始化权重
    

    #卷积
    


    #RELU激活
    

  #第五层卷积层
  with tf.name_scope("conv5") as scope:
    #初始化权重
   



    #REUL激活层
    
    #最大池化
    

  #第六层全连接层
  pool5 = tf.reshape(pool5,(-1,6*6*256))
  weight6 = tf.Variable(tf.truncated_normal([6*6*256,4096],stddev=0.1,dtype=tf.float32),
                           name="weight6")
  ful_bias1 = tf.Variable(tf.constant(0.0,dtype=tf.float32,shape=[4096]),name="ful_bias1")
  ful_con1 = tf.nn.relu(tf.add(tf.matmul(pool5,weight6),ful_bias1))
  ful_drop1 = tf.nn.dropout(ful_con1, keep_prob=keep_prob)

  #第七层第二层全连接层
  weight7 = tf.Variable(tf.truncated_normal([4096,4096],stddev=0.1,dtype=tf.float32),
                          name="weight7")
  ful_bias2 = tf.Variable(tf.constant(0.0,dtype=tf.float32,shape=[4096]),name="ful_bias2")
  ful_con2 = tf.nn.relu(tf.add(tf.matmul(ful_drop1,weight7),ful_bias2))
  ful_drop2 = tf.nn.dropout(ful_con2, keep_prob=keep_prob)
  #第八层第三层全连接层
  weight8 = tf.Variable(tf.truncated_normal([4096,5],stddev=0.1,dtype=tf.float32),
                          name="weight8")
  ful_bias3 = tf.Variable(tf.constant(0.0,dtype=tf.float32,shape=[5]),name="ful_bias3")
  ful_con3 = tf.add(tf.matmul(ful_drop2,weight8),ful_bias3)

  return ful_con3
'''
搭建网络
'''

y_conv = AlexNet(x)

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(
            logits=y_conv, labels=y_))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())

  train_error =[]
  test_error=[]
  train_accuracy=[]
  test_accuracy=[]

  for epoch in range(50):
    #打印当前时间和第几个ecoph
    print("{} Epoch number: {}".format(datetime.now(), epoch + 1))
    #最开始定义训练准确度为0，每次ecope最开始为0
    train_correct = 0.0
    loss_epoch = 0.0
    #每次跑一个batch  
    for i in range(train_batches_per_epoch):
      batch_xs, batch_ys = train_generator.next_batch(batch_size)
      #run 优化器，损失函数，精度，且给它们需要的参数
      _, loss_t, train_ac = sess.run([train_step, cross_entropy, accuracy], feed_dict={
                    x: batch_xs, y_: batch_ys, keep_prob: 0.5})
      #将每次batch训练得到的精度（损失值）加上最开始定义的0训练准确（0损失值），经过循环，最后得到每个epoch的训练准确度（损失值）
      train_correct += train_ac
      loss_epoch += loss_t
    #打印每个ecope的平均损失，平均训练精度
    train_loss = round(loss_epoch / train_batches_per_epoch, 3)
    train_acc = round(train_correct / train_batches_per_epoch, 3)
    print ("Epoch Loss= " + str(train_loss) + 
            ",Epoch train ac= " + str(train_acc))
    train_error.append(train_loss)
    train_accuracy.append(train_acc)

    test_correct = 0.0
    loss_epoch = 0.0
    #每次跑一个batch  
    for i in range(val_batches_per_epoch):
      batch_tx, batch_ty = val_generator.next_batch(batch_size)
      #run测试精度，且给它们需要的参数
      val_loss, val_ac = sess.run([cross_entropy, accuracy], feed_dict={
                    x: batch_tx, y_: batch_ty, keep_prob:1})
      #将每次batch测试得到的精度（损失值）加上最开始定义的0准确，经过循环，最后得到每个epoch的测试准确度
      test_correct += val_ac
      loss_epoch += val_loss

    #计算每个ecope的测试精度
    test_loss = round(loss_epoch / val_batches_per_epoch, 3)
    test_ac = test_correct / float(val_batches_per_epoch)

    test_error.append(test_loss)
    test_accuracy.append(test_ac)

    #打印每个ecope的测试准确度
    print ('test accuracy: %s' % test_ac)
    print ('\n')

    train_generator.reset_pointer()
    val_generator.reset_pointer()
  with open('.\\train_error.txt', 'w') as writer:
    for line in train_error:
      writer.write(str(line))
      writer.write('\n')
  with open('.\\test_error.txt', 'w') as writer:
    for line in test_error:
      writer.write(str(line))
      writer.write('\n')
  with open('.\\train_accuracy.txt', 'w') as writer:
    for line in train_accuracy:
      writer.write(str(line))
      writer.write('\n')
  with open('.\\test_accuracy.txt', 'w') as writer:
    for line in test_accuracy:
      writer.write(str(line))
      writer.write('\n')