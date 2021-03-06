# -*- coding=utf-8 -*-
from course_mark.hex2b64 import HB64
from course_mark import RSAJS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, request
import requests
import time
from lxml import etree

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
        self.csrftoken = lxml.xpath("//input[@id='csrftoken']/@value")

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
            #print("登录成功")
            return self.session
        else:
            #print("用户名或密码不正确，登录失败")
            exit()


def TimeTable(session, table_url, term, xuenian):
    if term == "now":
        xqm = 12
    else:
        xqm = 3
    data = {"xnm": xuenian, "xqm": xqm}
    table_info = session.post(table_url, data=data).json()
    # return table_info["kbList"]
    kb = []
    kbList = []
    for each in table_info["kbList"]:
        kbList.append(each["xqjmc"])
        kbList.append(each["jc"])
        kbList.append(each["cdmc"])
        kbList.append(each["zcd"])
        kbList.append(each["kcmc"])
        kbList.append(each["xm"])
        kb.append(kbList)
    return kb

def Cj(session, cj_url, term, xuenian):
    if term == "now":
        x = 3
    else :
        x = 12
    data = {"xnm": xuenian, "xqm": x, "queryModel.showCount": 15, "queryModel.currentPage": 1}
    table_info = session.post(cj_url, data=data).json()
    cj = []
    cjlist = []
    if table_info['totalCount'] > 15:

        for each in table_info["items"]:
            cjlist.append(each['kcmc'])
            mx_cj_url_data = {"xnm": xuenian, "xqm": x, "jxb_id": each['jxb_id']}
            mx_cj_url = "https://jwgl.suse.edu.cn/cjcx/cjcx_cxXsXmcjList.html?gnmkdm=N305007"
            mx_cj_info = session.post(mx_cj_url, data=mx_cj_url_data).json()
            if len(mx_cj_info["items"]) == 2:
                i = 1
                if len(mx_cj_info["items"]) == 2:
                    for each2 in mx_cj_info["items"]:
                        cjlist.append(each2['xmblmc'])
                        if 'xmcj' not in each2:
                            cjlist.append("无成绩")
                        else:
                            cjlist.append(each2['xmcj'])
                        if i == 1:
                            cjlist.append('期末(0%)')
                            cjlist.append('100')
                        i += 1
            else:
                for each2 in mx_cj_info["items"]:
                    cjlist.append(each2['xmblmc'])
                    if 'xmcj' not in each2:
                        cjlist.append("无成绩")
                    else:
                        cjlist.append(each2['xmcj'])
            cj.append(cjlist)
        data = {"xnm": xuenian, "xqm": x, "queryModel.showCount": 15, "queryModel.currentPage": 2}
        table_info = session.post(cj_url, data=data).json()

        for each in table_info["items"]:
            cjlist.append(each['kcmc'])
            mx_cj_url_data = {"xnm": xuenian, "xqm": x, "jxb_id": each['jxb_id']}
            mx_cj_url = "https://jwgl.suse.edu.cn/cjcx/cjcx_cxXsXmcjList.html?gnmkdm=N305007"
            mx_cj_info = session.post(mx_cj_url, data=mx_cj_url_data).json()
            i = 1
            if len(mx_cj_info["items"]) == 2:
                for each2 in mx_cj_info["items"]:
                    cjlist.append(each2['xmblmc'])
                    if 'xmcj' not in each2:
                        cjlist.append("无总成绩")
                    else:
                        cjlist.append(each2['xmcj'])
                    if i == 1:
                        cjlist.append('期末(0%)')
                        cjlist.append('100')
                    i += 1
            else:
                for each2 in mx_cj_info["items"]:
                    cjlist.append(each2['xmblmc'])
                    if 'xmcj' not in each2:
                        cjlist.append("无总成绩")
                    else:
                        cjlist.append(each2['xmcj'])
            cj.append(cjlist)

    else :
        for each in table_info["items"]:
            cjlist.append(each['kcmc'])
            mx_cj_url_data = {"xnm": xuenian, "xqm": x, "jxb_id": each['jxb_id']}
            mx_cj_url = "https://jwgl.suse.edu.cn/cjcx/cjcx_cxXsXmcjList.html?gnmkdm=N305007"
            mx_cj_info = session.post(mx_cj_url, data=mx_cj_url_data).json()
            if len(mx_cj_info["items"]) == 2:
                i = 1
                if len(mx_cj_info["items"]) == 2:
                    for each2 in mx_cj_info["items"]:
                        cjlist.append(each2['xmblmc'])
                        if 'xmcj' not in each2:
                            cjlist.append("无成绩")
                        else:
                            cjlist.append(each2['xmcj'])
                        if i == 1:
                            cjlist.append('期末(0%)')
                            cjlist.append('100')
                        i += 1
            else:
                for each2 in mx_cj_info["items"]:
                    cjlist.append(each2['xmblmc'])
                    if 'xmcj' not in each2:
                        cjlist.append("无成绩")
                    else:
                        cjlist.append(each2['xmcj'])
            cj.append(cjlist)
    return cj

