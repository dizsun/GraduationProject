# coding=UTF-8
import base64
import MySQLdb
import APKManager
import sys, re
from md5_util import GetFileMd5, get_signature_and_md5
from APKManager import APP

reload(sys)
sys.setdefaultencoding("utf-8")


class SQLUtil:
    def __init__(self):
        pass

    @staticmethod
    def execute(sqli):
        """执行sql语句,若是有结果则返回执行结果,若执行出现错误则返回None"""
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='test',
        )
        cur = conn.cursor()
        try:
            result = cur.execute(sqli)
            cur.close()
            conn.commit()
            conn.close()
            return result
        except Exception, e:
            print u"执行sql时出现错误:", e.message
            return None

    def is_duplicate(self, apk_md5):
        """检测数据库中是否有重复的apk,若有则返回True,否则返回False,若查询错误也返回False"""
        if not apk_md5:
            return
        sqli = "select apk_md5 from apk_raw_info where apk_md5='" + str(apk_md5) + "'"
        duplicate_count = self.execute(sqli)
        if duplicate_count and duplicate_count > 0:
            return True
        else:
            return False

    def is_duplicate_apk_sign_md5(self, apk_sign_md5, apk_md5):
        """检测数据库中是否有重复的apk,若有则返回True,否则返回False,若查询错误也返回False"""
        if not apk_sign_md5:
            return
        sqli = "select apk_md5 from apk_raw_info where apk_sign_md5='" + str(apk_sign_md5) + "' and apk_md5='" + str(apk_md5) + "'"
        duplicate_count = self.execute(sqli)
        if duplicate_count and duplicate_count > 0:
            return True
        else:
            return False

    def insert_apk_raw_info(self, apk_md5, apk_sign_md5=None, apk_name=None, apk_package_name=None, apk_methods=None, apk_permissions=None, apk_flag=None):
        """插入数据,若插入成功返回True,否则返回False"""
        if not apk_md5:
            return False
        if self.is_duplicate(apk_md5):
            return False
        values = "'" + str(apk_md5) + "'"
        if apk_sign_md5:
            values += ",'" + str(apk_sign_md5) + "'"
        else:
            values += ",NULL"
        if apk_name:
            apk_name = base64.b64encode(apk_name)
            values += ",'" + str(apk_name) + "'"
        else:
            values += ",NULL"
        if apk_package_name:
            values += ",'" + str(apk_package_name) + "'"
        else:
            values += ",NULL"
        if apk_methods:
            tempstr = ""
            for apk_method in apk_methods:
                if tempstr:
                    tempstr += '#'
                tempstr += str(apk_method)
            apk_methods_ = base64.b64encode(tempstr)
            del apk_methods
            if apk_methods_:
                values += ",'" + str(apk_methods_) + "'"
        else:
            values += ",NULL"
        if apk_permissions:
            tempstr = ""
            for apk_permission in apk_permissions:
                if tempstr:
                    tempstr += '#'
                tempstr += str(apk_permission)
            apk_permissions_ = base64.b64encode(tempstr)
            del apk_permissions
            if apk_permissions_:
                values += ",'" + str(apk_permissions_) + "'"
        else:
            values += ",NULL"
        if apk_flag:
            values += "," + str(int(apk_flag))
        else:
            values += ",NULL"
        sqli = "insert into apk_raw_info(apk_md5,apk_sign_md5,apk_name,apk_package_name,apk_methods,apk_permissions,apk_flag)" \
               + " values(" + values + ")"
        if self.execute(sqli):
            return True
        else:
            return False

    def insert_apk_method(self, apk_md5, apk_method=None, citations=None):
        """插入数据,若插入成功返回True,否则返回False"""

        pass

    def insert_apk_permission(self, apk_md5, apk_permission=None, citations=None):
        pass

    def delete_apk_raw_info(self, apk_md5=None, apk_sign_md5=None, apk_name=None, apk_package_name=None, apk_flag=None):
        """删除数据,删除成功返回True,否则返回False"""
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='test',
        )
        cur = conn.cursor()
        sqli = "delete from apk_raw_info where "
        tail = ""
        if apk_md5:
            if tail == "":
                tail += "apk_md5='%s'" % apk_md5
            else:
                tail += " and apk_md5='%s'" % apk_md5
        if apk_sign_md5:
            if tail == "":
                tail += "apk_sign_md5='%s'" % apk_sign_md5
            else:
                tail += " and apk_sign_md5='%s'" % apk_sign_md5
        if apk_name:
            if tail == "":
                tail += "apk_name='%s'" % base64.b64encode(apk_name)
            else:
                tail += " and apk_name='%s'" % base64.b64encode(apk_name)
        if apk_package_name:
            if tail == "":
                tail += "apk_package_name='%s'" % apk_package_name
            else:
                tail += " and apk_package_name='%s'" % apk_package_name
        if apk_flag:
            if tail == "":
                tail += "apk_flag='%s'" % apk_flag
            else:
                tail += " and apk_flag='%s'" % apk_flag
        if tail != "":
            cur.execute(sqli + tail)
            cur.close()
            conn.commit()
            conn.close()
            return True
        else:
            return False

    def update_apk_raw_info(self, apk_md5, apk_sign_md5=None, apk_name=None, apk_package_name=None, apk_methods=None, apk_permissions=None, apk_flag=None):
        """更新数据,更新成功返回True,否则返回False,若更新参数未填写也返回False"""
        if not apk_md5:
            return False
        sqli = "update apk_raw_info set"
        middle = ""
        tail = " where apk_md5='%s'" % apk_md5
        if apk_sign_md5:
            if middle:
                middle += ",apk_sign_md5='%s'" % apk_sign_md5
            else:
                middle += " apk_sign_md5='%s'" % apk_sign_md5
        if apk_name:
            if middle:
                middle += ",apk_name='%s'" % base64.b64encode(apk_name)
            else:
                middle += " apk_name='%s'" % base64.b64encode(apk_name)
        if apk_package_name:
            if middle:
                middle += ",apk_package_name='%s'" % apk_package_name
            else:
                middle += " apk_package_name='%s'" % apk_package_name
        if apk_methods:
            tempstr = ""
            for apk_method in apk_methods:
                if tempstr:
                    tempstr += '#'
                tempstr += str(apk_method)
            apk_methods_ = base64.b64encode(tempstr)
            del apk_methods
            if middle:
                middle += ",apk_methods='%s'" % apk_methods_
            else:
                middle += " apk_methods='%s'" % apk_methods_
        if apk_permissions:
            tempstr = ""
            for apk_permission in apk_permissions:
                if tempstr:
                    tempstr += '#'
                tempstr += str(apk_permission)
            apk_permissions_ = base64.b64encode(tempstr)
            del apk_permissions
            if middle:
                middle += ",apk_permissions='%s'" % apk_permissions_
            else:
                middle += " apk_permissions='%s'" % apk_permissions_
        if apk_flag:
            if middle:
                middle += ",apk_flag=%d" % apk_flag
            else:
                middle += " apk_flag=%d" % apk_flag
        if middle:
            if self.execute(sqli + middle + tail):
                return True
            else:
                return False
        else:
            return False

    def search_apk_raw_info(self, apk_md5=None, apk_package_name=None, apk_flag=None, top=0):
        """
        查询数据,若表中数据为0则返回None,否则返回数据list
        list中是APP类,APP类见APKManager
        """
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='test',
        )
        cur = conn.cursor()
        sqli = "select * from apk_raw_info"
        tail = ""
        if apk_md5:
            if tail:
                tail += " and apk_md5='%s'" % apk_md5
            else:
                tail += " where apk_md5='%s'" % apk_md5
        if apk_package_name:
            if tail:
                tail += " and apk_package_name='%s'" % apk_package_name
            else:
                tail += " where apk_package_name='%s'" % apk_package_name
        if apk_flag:
            if tail:
                tail += " and apk_flag=%d" % int(apk_flag)
            else:
                tail += " where apk_flag=%d" % int(apk_flag)

        # 获得表中有多少条数据
        t_count = cur.execute(sqli + tail)
        if not t_count:
            cur.close()
            conn.close()
            return []
        if top == 0:
            top = t_count
        count = top if t_count > top else t_count
        apps = []
        for i in range(0, count):
            data = cur.fetchone()
            app = APP()
            app.apk_md5 = data[0]
            app.apk_sign_md5 = data[1]
            if data[2]:
                app.apk_name = base64.b64decode(data[2])
            app.apk_package_name = data[3]
            if data[4]:
                app.apk_methods = [d for d in base64.b64decode(data[4]).split('#')]
            if data[5]:
                app.apk_permissions = [d for d in base64.b64decode(data[5]).split('#')]
            app.apk_flag = data[6]
            apps.append(app)
        cur.close()
        conn.commit()
        conn.close()
        return apps

    def search_apk_raw_info_md5_with_flag(self, flag,top=500):
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='test',
        )
        cur = conn.cursor()
        sqli = "select apk_md5,apk_name from apk_raw_info where apk_flag=%d limit 0,%d" % (int(flag),top)
        cur.execute(sqli)
        apps = []
        for i in range(0, top):
            data = cur.fetchone()
            app = APP()
            app.apk_md5 = data[0]
            app.apk_name = base64.b64decode(data[1])
            apps.append(app)
        cur.close()
        conn.commit()
        conn.close()
        return apps

    def search_apk_raw_info_flag(self, apk_md5):
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='test',
        )
        cur = conn.cursor()
        sqli = "select apk_flag from apk_raw_info where apk_md5='%s'" % str(apk_md5)
        cur.execute(sqli)
        flag = cur.fetchone()[0]
        cur.close()
        conn.commit()
        conn.close()
        return flag

    def search_apk_method(self, apk_md5=None, apk_method=None, citations=None, top=0):
        pass

    def search_apk_permission(self, apk_md5=None, apk_permission=None, citations=None, top=0):
        pass

    def get_count(self, apk_md5=None, apk_package_name=None, apk_flag=None):
        sqli = "select apk_md5 from apk_raw_info"
        tail = ""
        if apk_md5:
            if tail:
                tail += " and apk_md5='%s'" % apk_md5
            else:
                tail += " where apk_md5='%s'" % apk_md5
        if apk_package_name:
            if tail:
                tail += " and apk_package_name='%s'" % apk_package_name
            else:
                tail += " where apk_package_name='%s'" % apk_package_name
        if apk_flag:
            if tail:
                tail += " and apk_flag=%d" % int(apk_flag)
            else:
                tail += " where apk_flag=%d" % int(apk_flag)

        count = self.execute(sqli + tail)
        if count:
            return count
        else:
            return 0


