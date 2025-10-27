import random as r

def max(s):
    temp = 0
    for i in s:
        if i > temp:
            temp = i
    return temp

def min(s):
    temp = 10
    for i in s:
        if i < temp:
            temp = i
    return temp

set_a = set()
set_b = set()

for i in range(10):
    set_a.add(r.randint(0,10))
    set_b.add(r.randint(0,10))

# (1)
print("(1):")
print(f"集合A的内容是:{set_a}")
print(f"集合A的长度为:{len(set_a)}")
print(f"集合A的最大值为{max(set_a)}")
print(f"集合A的最小值为{min(set_a)}",end="\n\n")
print(f"集合B的内容是:{set_b}")
print(f"集合B的长度为:{len(set_b)}")
print(f"集合B的最大值为{max(set_b)}")
print(f"集合B的最小值为{min(set_b)}",end="\n\n")

# (2)
print("(2):")
print(f"AB集合的并集为:{set_a.union(set_b)}")

# (3)
print("(3):")
print(f"AB集合的交集为:{set_a.intersection(set_b)}")

# (4)
print("(4):")
print(f"{set_a.difference(set_b)}")

# (5)
print("(5):")
print(f"{set_a.symmetric_difference(set_b)}")