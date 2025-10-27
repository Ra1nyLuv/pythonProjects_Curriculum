import numpy as np
import cv2


class ImageDataGenerator:
    def __init__(self, class_list, shuffle=False, scale_size=(227, 227)):

        self.shuffle = shuffle
        self.scale_size = scale_size
        self.pointer = 0

        self.read_class_list(class_list)

        if self.shuffle:
            self.shuffle_data()

    def read_class_list(self, class_list):
        """
        浏览文件，提取图片路径和图片标签
        """
        with open(class_list) as f:
            lines = f.readlines()
            self.images = []
            self.labels = []
            for l in lines:
                items = l.split(' ')
                self.images.append(items[0])
                self.labels.append(int(items[1]))
            # 存储数据的总数
            self.data_size = len(self.labels)
            # np.unique():去除数组中的重复数字,并进行排序之后输出。
            category = np.unique(self.labels)
            self.n_classes = len(category)

    def shuffle_data(self):
        """
        随机打乱图片和标签
        """
        images = self.images
        labels = self.labels
        self.images = []
        self.labels = []
        # 创建一个置换索引列表，并根据列表打乱数据
        idx = np.random.permutation(len(labels))
        for i in idx:
            self.images.append(images[i])
            self.labels.append(labels[i])

    def reset_pointer(self):
        """
        reset pointer to begin of the list
        """
        self.pointer = 0

        if self.shuffle:
            self.shuffle_data()

    def next_batch(self, batch_size):
        """
        此函数从路径列表和标签列表中获取下一个n（=batch_size）数据，并将图像加载到内存中
        """
        # 获取下一批图像（路径）和标签
        paths = self.images[self.pointer: self.pointer + batch_size]
        labels = self.labels[self.pointer: self.pointer + batch_size]
        # 更新指针位置
        self.pointer += batch_size
        # 如取图片数据
        images = np.ndarray(
            [batch_size, self.scale_size[0], self.scale_size[1], 3])
        for i in range(len(paths)):
            img = cv2.imread(paths[i])
            img = cv2.resize(img,(self.scale_size[0], self.scale_size[1]))
            img = np.asarray(img, dtype=np.float32)

            images[i] = img
        # 将标签展开为一个one hot形式的编码
        one_hot_labels = np.zeros((batch_size, self.n_classes))
        for i in range(len(labels)):
            one_hot_labels[i][labels[i]] = 1
        # 返回图像和标签的数组
        return images, one_hot_labels
