# coding=UTF-8
import sys
import APKManager
import pandas
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
import math

reload(sys)
sys.setdefaultencoding("utf-8")


class PermissionCoef:
    def __init__(self):
        self.permission_names = []
        self.coef_map = {}
        self.coefs = []


def mechine_learning():
    url = r'data2.txt'
    permission_list = []
    f = open('top_permissions.txt', 'r')
    for apk_permission in f.readlines():
        permission_list.append(apk_permission.strip())
    f.close()
    permission_list.append('flag')
    dataset = pandas.read_csv(url, names=permission_list)
    array = dataset.values
    X = array[:, 0:105]
    Y = array[:, 105]

    validation_size = 0.20
    seed = 7
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
    scoring = 'accuracy'
    models = []
    models.append(('LR', LogisticRegression()))
    models.append(('KNN', KNeighborsClassifier()))
    models.append(('CART', DecisionTreeClassifier()))
    models.append(('NB', MultinomialNB()))
    models.append(('SVM', SVC()))
    results = []
    names = []
    for name, model in models:
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        results.append(cv_results)
        names.append(name)
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)

    return results, names


def compare_algorithms():
    """绘制图表比较各算法"""
    results, names = mechine_learning()
    fig = plt.figure()
    fig.suptitle('Algorithm Comparison')
    ax = fig.add_subplot(111)
    plt.boxplot(results)
    ax.set_xticklabels(names)
    plt.show()


def LR_result():
    url = r'data2.txt'
    permission_list = []
    f = open('top_permissions.txt', 'r')
    for apk_permission in f.readlines():
        permission_list.append(apk_permission.strip())
    f.close()
    permission_list.append('flag')
    dataset = pandas.read_csv(url, names=permission_list)
    array = dataset.values
    X = array[:, 0:105]
    Y = array[:, 105]

    validation_size = 0.20
    seed = 7
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
    LR = LogisticRegression()
    LR.fit(X_train, Y_train)
    predictions = LR.predict(X_validation)
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))


def get_data(apk_file):
    """从apk文件中提取permisions并且按top_permissions文件中的permissions进行规范化得到状态数组"""
    if not APKManager.APKManager.is_apk_file(apk_file):
        return None
    apk_permissions = APKManager.APKManager(apk_file).get_apk_obj().permissions
    sensitive_permission_state = []
    coef = get_coef()
    for permission_name in coef.permission_names:
        if permission_name in apk_permissions:
            sensitive_permission_state.append(1)
        else:
            sensitive_permission_state.append(0)
    return sensitive_permission_state


def get_coef():
    """从permissions文件中获取PermissionCoef类，包括权限名称和权限权重"""
    try:
        f = open('top_permissions.txt')
        top_permissions = [l.strip() for l in f.readlines()]
        f.close()
        f = open('permissions.txt')
        coef_map = {}
        coefs = []
        for line in f.readlines():
            item = line.strip().split(':')
            coef_map[item[0]] = item[1]
            coefs.append(float(item[1]))
        f.close()
        permission_coef = PermissionCoef()
        permission_coef.permission_names = top_permissions
        permission_coef.coef_map = coef_map
        permission_coef.coefs = coefs
        return permission_coef
    except Exception, e:
        print e.message
        return None


def check_sensitive_permissions(apk_file=None, apk_data=None, alpha=1, gate=1.6):
    """
    敏感权限检测
    @:param gete 门限值
    @:param alpha h函数的参数，是展开系数，alpha越小函数图形越陡峭
    @:return result 是未规范化的结果值 h 函数是将结果规范化的函数
    """
    if not apk_data:
        data = get_data(apk_file)
    else:
        data = apk_data
    coefs = get_coef().coefs
    total = len(coefs)
    result = 0.0
    for i in range(0, total):
        result += int(data[i]) * float(coefs[i])
    h = 1 / (1 + math.exp(-1 * (result - gate) * alpha))
    result = True if result > gate else False
    return result, h


def search_best_gate():
    """搜索最佳门限值"""
    data2 = 'data2.txt'
    f = open(data2)
    datas = [l.strip().split(',') for l in f.readlines()]
    f.close()
    glist = []
    blist = []
    for i in range(-50, 101):
        goodcount = 0.0
        badcount = 0.0
        goodt = badt = 0
        gate = i / 10.0
        for data in datas:
            temp = check_sensitive_permissions(apk_data=data)
            if data[105] == '0':
                badcount += 1
                if temp > gate:
                    badt += 1
            else:
                goodcount += 1
                if temp < gate:
                    goodt += 1
        glist.append(goodt / goodcount)
        blist.append(badt / badcount)
    return glist, blist


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


if __name__ == '__main__':
    """gate=1.6"""
    apkfile = r'D:\apk\aolei.flcp.apk'
    mal_apk = r'D:\malwares\drebin-0\0a3be4156b705957d201a86250d0d7f4c5470f1737ed6d438a129a39b475397b'
    data2 = 'data2.txt'
    # print check_sensitive_permissions(apkfile)
    # print check_sensitive_permissions(mal_apk)

    # f = open(data2)
    # datas = [l.strip().split(',') for l in f.readlines()]
    # f.close()
    # goodtotal = 0.0
    # goodcount = 0.0
    # badtotal = 0.0
    # badcount = 0.0
    # mmax = mmin = 0
    # goodmax = goodmin = 0
    # badmax = badmin = 0
    # goodt = badt = 0
    # gate = 1
    # for data in datas:
    #     temp = check_sensitive_permissions(apk_data=data)
    #     mmax = mmax if mmax > temp else temp
    #     mmin = mmin if mmin < temp else temp
    #     if data[105] == '0':
    #         badtotal += temp
    #         badcount += 1
    #         if temp > gate: badt += 1
    #         badmax = badmax if badmax > temp else temp
    #         badmin = badmin if badmin < temp else temp
    #     else:
    #         goodtotal += temp
    #         goodcount += 1
    #         if temp < gate: goodt += 1
    #         goodmax = goodmax if goodmax > temp else temp
    #         goodmin = goodmin if goodmin < temp else temp
    # print '官方app均值：', goodtotal / goodcount, '最大值：', goodmax, '最小值：', goodmin
    # print '恶意app均值：', badtotal / badcount, '最大值：', badmax, '最小值：', badmin
    # print '最大值和最小值：', mmax, mmin
    # print '官方app误判比例：', goodt / goodcount
    # print '恶意app误判比例：', badt / badcount

    # 获取最佳gate值
    # g,b=search_best_gate()
    # ii=0
    # for i in range(-50,101):
    #     print i/10.0,':',g[ii],':',b[ii]
    #     ii+=1

    f = open("permissions.txt")
    rlines = f.readlines()
    f.close()
    lines = [l.strip() for l in rlines]
    f = open("java.txt", 'a')
    for line in lines:
        paras = line.split(':')
        f.write('preferencesEditor.putString("%s","%s");\n' % (paras[0], paras[1]))
    f.close()