def login_to_kb(username: str, password: str, term: str, xuenian: str):
    # 登录主页url
    login_url = "http://jwgl.suse.edu.cn/xtgl/login_slogin.html?language=zh_CN&_t="
    # 请求PublicKey的URL
    login_KeyUrl = "http://jwgl.suse.edu.cn/xtgl/login_getPublicKey.html?time="
    # 登录后的课表URL
    table_url = "http://jwgl.suse.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151"

    zspt = Longin(username, password, login_url, login_KeyUrl)

    response_cookies = zspt.Longin_Home()
    table = TimeTable(response_cookies, table_url, term, xuenian)
    return str(table[0])

def login_to_cj(username: str, password: str, term: str, xuenian: str):
    # 登录主页url
    login_url = "http://jwgl.suse.edu.cn/xtgl/login_slogin.html?language=zh_CN&_t="
    # 请求PublicKey的URL
    login_KeyUrl = "http://jwgl.suse.edu.cn/xtgl/login_getPublicKey.html?time="
    # 登录后的成绩URL
    # cj_url = "https://jwgl.suse.edu.cn/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305007"
    cj_url = "https://jwgl.suse.edu.cn/cjcx/cjcx_cxXsKcList.html?gnmkdm=N305007"

    zspt = Longin(username, password, login_url, login_KeyUrl)

    response_cookies = zspt.Longin_Home()
    cj = Cj(response_cookies, cj_url, term, xuenian)

    return str(cj[0])

def get_cj(username: str, password: str, term: str, xuenian: str):
    cj = login_to_cj(username, password, term, xuenian)
    #i = 1
    # for each in cj:
    #     if i == 2:
    #         print(each, end=" ")
    #     elif i == 4:
    #         print(each, end=" ")
    #     elif i == 6:
    #         print(each, end=" ")
    #     elif i == 7:
    #         print(each, end=" ")
    #         i = 0
    #     else:
    #         print(each)
    #     i += 1
    return cj

def get_kb(username: str, password: str, term: str, xuenian: str):
    kb = login_to_kb(username, password, term, xuenian)
    return kb

app = Flask(__name__)

# HOSTNAME = '127.0.0.1'
#
# PORT = '3306'
#
# DATABASE = 'flask'
#
# USERNAME = 'root'
#
# PASSWORD = 'root'
#
# DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
#
# app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#
# db = SQLAlchemy(app)
#
# class Student(db.Model):
#     __tablename__ = 'student'
#     #主键 是否自增
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     #varchar(255) 是否可以为空
#     name = db.Column(db.String(50), nullable=False)
#     password = db.Column(db.String(50), nullable=False)
#     #text  是否可以为空
#     kb = db.Column(db.Text, nullable=False)
#     cj = db.Column(db.Text, nullable=False)
# db.create_all()
#
# @app.route('/post')
# def insert():
#     article = Student(title="我我我", content="你你你")
#     db.session.add(article)
#     db.session.commit()
#     return "添加成功"
#
# @app.route('/get/kb')
# def get_studuet_kb():
#     username = request.args.get("username")
#     student = Student.query.filter(Student.name == username)[0]
#     return student.kb
#
# @app.route('/get/cj')
# def get_student_cj():
#     username = request.args.get("username")
#     student = Student.query.filter(Student.name == username)[0]
#     return student.cj

@app.route('/put_kb')
def put_kb():
    username = request.args.get("username")
    term = request.args.get("term")
    xuenian = request.args.get("xuenian")
    password = request.args.get("password")
    # student = Student.query.filter(Student.name == username)[0]
    # student.name = username
    # password = student.password
    kb = get_kb(username, password, term, xuenian)
    # student.kb = kb
    # db.session.commit()
    return kb

@app.route('/put_cj')
def put_cj():
    username = request.args.get("username")
    term = request.args.get("term")
    xuenian = request.args.get("xuenian")
    password = request.args.get("password")
    # student = Student.query.filter(Student.name == username)[0]
    # student.name = username
    # password = student.password
    cj = get_cj(username, password, term, xuenian)
    # student.cj = cj
    # db.session.commit()
    return cj


if __name__ == "__main__":

    app.run(host='127.0.0.1', port=8000)


