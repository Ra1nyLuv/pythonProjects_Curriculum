import random
r = random.randint(1,100)
# 读入
while True:
    x = input("请输入'y'进行抽奖:\n")
    if x == 'y':
        if 1 == r:
            print("一等奖")
            break
        elif r in range(2,5):
            print("二等奖")
            break
        elif r in range(5,12):
            print("三等奖")
            break
        else:
            print('谢谢惠顾')
    elif x == 'n':
        print('下次再来玩')
        exit()

    else:
        print('输入有误,请重新输入')
