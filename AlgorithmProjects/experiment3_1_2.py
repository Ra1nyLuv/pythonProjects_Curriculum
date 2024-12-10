def activity_selection(n, s, f):
    activities = sorted(zip(s, f), key=lambda x: x[1])
    selected = [0] * n
    selected[0] = 1
    j = 0
    for i in range(1, n):
        if activities[i][0] >= activities[j][1]:
            selected[i] = 1
            j = i
        else:
            selected[i] = 0
    return selected

# 测试
n = 11
s = [1, 3, 0, 5, 3, 5, 6, 8, 8, 2, 12]
f = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
print(activity_selection(n, s, f))