def f_write(filename, data):
    f = open(filename, 'a')
    f.write(data)
    f.close()


def insert_into_apk_method():
    conn1 = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='test',
    )
    cur1 = conn1.cursor()
    sqli1 = 'select apk_md5 from apk_raw_info limit 0,10000'
    total = cur1.execute(sqli1)
    count = 0
    badfile = 0
    all_md5 = cur1.fetchall()
    cur1.close()
    conn1.commit()
    conn1.close()

    id_number = 0

    for md5_iter in all_md5:
        conn1 = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='test',
        )
        cur1 = conn1.cursor()
        sqli1 = "select apk_methods from apk_raw_info where apk_md5='%s'" % md5_iter[0]
        n = cur1.execute(sqli1)
        if n:
            apk_methods_raw = cur1.fetchone()[0]
            apk_md5 = md5_iter[0]
            apk_methods = [re.findall(r'->(.*?)$', str(d))[0] for d in base64.b64decode(apk_methods_raw).split('#')]
            for apk_method in apk_methods:
                if id_number <= 103637:
                    id_number += 1
                    sys.stdout.write("\r id_number:%d" % id_number)
                    continue
                try:
                    sqli2 = "select apk_md5,apk_method,citations from apk_method where apk_md5='%s' and apk_method='%s'" % (apk_md5, base64.b64encode(apk_method))
                    conn2 = MySQLdb.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='test',
                    )
                    cur2 = conn2.cursor()
                    d_count = cur2.execute(sqli2)
                    if d_count:
                        citations = cur2.fetchone()[2] + 1
                        sqli3 = "update apk_method set citations=%d where apk_md5='%s' and apk_method='%s'" % (citations, apk_md5, base64.b64encode(apk_method))
                    else:
                        citations = 1
                        sqli3 = "insert into apk_method(apk_md5,apk_method,citations) VALUES ('%s','%s',%d)" % (apk_md5, base64.b64encode(apk_method), citations)
                    cur2.close()
                    conn2.commit()
                    conn2.close()
                    conn3 = MySQLdb.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='test',
                    )
                    cur3 = conn3.cursor()
                    cur3.execute(sqli3)
                    cur3.close()
                    conn3.commit()
                    conn3.close()
                except Exception, e:
                    badfile += 1
                    print "错误:", apk_md5, ":", apk_method, e.message
                id_number += 1
                f = open('id_number.txt', 'w')
                f.write(str(id_number))
                f.close()
                sys.stdout.write("\r id_number:%d" % id_number)
        else:
            badfile += 1
            print "错误"
        cur1.close()
        conn1.commit()
        conn1.close()
        count += 1
        rate = count / (total + 0.0)
        f = open('count.txt', 'w')
        f.write("已完成:" + str(count) + "||" + str(rate * 100) + "%||发生错误文件数:" + str(badfile))
        f.close()
        print "已完成:" + str(count) + "||" + str(rate * 100) + "%||发生错误文件数:" + str(badfile)


