import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import t


def simple_linear_regression(X, Y):
    """
    计算简单线性回归模型的参数，并返回模型的斜率(a)、截距(b)及R²值。
    """
    x_mean = np.mean(X)
    y_mean = np.mean(Y)

    # 计算斜率(a)和截距(b)
    n = np.sum((X - x_mean) * (Y - y_mean))
    d = np.sum((X - x_mean) ** 2)
    a = n / d
    b = y_mean - a * x_mean

    return a, b


def predict(X, a, b):
    """
    使用给定的线性回归模型参数预测Y值。
    """
    return [a * x + b for x in X]


def evaluate_model(Y_true, Y_pred, y_mean):
    """
    计算并返回模型的R²值。
    """
    ss_residual = sum((Y_pred - Y_true) ** 2)
    ss_total = sum((Y_true - y_mean) ** 2)
    r_squared = 1 - ss_residual / ss_total
    return r_squared


def plot_results(X, Y, Y_pred):
    """
    绘制原始数据点和回归线。
    """
    plt.scatter(X, Y, label='Original data')
    plt.plot(X, Y_pred, color='red', label='Fitted line')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # 数据准备
    X = np.array([2, 3, 4, 5, 6])
    Y = 2 * X + np.random.normal(1, 2, 5)

    # 模型训练
    a, b = simple_linear_regression(X, Y)

    # 预测
    Y_pred = predict(X, a, b)

    # 结果可视化
    plot_results(X, Y, Y_pred)

    # 模型评估
    score = evaluate_model(Y, Y_pred, np.mean(Y))
    print(f'R-squared: {score}')

    # 计算t值和p值
    n = len(X)
    se_model = np.sqrt(sum((Y_pred - Y) ** 2) / (n - 2))
    sss = np.sqrt(sum((X - np.mean(X)) ** 2))
    t_val = a / (se_model / sss)
    p_val = 2 * (1 - t.cdf(np.abs(t_val), n - 2))
    print(f'T-value: {t_val}, P-value: {p_val}')