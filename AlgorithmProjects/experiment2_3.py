def bit_per_pixel(pixel):
    """ 计算存储一个像素所需的位数 """
    return pixel.bit_length()

def segment_length(bit_sequence):
    """ 将像素按位数相同的条件分段 """
    segments = []
    current_bit = bit_sequence[0]
    count = 0
    for bit in bit_sequence:
        if bit == current_bit:
            count += 1
        else:
            segments.append(count)
            current_bit = bit
            count = 1
    segments.append(count)
    return segments

def dynamic_programming_compression(l, b):
    """ 动态规划计算最优压缩方案 """
    n = len(l)
    s = [0] * (n + 1)
    kay = [0] * (n + 1)

    def lsum(a, b_index):
        return sum(l[a:b_index+1])

    def bmax(a, b_index):
        return max(b[a:b_index+1])

    for i in range(1, n + 1):
        s[i] = s[i-1] + l[i-1] * b[i-1] + 11
        kay[i] = 1
        for k in range(2, min(i + 1, 257)):
            if i - k >= 0:
                new_s = s[i-k] + lsum(i-k, i-1) * bmax(i-k, i-1) + 11
                if new_s < s[i]:
                    s[i] = new_s
                    kay[i] = k
    return s, kay

# 示例
image = [
    [10, 9, 12, 40],
    [50, 35, 15, 12],
    [8, 10, 9, 15],
    [240, 160, 130, 11]
]

# 图像线性化
pixels = [image[i][j] for i in range(len(image)) for j in range(len(image[0]))]

# 计算每个像素所需的位数
bit_sequence = [bit_per_pixel(pixel) for pixel in pixels]

# 分段
l = segment_length(bit_sequence)
b = [bit_sequence[0]]
current_bit = bit_sequence[0]
for bit in bit_sequence:
    if bit != current_bit:
        b.append(bit)
        current_bit = bit

# 确保 b 和 l 长度一致
if len(b) < len(l):
    b.append(bit_sequence[-1])

# 动态规划求解最优压缩方案
s, kay = dynamic_programming_compression(l, b)

# 输出结果
print("原始图像:")
for row in image:
    print(row)
print("\n像素线性化:", pixels)
print("位数序列:", bit_sequence)
print("分段长度:", l)
print("每段位数:", b)
print("最优压缩空间:", s[-1])
print("最优分段策略:", kay)