def insert_into_apk_permission():
    conn1 = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='test',
    )
    cur1 = conn1.cursor()
    sqli1 = 'select apk_md5 from apk_raw_info limit 0,10000'
    total = cur1.execute(sqli1)
    count = 0
    badfile = 0
    all_md5 = cur1.fetchall()
    cur1.close()
    conn1.commit()
    conn1.close()

    id_number = 0

    for md5_iter in all_md5:
        conn1 = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='test',
        )
        cur1 = conn1.cursor()
        sqli1 = "select apk_permissions from apk_raw_info where apk_md5='%s'" % md5_iter[0]
        n = cur1.execute(sqli1)
        if n:
            apk_permissions_raw = cur1.fetchone()[0]
            apk_md5 = md5_iter[0]
            apk_permissions = [d for d in base64.b64decode(apk_permissions_raw).split('#')]
            for apk_permission in apk_permissions:
                # if id_number <= 103637:
                #     id_number += 1
                #     sys.stdout.write("\r id_number:%d" % id_number)
                #     continue
                try:
                    sqli2 = "select apk_md5,apk_permission,citations from apk_permission where apk_md5='%s' and apk_permission='%s'" % (apk_md5, base64.b64encode(apk_permission))
                    conn2 = MySQLdb.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='test',
                    )
                    cur2 = conn2.cursor()
                    d_count = cur2.execute(sqli2)
                    if d_count:
                        citations = cur2.fetchone()[2] + 1
                        sqli3 = "update apk_permission set citations=%d where apk_md5='%s' and apk_permission='%s'" % (citations, apk_md5, base64.b64encode(apk_permission))
                    else:
                        citations = 1
                        sqli3 = "insert into apk_permission(apk_md5,apk_permission,citations) VALUES ('%s','%s',%d)" % (apk_md5, base64.b64encode(apk_permission), citations)
                    cur2.close()
                    conn2.commit()
                    conn2.close()
                    conn3 = MySQLdb.connect(
                        host='localhost',
                        port=3306,
                        user='root',
                        passwd='root',
                        db='test',
                    )
                    cur3 = conn3.cursor()
                    cur3.execute(sqli3)
                    cur3.close()
                    conn3.commit()
                    conn3.close()
                except Exception, e:
                    badfile += 1
                    print "错误:", apk_md5, ":", apk_permission, e.message
                id_number += 1
                f = open('id_number1.txt', 'w')
                f.write(str(id_number))
                f.close()
                sys.stdout.write("\r id_number:%d" % id_number)
        else:
            badfile += 1
            print "错误"
        cur1.close()
        conn1.commit()
        conn1.close()
        count += 1
        rate = count / (total + 0.0)
        f = open('count1.txt', 'w')
        f.write("已完成:" + str(count) + "||" + str(rate * 100) + "%||发生错误文件数:" + str(badfile))
        f.close()
        print "已完成:" + str(count) + "||" + str(rate * 100) + "%||发生错误文件数:" + str(badfile)


