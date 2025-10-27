def traverse(s):
    letter_count = 0
    digit_count = 0
    space_count = 0
    other_count = 0

    for char in s:
        if char.isalpha():
            letter_count += 1
        elif char.isdigit():
            digit_count += 1
        elif char.isspace():
            space_count += 1
        else:
            other_count += 1

    return letter_count, digit_count, space_count, other_count

line = input('请输入一行字符：')
result = traverse(line)
print("字母个数：", result[0])
print("数字个数：", result[1])
print("空格个数：", result[2])
print("其他字符个数：", result[3])
