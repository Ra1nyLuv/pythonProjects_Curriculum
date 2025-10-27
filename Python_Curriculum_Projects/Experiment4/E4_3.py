def Q1():
   pi = 0.0
   flag = 1
   for i in range(1, 10001, 2):
       pi = flag * (1 / i) + pi
       flag = -flag
   print(pi * 4)

Q1()