def update_f_citations_in_apk_permission():
    conn = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='root',
        db='test',
    )
    cur = conn.cursor()
    sqli1 = 'select distinct apk_permission from apk_permission limit 0,3000'
    total = cur.execute(sqli1)
    apk_permissions = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    apk_permissions = [p[0] for p in apk_permissions]
    for apk_permission in apk_permissions:
        # print apk_permission
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='test',
        )
        cur = conn.cursor()
        sqli2 = "select citations from apk_permission where apk_permission='%s'" % apk_permission
        cur.execute(sqli2)
        f_citations = len(cur.fetchall())
        cur.close()
        conn.commit()
        conn.close()
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='test',
        )
        cur = conn.cursor()
        sqli3 = "update apk_permission set f_citations=%d where apk_permission='%s'" % (f_citations, apk_permission)
        cur.execute(sqli3)
        cur.close()
        conn.commit()
        conn.close()


def update_signature():
    offical_apk_path = r"D:\apk"
    su = SQLUtil()
    paths = APKManager.get_all_apk_files(offical_apk_path, 'gbk')
    total = len(paths) + 0.0
    count = 0
    badfile = 0

    for path in paths:
        signature_md5 = get_signature_and_md5(path)
        if signature_md5:
            if su.update_apk_raw_info(apk_md5=signature_md5[1], apk_sign_md5=signature_md5[0]):
                count += 1
            else:
                badfile += 1
                f = open('remain_apk1.txt', 'a')
                f.write(path + '\n')
                f.close()
        else:
            badfile += 1
            f = open('remain_apk1.txt', 'a')
            f.write(path + '\n')
            f.close()
        rate = count / total
        sys.stdout.write("\r已完成:" + str(count) + "||" + str(rate * 100) + "%||发生错误文件数:" + str(badfile))

    app = su.search_apk_raw_info(apk_md5='6d9afd4e74264f0bd32ab70b45250fbs')

    if app:
        print app
        for apk_permission in app.apk_permissions:
            print apk_permission
        for apk_method in app.apk_methods:
            print re.findall(r'->(.*?)$', str(apk_method))[0]
            print apk_method


