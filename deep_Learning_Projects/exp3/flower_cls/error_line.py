#-*-coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

#散点图数据
train_error =[]
test_error =[]
with open(r'./train_error.txt', 'r') as f:
    for line in f.readlines():
    	print(line)
    	train_error.append(float(line))
with open(r'./test_error.txt', 'r') as f:
    for line in f.readlines():
        test_error.append(float(line))
plt.xlabel('epoch')
plt.plot(train_error, label='train error')
plt.plot(test_error, label='test error')
plt.legend()

plt.savefig('./figure1')
plt.show()

train_accuracy =[]
test_accuracy =[]
with open(r'./train_accuracy.txt', 'r') as f:
    for line in f.readlines():
        train_accuracy.append(float(line))
with open(r'./test_accuracy.txt', 'r') as f:
    for line in f.readlines():
        test_accuracy.append(float(line))
plt.clf()
plt.xlabel('epoch')
plt.plot(train_accuracy, label='train accuracy')
plt.plot(test_accuracy, label='test accuracy')
plt.legend()

plt.savefig('./figure2')
plt.show()