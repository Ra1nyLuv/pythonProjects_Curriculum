import random

d = dict()

ls = list()

for i in range(100):
    ls.append(random.randint(10,99))
    d[ls[(i)]] = 0

for key in ls:
    if key in d:
        d[key] += 1
    else:
        d[key] = 1

ret = dict(sorted(d.items(), key=lambda d: d[1] , reverse=True))

for key in ret:
    print(f"{key}出现的次数是{ret[key]}")