def init_database():
    offical_apk_path = r"D:\apk"
    su = SQLUtil()
    paths = APKManager.get_all_apk_files(offical_apk_path, 'gbk')
    total = len(paths) + 0.0
    count = 0
    badfile = 0
    for path in paths:
        manager = APKManager.APKManager(path)
        apk_md5 = GetFileMd5(path)
        apk_name = path.encode(encoding='utf8')
        if not su.is_duplicate(apk_md5):
            try:
                apk_package_name = manager.get_apk_obj().get_package()
                apk_methods = manager.get_dvm_obj().get_methods()
                apk_permissions = manager.get_apk_obj().get_permissions()
                apk_flag = "1"
                su.insert_apk_raw_info(apk_md5=apk_md5,
                                       apk_name=apk_name,
                                       apk_package_name=apk_package_name,
                                       apk_methods=apk_methods,
                                       apk_permissions=apk_permissions,
                                       apk_flag=apk_flag)
            except Exception:
                f = open('remain_apk.txt', 'a')
                f.write(apk_name + '\n')
                f.close()
                badfile += 1
        count += 1
        rate = count / total
        sys.stdout.write("\r已完成:" + str(count) + "||" + str(rate * 100) + "%||发生错误文件数:" + str(badfile))
    sys.stdout.write('\r')
    sys.stdout.write('100% finished!')

    print su.get_count()
    print su.is_duplicate(apk_md5='1231')
    su.insert_apk_raw_info(apk_md5='123')
    su.insert_apk_raw_info(apk_md5='111', apk_sign_md5=None, apk_name='gh231h', apk_package_name='1234123', apk_methods='342', apk_permissions='235', apk_flag='0')
    su.update_apk_raw_info(apk_md5='111', apk_sign_md5='123445', apk_name='352345', apk_package_name='67532467', apk_methods='6812', apk_permissions='734', apk_flag='0')
    su.delete_apk_raw_info(apk_md5='123')
    apps = su.search_apk_raw_info()
    for app in apps:
        print app.apk_md5


