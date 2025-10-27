import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

# 样本数据点
X_data = np.array([3.3, 4.4, 5.5, 6.71, 6.93, 4.168, 9.779, 6.182, 7.59, 2.167, 7.042, 10.791, 5.313, 7.997, 5.654, 9.27, 3.1], dtype=np.float32)
Y_data = np.array([1.7, 2.76, 2.09, 3.19, 1.694, 1.573, 3.366, 2.596, 2.53, 1.221, 2.827, 3.465, 1.65, 2.904, 2.42, 2.94, 1.3], dtype=np.float32)

# 将数据转换为列向量
X = X_data.reshape(-1, 1)
Y = Y_data.reshape(-1, 1)

# 初始化参数 w 和 b
np.random.seed(1) # 为了结果可复现
w = np.random.randn(1, 1).astype(np.float32)
b = np.zeros((1, 1), dtype=np.float32)

# 设置超参数
learning_rate = 0.01
epochs = 100

# 训练模型
for epoch in range(epochs):
    # 前向传播
    Y_pred = np.dot(X, w.T) + b

    # 计算损失 (均方误差)
    loss = np.mean((Y_pred - Y) ** 2)

    # 反向传播 (计算梯度)
    dw = (2 / X.shape[0]) * np.dot((Y_pred - Y).T, X)
    db = (2 / X.shape[0]) * np.sum(Y_pred - Y)

    # 更新参数
    w = w - learning_rate * dw
    b = b - learning_rate * db

    # 每隔10个epoch打印一次损失
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{epochs}], Loss: {loss:.4f}')

# 打印训练后的参数
print("\n训练完成!")
print(f'学习到的权重 w: {w[0][0]:.4f}')
print(f'学习到的偏置 b: {b[0][0]:.4f}')

# 可以使用训练好的模型进行预测
test_x = np.array([[5.0]], dtype=np.float32) # 示例测试点
predicted_y = np.dot(test_x, w.T) + b
print(f'\n当 x = {test_x[0][0]} 时, 预测的 y = {predicted_y[0][0]:.4f}')

# 绘制结果图
plt.figure(figsize=(8, 6))
plt.scatter(X_data, Y_data, color='blue', label='原始数据点') # 绘制原始数据点

# 绘制拟合的直线
# 生成一系列x值用于绘制直线
x_line = np.linspace(X_data.min(), X_data.max(), 100).reshape(-1, 1)
y_line = np.dot(x_line, w.T) + b
plt.plot(x_line, y_line, color='red', label='拟合的回归线') # 绘制回归线

plt.xlabel('X 数据')
plt.ylabel('Y 数据')
plt.title('线性回归拟合结果')
plt.legend() # 显示图例
plt.grid(True) # 显示网格
plt.show() # 显示图形