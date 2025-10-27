s = "学而时习之，不亦说乎？有朋自远方来，不亦说乎？人不知而不愠，不亦君子乎？"

chinese_count = 0
punctuation_count = 0

for c in s:
    if c in '，。？！；、：“”‘’（）':
        punctuation_count += 1
    else:
        chinese_count += 1

print("汉字个数：{}，标点符号个数：{}".format(chinese_count, punctuation_count))
