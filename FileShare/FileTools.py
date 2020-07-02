#! /usr/bin/env python3
# *_* coding: utf-8 *_*
# @File  : FileTools.py
# @Author: Frank1126lin
# @Date  : 2020/7/2

import os
import time


# 获取文件类型
def get_type(path):
    '''
    给定文件地址path,返回文件类型
    :param path: 文件地址
    :return: 文件类型
    '''
    if os.path.isdir(path):
        return 'Dir'
    else:
        return os.path.splitext(path)[-1][1:]


# 获取文件修改时间
def get_cdate(path):
    '''
    给定文件地址（path),返回文件修改时间date
    :param path: 文件或文件夹地址
    :return: 文件最后一次修改时间
    '''
    return time.ctime(os.path.getmtime(path))


# 获取文件或文件夹大小
def get_size(path):
    if os.path.isfile(path):
        return get_file_size(path)
    if os.path.isdir(path):
        return get_dir_size(path)


def get_file_size(filepath):
    size = os.path.getsize(filepath)
    return size_handle(size)

def get_dir_size(dirpath):
    size = 0
    for root, dirs, files in os.walk(dirpath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
    return size_handle(size)


def size_handle(size):
    unit_list = [
        (60, 'EB'),
        (50, 'PB'),
        (40, 'TB'),
        (30, 'GB'),
        (20, 'MB'),
        (10, 'KB'),
        (1, 'B'),
    ]
    if size == 0:
        return "0 B"
    for i in range(len(unit_list)):
        if size >> unit_list[i][0] > 0:
            num = round(size / 2 ** unit_list[i][0], 2)
            unit = unit_list[i][1]
            return str(num)+str(unit)