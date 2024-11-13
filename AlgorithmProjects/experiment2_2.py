def lcs(X, Y):
    m = len(X)
    n = len(Y)
    # 创建一个二维数组来存储最长公共子序列的长度
    c = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # 填充c表
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])

    # 构建最长公共子序列
    lcs_str = ""
    i, j = m, n
    while i > 0 and j > 0:
        if X[i - 1] == Y[j - 1]:
            lcs_str = X[i - 1] + lcs_str
            i -= 1
            j -= 1
        elif c[i - 1][j] > c[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return lcs_str, c[m][n]


# 示例
X = "ABCBDAB"
Y = "BDCAB"
lcs_str, length = lcs(X, Y)
print("最长公共子序列:", lcs_str)
print("长度:", length)