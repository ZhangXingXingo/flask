# -*- coding=utf-8 -*-
import requests
import time
from lxml import etree
from 数据库.hex2b64 import HB64
from 数据库 import RSAJS


class Longin():

    def __init__(self, user, password, login_url, login_KeyUrl):
        # 初始化程序数据
        self.Username = user
        self.Password = password
        nowTime = lambda: str(round(time.time() * 1000))
        self.now_time = nowTime()
        self.login_url = login_url
        self.login_Key = login_KeyUrl

    def Get_indexHtml(self):
        # 获取教务系统网站
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Referer": self.login_url + self.now_time,
            "Upgrade-Insecure-Requests": "1"
        })
        self.response = self.session.get(self.login_url + self.now_time).content.decode("utf-8")

    def Get_csrftoken(self):
        # 获取到csrftoken
        lxml = etree.HTML(self.response)
        self.csrftoken = lxml.xpath("//input[@id='csrftoken']/@value")[0]

    def Get_PublicKey(self):
        # 获取到加密公钥
        key_html = self.session.get(self.login_Key + self.now_time)
        key_data = key_html.json()
        self.modulus = key_data["modulus"]
        self.exponent = key_data["exponent"]

    def Get_RSA_Password(self):
        # 生成RSA加密密码
        rsaKey = RSAJS.RSAKey()
        rsaKey.setPublic(HB64().b642hex(self.modulus), HB64().b642hex(self.exponent))
        self.enPassword = HB64().hex2b64(rsaKey.encrypt(self.Password))

    def Longin_Home(self):
        # 登录信息门户,成功返回session对象
        self.Get_indexHtml()
        self.Get_csrftoken()
        self.Get_PublicKey()
        self.Get_RSA_Password()
        login_data = [("csrftoken", self.csrftoken), ("yhm", self.Username), ("mm", self.enPassword),
                      ("mm", self.enPassword)]
        login_html = self.session.post(self.login_url + self.now_time, data=login_data)
        # 当提交的表单是正确的，url会跳转到主页，所以此处根据url有没有跳转来判断是否登录成功
        if login_html.url.find("login_slogin.html") == -1:  # -1没找到，说明已经跳转到主页
            print("登录成功")
            return self.session
        else:
            print("用户名或密码不正确，登录失败")
            exit()

# qsxqj
# xsxx
# sjkList
# xqjmcMap
# xskbsfxstkzt
# kbList
# xsbjList
# zckbsfxssj
# djdzList
# kblx
# sfxsd
# xqbzxxszList
# xkkg
# jxhjkcList
# xnxqsfkz
# class TimeTable():
#     def __init__(self, session, table_url, term):
#         if term == "now":
#             xqm = 12
#         else :
#             xqm = 3
#         data = {"xnm": 2021, "xqm": xqm}
#         table_info = session.post(table_url, data=data).json()
#
#         for each in table_info["kbList"]:
#             # print(each)
#             plt = r'{} | {:<8s} | {:<13s} | {:<15s} | {:<22s} | {:<30s}'
#             print(plt.format(each["xqjmc"], each["jc"], each["cdmc"], each["zcd"], each["kcmc"], each['xm']))

def TimeTable(session, table_url, term):
    if term == "now":
        xqm = 12
    else:
        xqm = 3
    data = {"xnm": 2021, "xqm": xqm}
    table_info = session.post(table_url, data=data).json()
    # return table_info["kbList"]
    kb = []
    kbList = []
    for each in table_info["kbList"]:
        # print(each)
        # plt = r'{} | {:<8s} | {:<13s} | {:<15s} | {:<22s} | {:<30s}'
        # print(plt.format(each["xqjmc"], each["jc"], each["cdmc"], each["zcd"], each["kcmc"], each['xm']))
        kbList.append(each["xqjmc"])
        kbList.append(each["jc"])
        kbList.append(each["cdmc"])
        kbList.append(each["zcd"])
        kbList.append(each["kcmc"])
        kbList.append(each["xm"])
        kb.append(kbList)
    return kb

# currentPage
# currentResult
# entityOrField
# items
# limit
# offset
# pageNo
# pageSize
# showCount
# sortName
# sortOrder
# sorts
# totalCount
# totalPage
# totalResult
# class Cj():
#     def __init__(self, session, cj_url):
#         data = {"xnm": 2021, "xqm": 12, "queryModel.showCount": 15,"queryModel.currentPage": 1}
#         table_info = session.post(cj_url, data=data).json()
#
#         for each in table_info["items"]:
#             print(each)
#             plt = r'{} | {:<8d} | {:<13d} | {:<15d} | {:<22d} | {:<30d}'
#             print(plt.format(each["xqjmc"], each["jc"], each["cdmc"], each["zcd"], each["kcmc"], each['xm']))

def Cj(session, cj_url, term):
    if term == "now":
        x = 3
    else :
        x = 12
    data = {"xnm": 2021, "xqm": x, "queryModel.showCount": 15, "queryModel.currentPage": 1}
    table_info = session.post(cj_url, data=data).json()
    # print(table_info)
    # if table_info['totalCount'] > 15:
    #     for each in table_info["items"]:
    #         print(each)
    #     data = {"xnm": 2021, "xqm": x, "queryModel.showCount": 15, "queryModel.currentPage": 2}
    #     table_info = session.post(cj_url, data=data).json()
    #     for each in table_info["items"]:
    #         print(each)
    # else :
    for each in table_info["items"]:
            print(each)
    # for each in table_info["items"]:
    #     print(each)
        # plt = r'{} | {:<8d} | {:<13d} | {:<15d} | {:<22d} | {:<30d}'
        # print(plt.format(each["xqjmc"], each["jc"], each["cdmc"], each["zcd"], each["kcmc"], each['xm']))

def login_to_kb(username: str, password: str, term: str):
    # 登录主页url
    login_url = "http://jwgl.suse.edu.cn/xtgl/login_slogin.html?language=zh_CN&_t="
    # 请求PublicKey的URL
    login_KeyUrl = "http://jwgl.suse.edu.cn/xtgl/login_getPublicKey.html?time="
    # 登录后的课表URL
    table_url = "http://jwgl.suse.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151"

    zspt = Longin(username, password, login_url, login_KeyUrl)
    response_cookies = zspt.Longin_Home()
    print(response_cookies.cookies)
    table = TimeTable(response_cookies, table_url, term)
    return table

def login_to_cj(username: str, password: str, term: str):
    # 登录主页url
    login_url = "http://jwgl.suse.edu.cn/xtgl/login_slogin.html?language=zh_CN&_t="
    # 请求PublicKey的URL
    login_KeyUrl = "http://jwgl.suse.edu.cn/xtgl/login_getPublicKey.html?time="
    # 登录后的成绩URL
    cj_url = "https://jwgl.suse.edu.cn/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005"

    zspt = Longin(username, password, login_url, login_KeyUrl)
    response_cookies = zspt.Longin_Home()
    print(response_cookies.cookies)
    cj = Cj(response_cookies, cj_url, term)
def get_kb(username: str, password: str, term: str):
    kb = login_to_kb("19171040207", "lhz233666", "now")
    i = 0
    # for each in kb[0]:
    #     if i % 6 == 0:
    #         print("\n")
    #     print(each, end=" ")
    #
    print(str(kb[0]))

if __name__ == "__main__":
    login_to_cj("19171040207", "lhz233666", "now")
