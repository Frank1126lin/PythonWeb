#! /usr/bin/env python3
# *_* coding: utf-8 *_*
# @File  : fileserver2.py
# @Author: Frank1126lin
# @Date  : 2020/6/30


'''
使用FASTAPI创建文件共享服务
'''

import os
import time
import socket
import platform
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
ROOT = os.getcwd()


app = FastAPI()


# 定义主函数，默认页是根目录URL+文件列表
@app.get('/')
def main():
    return views(ROOT)

# URL 处理
@app.get('/{path}')
def level(path):
    path2 = unquote(path)
    list_path = path2.split(">") # 相对地址列表，如[“home”, "frank", "123"]
    dir_path = get_dir_path(ROOT, list_path) # 获取url对应文件地址
    return views(dir_path, path)


def get_dir_path(root, list_path=None):
    '''
    从url的相对地址转换为路径的文件绝对地址
    '''
    if list_path is None:
        return root
    else:
        path = "/".join(list_path)
        abs_path = ''.join([root, "/", path])
        if platform.system() == "Windows":  # 因为这里os.path.join()不支持列表，所以只能自己写
            abs_path = abs_path.replace("/","\\")
        # print(abs_path)
        return abs_path


def views(dir_path, path=None):
    """
    视图函数，返回相应视图
    """
    # 1. 路径不存在
    if not os.path.exists(dir_path):
        return "dir is not exist."

    # 2. 路径地址是文件
    elif os.path.isfile(dir_path):
        response = FileResponse(dir_path)
        return response
    # 3. 路径地址是文件夹
    else:
        # 拿到字典数据进行展示
        dic = dir_dict(dir_path)
        # 准备前端HTML路径（这里可以用jinja2写））
        headers = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>文件共享服务</title>'
        response = headers + '<h1>Name ---- Size ---- Type ---- Modify Date<h1>'

        for k, v in dic.items():
            if path is None: # 针对根目录
                file_url = k
            else:
                file_url = '>'.join([path,k])
            file_href =  '<a href="' + file_url + '">' + k + '</a>'
            response += '<h2>' + file_href + '----' + v[0] + '----' + v[1] + '----' + v[2] + '<h2>'
        return Response(content=response)


def dir_dict(dir_path):
    """
    给出文件夹绝对地址，以字典形式返回文件夹内相应内容
    """
    if os.path.isdir(dir_path):
        dir_dic = {}
        for file in os.listdir(dir_path):
            file_name = file
            file_path = os.path.join(dir_path, file) # 函数内部使用
            file_size = get_size(file_path)
            file_cdate = get_cdate(file_path)
            file_type = get_type(file_path)
            dir_dic[file_name] = [file_size, file_type, file_cdate]
        return dir_dic




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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001)
