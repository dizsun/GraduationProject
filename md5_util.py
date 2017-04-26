# coding:UTF-8
# python check file MD5
# python version 2.6

import hashlib
import os, sys
import APKManager


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


def get_signature_and_md5(filepath):
    try:
        p = os.popen(r'java -cp "C:\Program Files\ApkSignatureToolJar\wandoujia-tools.jar" com.wandoujia.tools.ApkSignatureToolsMain ' + filepath)
        s = p.readlines()
        if s:
            return s[0].strip().split('=')[1], s[1].strip().split('=')[1]
        else:
            print "get_signature_and_md5 error"
            return None
    except Exception:
        return None


if __name__ == "__main__":
    path = r'D:\apk\LINE.apk'
    # print GetFileMd5(path)
    # print APKManager(path).get_apk_obj().get_package()
    # malwares_path = r"D:\malwares"
    # for p in APKManager.get_all_apk_files(malwares_path):
    #     print GetFileMd5(p)

    print get_signature_and_md5(path)
