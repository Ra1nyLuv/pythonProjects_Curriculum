def game_table(k):
    n = 2 ** k
    table = [[0] * (n - 1) for _ in range(n)]

    # 初始化2x2的比赛日程表
    if n >= 2:
        table[0][0] = 1
        table[0][1] = 2
        table[1][0] = 2
        table[1][1] = 1

    for t in range(1, k):
        temp = n // 2
        for i in range(temp, n):
            for j in range(temp):
                table[i][j] = table[i - temp][j] + temp

        for i in range(temp):
            for j in range(temp, n - 1):
                table[i][j] = table[i + temp][j - temp]

        for i in range(temp, n):
            for j in range(temp, n - 1):
                table[i][j] = table[i - temp][j - temp]

    return table


# 示例：8个选手的比赛日程表
k = 3
table = game_table(k)

# 打印比赛日程表
for row in table:
    print(row)