import numpy as np
import matplotlib.pyplot as plt
# 数据集的准备
from sklearn import datasets

iris = datasets.load_iris()
iris_x = iris.data
iris_y = iris.target

# 由于我们的逻辑回归解决的是二分类问题，所以我们值需要前两二分类的数据就可以啦
x = iris_x[iris_y < 2, :2]
y = iris_y[iris_y < 2]

plt.scatter(x[y == 0, 0], x[y == 0, 1])
plt.scatter(x[y == 1, 0], x[y == 1, 1])
plt.show()

# 对我们的数据进行划分
from sklearn.model_selection import train_test_split

train_x, test_x, train_y, test_y = train_test_split(x, y)


# 定义我们sigmoid
def sigmoid(z):
    return 1 / (1 + np.exp(-z))


# 定义我们的损失函数
def J(theta, x_b, y):
    y_hat = sigmoid(x_b.dot(theta))
    return -1 / len(y) * np.sum((y * np.log(y_hat)) + ((1 - y) * np.log(1 - y_hat)))


# 定义我们的导数，前面我们已经用公式推导出来了
def dJ(theta, x_b, y):
    return x_b.T.dot(sigmoid(x_b.dot(theta)) - y) / len(y)


# 使用我们的梯度下降来求得最优解
def gradient_descent(theta, x_b, y):
    # 利用我们的梯度下降来得到最佳的theta
    eta = 0.1  # 学习学率
    epsilon = 1e-8  # 相当于0的存在
    # 此时，我们的theta，应该是一个向量，不再是一个标量
    while True:
        gradient = dJ(theta, x_b, y)
        last_theta = theta
        theta = theta - eta * gradient  # 进行迭代操作

        if abs(J(theta, x_b, y) - J(last_theta, x_b, y)) < epsilon:
            return theta  # 返回最佳的theta值
            break;


# 这在前面的线性回归中已经有涉及到了
x_b = np.hstack([np.ones((len(train_x), 1)), train_x])
initial_theta = np.zeros(x_b.shape[1])

theta = gradient_descent(initial_theta, x_b, train_y)

# 进行数据的预测
test_x_b = np.hstack([np.ones((len(test_x), 1)), test_x])
y_predict = test_x_b.dot(theta)

print(y_predict)  # 我们知道 > 0.5 为1， 小于0.5为0
# # 这就与我们前面的decisipon_function联系起来

print(np.array(y_predict >= 0.5, dtype='int'))
print(test_y)

from sklearn.linear_model import LogisticRegression

log_reg = LogisticRegression()
log_reg.fit(train_x, train_y)
log_reg.decision_function(test_x)