if __name__ == '__main__':
    # offical_apk_path = r"D:\apk"
    # malwares_path = r"D:\malwares"
    # path = r'D:\apk\10023547_com.tencent.tmgp.mhzxsy_u111_1.2.6.apk'
    # su = sql_util()
    # print su.get_count(apk_flag='0')

    # <editor-fold desc="制作机器学习数据表">
    # permission_list = []
    # f = open('top_permissions.txt', 'r')
    # for apk_permission in f.readlines():
    #     permission_list.append(apk_permission.strip())
    # f.close()
    # f = open('apk_md5s.txt', 'r')
    # apk_md5s = [m.strip() for m in f.readlines()]
    # f.close()
    # total = len(apk_md5s)
    # count = 0
    # for apk_md5 in apk_md5s:
    #     # 获取flag
    #     conn = MySQLdb.connect(
    #         host='localhost',
    #         port=3306,
    #         user='root',
    #         passwd='root',
    #         db='test',
    #     )
    #     cur = conn.cursor()
    #     sqli = "select apk_flag from apk_raw_info where apk_md5='%s'" % apk_md5
    #     cur.execute(sqli)
    #     flag = cur.fetchone()
    #     flag = flag[0] if flag else 0
    #     cur.close()
    #     conn.commit()
    #     conn.close()
    #     # 获取各个permission的存在情况
    #     conn = MySQLdb.connect(
    #         host='localhost',
    #         port=3306,
    #         user='root',
    #         passwd='root',
    #         db='test',
    #     )
    #     cur = conn.cursor()
    #     sqli = "select apk_permission from apk_permission where apk_md5='%s'" % apk_md5
    #     cur.execute(sqli)
    #     permissions = cur.fetchall()
    #     permissions = [] if not permissions else [base64.b64decode(p[0]) for p in permissions]
    #     cur.close()
    #     conn.commit()
    #     conn.close()
    #     for permission in permission_list:
    #         if permission in permissions:
    #             f_write('data.txt', '1 ')
    #         else:
    #             f_write('data.txt', '0 ')
    #     f_write('data.txt', str(flag))
    #     f_write('data.txt', '\n')
    #     count += 1
    #     rate = count / (total + 0.0)
    #     sys.stdout.write("\r已完成:" + str(count) + "||" + str(rate * 100) + "%")
    # </editor-fold>

    print base64.b64decode('RDpcbWFsd2FyZXNcZHJlYmluLTFcNjBlMWNmMjhiYmE4MzVhY2IxNjZmMDJiMTRmODAyNmVmMmMxYWMwZmI4NzI0NGM5YzVlNmFiZDMwNmM2NDlmZQ==')
