# http://yann.lecun.com/exdb/mnist/,下载mnist数据库至MNIST文件夹，完成后，解压缩至此

import numpy as np#import语句用来导入其他python文件（专业术语：模块module），使用该模块里定义的类(class)、方法(def)、变量，从而达到复用代码
import struct
# import matplotlib.pyplot as plt

# 训练集文件（根据自己mnist数据集下载位置更改）.\MNIST\t10k-labels.idx1-ubyte
train_images_idx3_ubyte_file = './MNIST/train-images.idx3-ubyte'
# 训练集标签文件
train_labels_labels_idx1_ubyte_file = './MNIST/train-labels.idx1-ubyte'

# 测试集文件
test_images_idx3_ubyte_file = './MNIST/t10k-images.idx3-ubyte'
# 测试集标签文件
test_labels_labels_idx1_ubyte_file = './MNIST/t10k-labels.idx1-ubyte'


def decode_idx3_ubyte(idx3_ubyte_file):
    """
    解析idx3文件的通用函数
    :param idx3_ubyte_fil. idx3文件路径
    :return: 数据集
    """
    # 读取二进制数据
    bin_data = open(idx3_ubyte_file, 'rb').read()

    # 解析文件头信息，依次为魔数、图片数量、每张图片高、每张图片宽
    offset = 0
    #因为数据结构中前4行的数据类型都是32位整型，所以采用i格式，但我们需要读取前4行数据，
    #所以需要4个i。我们后面会看到标签集中，只使用2个i。
    fmt_header = '>IIII' 
    magic_number, num_images, num_rows, num_cols = struct.unpack_from(fmt_header, bin_data, offset)
    print('magic_number:%d, num_images: %d, size_images: %d*%d' % (magic_number, num_images, num_rows, num_cols))

    # 解析数据集
    image_size = num_rows * num_cols
    #获得数据在缓存中的指针位置，从前面介绍的数据结构可以看出，
    #读取了前4行之后，指针位置（即偏移位置offset）指向0016。
    offset += struct.calcsize(fmt_header)  
    # print(offset)
    #图像数据像素值的类型为unsigned byte型，对应的format格式为B。这里还有加上图像大小784，
    #是为了读取784个B格式数据，如果没有则只会读取一个值（即一副图像中的一个像素值）
    fmt_image = '>' + str(image_size) + 'B'  
    # print(fmt_image,offset,struct.calcsize(fmt_image))
    images = np.empty((num_images, num_rows, num_cols))
    for i in range(num_images):
        if (i + 1) % 10000 == 0:
            print('proceed %d' % (i + 1) + 'image')
            # print(offset)
        images[i] = np.array(struct.unpack_from(fmt_image, bin_data, offset)).reshape((num_rows, num_cols))
        offset += struct.calcsize(fmt_image)

    return images


def decode_idx1_ubyte(labels_idx1_ubyte_file):
    """
    解析idx1文件的通用函数
    :param labels_idx1_ubyte_fil. idx1文件路径
    :return: 数据集
    """
    # 读取二进制数据
    bin_data = open(labels_idx1_ubyte_file, 'rb').read()

    # 解析文件头信息，依次为魔数和标签数
    offset = 0
    fmt_header = '>II'
    magic_number, num_images = struct.unpack_from(fmt_header, bin_data, offset)
    print('magic_number:%d, num_images: %d labels' % (magic_number, num_images))

    # 解析数据集
    offset += struct.calcsize(fmt_header)
    fmt_image = '>B'
    labels = np.empty(num_images)
    for i in range(num_images):
        if (i + 1) % 10000 == 0:
            print ('proceed %d' % (i + 1) + 'image')
        labels[i] = struct.unpack_from(fmt_image, bin_data, offset)[0]
        offset += struct.calcsize(fmt_image)
    return labels


def load_train_images(idx_ubyte_file=train_images_idx3_ubyte_file):
    """
    :param idx_ubyte_fil. idx文件路径
    :return: n*row*col维np.array对象，n为图片数量
    """
    return decode_idx3_ubyte(idx_ubyte_file)


def load_train_labels(idx_ubyte_file=train_labels_labels_idx1_ubyte_file):
    """
    :param idx_ubyte_fil. idx文件路径
    :return: n*1维np.array对象，n为图片数量
    """
    return decode_idx1_ubyte(idx_ubyte_file)


def load_test_images(idx_ubyte_file=test_images_idx3_ubyte_file):
    """
    :param idx_ubyte_fil. idx文件路径
    :return: n*row*col维np.array对象，n为图片数量
    """
    return decode_idx3_ubyte(idx_ubyte_file)


