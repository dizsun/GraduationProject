# coding=UTF-8
from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis
import os
import platform


def platform_slash():
    if "Windows" in platform.platform():
        return '\\'
    else:
        return '/'

def get_all_apk_files(mpath):
    if mpath[-1] == platform_slash():
        mpath = mpath[:-1]
    paths = os.listdir(mpath)
    list = []
    for p in paths:
        if os.path.isdir(mpath + platform_slash() + p):
            list += get_all_apk_files(mpath + platform_slash() + p.decode(encoding='utf8'))
        elif p[-4:] == '.apk':
            list.append(mpath + platform_slash() + p.decode(encoding='utf8'))
    return list


class APKManager:
    def __init__(self):
        pass

    def get_androguard_obj(self, apkfile):
        a = apk.APK(apkfile, False, "r", None, 2)  # 获取APK文件对象
        d = dvm.DalvikVMFormat(a.get_dex())  # 获取DEX文件对象
        x = analysis.VMAnalysis(d)  # 获取分析结果对象
        return a, d, x

    def get_apk_obj(self, apkfile):
        try:
            return apk.APK(apkfile, False, "r", None, 2)
        except Exception:
            return None

    def get_dvm_obj(self, apkfile):
        try:
            return dvm.DalvikVMFormat(self.get_apk_obj(apkfile))
        except Exception:
            return None
