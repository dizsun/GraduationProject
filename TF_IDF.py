# coding=UTF-8
import math
import APKManager


class TFIDF:
    def __init__(self, documents):
        self.documents = documents
        self.tfs = []
        self.idf = {}
        self.terms = set()
        self.term_idf = {}  # 非log

    def get_tf(self, document):
        """
        :param document: 需要解析的文档的所有关键词集合
        :return:某个文档的词频
        """
        tf_dic = {}
        maxtf = 0
        for term in document:
            tf_dic[term] = tf_dic.get(term, 0) + 1
            self.terms.add(term)
        for value in tf_dic.values():
            if maxtf < value:
                maxtf = value
        for key in tf_dic.keys():
            tf_dic[key] /= (maxtf + 0.0)
        return tf_dic

    def get_idf(self):
        """
        :return: 获取所有关键词的逆文档频率
        """
        for document in self.documents:
            self.tfs.append(self.get_tf(document))
        for term in self.terms:
            term_idf = 0
            for tf in self.tfs:
                if tf.get(term, -1) != -1:
                    term_idf += 1
            self.idf[term] = math.log(len(self.tfs) / (term_idf + 1.0), len(self.tfs))

    def update_idf(self, document):
        for item in document:
            self.terms.add(item)
            self.term_idf[item] = self.term_idf.get(item, 0) + 1

    @staticmethod
    def get_top_term(dic, top):
        temp_dic = []
        count = 0
        for key in dic.keys():
            if count < top:
                count += 1
                temp_dic.append(key)
            else:
                for item in temp_dic:
                    if dic[item] < dic[key]:
                        temp_dic.remove(item)
                        temp_dic.append(key)
        return temp_dic

    def get_tf_idf(self, document, top=0):
        if not self.idf:
            self.get_idf()
        tf_dic = self.get_tf(document)
        tf_idf = {}
        for term in tf_dic.keys():
            tf_idf[term] = tf_dic.get(term, 0) * self.idf.get(term, 0)
        if top == 0:
            return tf_idf
        else:
            return self.get_top_term(tf_idf, top)


mal_apks_path = '/Users/sundiz/Desktop/androidmalware/Android'
if __name__ == '__main__':
    apks_path = APKManager.get_all_apk_files(mal_apks_path)
    apk_methods = {}
    methods = []
    for apk_path in apks_path:
        mal_apk = APKManager.APKManager().get_dvm_obj(apk_path)
        apk_methods[apk_path] = mal_apk.get_methods()
        methods.append(apk_methods[apk_path])
    tfidf = TFIDF(methods)
    for apk_name in apk_methods.keys():
        print '*' * 150
        print apk_name.replace(mal_apks_path + '/', '')
        for m in tfidf.get_tf_idf(apk_methods[apk_name], 5):
            print m
