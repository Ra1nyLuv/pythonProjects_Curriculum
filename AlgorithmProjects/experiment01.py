# 快速排序算法
# 思路: 分而治之

import random


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        # 随机生成一个pivot索引
        pivot_index = random.randint(0, len(arr) - 1)
        pivot = arr[pivot_index]

        # 将索引换到数据的首位, 方便排序操作
        arr[0], arr[pivot_index] = arr[pivot_index], arr[0]

        # 排序, 列表推导式
        less = [i for i in arr[1:] if i <= pivot]
        greater = [i for i in arr[1:] if i > pivot]

        # 递归调用,把三段排好序的数据拼在一起, 返回结果
        return quicksort(less) + [pivot] + quicksort(greater)

# 不同规模的测试数据
small_sample = list(range(10))
big_sample = list(range(100))
large_sample = list(range(1000))


example_list = large_sample
# 打乱测试数据的顺序
random.shuffle(example_list)
# 输出排序前的数据
print(example_list)
# 调用函数
sorted_list = quicksort(example_list)
# 输出排序后的数据
print(sorted_list)

