#! /usr/bin/env python3
# *_* coding: utf-8 *_*
# @File  : main.py
# @Author: Frank1126lin
# @Date  : 2020/7/2

import os
import platform
from MyIP import get_host_ip
from FileTools import get_type, get_cdate, get_size
from urllib.parse import unquote
from starlette.responses import FileResponse,Response
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


ROOT = os.path.abspath(os.path.dirname(os.getcwd()))

app = FastAPI()

templates = Jinja2Templates(directory="./statics/templates")


@app.get("/")
async def index(request: Request):
    dir_di = dir_dict(ROOT)
    if dir_di is None:
        return "None dir."
    for k, v in dir_di.items():
        v.append(k)
    return templates.TemplateResponse("index.html", {"request": request, "dir_di": dir_di})


@app.get("/favicon.ico")
async def get_ico(request: Request):
    return FileResponse("share.png")

@app.get('/{path}')
async def main(request: Request, path:str):
    path2 = unquote(path)
    list_path = path2.split(">") # 获取文件路径的列表，如[‘home’, 'frank', '123']
    if "favicon.ico" in list_path:
        list_path.remove("favicon.ico")

    if list_path is None:
        path = ROOT
    else:
        path = ''.join([ROOT, "/", "/".join(list_path)])
        if platform.system() == "Windows":
            path = path.replace("/", "\\")


    if not os.path.exists(path):

        return "Path is not exist."

    elif os.path.isfile(path):

        return FileResponse(path)

    elif os.path.isdir(path):
        dir_di = dir_dict(path)
        for k, v in dir_di.items():
            f_url = '>'.join(list_path+[k])
            v.append(f_url)
        return templates.TemplateResponse("index.html", {"request":request, "dir_di": dir_di})


def dir_dict(dir_path:str):
    """
    输入：文件夹地址
    返回：文件夹目录，字典形式
    """
    if os.path.isdir(dir_path):
        dir_dict = {}
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)  # 函数内部使用
            file_name = file
            file_size = get_size(file_path)
            file_cdate = get_cdate(file_path)
            file_type = get_type(file_path)
            dir_dict[file_name] = [file_size, file_type, file_cdate]
        return dir_dict
    else:
        pass

if __name__ == '__main__':
    import uvicorn
    port = 8001
    print(ROOT)
    print("Click Here: http://{0}:{1}".format(get_host_ip(), port))
    uvicorn.run(app, host='0.0.0.0', port=port)
