# coding=UTF-8
import os
from androguard.core.bytecodes import apk, dvm
from androguard.core.analysis import analysis

path = '/Users/sundiz/Desktop/androidmalware'


def get_all_apk_files(mpath):
    paths = os.listdir(mpath)
    list = []
    for p in paths:
        if os.path.isdir(mpath + '/' + p):
            list += get_all_apk_files(mpath + '/' + p)
        elif p[-4:] == '.apk':
            list.append(mpath + '/' + p)
    return list


dvm.DalvikVMFormat(apk.APK('/Users/sundiz/Desktop/new.apk', False, "r", None, 2))
