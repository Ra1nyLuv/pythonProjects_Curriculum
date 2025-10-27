import random
target = random.randint(0,9)
print("请输入一个0~9之间的整数:\n")
cnt = 0
while True:
    n = eval(input(""))
    cnt += 1
    if n > target:
        print("遗憾,太大了")
    elif n < target:
        print("遗憾,太小了")
    else:
        print(f"预测{cnt}次,你猜中了~")