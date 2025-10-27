for num in range(2,1000):
    factors = []
    for i in range(1,num):
        if num % i == 0:
            factors.append(i)

    if sum(factors) == num:
        print(num)