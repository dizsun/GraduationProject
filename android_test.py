# coding=UTF-8
from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis
import os


def get_androguard_obj(apkfile):
    a = apk.APK(apkfile, False, "r", None, 2)  # 获取APK文件对象
    d = dvm.DalvikVMFormat(a.get_dex())  # 获取DEX文件对象
    x = analysis.VMAnalysis(d)  # 获取分析结果对象
    return a, d, x


def get_apk_obj(apkfile):
    try:
        return apk.APK(apkfile, False, "r", None, 2)
    except Exception:
        return None


def get_dvm_obj(apkfile):
    try:
        return dvm.DalvikVMFormat(get_apk_obj(apkfile))
    except Exception:
        return None


def get_all_permissions(permissions_file):
    """
    从文件中获取android所有的权限,然后编号返回一个以权限名为key,以编号为value的字典
    """
    f = open(permissions_file)
    per_dic = {}
    count = 1
    for line in f.readlines():
        per_dic[line.replace('\n', '')] = count
        count += 1
    f.close()
    return per_dic


class SensitivePermissionsCombinations:
    def __init__(self):
        self.permissions = []
        self.convince = 0.0

    def __str__(self):
        return 'permissions:' + str(self.permissions) + ',convince:' + str(self.convince)


def check_mal_per_com(apk_obj, sensitive_permissions_combinations_file):
    """
    检查apk文件的权限是否有敏感权限组合
    """
    if not apk_obj:
        return None
    apk_permissions = apk_obj.get_permissions()
    sensitive_per_comb_file = open(sensitive_permissions_combinations_file)
    sensitive_per_comb_objs = []
    sensitive_per_comb_obj = SensitivePermissionsCombinations()
    for item in sensitive_per_comb_file.readlines():
        if '0' not in item:
            sensitive_per_comb_obj.permissions.append(item.replace('\n', ''))
        else:
            sensitive_per_comb_obj.convince = float(item)
            sensitive_per_comb_objs.append(sensitive_per_comb_obj)
            sensitive_per_comb_obj = SensitivePermissionsCombinations()
    sensitive_per_comb_file.close()
    apk_sensitive_per_comb_objs = []
    for sensitive_per_comb_obj in sensitive_per_comb_objs:
        count = 0
        for mal_per in sensitive_per_comb_obj.permissions:
            if mal_per in apk_permissions:
                count += 1
        if count == len(sensitive_per_comb_obj.permissions):
            apk_sensitive_per_comb_objs.append(sensitive_per_comb_obj)
    return apk_sensitive_per_comb_objs


def check_apk_sensitive_methods(dvm_obj, mal_methods):
    """
    获取应用的恶意API调用次数
    :param androguard_obj: androguard对象
    :param mal_methods: 已知恶意API库
    :return: 调用次数
    """
    if not dvm_obj:
        return None
    i = 0
    apk_methods = dvm_obj.get_methods()
    for apk_method in apk_methods:
        for mal_method in mal_methods:
            if mal_method in str(apk_method):
                i += 1
    return i


def check_jaccard_coefficent(apk_obj1, apk_obj2):
    """
    获取两个apk文件的Jaccard相似系数
    """
    list1 = []
    list2 = []
    for per in apk_obj1.get_permissions():
        list1.append(per)
    for per in apk_obj2.get_permissions():
        list2.append(per)
    if len(set(list1 + list2)) != 0:
        jaccard = len(set(list1).intersection(set(list2))) / (len(set(list1 + list2)) + 0.0)
    return jaccard


def get_all_apk_files(mpath):
    paths = os.listdir(mpath)
    list = []
    for p in paths:
        if os.path.isdir(mpath + '/' + p):
            list += get_all_apk_files(mpath + '/' + p)
        elif p[-4:] == '.apk':
            list.append(mpath + '/' + p)
    return list


# sp = r'C:\Users\dizsun\AndroidStudioProjects\MyApplication\app\app-release.apk'
sp = '/Users/sundiz/Documents/WorkPlaces/AndroidStudio/MyApplication/app/app-release.apk'
apk_file1 = '/Users/sundiz/Desktop/weixin.apk'
apk_file2 = '/Users/sundiz/Desktop/new.apk'
sensitive_permissions_combinations_file = 'sensitive_permissions_combinations.txt'  #敏感权限组合文件路径
all_permissions_file = 'permissions.txt'    #所有权限文件
apks_path = '/Users/sundiz/Desktop/androidmalware'  #恶意软件集合路径
sensitive_methods_path = 'pretty_sensitive_methods.txt' #敏感API文件路径
if __name__ == '__main__':
    # a1, d1, x1 = get_androguard_obj(sp)
    # a2, d2, x2 = get_androguard_obj(apk_file2)
    # jaccard = check_jaccard_coefficent(a1, a2)
    # print jaccard
    # apk_sensitive_per_com_objs = check_mal_per_com(a1, sensitive_permissions_combinations_file)
    # for apk_sensitive_per_com_obj in apk_sensitive_per_com_objs:
    #     print apk_sensitive_per_com_obj
    sen_per_com_result = {}  # 敏感权限组合检查结果
    sen_met_result = {}  # 敏感API检查结果
    apks = get_all_apk_files(apks_path)  # 所有apk的路径
    for apkfile in apks:
        a = get_apk_obj(apkfile)
        d = get_dvm_obj(apkfile)
        coms = check_mal_per_com(a, sensitive_permissions_combinations_file)
        sen_per_com_result[apkfile] = len(coms)
        mets = check_apk_sensitive_methods(d, sensitive_methods_path)
        sen_met_result[apkfile] = mets
    count1 = 0  # 有敏感权限组合的apk数
    count2 = 0  # 有敏感API的apk数
    count3 = 0  # 两者都有的apk数
    has2attr_list = []  # 两者都有的apk
    for apkfile in sen_per_com_result:
        print apkfile, sen_per_com_result[apkfile], sen_met_result[apkfile]
        has2attr = 0
        if sen_per_com_result[apkfile] and sen_per_com_result[apkfile] != 0:
            count1 += 1
            has2attr += 1
        if sen_met_result[apkfile] and sen_met_result[apkfile] != 0:
            count2 += 1
            has2attr += 1
        if has2attr == 2:
            has2attr_list.append(apkfile)
            count3 += 1
    print '敏感权限组合查处率:', count1 / (len(apks) + 0.0), '敏感API查处率:', count2 / (len(apks) + 0.0), '两项都有查处率:', count3 / (len(apks) + 0.0)

