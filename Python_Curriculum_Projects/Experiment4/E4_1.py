n = eval(input("请输入一个整数:\n"))
def alternate(n):#分支
    if n % 2 != 0:
        print(n**2)
    else:
        print(n**3)

def conditionate(n):#条件
    print(n**2 if n % 2 != 0 else n**3 )

alternate(n)
conditionate(n)