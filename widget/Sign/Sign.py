#登陆注册功能
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWebEngineWidgets import *
from PySide2.QtWebChannel import QWebChannel
from widget.StyleTool import *
import requests
import http.cookiejar as cookielib
mysession = requests.session()
mysession.cookies = cookielib.LWPCookieJar(filename = "mysession.txt")

class HtmlView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        QWebEngineView.__init__(self, *args, **kwargs)
        self.setAttribute(Qt.WA_TranslucentBackground)#背景透明
        
        self.htmljs = HtmlJsChannel(self)
        self.channel = QWebChannel()
        self.channel.registerObject('pyjs', self.htmljs)
        self.page().setWebChannel(self.channel)
        self.page().setBackgroundColor(Qt.transparent)#web背景透明
        #隐藏滚动条
        self.page().settings().setAttribute(QWebEngineSettings.ShowScrollBars,False)

        path = "file:///"+FilePath.replace("\\", "/")+"/Sign/SignIN.html"
        url = QUrl(path)
        self.load(url)
    
class HtmlJsChannel(QObject):
    def __init__(self, parent):
        super().__init__(parent)
    @Slot(str,str)
    def formsignInBtn(self,Email,Password):
        url = "http://127.0.0.1:8000/signIn/"
        data = {"Email":Email,
                "Password":Password}
        res = mysession.post(url=url,data=data)
        print(res.text)
        if res.text == 'OK':
            print(isLogin())
            #self.parent().close()
        
    @Slot(str,str,str)
    def formsignUpBtn(self,User,Email,Password):
        url = "http://127.0.0.1:8000/signUp/"
        data = {"User":User,
                "Email":Email,
                "Password":Password}
        res = requests.post(url=url,data=data)
        print(res.text)
        if res.text == 'OK':
            self.parent().close()


def isLogin():
    """判断是否登录"""
    url = "http://127.0.0.1:8000/isLogin/"
    try:
        res = mysession.get(url=url)
    except:
        return False
    print(res.text)
    if res.text == '已登录':
        return True
    else:
        return False