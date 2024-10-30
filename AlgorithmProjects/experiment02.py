def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# 示例数组
arr = [26, 99, 23, 45, 15, 29, 65, 35, 20, 3]

# 记录排序前的时间
import time
start_time = time.time()

# 调用合并排序函数
merge_sort(arr)

# 记录排序后的时间
end_time = time.time()

# 输出排序后的数组
print("排序后的数组:", arr)

# 输出算法花费的时间
print("排序花费的时间: {:.6f}秒".format(end_time - start_time))