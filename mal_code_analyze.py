# coding=UTF-8
import sys
import APKManager
import re

reload(sys)
sys.setdefaultencoding("utf-8")


def check_apk_mal_methods(dvm_obj, mal_methods):
    """
    获取应用的恶意API调用次数
    :param dvm_obj: dvm对象
    :param mal_methods: 已知恶意API库
    :return: 调用次数
    """
    i = 0
    apk_methods = dvm_obj.get_methods()
    for apk_method in apk_methods:
        if apk_method in mal_methods:
            i += 1
    return i


def get_mal_methods():
    """
    获取恶意API库
    """
    path = 'sensitive_methods.txt'
    mal_methods_file = open(path)
    mal_methods = [m.strip() for m in mal_methods_file.readlines()]
    mal_methods_file.close()
    return mal_methods


def check_code(path, patterns):
    strings = APKManager.APKManager(path).get_dvm_obj().get_strings()
    for string in strings:
        for pattern in patterns:
            if pattern.search(string):
                return True
    return False


def check_sensitive_code(path):
    regexs = [r'^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}',
              r'^(?:http|ftp)s?://',
              r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
              r'localhost|'
              r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
              r'(?::\d+)?',
              r'(?:/?|[/?]\S+)$']
    patterns = []
    for regex in regexs:
        patterns.append(re.compile(regex, re.IGNORECASE))
    if isinstance(path, str):
        return check_code(path, patterns)
    else:
        result = []
        for p in path:
            result.append(check_code(p, patterns))
        return result


if __name__ == '__main__':
    print check_sensitive_code('/Users/sundiz/Desktop/app-release.apk')
