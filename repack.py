# coding=UTF-8
import APKManager
import os
import ssdeep

# 模糊hash算法的使用测试,此包还能直接比较两个hash的相似度
# hash1 = ssdeep.hash("Hello world,this is the test of fuzzy hash,if you have see this sentence,you are in using Ssdeep")
# hash2=ssdeep.hash("Hello world,this is the test of fuzzy hash,if you have see this sentence,you are in using ssdeep")
# cmphash=ssdeep.compare(hash1,hash2)
# print hash1
# print hash2
# print cmphash

f1 = '/Users/sundiz/Desktop/new.apk'
f2 = '/Users/sundiz/Desktop/test/dist/app-release.apk'
apk_manager = APKManager.APKManager()
a1 = apk_manager.get_apk_obj(f1)
a2 = apk_manager.get_apk_obj(f2)
hash1 = ssdeep.hash(a1.get_raw())
hash2 = ssdeep.hash(a2.get_raw())
cmp_hash = ssdeep.compare(hash1, hash2)
print hash1
print hash2
print cmp_hash

# python执行cmd获取apk签名
p = os.popen('java -cp /Applications/signapk/wandoujia-tools.jar com.wandoujia.tools.ApkSignatureToolsMain /Users/sundiz/Desktop/new_uc.apk')
print p.readlines()[0].replace('\n', '')
