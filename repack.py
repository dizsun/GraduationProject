# coding=UTF-8
import APKManager
import os
import platform

# import ssdeep


# def test_fuzzy_hash():
#     # 模糊hash算法的使用测试,此包还能直接比较两个hash的相似度
#     hash1 = ssdeep.hash("Hello world,this is the test of fuzzy hash,if you have see this sentence,you are in using Ssdeep")
#     hash2 = ssdeep.hash("Hello world,this is the test of fuzzy hash,if you have see this sentence,you are in using ssdeep")
#     cmphash = ssdeep.compare(hash1, hash2)
#     print hash1
#     print hash2
#     print cmphash
#     f1 = '/Users/sundiz/Desktop/new.apk'
#     f2 = '/Users/sundiz/Desktop/test/dist/app-release.apk'
#     apk_manager = APKManager.APKManager()
#     a1 = apk_manager.get_apk_obj(f1)
#     a2 = apk_manager.get_apk_obj(f2)
#     hash1 = ssdeep.hash(a1.get_raw())
#     hash2 = ssdeep.hash(a2.get_raw())
#     cmp_hash = ssdeep.compare(hash1, hash2)
#     print hash1
#     print hash2
#     print cmp_hash
#
#
# def test_singature():
#     # python执行cmd获取apk签名
#     p = os.popen('java -cp /Applications/signapk/wandoujia-tools.jar com.wandoujia.tools.ApkSignatureToolsMain /Users/sundiz/Desktop/app-release.apk')
#     print p.readlines()[0].replace('\n', '')


# def compare_fuzzy_hash(apk_raw_data1, apk_raw_data2):
#     hash1 = ssdeep.hash(apk_raw_data1)
#     hash2 = ssdeep.hash(apk_raw_data2)
#     cmphash = ssdeep.compare(hash1, hash2)
#     return cmphash / 100.0


def compare_signature(apk_file1, apk_file2):
    if 'Windows' in platform.system():
        signaturetool = r'java -cp D:\SignatureTool\wandoujia-tools.jar com.wandoujia.tools.ApkSignatureToolsMain '
    else:
        signaturetool = 'java -cp /Applications/signapk/wandoujia-tools.jar com.wandoujia.tools.ApkSignatureToolsMain '
    p1 = os.popen(signaturetool + apk_file1)
    p2 = os.popen(signaturetool + apk_file2)
    signature1 = p1.readlines()[0].strip().split('=')[1]
    signature2 = p2.readlines()[0].strip().split('=')[1]
    print signature1, signature2
    return signature1 == signature2


# def check_repack(apk_file1, apk_file2):
#     if not compare_signature(apk_file1, apk_file2):
#         return True
#     apk_raw1 = APKManager.APKManager(apk_file1).get_apk_obj().get_raw()
#     apk_raw2 = APKManager.APKManager(apk_file2).get_apk_obj().get_raw()
#     if compare_fuzzy_hash(apk_raw1, apk_raw2) != 1.0:
#         return True
#     else:
#         return False



if __name__ == '__main__':
    # print check_repack('/Users/sundiz/Desktop/app-release.apk', '/Users/sundiz/Desktop/new.apk')
    pass
