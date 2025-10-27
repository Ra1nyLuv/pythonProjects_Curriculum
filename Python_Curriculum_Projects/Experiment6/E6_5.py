d = dict()

for i in range(3):
    name = input("学生名字:\n")
    score = float(input("学生成绩:\n"))
    d[name] = score

def assess(d):
    min = 0
    for i in d:
        if d[i] > min:
            min = d[i]
    max = 100
    for i in d:
        if d[i] < max:
            max = d[i]

    avg_score = float()
    for i in d:
        avg_score += d[i]

    return min, max, avg_score/3

who_max, who_min = None, None
l = list(assess(d))
for i in d:
    if l[0] == d[i]:
        who_max = i

for i in d:
    if l[1] == d[i]:
        who_min = i

print(f"最高分属于:{who_max},成绩为:{l[0]}:")
print(f"最低分属于:{who_min},成绩为:{l[1]}")
print(f"平均分:{l[2]:.2f}")

