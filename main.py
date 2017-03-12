# coding=UTF-8
from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis
import os
import re


def get_androguard_obj(apkfile):
    """
    获取apk路径下的apk文件并解析为apk对象
    :param apkfile:
    :return:
    """
    a = apk.APK(apkfile, False, "r", None, 2)  # 获取APK文件对象
    d = dvm.DalvikVMFormat(a.get_dex())  # 获取DEX文件对象
    x = analysis.VMAnalysis(d)  # 获取分析结果对象
    return a, d, x


def get_apkfiles(path):
    """
    从文件夹目录得到所有apk的绝对路径
    :param path:
    :return:
    """
    return [path + file_name for file_name in os.listdir(path)]


def check_apk_mal_methods(dvm_obj, mal_methods):
    """
    获取应用的恶意API调用次数
    :param androguard_obj: androguard对象
    :param mal_methods: 已知恶意API库
    :return: 调用次数
    """
    i = 0
    apk_methods = dvm_obj.get_methods()
    for apk_method in apk_methods:
        for mal_method in mal_methods:
            if mal_method in str(apk_method):
                i += 1
    return i


def get_mal_methods(path):
    """
    获取恶意API库
    :param path: 恶意API库文件路径
    :return:
    """
    mal_methods_file = open(path)
    mal_methods = mal_methods_file.readlines()
    mal_methods_file.close()
    return mal_methods


apks_path = 'softwares/'
apk_path = 'WeatherForecast.apk'
mal_methods_path = 'sensitive_methods.txt'

if __name__ == '__main__':
    # apkfiles = get_apkfiles(apks_path)
    # mal_methods = get_mal_methods(mal_methods_path)
    # for apkfile in apkfiles:
    #     print apkfile
    #     androguard_obj = get_androguard_obj(apkfile)
    #     mal_API_count = check_apk_mal_methods(androguard_obj, mal_methods)
    #     print apkfile + '::' + mal_API_count
    a1, d1, x1 = get_androguard_obj(apk_path)
    # mal_methods_file = open(mal_methods_path)
    # mal_methods = mal_methods_file.readlines()
    # 获取应用调用的所有方法
    # apk_methods = d1.get_methods()
    # for apk_method in apk_methods:
    #     for mal_method in mal_methods:
    #         if mal_method in str(apk_method):
    #             print apk_method
    # for c in d1.get_classes():
    #     print c.name
    # for apk_method in apk_methods:
    #     print apk_method

    # 获取应用的所有权限许可
    # permissions = a1.get_permissions()
    # for permission in permissions:
    #     print permission
    # print len(permissions)


    public_pkgs = ('Lorg/apache', 'Landroid', 'Ljava', 'Landroid/support', 'Lnet', 'Lnu/',
                   'Lorg/codehaus/groovy/', 'Lgroovy', 'Ljunit', 'Lorg', '[')
    # pkgs = x1.get_tainted_packages()
    # for pkg in pkgs.get_packages():
    #     is_public = False
    #     for public_pkg in public_pkgs:
    #         if public_pkg in pkg[1]:
    #             is_public = True
    #     if not is_public:
    #         # print pkg[1]
    #         print d1.get_class(re.sub(';', '', pkg[1]))

    class_list = d1.get_classes()
    class_item = class_list[10]
    print class_item.get_name()
