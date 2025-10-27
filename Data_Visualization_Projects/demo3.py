import numpy as np
import matplotlib.pyplot as plt

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 股票信息
stock_info = {
    "601899": {"name": "紫金矿业", "weight": 3.652},
    "002594": {"name": "比亚迪", "weight": 4.155},
    "601012": {"name": "隆基绿能", "weight": 1.176},
    "300750": {"name": "宁德时代", "weight": 8.178},
    "000333": {"name": "美的集团", "weight": 4.697},
    "300124": {"name": "汇川技术", "weight": 1.797},
    "600276": {"name": "恒瑞医药", "weight": 2.688},
    "300760": {"name": "迈瑞医疗", "weight": 1.736},
    "002475": {"name": "立讯精密", "weight": 2.531},
    "688981": {"name": "中芯国际", "weight": 2.174}
}

# 确保标准差和预期收益率数组长度与股票数量一致
# 这里假设你补充了缺少的数据
std_devs = np.array([0.0356, 0.0438, 0.0208, 0.0252, 0.0319, 0.0293, 0.0231, 0.017, 0.023, 0.021])
expected_returns = np.array([-0.0129, -0.0086, -0.0076, -0.0053, -0.0052, -0.0021, -0.0014, 0.0, 0.001, 0.002])

# 无风险利率
risk_free_rate = 0.014

# 假设资产之间的相关系数矩阵为单位矩阵（即资产之间不相关）
correlation_matrix = np.eye(len(stock_info))

# 计算协方差矩阵
covariance_matrix = np.outer(std_devs, std_devs) * correlation_matrix

# 生成随机投资组合
num_portfolios = 10000
weights_matrix = np.random.random((num_portfolios, len(stock_info)))
weights_matrix = weights_matrix / weights_matrix.sum(axis=1)[:, np.newaxis]

# 计算每个投资组合的预期回报和标准差
portfolio_returns = np.dot(weights_matrix, expected_returns)
portfolio_std_devs = np.sqrt(np.einsum('ij,jk,ik->i', weights_matrix, covariance_matrix, weights_matrix))

# 计算每个投资组合的夏普比率
sharpe_ratios = (portfolio_returns - risk_free_rate) / portfolio_std_devs

# 找到夏普比率最大的投资组合（最优风险组合）
optimal_portfolio_index = np.argmax(sharpe_ratios)
optimal_return = portfolio_returns[optimal_portfolio_index]
optimal_std_dev = portfolio_std_devs[optimal_portfolio_index]
optimal_weights = weights_matrix[optimal_portfolio_index]

# 计算最优资本配置线（CAL）
cal_slope = sharpe_ratios[optimal_portfolio_index]
cal_std_devs = np.linspace(0, 0.06, 100)
cal_returns = risk_free_rate + cal_slope * cal_std_devs

# 绘制有效边界曲线和最优资本配置线
plt.figure(figsize=(10, 6))
plt.scatter(portfolio_std_devs, portfolio_returns, marker='o', s=10, alpha=0.3, label='有效边界')
plt.scatter(optimal_std_dev, optimal_return, marker='*', color='r', s=200, label='最优风险组合')
plt.plot(cal_std_devs, cal_returns, color='g', label='最优资本配置线')
plt.title('有效边界曲线和最优资本配置线')
plt.xlabel('标准差（风险）')
plt.ylabel('预期回报')
plt.grid(True)
plt.legend()
plt.show()
    