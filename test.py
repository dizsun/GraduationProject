# coding=UTF-8
import os
from APKManager import APKManager

# import Levenshtein.StringMatcher
# import Levenshtein



# 计算字符串相似度
# str1 = 'abcd'
# str2 = 'cdef'
# sm = Levenshtein.StringMatcher.StringMatcher(seq1=str1, seq2=str2)
# print sm.distance()

apkmanager = APKManager('/Users/sundiz/Desktop/androidapp/wangzherongyao.apk')
mapk = apkmanager.get_apk_obj()
for per in mapk.get_permissions():
    print per
