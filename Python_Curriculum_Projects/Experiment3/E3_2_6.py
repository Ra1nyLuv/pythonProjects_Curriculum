a = input()

print(a.__len__())

for c in a:
    print(c,end=' ')

print()

for c in a[::-1]:
    print(c,end=' ')