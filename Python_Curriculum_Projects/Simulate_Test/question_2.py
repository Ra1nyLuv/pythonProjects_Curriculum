# 读入
with open(r'C:\Users\RainyLuv\PycharmProjects\pythonProject\.idea\Python_Files\Simulate_Test\sample.txt', 'r', encoding = 'utf8') as fr:
    ls = list()
    d = dict()
    ls = fr.read().upper().replace('\n',' ').split(' ')

    for i in ls:
        d[i] = 0        #   赋初值

    for i in d.keys():
        for j in ls:
            if i==j:
                d[i] += 1
    d = sorted(d.items(), key=lambda x: x[1], reverse=True)

    print(d)
    
    for i in range(5):
        print(d[i])

# 用字典存储


# 处理字典数据


# 输出



