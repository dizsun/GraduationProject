# coding=UTF-8
import base64
import MySQLdb
from APKManager import APKManager

# path = r'C:\Users\dizsun\Desktop\app\com.tencent.tmgp.sgame.apk'
# apkmanager = APKManager(path)
# conn = MySQLdb.connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='root',
#     db='test',
# )
# cur = conn.cursor()


# 插入一条数据
# cur.execute("insert into apk_raw_info(apk_md5,apk_sign_md5,apk_name,apk_package_name,apk_methods,apk_permissions,apk_flag) values('123',NULL,NULL,NULL,NULL,NULL,NULL)")
# 插入一条数据
# sqli="insert into apk_raw_info(%s,%s,%s,%s,%s,%s,%s)"
# cur.execute(sqli,('3','Huhu','2 year 1 class','7'))
# 一次插入多条记录
# sqli = "insert into student values(%s,%s,%s,%s)"
# cur.executemany(sqli,[
#     ('3','Tom','1 year 1 class','6'),
#     ('3','Jack','2 year 1 class','7'),
#     ('3','Yaheng','2 year 2 class','7'),
#     ])

# 修改查询条件的数据
# ps = ''
# for p in apkmanager.get_apk_obj().get_permissions():
#     if ps:
#         ps += '#'
#     ps += p
# ms = ''
# for m in apkmanager.get_dvm_obj().get_methods():
#     if ms:
#         ms += '#'
#     ms += str(m)
# apkmd5 = '8ecc4a740c016b413d9cccc784fa9f3b'
# # sqi = "update apk_raw_info set apk_methods='%s',apk_permissions='%s' where apk_md5 = '%s'" % (base64.b64encode(ms), base64.b64encode(ps), apkmd5)
# sqi = "update apk_raw_info set apk_name='%s' where apk_md5='%s'" % (path, apkmd5)
# cur.execute(sqi)

# 删除查询条件的数据
# cur.execute("delete from student where age='9'")

# 查询数据
# 获得表中有多少条数据
# aa = cur.execute("select * from apk_raw_info")
# print aa
#
# # 打印表中的多少数据
# ms = []
# ps = []
# info = cur.fetchmany(aa)
# for ii in info:
#     print ii[0], ii[2]
# if ii[4]:
#     ms = base64.b64decode(ii[4]).split('#')
#     ps = base64.b64decode(ii[5]).split('#')

# print len(ps), len(ms)
# print ps[0], ms[0], ps[1], ms[1]
# cur.close()
# conn.commit()
# conn.close()

f = open('regression_test')
l = f.readline()
f.close()
f = open('regression_test', 'w')
f.write(l.replace('gate', '\ngate'))
f.close()
