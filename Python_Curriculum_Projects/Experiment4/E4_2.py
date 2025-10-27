def calculate_shipping_fee(p, w, s):
    if s < 250:
        d = 0
    elif s < 500:
        d = 0.025
    elif s < 1000:
        d = 0.045
    elif s < 2000:
        d = 0.075
    elif s < 2500:
        d = 0.09
    elif s < 3000:
        d = 0.12
    else:
        d = 0.15

    f = p * w * s * (1 - d)
    return f

# 输入基本运费 p，货物重量 w，距离 s
p = float(input("请输入基本运费："))
w = float(input("请输入货物重量："))
s = float(input("请输入距离："))

total_fee = calculate_shipping_fee(p, w, s)
print(f"总运费为:{ total_fee:.2f}")