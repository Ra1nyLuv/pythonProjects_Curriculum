import random


def monte_carlo_pi(n):
    count = 0
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x ** 2 + y ** 2 <= 1:
            count += 1

    pi = 4 * count / n
    return pi


n = int(1e7)  # 迭代次数
pi = monte_carlo_pi(n)
print(pi)
