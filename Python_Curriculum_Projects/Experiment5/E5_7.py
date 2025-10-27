def fib(a, b, n):
    if n == 1:
        return a
    elif n == 2:
        return b
    else:
        return fib(b, a+b, n-1)

max_n = 0
for n in range(1, 5001):
    result = fib(0, 1, n)
    if result <= 5000:
        max_n = n
    else:
        break

print("最大的n为:", max_n)