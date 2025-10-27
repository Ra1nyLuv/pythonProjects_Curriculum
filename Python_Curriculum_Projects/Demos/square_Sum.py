#求平方和累加
def square_sum(n):
    ret = 0
    for i in range(n, 0, -1):
        ret += i * i
    return ret

n = eval(input())
print(square_sum(n))