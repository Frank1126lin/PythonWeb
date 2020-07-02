#! /usr/bin/env python3
# *_* coding: utf-8 *_*
# @File  : MyIP.py
# @Author: Frank1126lin
# @Date  : 2020/7/2

import socket


# IPV4 for Production
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
