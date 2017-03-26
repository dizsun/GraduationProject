# coding=UTF-8
from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis
from androguard.patch.zipfile import BadZipfile
import os
import threading


def get_all_apk_files(mpath):
    """从给定路径获取该路径下所有apk文件的绝对路径"""
    if mpath[-1] == os.sep:
        mpath = mpath[:-1]
    paths = os.listdir(mpath)
    mlist = []
    for p in paths:
        if os.path.isdir(mpath + os.sep + p):
            mlist += get_all_apk_files(mpath + os.sep + p.decode(encoding='utf8'))
        elif 'readme' not in p.lower():
            mlist.append(mpath + os.sep + p.decode(encoding='utf8'))
    return mlist


class APKManager:
    """获取APk文件对象的工具"""
    def __init__(self, apkfile):
        self.apkfile = apkfile

    def get_androguard_obj(self):
        """获取androguard对象"""
        try:
            a = apk.APK(self.apkfile, False, "r", None, 2)  # 获取APK文件对象
            d = dvm.DalvikVMFormat(a.get_dex())  # 获取DEX文件对象
            x = analysis.VMAnalysis(d)  # 获取分析结果对象
            return a, d, x
        except BadZipfile:
            return None

    def get_apk_obj(self):
        """获取apk对象"""
        try:
            return apk.APK(self.apkfile, False, "r", None, 2)
        except BadZipfile:
            return None
        except RuntimeError:
            print 'RuntimeError:', self.apkfile
            return False
        except IOError:
            print 'IOError:', self.apkfile
            return False

    def get_dvm_obj(self):
        """获取dvm对象"""
        try:
            return dvm.DalvikVMFormat(self.get_apk_obj().get_dex())
        except BadZipfile:
            return None
        except RuntimeError:
            print 'RuntimeError:', self.apkfile
            return False
        except IOError:
            print 'IOError:', self.apkfile
            return False

    @staticmethod
    def is_apk_file(filename):
        """判定是否是可用的apk文件"""
        try:
            apk.APK(filename, False, "r", None, 2)
            return True
        except BadZipfile:
            return False
        except RuntimeError:
            print 'RuntimeError:', filename
            return False
        except IOError:
            print 'IOError:', filename
            return False


def check_apk(apk_paths):
    """检测apk完整性"""
    goodapk = 0
    allapk = 0
    badapks = []
    for apk_path in apk_paths:
        if APKManager.is_apk_file(apk_path):
            goodapk += 1
        else:
            badapks.append(apk_path)
        allapk += 1
    print u'所有apk总数:', allapk, u',损坏文件数:', allapk - goodapk, u',apk完整率:', 100 * (goodapk / float(allapk)), '%'
    return allapk, allapk - goodapk, badapks


if '__main__' == __name__:
    # apkfile2 = r'D:\malwares\android-malware-master\android-malware-master\triada\2fd9f60cf6a1ec8901feba1883d98c13bb385c54c226eb1c34b657e6af8e11aa'
    # apkfile1 = r'D:\malwares\android-malware-master\android-malware-master\triada\README'
    apks_path = r'D:\malwares'
    apk_paths = get_all_apk_files(apks_path)
    threads = [threading.Thread(target=check_apk, args=(apk_paths[0:500],)),
               threading.Thread(target=check_apk, args=(apk_paths[500:1000],)),
               threading.Thread(target=check_apk, args=(apk_paths[1000:1500],)),
               threading.Thread(target=check_apk, args=(apk_paths[1500:2000],)),
               threading.Thread(target=check_apk, args=(apk_paths[2000:2500],)),
               threading.Thread(target=check_apk, args=(apk_paths[2500:3000],)),
               threading.Thread(target=check_apk, args=(apk_paths[3000:3500],)),
               threading.Thread(target=check_apk, args=(apk_paths[3500:4000],)),
               threading.Thread(target=check_apk, args=(apk_paths[4000:4500],)),
               threading.Thread(target=check_apk, args=(apk_paths[4500:5000],)),
               threading.Thread(target=check_apk, args=(apk_paths[5000:5500],)),
               threading.Thread(target=check_apk, args=(apk_paths[5500:],))
               ]
    for t in threads:
        # t.setDaemon(True)
        t.start()
        # t.join()
    print 'all task has completed!'
