str1 = input("请输入英文文本:\n")

d = dict()

ls = str1.split(" ")

for i in ls:
    d[i] = 0

for i in ls:
    if i in d:
        d[i] += 1
    else:
        d[i] = 1

ret = dict(sorted(d.items(), key=lambda d:d[1], reverse=True))

print(ret)