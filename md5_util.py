# coding:UTF-8
# python check file MD5
# python version 2.6

import hashlib
import os, sys
from APKManager import APKManager


# 简单的测试一个字符串的MD5值
def GetStrMd5(src):
    m0 = hashlib.md5()
    m0.update(src)
    print m0.hexdigest()
    pass


# 大文件的MD5值
def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def CalcSha1(filepath):
    with open(filepath, 'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        print(hash)
        return hash


def CalcMD5(filepath):
    with open(filepath, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        print(hash)
        return hash


if __name__ == "__main__":
    path = r'C:\Users\dizsun\Desktop\app\com.tencent.tmgp.sgame.apk'
    # print GetFileMd5(path),len(GetFileMd5(path))
    # print APKManager(path).get_apk_obj().get_package()
    sys.stdout.write('hello')
    sys.stdout.write('%\r')
    sys.stdout.write('ghdfgud')

