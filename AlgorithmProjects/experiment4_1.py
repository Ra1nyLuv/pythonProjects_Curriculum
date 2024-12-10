def place(k):
    for i in range(1, k):
        if x[i] == x[k] or abs(x[i] - x[k]) == abs(i - k):
            return False
    return True

def backtrack(t):
    global count, unique_solutions
    if t > n:
        count += 1
        # 标准化解
        solution = normalize_solution(x[1:])
        if solution not in unique_solutions:
            unique_solutions.append(solution)
    else:
        for i in range(1, n + 1):
            x[t] = i
            if place(t):
                backtrack(t + 1)

def normalize_solution(solution):
    # 这里可以根据棋盘的对称性进行标准化处理
    # 例如，将解按照一定规则排序，使得等效解具有相同的表示形式
    # 简单起见，这里可以对列索引进行排序
    return tuple(sorted(solution))

# 测试示例
n = 8
x = [0] * (n + 1)
count = 0
unique_solutions = []
backtrack(1)
print("Total solutions:", count)
print("Unique solutions:")
for solution in unique_solutions:
    print(solution)
print("Total unique solutions:", len(unique_solutions))