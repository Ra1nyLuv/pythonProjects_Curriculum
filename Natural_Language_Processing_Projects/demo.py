import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# 设置 Matplotlib 支持中文字符
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 数据准备
# 标准差（波动率）
std_dev = np.array([0.0214, 0.0381, 0.0136, 0.0307, 0.0096])

# 相关系数矩阵
corr_matrix = np.array([
    [1.00, -0.22, -0.12, -0.59, 0.01],
    [-0.22, 1.00, 0.69, 0.62, 0.49],
    [-0.12, 0.69, 1.00, 0.71, 0.65],
    [-0.59, 0.62, 0.71, 1.00, 0.31],
    [0.01, 0.49, 0.65, 0.31, 1.00]
])

# 计算协方差矩阵
cov_matrix = np.outer(std_dev, std_dev) * corr_matrix

# 预期收益率
expected_returns = np.array([0.03621, -0.01072, -0.00114, -0.0040, 0.00003])

# 无风险利率
rf = 0.02

# 目标函数：最小化风险（方差）
def portfolio_variance(weights):
    return np.dot(weights.T, np.dot(cov_matrix, weights))

# 约束条件：权重之和为1
constraints_sum_one = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1})

# 权重范围：0到1
bounds = tuple((0, 1) for _ in range(len(expected_returns)))

# 初始猜测：等权重
initial_guess = np.ones(len(expected_returns)) / len(expected_returns)

# 优化函数封装
def optimize_portfolio(objective_function, initial_guess, bounds, constraints):
    result = minimize(objective_function, initial_guess, method='SLSQP', bounds=bounds, constraints=constraints)
    if not result.success:
        raise ValueError("优化失败: " + result.message)
    return result.x

# 目标函数：最大化Sharpe Ratio
def negative_sharpe_ratio(weights):
    portfolio_return = np.dot(weights, expected_returns)
    portfolio_std = np.sqrt(portfolio_variance(weights))
    return -(portfolio_return - rf) / portfolio_std

# 优化：最大化Sharpe Ratio
optimal_weights = optimize_portfolio(negative_sharpe_ratio, initial_guess, bounds, constraints_sum_one)

# 计算组合的预期收益率和标准差
portfolio_return = np.dot(optimal_weights, expected_returns)
portfolio_std = np.sqrt(portfolio_variance(optimal_weights))

# 计算Sharpe Ratio
sharpe_ratio = (portfolio_return - rf) / portfolio_std

# 输出最优权重
print("各股票在最优组合中的权重：")
for stock, weight in zip(['北方华创', '智飞生物', '贵州茅台', '宁德时代', '片仔癀'], optimal_weights):
    print(f"{stock}: {weight:.4f}")

# 输出组合的预期收益率和标准差
print(f"\n最优组合的预期收益率: {portfolio_return:.4f}")
print(f"最优组合的标准差: {portfolio_std:.4f}")
print(f"最优组合的Sharpe Ratio: {sharpe_ratio:.4f}")

# 可视化
# 1. 有效边缘曲线
def efficient_frontier():
    target_returns = np.linspace(min(expected_returns), max(expected_returns), 100)
    efficient_portfolios = []

    for target_return in target_returns:
        constraints = (
            {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
            {'type': 'eq', 'fun': lambda weights: np.dot(weights, expected_returns) - target_return}
        )
        try:
            result = optimize_portfolio(portfolio_variance, initial_guess, bounds, constraints)
            efficient_portfolios.append(result)
        except ValueError as e:
            print(f"优化失败: {e}")
            continue

    efficient_returns = [np.dot(weights, expected_returns) for weights in efficient_portfolios]
    efficient_risks = [np.sqrt(portfolio_variance(weights)) for weights in efficient_portfolios]

    plt.figure(figsize=(10, 6))
    plt.plot(efficient_risks, efficient_returns, 'b-', label='有效边缘曲线')
    plt.scatter(portfolio_std, portfolio_return, color='red', label='最优组合')
    plt.title('有效边缘曲线')
    plt.xlabel('风险（标准差）')
    plt.ylabel('预期收益率')
    plt.legend()
    plt.grid(True)
    plt.show()

# 2. 最优资本配置线（CAL）
def capital_allocation_line():
    cal_returns = np.linspace(rf, portfolio_return, 100)
    cal_risks = (cal_returns - rf) / sharpe_ratio

    plt.figure(figsize=(10, 6))
    plt.plot(cal_risks, cal_returns, 'g-', label='最优资本配置线（CAL）')
    plt.scatter(portfolio_std, portfolio_return, color='red', label='最优组合')
    plt.title('最优资本配置线（CAL）')
    plt.xlabel('风险（标准差）')
    plt.ylabel('预期收益率')
    plt.legend()
    plt.grid(True)
    plt.show()

# 3. 最优组合的权重分布
def optimal_weights_distribution():
    stocks = ['北方华创', '智飞生物', '贵州茅台', '宁德时代', '片仔癀']
    plt.figure(figsize=(10, 6))
    plt.bar(stocks, optimal_weights, color='skyblue')
    plt.title('最优组合的权重分布')
    plt.xlabel('股票名称')
    plt.ylabel('权重')
    plt.grid(True)
    plt.show()

# 调用可视化函数
efficient_frontier()
capital_allocation_line()
optimal_weights_distribution()
    