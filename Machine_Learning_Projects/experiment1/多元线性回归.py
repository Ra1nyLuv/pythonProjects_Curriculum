import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

# 加载数据
california = fetch_california_housing()
X = california.data
Y = california.target

# 划分训练集和测试集
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.2, random_state=42)

# 添加偏置项
train_x = np.hstack([np.ones((len(train_X), 1)), train_X])
test_x = np.hstack([np.ones((len(test_X), 1)), test_X])

# 计算权重向量K
K = np.linalg.inv(train_x.T.dot(train_x)).dot(train_x.T).dot(train_Y)

# 预测
predict_y = test_x.dot(K)

# 计算R²分数
print("手动计算的R²:", r2_score(test_Y, predict_y))

# 使用sklearn的LinearRegression模型
lin_reg = LinearRegression()
lin_reg.fit(train_X, train_Y)
sk_y_predict = lin_reg.predict(test_X)

# 计算并打印R²分数
print("sklearn计算的R²:", r2_score(test_Y, sk_y_predict))