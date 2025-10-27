import numpy as np
import matplotlib.pyplot as plt
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
# 输入数据
stocks = ['比亚迪', '立讯精密', '中芯国际', '隆基绿能', '宁德时代', '美的集团', '紫金矿业', '迈瑞医疗']
std_devs = np.array([0.0356, 0.0438, 0.0208, 0.0252, 0.0319, 0.0293, 0.0231, 0.0171])
expected_returns = np.array([-0.0129, -0.0086, -0.0076, -0.0053, -0.0052, -0.0021, -0.0014, 0.00])

# 假设资产之间的相关系数矩阵为单位矩阵（即资产之间不相关）
correlation_matrix = np.eye(len(stocks))

# 计算协方差矩阵
covariance_matrix = np.outer(std_devs, std_devs) * correlation_matrix

# 生成随机投资组合
num_portfolios = 10000
weights_matrix = np.random.random((num_portfolios, len(stocks)))
weights_matrix = weights_matrix / weights_matrix.sum(axis=1)[:, np.newaxis]

# 计算每个投资组合的预期回报和标准差
portfolio_returns = np.dot(weights_matrix, expected_returns)
portfolio_std_devs = np.sqrt(np.einsum('ij,jk,ik->i', weights_matrix, covariance_matrix, weights_matrix))

# 绘制有效边界曲线
plt.figure(figsize=(10, 6))
plt.scatter(portfolio_std_devs, portfolio_returns, marker='o', s=10, alpha=0.3)
plt.title('有效边界曲线')
plt.xlabel('标准差（风险）')
plt.ylabel('预期回报')
plt.grid(True)
plt.show()