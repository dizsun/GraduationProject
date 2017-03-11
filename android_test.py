# coding=UTF-8
from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis


def get_androguard_obj(apkfile):
    a = apk.APK(apkfile, False, "r", None, 2)  # 获取APK文件对象
    d = dvm.DalvikVMFormat(a.get_dex())  # 获取DEX文件对象
    x = analysis.VMAnalysis(d)  # 获取分析结果对象
    return a, d, x


class MalPermissonsCombinations:
    def __init__(self):
        self.permissions = []
        self.convince = 0.0

    def __str__(self):
        return 'permissions:' + str(self.permissions) + ',convince:' + str(self.convince)


def check_mal_per_com(apk_obj, mal_permissions_combinations_file):
    apk_permissions = apk_obj.get_permissions()
    mal_per_comb_file = open(mal_permissions_combinations_file)
    mal_per_comb_objs = []
    mal_per_comb_obj = MalPermissonsCombinations()
    for item in mal_per_comb_file.readlines():
        if '0' not in item:
            mal_per_comb_obj.permissions.append(item.replace('\n', ''))
        else:
            mal_per_comb_obj.convince = float(item)
            mal_per_comb_objs.append(mal_per_comb_obj)
            mal_per_comb_obj = MalPermissonsCombinations()
    mal_per_comb_file.close()
    apk_mal_per_com_objs = []
    for mal_per_comb_obj in mal_per_comb_objs:
        count = 0
        for mal_per in mal_per_comb_obj.permissions:
            if mal_per in apk_permissions:
                count += 1
        if count == len(mal_per_comb_obj.permissions):
            apk_mal_per_com_objs.append(mal_per_comb_obj)
    for apk_mal_per_com_obj in apk_mal_per_com_objs:
        print apk_mal_per_com_obj


sp = r'C:\Users\dizsun\AndroidStudioProjects\MyApplication\app\app-release.apk'
mal_permissions_combinations_file = 'mal_permissions_combinations.txt'
if __name__ == '__main__':
    a1, d1, x1 = get_androguard_obj(sp)
    # x = ao[2]
    # pkgs = x.get_tainted_packages()
    # for pkg in pkgs.get_packages():
    #     print pkg
    #     print '\n'
    # 获取应用调用的所有方法
    for method in d1.get_methods():
        if 'sayHello' in str(method):
            print method
    # 获取应用的恶意相关权限许可
    # check_mal_per_com(a1, mal_permissions_combinations_file)
