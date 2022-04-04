#Houdini内容浏览器笔记本页面
import json
import uuid#生成随机名字
import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from widget.StyleTool import *
from widget.CaptureImage import CaptureScreen


def getJsonData(path):
    """获取json文件"""
    try:
        with open(path, 'r',encoding='utf-8') as json_file:
            data = json_file.read()
            result = json.loads(data)
    except:
        try:
            with open(path, 'r',encoding='gbk') as json_file:
                data = json_file.read()
                result = json.loads(data)
        except:
            print("json文件读取失败")
            return None
    return result

class QHoudiniNoteBook(QTextEdit):
    """笔记本页面类"""
    def __init__(self, parent=None):
        super(QHoudiniNoteBook, self).__init__(parent)
        self.setFrameShape(QFrame.NoFrame)#无边框
        self.setStyleSheet(u"background-color: rgb(44, 49, 57);")
        
        self.v_layout = QVBoxLayout(self)
        self.h_layout = QHBoxLayout()
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)
        
        button = QPushButton("", self)#关闭按钮
        button.clicked.connect(self.close)
        button.setMinimumSize(QSize(30, 30))
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.setStyleSheet(NodeWidgetButtonStyle)
        addStyleIcon(button,"cil-chevron-circle-left-alt.png")
        self.h_layout.addWidget(button)
        
        self.button2 = QPushButton("",self)#保存按钮
        self.button2.clicked.connect(self.saveBook)
        self.button2.setMinimumSize(QSize(30, 30))
        self.button2.setCursor(QCursor(Qt.PointingHandCursor))
        self.button2.setStyleSheet(NodeWidgetButtonStyle)
        addStyleIcon(self.button2,"cil-save.png")
        self.h_layout.addWidget(self.button2)
        
        self.button3 = QPushButton("",self)#截图按钮
        self.button3.clicked.connect(self.captureScreen)
        self.button3.setMinimumSize(QSize(30, 30))
        self.button3.setCursor(QCursor(Qt.PointingHandCursor))
        self.button3.setStyleSheet(NodeWidgetButtonStyle)
        addStyleIcon(self.button3,"cil-cut.png")
        self.h_layout.addWidget(self.button3)

        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.v_layout.setSpacing(0)
        self.v_layout.setAlignment(Qt.AlignTop)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.h_layout.setSpacing(0)
        self.h_layout.setAlignment(Qt.AlignLeft)
        
        self.bookpath = ""
        
    def saveBook(self):
        """保存笔记本"""
        textdata = self.toHtml()
        data = {"type":"QHoudiniTextWidget",
            "data":textdata}
        json.dump(data, open(self.bookpath,'w'),ensure_ascii=False,indent=4)
    
    def initBook(self,path):
        """初始化笔记本"""
        self.bookpath = path
        data = getJsonData(path)
        if data["type"]=="QHoudiniTextWidget":
            textdata = data["data"]
            self.setText(textdata)
    
    def captureScreen(self):
        """截图"""
        self.windows = CaptureScreen()
        self.windows.saveimage.connect(self.setImage)
        self.windows.show()
    
    def setImage(self,image):
        """设置截图"""
        # 生成一个随机字符串
        uuid_str = uuid.uuid4().hex
        resp = os.path.relpath(self.bookpath)#绝对路径转相对路径
        print(resp)
        name = resp[:-5] + "_" + uuid_str + '.jpg'
        image.save(name, quality=95)   # 保存图片到当前文件夹中
        
        # 0.获取光标对象
        tc = self.textCursor()
        # 1.创建一个 QTextImageFormat 对象
        tif = QTextImageFormat()
        # 2.设置相关的参数
        tif.setName(name)    #图片名称
        tc.insertImage(tif)          #插入图片