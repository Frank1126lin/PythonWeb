#! /usr/bin/env python3
# *_* coding: utf-8 *_*
# @File  : fileserver.py
# @Author: Frank1126lin
# @Date  : 2020/2/19
'''
使用FASTAPI创建文件共享服务TBP
'''

import os
import socket
from fastapi import FastAPI
from starlette.responses import FileResponse


# Local for dev
BASEURL = '0.0.0.0'

# IPV4 for Production
# def get_host_ip():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         s.connect(('8.8.8.8', 80))
#         ip = s.getsockname()[0]
#     finally:
#         s.close()
#     return ip
# BASEURL = '{0}:{1}'.format(get_host_ip(), 8001)
# print(BASEURL)

# 文件绝对路径
ROOTDIR = os.getcwd()

app = FastAPI()


# 定义主函数，默认页是根目录URL+文件列表 TODO 需要将列表转化为链接
@app.get('/')
def main():
    path_list = []
    for name in os.listdir(ROOTDIR):
        path_list.append('/'.join([BASEURL, name]))
    return path_list



# 处理url
@app.get('/{path}')
def level1(path):
    file_path = path
    return get_record(ROOTDIR, file_path)

@app.get('/{path}/{path2}')
def level2(path, path2):
    file_path = '/'.join([path, path2])
    # print(file_path)
    return get_record(ROOTDIR, file_path)

@app.get('/{path}/{path2}/{path3}')
def level3(path, path2, path3):
    file_path = '/'.join([path, path2, path3])
    return get_record(ROOTDIR, file_path)

def get_record(root, path):
    '''
    处理系统文件，并返回文件/文件夹清单
    参数：
    root, 绝对地址
    path,文件或文件夹的相对地址
    返回：消息/文件清单/文件/None
    '''
    file_path = os.path.join(root, path)
    if not os.path.exists(file_path):
        return {'msg':'地址不存在！'}
    if os.path.isdir(file_path):
        url_path_list = []
        for name in os.listdir(file_path):
            url_path_list.append('/'.join([BASEURL, path, name]))
        return url_path_list
    if os.path.isfile(file_path):
        response = FileResponse(file_path)
        return response
    else:
        return
