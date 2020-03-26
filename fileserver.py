#! /usr/bin/env python3
# *_* coding: utf-8 *_*
# @File  : fileserver.py
# @Author: Frank1126lin
# @Date  : 2020/2/19


'''
使用FASTAPI创建文件共享服务To Be Perfect
'''

import os
import time
import socket
from urllib.parse import unquote
from fastapi import FastAPI
from starlette.responses import FileResponse, Response


# IPV4 for Production
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
BASEURL = 'http://{0}:{1}'.format(get_host_ip(), 8001)
print(BASEURL)

# 文件绝对路径
ROOTDIR = os.getcwd()


app = FastAPI()


# 定义主函数，默认页是根目录URL+文件列表
@app.get('/')
def main():
    return get_record(ROOTDIR)

# 处理url TODO 多级目录如何完成
@app.get('/{path}')
def level1(path):
    path = unquote(path)
    return get_record(ROOTDIR, path)

@app.get('/{path}/{path2}')
def level2(path, path2):
    path = unquote(path)
    path2 = unquote(path2)
    middle_path = os.path.join(ROOTDIR, path)
    return get_record(middle_path, path2)

@app.get('/{path}/{path2}/{path3}')
def level3(path, path2, path3):
    path = unquote(path)
    path2 = unquote(path2)
    path3 = unquote(path3)
    middle_path = os.path.join(ROOTDIR, path, path2)
    return get_record(middle_path, path3)

@app.get('/{path}/{path2}/{path3}/{path4}')
def level3(path, path2, path3, path4):
    path = unquote(path)
    path2 = unquote(path2)
    path3 = unquote(path3)
    path4 = unquote(path4)
    middle_path = os.path.join(ROOTDIR, path, path2, path3)
    return get_record(middle_path, path4)

#获取文件记录
def get_record(root, path=''):
    '''
    处理系统文件，并返回文件/文件夹清单
    参数：
    root：上层地址如home/frank/
    path,文件或文件夹的地址名 如web
    返回：消息/文件清单/文件/None
    '''
    abs_path = os.path.join(root, path)
    if not os.path.exists(abs_path):
        return 'dir is not Exist'
    if os.path.isdir(abs_path):
        headers = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>文件共享服务</title>'
        response = headers + '<h1>Name ---- Size ---- Type ---- Modify Date<h1>'
        for name in sorted(os.listdir(abs_path)):
            file_name = name
            file_path = '/'.join([path, name])
            file_size = get_size(os.path.join(abs_path, name))
            # print(file_size)
            file_size = str(file_size[0]) + file_size[1]
            file_type = get_type(os.path.join(abs_path, name))
            file_cdate = get_cdate(os.path.join(abs_path, name))

            file_name = '<a href="' + file_path + '">' + file_name + '</a>'
            response += '<h2>' + file_name + '----' + file_size + '----' + file_type + '----' + file_cdate + '<h2>'
        return Response(content=response)
    if os.path.isfile(abs_path):
        response = FileResponse(abs_path)
        return response
    else:
        return


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
        return [0, 'B']
    for i in range(len(unit_list)):
        if size >> unit_list[i][0] > 0:
            return [round(size / 2 ** unit_list[i][0], 2), unit_list[i][1]]

