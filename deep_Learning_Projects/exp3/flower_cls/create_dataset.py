#coding=utf-8
import numpy as np
import cv2
import os
import random
import math


'''
遍历文件夹
root    表示正在遍历的文件夹的名字（根/子）
dirs    记录正在遍历的文件夹下的子文件夹集合
files    记录正在遍历的文件夹中的文件集合
os.path.join(): 将多个路径组合后返回
''' 
img_set = {}
for root, dirs, _ in os.walk('.\\flower_data'):
	label_num = 0
	for dir_name in dirs:
		#dir_name = 'daisy'
		flower_label = label_num
		# flower_label = 0
		for root_1, _, files in os.walk(os.path.join(root, dir_name)): #'.\\flower_data\\daisy'
			for file_name in files:
				img_path = os.path.join(root_1, file_name)
				# .\flower_data\daisy\4333085242_bbeb3e2841_m.jpg
				if flower_label not in img_set.keys():
					img_set[flower_label] = [img_path]
					# {0:['.\flower_data\daisy\4333085242_bbeb3e2841_m.jpg']}
				else:
					img_set[flower_label].append(img_path)
					# {0:['.\flower_data\daisy\4333085242_bbeb3e2841_m.jpg','.\flower_data\daisy\22244161124_53e457bb66_n.jpg']}
		label_num+=1
	
train_set = []
test_set = []
for key_i in img_set.keys():
	test_num = math.ceil(0.3*len(img_set[key_i]))
	#打乱顺序
	random_index = np.arange(len(img_set[key_i]))
	random.shuffle(random_index)
	for j in range(test_num):
		test_set.append(img_set[key_i][random_index[j]] + ' ' + str(key_i))
	for j_1 in range (test_num, len(img_set[key_i])):
		train_set.append(img_set[key_i][random_index[j_1]] + ' ' + str(key_i))

with open('.\\train_set.txt', 'w') as writer:
	for line in train_set:
		writer.write(line)
		writer.write('\n')
with open('.\\test_set.txt', 'w') as writer:
	for line in test_set:
		writer.write(line)
		writer.write('\n')