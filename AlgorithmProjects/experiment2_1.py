def matrix_chain_order(p):
    n = len(p) - 1  # 矩阵的数量
    # 初始化两个二维数组，m存储最小乘法次数，s记录分割点
    m = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    s = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    # 对角线遍历，从长度为2的子序列开始
    for length in range(2, n + 1):  # 子链的长度
        for i in range(1, n - length + 2):  # 子链的起始位置
            j = i + length - 1  # 子链的结束位置
            m[i][j] = float('inf')  # 初始化为无穷大
            for k in range(i, j):  # 尝试所有可能的分割点
                q = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if q < m[i][j]:
                    m[i][j] = q  # 更新最小乘法次数
                    s[i][j] = k  # 记录最佳分割点

    return m, s

def print_optimal_parens(s, i, j):
    if i == j:
        print(f'A{i}', end='')
    else:
        print('(', end='')
        print_optimal_parens(s, i, s[i][j])
        print_optimal_parens(s, s[i][j] + 1, j)
        print(')', end='')

# 测试数据
p = [30, 35, 15, 5, 10, 20, 25]

# 计算最小乘法次数和分割点
m, s = matrix_chain_order(p)

# 输出最小乘法次数
print("Minimum number of multiplications is:", m[1][len(p) - 1])

# 打印最佳括号化方案
print("Optimal parenthesization is: ", end='')
print_optimal_parens(s, 1, len(p) - 1)