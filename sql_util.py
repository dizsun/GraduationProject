# coding=UTF-8
import base64
import MySQLdb
import APKManager
import sys
from md5_util import GetFileMd5
from APKManager import APP


class sql_util:
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='root',
            db='test',
        )

        self.cur = None

    def begin(self):
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.commit()
        self.conn.close()

    def insert_apk_raw_info(self, apk_md5, apk_sign_md5=None, apk_name=None, apk_package_name=None, apk_methods=None, apk_permissions=None, apk_flag=None):
        """插入数据"""
        if not apk_md5:
            return
        self.begin()
        # 查重
        duplicate_count = self.cur.execute("select * from apk_raw_info where apk_md5='%s'" % apk_md5)
        if duplicate_count:
            return
        sqli = "insert into apk_raw_info values(%s,%s,%s,%s,%s,%s,%s)"
        if apk_name:
            apk_name = base64.b64encode(apk_name)
        if apk_methods:
            tempstr = ""
            for apk_method in apk_methods:
                if tempstr:
                    tempstr += '#'
                tempstr += str(apk_method)
            apk_methods = base64.b64encode(tempstr)
        if apk_permissions:
            tempstr = ""
            for apk_permission in apk_permissions:
                if tempstr:
                    tempstr += '#'
                tempstr += str(apk_permission)
            apk_permissions = base64.b64encode(tempstr)
        self.cur.execute(sqli, (apk_md5, apk_sign_md5, apk_name, apk_package_name, apk_methods, apk_permissions, apk_flag))
        self.close()

    def delete_apk_raw_info(self, apk_md5=None, apk_sign_md5=None, apk_name=None, apk_package_name=None, apk_flag=None):
        """删除数据"""
        self.begin()
        sqli = "delete from student where "
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
            self.cur.execute(sqli + tail)
        self.close()

    def update_apk_raw_info(self, apk_md5, apk_sign_md5=None, apk_name=None, apk_package_name=None, apk_methods=None, apk_permissions=None, apk_flag=None):
        """更新数据"""
        if not apk_md5:
            return
        self.begin()
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
            if middle:
                middle += ",apk_methods='%s'" % base64.b64encode(apk_methods)
            else:
                middle += " apk_methods='%s'" % base64.b64encode(apk_methods)
        if apk_permissions:
            if middle:
                middle += ",apk_permissions='%s'" % base64.b64encode(apk_permissions)
            else:
                middle += " apk_permissions='%s'" % base64.b64encode(apk_permissions)
        if apk_flag:
            if middle:
                middle += ",apk_flag='%s'" % apk_flag
            else:
                middle += " apk_flag='%s'" % apk_flag
        if middle:
            self.cur.execute(sqli + middle + tail)
        self.close()

    def search_apk_raw_info(self, apk_md5=None, apk_flag=None, top=0):
        """查询数据"""
        self.begin()
        sqli = "select * from apk_raw_info"
        tail = ""
        if apk_md5:
            if tail:
                tail += " and apk_md5='%s'" % apk_md5
            else:
                tail += " where apk_md5='%s'" % apk_md5
        if apk_flag:
            if tail:
                tail += " and apk_flag='%s'" % apk_flag
            else:
                tail += " where apk_flag='%s'" % apk_flag
        # 获得表中有多少条数据
        t_count = self.cur.execute(sqli + tail)
        if top == 0:
            top = t_count
        count = top if t_count > top else t_count
        apps = []
        for i in range(0, count):
            data = self.cur.fetchone()
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
        self.close()
        return apps


if __name__ == '__main__':
    offical_apk_path = r"D:\apk"
    malwares_path = r"D:\malwares"
    su = sql_util()
    paths = APKManager.get_all_apk_files(malwares_path)
    total = len(paths) + 0.0
    count = 0
    for path in paths:
        try:
            manager = APKManager.APKManager(path)
            apk_md5 = GetFileMd5(path)
            apk_name = path
            apk_package_name = manager.get_apk_obj().get_package()
            apk_methods = manager.get_dvm_obj().get_methods()
            apk_permissions = manager.get_apk_obj().get_permissions()
            apk_flag = "0"
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
        count += 1
        rate = count / total
        sys.stdout.write('%\r')
        sys.stdout.write("completed number:" + str(count) + "," + str(rate) + "% finished")
    sys.stdout.write('%\r')
    sys.stdout.write('100% finished!')
    # su.insert_apk_raw_info(apk_md5='111')
    # su.update_apk_raw_info(apk_md5='1234565', apk_sign_md5='123445', apk_name='352345', apk_package_name='67532467', apk_methods='6812', apk_permissions='734', apk_flag='0')
    # su.delete_apk_raw_info(apk_md5='123456')
    # apps = su.search_apk_raw_info()
    # for app in apps:
    #     print app.apk_md5
