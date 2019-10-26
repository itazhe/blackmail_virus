import string
import os
import time
from multiprocessing import Process, Queue
import sys
from Crypto.Cipher import AES
# import queue

mp3_file_list = Queue()
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

def decrypt(key, data):
    key_bytes = key.encode()
    key_bytes = key_bytes + (16 - len(key_bytes)) * b'\0'
    iv = bytes(reversed(key_bytes))
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    # 解密
    decrypt_bytes = cipher.decrypt(data)
    # 去除填充内容
    result = unpadding(decrypt_bytes)
    return result


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
                if f[-5:].lower() == ".azhe":
                    dest_file_path = os.path.join(root, f)
                    print(dest_file_path)
                    with open(dest_file_path, "rb") as f:
                        data = decrypt(key, f.read())
                        if dest_file_path[-5:] == ".azhe":
                            dst_file_path = dest_file_path[:-5]
                        else:
                            dst_file_path = dest_file_path + ".jd"
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
