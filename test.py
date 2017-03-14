# coding=UTF-8
import re
import urllib2

# from androguard.core.bytecodes import apk, dvm
# from androguard.core.analysis import analysis
#
# path = '/Users/sundiz/Desktop/androidmalware'
#
#
# def get_all_apk_files(mpath):
#     paths = os.listdir(mpath)
#     list = []
#     for p in paths:
#         if os.path.isdir(mpath + '/' + p):
#             list += get_all_apk_files(mpath + '/' + p)
#         elif p[-4:] == '.apk':
#             list.append(mpath + '/' + p)
#     return list
#
#
# dvm.DalvikVMFormat(apk.APK('/Users/sundiz/Desktop/new.apk', False, "r", None, 2))

path = '/Users/sundiz/Desktop/androidapp/'
url = 'https://apkpure.com/cn/app'
download_pre = 'https://apkpure.com'

test_url = '    <div class="category-template-down"><a rel="nofollow" class="" title="下载 支付宝 最新版 apk" href="/cn/alipay/com.eg.android.AlipayGphone/download?from=category">下载 APK</a></div>'
download_url = 'https://download.apkpure.com/b/apk/Y29tLmhhbG8ud2lmaWtleS53aWZpbG9jYXRpbmdfNzM2XzQ5NmE5OTg0?_fn=V2lGaSBNYXN0ZXIgS2V5IGJ5IHdpZmkgY29tX3Y0LjEuNzlfYXBrcHVyZS5jb20uYXBr&amp;k=06ababc20fa7fee3fd9928a80e7c2bad58ca0268&amp;as=fd96fd057d42200b8f5644f21bfb8eaa58c75fe0&amp;_p=Y29tLmhhbG8ud2lmaWtleS53aWZpbG9jYXRpbmc%3D&amp;c=1%7CTOOLS'


# user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
# headers = {'User-Agent': user_agent}
# request = urllib2.Request(download_url, headers=headers)
# response = urllib2.urlopen(request)
# with open('/Users/sundiz/Desktop/androidapp/wifi.apk', "wb") as code:
#     code.write(response.read())


# print response.read()

def get_html_raw(url):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    request = urllib2.Request(url, headers=headers)
    response = urllib2.urlopen(request)
    return response.read()


result = get_html_raw(url)
links = re.findall(r'<div class="category-template-down"><a rel="nofollow" class="" title="下载 (.*?) 最新版 apk" href="(.*?)">', result, re.S)
for link in links:
    print link[0].decode(encoding='utf8'),link[1]


'''
<a id="download_link" rel="nofollow" class="ga" ga="redownload|com.halo.wifikey.wifilocating|category_APK_1_TOOLS" title="下载 WiFi万能钥匙 - wifi.com官方版本 最新版 apk" href="https://download.apkpure.com/b/apk/Y29tLmhhbG8ud2lmaWtleS53aWZpbG9jYXRpbmdfNzM2XzQ5NmE5OTg0?_fn=V2lGaSBNYXN0ZXIgS2V5IGJ5IHdpZmkgY29tX3Y0LjEuNzlfYXBrcHVyZS5jb20uYXBr&amp;k=06ababc20fa7fee3fd9928a80e7c2bad58ca0268&amp;as=fd96fd057d42200b8f5644f21bfb8eaa58c75fe0&amp;_p=Y29tLmhhbG8ud2lmaWtleS53aWZpbG9jYXRpbmc%3D&amp;c=1%7CTOOLS">请点我</a>
'''
