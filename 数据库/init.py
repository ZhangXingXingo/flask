# coding=gb2312

import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, request

import requests
import time
from lxml import etree
from hex2b64 import HB64
import RSAJS
app = Flask(__name__)

HOSTNAME = '127.0.0.1'

PORT = '3306'

DATABASE = 'test'

USERNAME = 'root'

PASSWORD = 'root'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Article(db.Model):
    __tablename__ = 'kb'
    #���� �Ƿ�����
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #varchar(255) �Ƿ����Ϊ��
    title = db.Column(db.String(255), nullable=False)
    #text  �Ƿ����Ϊ��
    content = db.Column(db.Text, nullable=False)

db.create_all()

@app.route('/post')
def insert():
    article = Article(title="������", content="������")

    db.session.add(article)

    db.session.commit()

    return "��ӳɹ�"
@app.route('/get')
def get():
    article = Article.query.filter_by(id=2)[0]
    print(article.title)
    return "��ѯ�ɹ�"
@app.route('/put/kb')
def put():
    article = Article.query.filter_by(id=2)[0]
    article.title = "������"
    username = request.args.get("username")
    password = request.args.get("password")
    term = request.args.get("term")
    kb = get_kb(username, password, term)

    article.content = kb

    db.session.commit()
    return "�޸ĳɹ�"
@app.route('/delete')
def delete():
    Article.query.filter_by(id=2).delete()

    db.session.commit()
    return "ɾ���ɹ�"
@app.route('/')
def hello():

    engine = db.get_engine()
    with engine.connect() as connect:
        res = connect.execute('select 1')
        print(res.fetchone())
    return "hello"
#############################################################################################################
class Longin():

    def __init__(self, user, password, login_url, login_KeyUrl):
        # ��ʼ����������
        self.Username = user
        self.Password = password
        nowTime = lambda: str(round(time.time() * 1000))
        self.now_time = nowTime()
        self.login_url = login_url
        self.login_Key = login_KeyUrl

    def Get_indexHtml(self):
        # ��ȡ����ϵͳ��վ
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
        # ��ȡ��csrftoken
        lxml = etree.HTML(self.response)
        self.csrftoken = lxml.xpath("//input[@id='csrftoken']/@value")[0]

    def Get_PublicKey(self):
        # ��ȡ�����ܹ�Կ
        key_html = self.session.get(self.login_Key + self.now_time)
        key_data = key_html.json()
        self.modulus = key_data["modulus"]
        self.exponent = key_data["exponent"]

    def Get_RSA_Password(self):
        # ����RSA��������
        rsaKey = RSAJS.RSAKey()
        rsaKey.setPublic(HB64().b642hex(self.modulus), HB64().b642hex(self.exponent))
        self.enPassword = HB64().hex2b64(rsaKey.encrypt(self.Password))

    def Longin_Home(self):
        # ��¼��Ϣ�Ż�,�ɹ�����session����
        self.Get_indexHtml()
        self.Get_csrftoken()
        self.Get_PublicKey()
        self.Get_RSA_Password()
        login_data = [("csrftoken", self.csrftoken), ("yhm", self.Username), ("mm", self.enPassword),
                      ("mm", self.enPassword)]
        login_html = self.session.post(self.login_url + self.now_time, data=login_data)
        # ���ύ�ı�����ȷ�ģ�url����ת����ҳ�����Դ˴�����url��û����ת���ж��Ƿ��¼�ɹ�
        if login_html.url.find("login_slogin.html") == -1:  # -1û�ҵ���˵���Ѿ���ת����ҳ
            print("��¼�ɹ�")
            return self.session
        else:
            print("�û��������벻��ȷ����¼ʧ��")
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
def Cj(session, cj_url):
    data = {"xnm": 2021, "xqm": 12, "queryModel.showCount": 15, "queryModel.currentPage": 1}
    table_info = session.post(cj_url, data=data).json()

    for each in table_info["items"]:
        print(each)
        plt = r'{} | {:<8d} | {:<13d} | {:<15d} | {:<22d} | {:<30d}'
        print(plt.format(each["xqjmc"], each["jc"], each["cdmc"], each["zcd"], each["kcmc"], each['xm']))
def login_to_kb(username: str, password: str, term: str):
    # ��¼��ҳurl
    login_url = "http://jwgl.suse.edu.cn/xtgl/login_slogin.html?language=zh_CN&_t="
    # ����PublicKey��URL
    login_KeyUrl = "http://jwgl.suse.edu.cn/xtgl/login_getPublicKey.html?time="
    # ��¼��Ŀα�URL
    table_url = "http://jwgl.suse.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151"

    zspt = Longin(username, password, login_url, login_KeyUrl)
    response_cookies = zspt.Longin_Home()
    print(response_cookies.cookies)
    table = TimeTable(response_cookies, table_url, term)
    return table
def login_to_cj(username: str, password: str):
    # ��¼��ҳurl
    login_url = "http://jwgl.suse.edu.cn/xtgl/login_slogin.html?language=zh_CN&_t="
    # ����PublicKey��URL
    login_KeyUrl = "http://jwgl.suse.edu.cn/xtgl/login_getPublicKey.html?time="
    # ��¼��Ŀα�URL
    table_url = "http://jwgl.suse.edu.cn/kbcx/xskbcx_cxXsKb.html?gnmkdm=N2151"
    # ��¼��ĳɼ�URL
    cj_url = "https://jwgl.suse.edu.cn/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005"

    zspt = Longin(username, password, login_url, login_KeyUrl)
    response_cookies = zspt.Longin_Home()
    print(response_cookies.cookies)
    table = TimeTable(response_cookies, table_url)
    #cj = Cj(response_cookies, cj_url)
def get_kb(username: str, password: str, term: str):
    kb = login_to_kb("19171040207", "lhz233666", "now")
    # i = 0
    # for each in kb[0]:
    #     if i % 6 == 0:
    #         print("\n")
    #     print(each, end=" ")
    #     i += 1
    # print(len(kb[0]))
    return str(kb[0])
###############################################################################################

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8000)

