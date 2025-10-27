for num in range(100, 1000):
    digit_sum = sum(int(digit)**2 for digit in str(num))
    if num // 9 == digit_sum:
        print("满足条件的 3 位数为:", num)
