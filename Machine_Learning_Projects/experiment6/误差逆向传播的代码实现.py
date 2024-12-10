# coding=utf-8
import numpy as np
import matplotlib.pylab as plt
import random


class NeuralNetwork(object):
    def __init__(self, sizes, act, act_derivative, cost_derivative):
        # sizes表示神经网络各层的神经元个数，第一层为输入层，最后一层为输出层
        # act为神经元的激活函数
        # act_derivative为激活函数的导数
        # cost_derivative为损失函数的导数
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(nueron_num, 1) for nueron_num in sizes[1:]]
        self.weights = [np.random.randn(next_layer_nueron_num, nueron_num)
                        for nueron_num, next_layer_nueron_num in zip(sizes[:-1], sizes[1:])]
        self.act = act
        self.act_derivative = act_derivative
        self.cost_derivative = cost_derivative
        self._w = None
        self._g = None
        self._predict = None

    # 正向传播,计算输出的结果啦
    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = self.act(np.dot(w, a) + b)
        return a

    # 批量随机梯度下降算法
    def SGD(self, training_data, epochs, batch_size, learning_rate, y_true):
        # 将训练样本training_data随机分为若干个长度为batch_size的batch
        # 使用各个batch的数据不断调整参数，学习率为learning_rate
        # 迭代epochs次
        n = len(training_data)
        for j in range(epochs):
            random.shuffle(training_data)
            # 进行数据的分割
            batches = [training_data[k:k + batch_size] for k in range(0, n, batch_size)]
            for batch in batches:
                # 接收更新完成的参数，进行打印
                weight_last, biase_last = self.update_batch(batch, learning_rate)
            print("Epoch {0} complete, total errors is {1}".format(j, np.sum((y_true.T - self._predict) ** 2)))

    def update_batch(self, batch, learning_rate):
        # 根据一个batch中的训练样本，调整各个参数值
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        for x, y in batch:
            delta_nabla_b, delta_nabla_w = self.backprop(x, y)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        # 计算梯度，并调整各个参数值
        self.weights = [w - (learning_rate / len(batch)) * nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (learning_rate / len(batch)) * nb for b, nb in zip(self.biases, nabla_b)]
        return self.weights[-1], self.biases[-1]

    # 反向传播（重点）
    def backprop(self, x, y):
        # 保存b和w的偏导数值
        nabla_g = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        # 正向传播
        activation = x
        # 保存每一层神经输出值
        activations = [x]
        # 保存每一层神经输入值
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = self.act(z)
            activations.append(activation)
        self._predict = np.array(activations[-1][0]).reshape(-1, 1)
        # 反向传播得到各个参数的偏导数值
        g = self.cost_derivative(activations[-1], y) * self.act_derivative(zs[-1])
        nabla_g[-1] = g
        nabla_w[-1] = np.dot(g, activations[-2].transpose())
        # 反向逐层计算
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = self.act_derivative(z)
            # 反向逐层求参数偏导
            g = np.dot(self.weights[-l + 1].transpose(), g) * sp
            nabla_g[-l] = g
            nabla_w[-l] = np.dot(g, activations[-l - 1].transpose())
        return (nabla_g, nabla_w)


# 损失函数的偏导数
def cost_derivative(output_activations, y):
    return 2 * (output_activations - y)


# sigmoid函数
def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


# sigmoid函数的导数
def sigmoid_derivative(z):
    return sigmoid(z) * (1 - sigmoid(z))


# 创建一个3层的全连接神经网络，每层的神经元个数为 1, 3, 1
# 其中第一层为输入层，最后一层为输出层
network = NeuralNetwork([1, 3, 1], sigmoid, sigmoid_derivative, cost_derivative)

# 训练集样本
x = np.array([np.linspace(-7, 7, 200)]).T
y = (np.cos(x) + 1) / 2

# 使用批量随机梯度下降算法对模型进行训练
# 迭代288次；每次随机抽取40个样本作为一个batch；学习率设为0.3
training_data = [(np.array([x_value]), np.array([y_value])) for x_value, y_value in zip(x, y)]
network.SGD(training_data, 3000, 40, 0.3, y)

# 测试集样本
x_test = np.array([np.linspace(-9, 9, 120)])
# 测试集结果
y_predict = network.feedforward(x_test)

# 图示对比训练集和测试集数据
plt.plot(x, y, 'r', x_test.T, y_predict.T, '*')
plt.show()