def load_test_labels(idx_ubyte_file=test_labels_labels_idx1_ubyte_file):
    """
    :param idx_ubyte_fil. idx文件路径
    :return: n*1维np.array对象，n为图片数量    """
    return decode_idx1_ubyte(idx_ubyte_file)


#标准正则化
def normalize_data(image):
    a_max = np.max(image)
    a_min = np.min(image)
    for j in range(image.shape[0]):
        image[j] = (image[j] - a_min) / (a_max - a_min)
    return image

#初始化参数
def initialize_with_zeros(n_x, n_h, n_y):
    np.random.seed(2)
    w1 = np.random.uniform(-np.sqrt(6) / np.sqrt(n_x + n_h), np.sqrt(6) /
            np.sqrt(n_h + n_x), size = (n_h, n_x))
    b1 = np.zeros((n_h, 1))
    w2 = np.random.uniform(-np.sqrt(6) / np.sqrt(n_y + n_h), np.sqrt(6) /
            np.sqrt(n_h + n_y), size = (n_y, n_h))
    b2 = np.zeros((n_y, 1))
    parameters = {"W1" : w1,
                    "b1" : b1,
                    "W2" : w2,
                    "b2" : b2}
    return parameters

#前向传播计算
def forward_propagation(X, parameters):
    W1=parameters["W1"]
    b1=parameters["b1"]
    W2=parameters["W2"]
    b2=parameters["b2"]
    Z1=np.dot(W1,X)+b1
    A1=np.tanh(Z1)
    Z2=np.dot(W2,A1)+b2
    A2=sigmoid(Z2)
    cache = {"Z1": Z1,
             "A1": A1,
             "Z2": Z2,
             "A2": A2}
    return A2, cache

#代价函数的计算
def costloss(A2, Y, parameters):
    t=0.00000000001
    logprobs=-(np.multiply(np.log(A2+t),Y)  + np.multiply(np.log(1-A2+t),(1-Y)))
    cost=np.sum(logprobs,axis=0,keepdims=True)/A2.shape[0]
    # print(logprobs)
    # print(Y)
    # print(A2)
    return cost

#反向传播
def back_propagation(parameters,cache,X,Y):
    W1=parameters["W1"]
    W2=parameters["W2"]
    A1 = cache["A1"]
    A2 = cache["A2"]
    Z1=cache["Z1"]
 
    dZ2=A2-Y
    dW2=np.dot(dZ2,A1.T)
    db2=np.sum(dZ2,axis=1,keepdims=True)
    dZ1=np.dot(W2.T,dZ2)*(1-np.power(A1,2))
    dW1=np.dot(dZ1,X.T)
    db1=np.sum(dZ1,axis=1,keepdims=True)
    grads = {"dW1": dW1,
             "db1": db1,
             "dW2": dW2,
             "db2": db2}
    return grads
#更新参数 
def update_para(parameters, grads, learning_rate ):
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    dW1 = grads["dW1"]
    db1 = grads["db1"]
    dW2 = grads["dW2"]
    db2 = grads["db2"]

    W1=W1-learning_rate*dW1
    b1=b1-learning_rate*db1
    W2=W2-learning_rate*dW2
    b2=b2-learning_rate*db2

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}
    return parameters

#定义sigmoid激活函数，softmax等
def sigmoid(x):
    s=1/(1+np.exp(-x))
    return s
def image2vector(image):
    v=np.reshape(image,[784,1])
    return v
def softmax(x):
    v=np.argmax(x)
    return v

if __name__ == '__main__':
    train_images = load_train_images()
    train_labels = load_train_labels()
    test_images = load_test_images()
    test_labels = load_test_labels()
 
    n_x=28*28
    n_h=32
    n_y=10
    parameters=initialize_with_zeros(n_x,n_h,n_y)
    for i in range(60000):
        img_train=train_images[i]
        label_train=np.zeros((10,1))
        l_rate=0.001
        if i>1000:
            l_rate=l_rate*0.999
        label_train[int(train_labels[i])]=1
        imgvector1=image2vector(img_train)
        imgvector=normalize_data(imgvector1)

        A2,cache=forward_propagation(imgvector,parameters)
        costl=costloss(A2,label_train,parameters)
        grads = back_propagation(parameters, cache, imgvector, label_train)
        parameters = update_para(parameters, grads, learning_rate = l_rate)
        print("cost after iteration %i:"%(i))
        print(costl)
    #预测10000张测试集图片中被正确识别的图片数
    predict_right_num=0
    for i in range(10000):
        img_train=test_images[i]
        vector_image=normalize_data(image2vector(img_train))
        label_trainx=test_labels[i]
        aa2,xxx=forward_propagation(vector_image,parameters)
        predict_value=softmax(aa2)
        if predict_value==int(label_trainx):
            predict_right_num=predict_right_num+1
    print(predict_right_num)

