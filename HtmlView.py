from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtWebEngineWidgets import *
from PySide2.QtWebChannel import QWebChannel
 
#https://cdn.jsdelivr.net/npm/wangeditor@latest/dist/wangEditor.min.js
# url = QUrl("file:///C:/Users/26593/Desktop/pyhoudini/data/GeometryNodes/adaptiveprune.html")
# view = HtmlView(self)
# view.load(url)
 
class HtmlView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        QWebEngineView.__init__(self, *args, **kwargs)
        self.channel = QWebChannel()
        self.channel.registerObject('backend', self.parent().htmljschannel)
        self.page().setWebChannel(self.channel)

    