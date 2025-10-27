n = eval(input("请输入一个2 <= n <= 1000的整数:\n"))
if n <= 2 or n >= 1000:
    print("请输入正确内容")
    exit()

ls = list()
d = dict()
for i in range(1,n):
    ls.append(i)

for i in ls:
    d[i+1] = False

for i in range(2,n//2):
    for key in d:
        if key % i == 0:
            d[key] = not d[key]

for i in d:
    if d[i] == True:
        print(i,end=" ")
