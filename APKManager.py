# coding=UTF-8
from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis
from androguard.patch.zipfile import BadZipfile
import os
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def get_all_apk_files(mpath, encoding='utf8'):
    """从给定路径获取该路径下所有apk文件的绝对路径"""
    if mpath[-1] == os.sep:
        mpath = mpath[:-1]
    paths = os.listdir(mpath)
    mlist = []
    for p in paths:
        if os.path.isdir(mpath + os.sep + p):
            mlist += get_all_apk_files(mpath + os.sep + p.decode(encoding=encoding))
        elif 'readme' not in p.lower():
            mlist.append(mpath + os.sep + p.decode(encoding=encoding))
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


class APP:
    def __init__(self):
        self.apk_md5 = ""
        self.apk_sign_md5 = ""
        self.apk_name = ""
        self.apk_package_name = ""
        self.apk_methods = []
        self.apk_permissions = []
        self.apk_flag = ""

    def __str__(self):
        return 'apk_md5:' + self.apk_md5 + '\napk_sign_md5:' + self.apk_sign_md5 + '\napk_name:' + self.apk_name + '\napk_flag:' + str(self.apk_flag)


def check_apk(apk_paths):
    """检测apk完整性"""
    goodapk = 0
    allapk = 0
    badapks = []
    total = len(apk_paths) + 0.0
    for apk_path in apk_paths:
        if APKManager.is_apk_file(apk_path):
            try:
                m = APKManager(apk_path).get_dvm_obj().get_methods()
                p = APKManager(apk_path).get_apk_obj().get_permissions()
                del p
                del m
                goodapk += 1
            except Exception:
                badapks.append(apk_path)
        else:
            badapks.append(apk_path)
        allapk += 1
        print "finished:" + str((allapk / total) * 100) + "%" + u"||损坏文件数:" + str(len(badapks))
    print u'所有apk总数:', allapk, u',损坏文件数:', allapk - goodapk, u',apk完整率:', 100 * (goodapk / float(allapk)), '%'
    return allapk, allapk - goodapk, badapks


def get_posix():
    pers = set()
    for line in open('mpermissions.txt'):
        pers.add(os.path.splitext(line.strip())[1].replace('.', ''))
    f = open('mpers.txt', 'w')
    for per in pers:
        f.write(per + '\n')
    f.close()


if '__main__' == __name__:
    # apkfile2 = r'D:\malwares\android-malware-master\android-malware-master\triada\2fd9f60cf6a1ec8901feba1883d98c13bb385c54c226eb1c34b657e6af8e11aa'
    apkfile1 = r'D:\malwares\android-malware-master\Android\Android\1ca231169ab226ceab0f5c71450097df.apk'
    apks_path = r'D:\malwares'
    offical_apk_path = r"D:\apk"
    apk_paths = get_all_apk_files(offical_apk_path, 'gbk')
    # result = check_apk(apk_paths)
    # f = open('badfile.txt', 'w')
    # for p in result[2]:
    #     f.write(p + '\n')
    # f.close()

    for apk_path in apk_paths:
        print apk_path


