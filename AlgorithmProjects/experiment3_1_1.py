def coin_change(amount):
    coins = [25, 10, 5, 1]
    coin_count = [0] * len(coins)
    for i in range(len(coins)):
        coin_count[i] = amount // coins[i]
        amount %= coins[i]
    return sum(coin_count)

# 测试
amount = 63
print(coin_change(amount))