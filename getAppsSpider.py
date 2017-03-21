# coding=UTF-8
import re
import os
import urllib2
import threading
app_path_mac = '/Users/sundiz/Desktop/androidapp/'
app_path_win = 'C:\\Users\\dizsun\\Desktop\\app\\'
url = 'https://apkpure.com/cn/app'
download_pre = 'https://apkpure.com'


def get_html_raw(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request, timeout=600)
    return response.read()


def download_apk(url, app_name):
    response = get_html_raw(url)
    with open(app_path_mac + app_name + '.apk', "wb") as code:
        code.write(response)


def download_onepage_apk(url):
    result = get_html_raw(url)
    links = re.findall(r'<div class="category-template-down"><a rel="nofollow" class="" title="下载 (.*?) 最新版 apk" href="(.*?)">', result, re.S)
    for link in links:
        # print link[0].decode(encoding='utf8'), download_pre + link[1]
        if link[0].decode(encoding='utf8') == 'APKPure':
            continue
        download_html = get_html_raw(download_pre + link[1])
        download_link = (re.findall(r'<a id="download_link" rel="nofollow" class="ga".*?href="(.*?)">', download_html, re.S))[0]
        try:
            print 'downloading:' + link[0].decode(encoding='utf8') + '......'
            download_apk(download_link, link[0].decode(encoding='utf8'))
            print 'downloaded:' + link[0].decode(encoding='utf8')
        except Exception:
            continue


# threads = []
#
# for num in range(2, 20):
#     url_num = download_pre + '/cn/app?page=' + str(num)
#     print 'page ' + str(num) + ' is downloading......'
#     t = threading.Thread(target=download_onepage_apk, args=(url_num,))
#     threads.append(t)
# for t in threads:
#     t.setDaemon(True)
#     t.start()
# t.join()
# print 'all task has completed!'