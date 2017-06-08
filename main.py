# coding=UTF-8
import permission_check
import mal_code_analyze
import sqlutil
import md5_util
import APKManager


def check_dulplicate_module(apk_file):
    signature, md5 = md5_util.get_signature_and_md5(apk_file)
    return sqlutil.SQLUtil().is_duplicate(md5)


def check_repack_module(apk_file):
    signature, md5 = md5_util.get_signature_and_md5(apk_file)
    return sqlutil.SQLUtil().is_duplicate_apk_sign_md5(signature)


class CheckProcess:
    def __init__(self, apk_file, apk_md5=None):

        self.apk_file = apk_file
        if not apk_md5:
            pass
            #signature, md5 = md5_util.get_signature_and_md5(apk_file)
            # self.md5 = md5
            # self.signature = signature
        else:
            self.md5 = apk_md5
        #self.su = sqlutil.SQLUtil()

    def check_dulplicate_and_repack_module(self):
        """
        :return: 返回是否与已有样本重复，是否是重打包
        """
        is_dulplicate_md5 = self.su.is_duplicate(self.md5)
        if is_dulplicate_md5 and not self.su.is_duplicate_apk_sign_md5(self.signature, self.md5):
            is_dulplicate_sign = True
        else:
            is_dulplicate_sign = False
        return is_dulplicate_md5, is_dulplicate_sign

    def check_permission_module(self):
        """
        :return: result: apk是正常软件返回True，否则返回False 
        :return: h: apk是正常软件的概率，[0.5,1.0]为正常软件，[0,0.5]为恶意软件
        """
        result, h = permission_check.check_sensitive_permissions(self.apk_file)
        return result, h

    def check_code_module(self):
        """
        :return: mal_code_num: 存在恶意代码的硬编码个数
        :return: sensitive_methods_t: 恶意API的调用次数
        :return: mal_codes: 硬编码
        """
        mal_code_num, mal_codes = mal_code_analyze.check_sensitive_code(self.apk_file)
        sensitive_methods_t = mal_code_analyze.check_apk_mal_methods(self.apk_file)
        return mal_code_num, sensitive_methods_t, mal_codes

    def report_module(self, dr=(False, False), pc_result=None, cc_result=None, r='正常软件', apkfile=''):
        result = ''
        apk_obj = APKManager.APKManager(apkfile).get_apk_obj()
        result += 'app名称：' + apk_obj.get_app_name() + "\n"
        result += 'app包名：' + apk_obj.get_package() + "\n"
        if dr[0]:
            result += '样本重复，检测结果为：'
            apk_flag = self.su.search_apk_raw_info_flag(self.md5)
            is_offical = '正常软件' if apk_flag == '1' else '恶意软件'
            result += is_offical + '\n'
            result += '是否是重打包软件：'
            is_repackge = '是' if dr[1] else '否'
            result += is_repackge + "\n"
        else:
            result += '检测结果：' + r + "\n"
            result += '是否是重打包软件：'
            is_repackge = '是' if dr[1] else '否'
            result += is_repackge + "\n"

        if pc_result:
            result += '敏感权限检测结果(是正常软件的概率):' + str(pc_result[1] * 100) + '%\n'
        if cc_result:
            result += '恶意代码检测结果:\n\t存在可疑代码的硬编码个数:' + str(cc_result[0]) + '\n\t可疑API的调用次数:' + str(cc_result[1])
            result += '\n'
            if r == '恶意软件':
                hard_codes = ['\t' + c + '\n' for c in cc_result[2]]
                result += '\t可疑硬编码：\n'
                for hard_code in hard_codes:
                    result += hard_code
        print result
        return result


def test_module(apk_file):
    cp = CheckProcess(apk_file)
    # dr = cp.check_dulplicate_and_repack_module()
    dr = (False, False)
    permission_check_result = cp.check_permission_module()
    code_check_result = cp.check_code_module()

    if permission_check_result[1] <= 0.5:
        cp.report_module(dr=dr, pc_result=permission_check_result, cc_result=code_check_result, r='恶意软件', apkfile=apk_file)
    else:
        cp.report_module(dr=dr, pc_result=permission_check_result, cc_result=code_check_result, apkfile=apk_file)


def test_one(apk_file, md5, gate=0.8):
    cp = CheckProcess(apk_file, md5)
    permission_check_result = cp.check_permission_module()
    if permission_check_result[1] < gate:
        return 0
    else:
        code_check_result = cp.check_code_module()
        if code_check_result[0] > 1 and code_check_result[1] > 1:
            return 0
        else:
            return 1


if __name__ == '__main__':
    # 恶意软件
    apkfile = r'/Users/sundiz/Desktop/malware/6f11b19242926af7f928d987b1780b214b698e6b326cf0522dc7a046715d6e19'
    # 正常软件
    apkfile1 = r'/Users/sundiz/Desktop/apk/yxlm.danji.uu.apk'
    # apkfile = r'D:\apk\LINE.apk'

    test_module(apkfile)
    test_module(apkfile1)
    # apps_1 = sqlutil.SQLUtil().search_apk_raw_info_md5_with_flag(flag=1, top=600)
    # apps_0 = sqlutil.SQLUtil().search_apk_raw_info_md5_with_flag(flag=0, top=600)
    # for g in range(50, 51, 5):
    #     TP = 0  # 预测为1，实际为1
    #     FP = 0  # 预测为1，实际为0
    #     FN = 0  # 预测为0，实际为1
    #     TN = 0  # 预测为0，实际为0
    #     count = 0
    #     for app_1 in apps_1:
    #         if count >= 500:
    #             break
    #         try:
    #             r = test_one(app_1.apk_name, app_1.apk_md5, g / 100.0)
    #             if r == 1:
    #                 TP += 1
    #             else:
    #                 FN += 1
    #         except:
    #             continue
    #         count += 1
    #     count = 0
    #     for app_0 in apps_0:
    #         if count >= 500:
    #             break
    #         try:
    #             r = test_one(app_0.apk_name, app_0.apk_md5, g / 100.0)
    #             if r == 1:
    #                 FP += 1
    #             else:
    #                 TN += 1
    #         except:
    #             continue
    #         count += 1
    #     f = open('regression_test', 'a')
    #     f.write('\ngate:%.2f,TP:%d,FP:%d,FN:%d,TN:%d' % (g, TP, FP, FN, TN))
    #     f.close()
    #     print 'TP:', TP, ',FP:', FP, ',FN:', FN, ',TN:', TN
