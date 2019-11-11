# -*- encoding: utf-8 -*-
# Software: PyCharm
# Time    : 2019/9/13 
# Author  : Wang
# File    : cityscapes.py

"""准备 cityscapes path_pairs"""

from __future__ import absolute_import

import os
from utils.base import BaseDataSet


class CityScapes(BaseDataSet):
    """prepare cityscapes path_pairs"""

    BASE_DIR = 'cityscapes'
    NUM_CLASS = 19

    def __init__(self, root='./dataset', split='train', **kwargs):
        super(CityScapes, self).__init__(root, split, **kwargs)
        if os.sep == '\\':  # windows
            root = root.replace('/', '\\')

        root = os.path.join(root, self.BASE_DIR)
        assert os.path.exists(root), "please download cityscapes data_set, put in dataset(dir),or check root"
        self.image_path, self.label_path = self._get_cityscapes_pairs(root, split)
        assert len(self.image_path) == len(self.label_path), "please check image_length = label_length"
        self.print_param()  # 用于核对当前数据集的信息

    def print_param(self):  # 用于核对当前数据集的信息
        print('INFO: dataset_root: {}, split: {}, '
              'base_size: {}, crop_size: {}, scale: {}, '
              'image_length: {}, label_length: {}'.format(self.root, self.split, self.base_size,
                                                          self.crop_size, self.scale, len(self.image_path),
                                                          len(self.label_path)))

    @staticmethod
    def _get_cityscapes_pairs(root, split):

        def get_pairs(root, file_image, file_label):
            file_image = os.path.join(root, file_image)
            file_label = os.path.join(root, file_label)
            with open(file_image, 'r') as f:
                file_list_image = f.read().split()
            with open(file_label, 'r') as f:
                file_list_label = f.read().split()
            if os.sep == '\\':  # for windows
                image_path = [os.path.join(root, x.replace('/', '\\')) for x in file_list_image]
                label_path = [os.path.join(root, x.replace('/', '\\')) for x in file_list_label]
            else:
                image_path = [os.path.join(root, x) for x in file_list_image]
                label_path = [os.path.join(root, x) for x in file_list_label]
            return image_path, label_path

        if split == 'train':
            image_path, label_path = get_pairs(root, 'trainImages.txt', 'trainLabels.txt')
        elif split == 'val':
            image_path, label_path = get_pairs(root, 'valImages.txt', 'valLabels.txt')
        elif split == 'test':
            image_path, label_path = get_pairs(root, 'testImages.txt', 'testLabels.txt')  # 返回文件路径，test_label并不存在
        else:  # 'train_val'
            image_path1, label_path1 = get_pairs(root, 'trainImages.txt', 'trainLabels.txt')
            image_path2, label_path2 = get_pairs(root, 'valImages.txt', 'valLabels.txt')
            image_path, label_path = image_path1+image_path2, label_path1+label_path2
        return image_path, label_path

    def get_path_pairs(self):
        return self.image_path, self.label_path


if __name__ == '__main__':
    CityScapes(split='train_val', base_size=520, crop_size=480, scale=True)
