import numpy as np
from matplotlib import pyplot as plt


def J(x):
    """目标函数"""
    return x ** 2 + 5


def dJ(x):
    """目标函数的导数（梯度）"""
    return 2 * x


def gradient_descent(initial_x, learning_rate, epsilon):
    """
    使用梯度下降法找到最小化目标函数的x值。

    参数:
    initial_x -- 初始的x值
    learning_rate -- 学习率
    epsilon -- 停止条件阈值

    返回:
    x -- 最终的x值
    history_x -- 每次迭代的x值列表
    """
    x = initial_x
    history_x = [x]

    while True:
        gradient = dJ(x)
        last_x = x
        x = x - learning_rate * gradient

        history_x.append(x)

        if abs(J(x) - J(last_x)) < epsilon:
            break

    return x, history_x


if __name__ == '__main__':
    # 构造数据集
    X = np.linspace(-5, 5, 50)
    Y = J(X)

    # 第一次实验
    initial_x_1 = 1
    learning_rate_1 = 0.1
    epsilon_1 = 1e-8
    x_1, _ = gradient_descent(initial_x_1, learning_rate_1, epsilon_1)
    print(f"Initial x: {initial_x_1}, Final x: {x_1}, J(x): {J(x_1)}")

    # 第二次实验
    initial_x_2 = 5
    learning_rate_2 = 0.3
    epsilon_2 = 1e-8
    x_2, history_x_2 = gradient_descent(initial_x_2, learning_rate_2, epsilon_2)
    print(f"Initial x: {initial_x_2}, Final x: {x_2}, J(x): {J(x_2)}")

    # 绘图
    plt.plot(X, Y, label='Function J(x)')
    plt.plot(np.array(history_x_2), J(np.array(history_x_2)), color='r', marker='o', linestyle='-',
             label='Gradient Descent Path')
    plt.scatter(x_2, J(x_2), color='g', label='Minimum Point')
    plt.title('Gradient Descent Optimization')
    plt.xlabel('x')
    plt.ylabel('J(x)')
    plt.legend()
    plt.show()