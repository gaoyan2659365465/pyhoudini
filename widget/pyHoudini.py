#coding=utf-8

import os
import json
import zipfile
import configparser#读取ini配置文件
from threading import Thread
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from widget.SetingWidget import SetingWidget
import server.Check.UpdateCheck
from widget.pathjson.NodeIconPath import NodeIconPath
from widget.QHoudiniEdit import QHoudiniEdit
from widget.CodeActive import CodeAC
from widget.NodeScrollArea import NodeScrollArea
from widget.StyleTool import *


PATH = ""
SORT = ""
SCRPATH=""

class NodeWidget(QWidget):
    def __init__(self,parent,icon):
        super().__init__(parent)
        self.icon = icon
        self.button = QPushButton("",self)
        self.button.clicked.connect(self.close)
        self.button.setMinimumSize(QSize(40, 40))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet(NodeWidgetButtonStyle)
        addStyleIcon(self.button,"cil-chevron-circle-left-alt.png")
        
        self.button2 = QPushButton("",self)
        self.button2.clicked.connect(self.saveTextEdit)
        self.button2.setMinimumSize(QSize(40, 40))
        self.button2.setCursor(QCursor(Qt.PointingHandCursor))
        self.button2.setStyleSheet(NodeWidgetButtonStyle)
        addStyleIcon(self.button2,"cil-save.png")
        
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(icon.icon_path))
        self.label.setFixedSize(48,48)
        
        #----------收藏按钮------------
        self.button3 = QPushButton("",self)
        self.button3.clicked.connect(self.hoardingClickedEvent)
        self.button3.setMinimumSize(QSize(40, 40))
        self.button3.setCursor(QCursor(Qt.PointingHandCursor))
        self.button3.setStyleSheet(NodeWidgetButtonStyle)
        icon2 = QIcon()
        icon2.addFile(FilePath + "image/xin.png", QSize(48,48), QIcon.Normal, QIcon.Off)
        self.button3.setIcon(icon2)
        #------------------------------
        self.addLayout()
        
        self.text_Edit = QHoudiniEdit(self)#QPlainTextEdit QTextEdit
        self.text_Edit.setGeometry(10,70,self.width()-20,self.height()-100)
        
        self.initTextEdit()
        self.setStyleSheet(NodeWidgetStyle)
    
    def addLayout(self):
        """添加各种Layout"""
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.h_layout.setSpacing(10)
        self.v_layout.setSpacing(0)
        self.h_layout.setAlignment(Qt.AlignLeft)
        self.v_layout.setAlignment(Qt.AlignTop)
        self.h_layout.setContentsMargins(10,0,0,0)#layout边缘
        self.v_layout.setContentsMargins(0,10,0,0)#layout边缘
        self.h_layout.addWidget(self.button)
        self.h_layout.addWidget(self.button2)
        self.h_layout.addWidget(self.button3)
        self.h_layout.addWidget(self.label)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)
    
    def hoardingClickedEvent(self):
        """收藏点击按钮"""
        icon2 = QIcon()
        icon2.addFile(FilePath + "image/xin-1.png", QSize(48,48), QIcon.Normal, QIcon.Off)
        self.button3.setIcon(icon2)
    
    def resizeEvent(self, a0):
        if self.text_Edit:
            self.text_Edit.setGeometry(10,70,self.width()-20,self.height()-100)
    
    def initTextEdit(self):
        """初始化富文本"""
        path = PATH[:-7] + '/data/'+SORT+"/"+ self.icon.icon_name + ".json"
        if os.path.exists(path) == False:
            return
        with open(path, 'r') as json_file:
            data = json_file.read()
            try:
                result = json.loads(data)
            except:
                data.encode(encoding='gbk').decode(encoding='utf-8')
                result = json.loads(data)
            self.text_Edit.loadWidget(result)
    
    def saveTextEdit(self):
        """保存富文本"""
        path = PATH[:-7] + '/data/'+SORT+"/"
        path_json = path + self.icon.icon_name + ".json"
        if not os.path.isdir(path):
            os.makedirs(path)
        data = self.text_Edit.saveWidget()
        json.dump(data, open(path_json,'w'),ensure_ascii=False,indent=4)
        
    def paintEvent(self, event):
        """重载-绘制"""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
        
class IconsWidget(QWidget):
    click=Signal(object)
    def __init__(self,p,i):
        super().__init__(p)
        self.icon_path = PATH+i[1][5:]
        if self.icon_path[-3:] != 'svg':
            self.icon_path = PATH+'/icons/OBJ/geo.svg'
        if os.path.exists(self.icon_path) == False:
            self.icon_path = PATH+'/icons/OBJ/geo.svg'
        self.icon_name = i[0]#0是名字
        label = QLabel(self)
        label.setPixmap(QPixmap(self.icon_path)\
            .scaled(p.iconsize,p.iconsize,Qt.IgnoreAspectRatio,Qt.SmoothTransformation))
        label.setFixedSize(p.iconsize,p.iconsize)#图标尺寸默认48
        self.label_text = QLabel(self)
        self.label_text.setText(self.icon_name)
        self.label_text.setFont(QFont("Microsoft YaHei",p.iconfontsize,QFont.Bold))#文字尺寸默认10
        self.label_text.setStyleSheet("color: #a4a4a4 ")
        self.setStyleSheet(IconsWidgetStyle)
        v_layout = QVBoxLayout(self)
        v_layout.setSpacing(0)#各控件间距
        v_layout.setContentsMargins(4,4,4,4)#layout边缘
        v_layout.addWidget(label,0,Qt.AlignHCenter)
        v_layout.addWidget(self.label_text,0,Qt.AlignHCenter)
    
    def mousePressEvent(self, a0):
        self.click.emit(self)
    
    def paintEvent(self, event):
        """重载-绘制"""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
    
class HoudiniHelp(QWidget):
    def __init__(self,parent):
        super().__init__()
        self.pyhoudiniwidget = parent#主窗体
        self.initIniFlie()
        self.initIconsDir()
        self.initSize()
        self.sort = SORT
        self.nodeiconpath = NodeIconPath(self.sort)
        self.initWidget()
        
        self.selectNode()
        
    def initNodeIconPath(self,name):
        """初始化图标路径"""
        global SORT
        SORT = name
        self.sort = name
        self.nodeiconpath = NodeIconPath(name)
        self.extention = CodeAC(self.line_edit)
        self.extention.active_script(self.nodeiconpath.names)
        self.selectNode()
        self.pyhoudiniwidget.miniw.initNodeIconPath(name)
                
    def initIniFlie(self):
        """初始化配置文件"""
        global SCRPATH
        global PATH
        global SORT
        conf = configparser.ConfigParser()
        # 读取.ini文件
        conf.read(FilePath+"config.ini")
        # get()函数读取section里的参数值
        SCRPATH  = conf.get("config","SCRPATH")
        PATH = FilePath[:-1]
        SORT  = conf.get("config","SORT")
        self.default_size = conf.get("config","DefaultSize")
        self.iconsize = int(conf.get("config","iconsize"))
        self.iconfontsize = int(conf.get("config","iconfontsize"))
        self.selectheight = int(conf.get("config","selectheight"))
    
    def initSize(self):
        """初始化窗口尺寸"""
        self.default_size = self.default_size.split(',')#字符串转列表
        self.resize(int(self.default_size[0]),int(self.default_size[1]))
    
    def initIconsDir(self):
        """判断图标文件夹是否存在"""
        if os.path.isdir(PATH + "/icons") == True:
            print("存在icons目录")
        else:
            print("不存在icons目录,正在解压...")
            try:
                z = zipfile.ZipFile(SCRPATH, 'r')
                z.extractall(path=PATH + "/icons")
                z.close()
            except:
                print("第一次运行请手动修改此处的图标zip路径并重新打开")
                os.system(r'notepad '+__file__[:-12]+"config.ini")
    
    def initWidget(self):
        """初始化子控件"""
        self.setbutton = QPushButton("",self)
        self.setbutton.setFixedSize(self.selectheight,self.selectheight)
        self.setbutton.clicked.connect(self.setingClickedEvent)
        self.setbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.setbutton.setStyleSheet(HoudiniHelpSetingButton)
        addStyleIcon(self.setbutton,"icon_settings.png")
        self.setbutton.setIconSize(QSize(20, 20))
        
        self.line_edit = QLineEdit(self)
        self.line_edit.setFixedHeight(self.selectheight)
        self.line_edit.setAttribute(Qt.WA_InputMethodEnabled, False)#屏蔽输入法
        self.line_edit.setStyleSheet(HoudiniHelpline_edit)
        self.line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"搜索节点..", None))
        self.line_edit.returnPressed.connect(self.selectNode)
        self.extention = CodeAC(self.line_edit)
        #代码补全-------------------------
        self.extention.active_script(self.nodeiconpath.names)
        #---------------------------------------

        self.selectbutton = QPushButton("",self)
        self.selectbutton.clicked.connect(self.selectNode)
        self.selectbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.selectbutton.setFixedSize(self.selectheight-4,self.selectheight-4)
        self.selectbutton.setStyleSheet(HoudiniHelpselectbutton)
        addStyleIcon(self.selectbutton,"cil-magnifying-glass.png")
        
        self.scrollArea = NodeScrollArea(self)
        self.scrollArea.resize(self.width(), self.height()-self.selectheight)
        
        self.select_hlayout = QHBoxLayout(self.line_edit)
        self.select_hlayout.setSpacing(0)
        self.select_hlayout.setContentsMargins(0,0,2,0)
        self.select_hlayout.addStretch()
        self.select_hlayout.addWidget(self.selectbutton)
        self.h_layout = QHBoxLayout()#横向
        self.h_layout.setSpacing(0)
        self.h_layout.setContentsMargins(0,0,0,0)
        self.h_layout.setAlignment(Qt.AlignLeft)
        self.h_layout.addWidget(self.setbutton)
        self.h_layout.addWidget(self.line_edit)
        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(0)
        self.v_layout.setContentsMargins(0,0,0,0)
        self.v_layout.setAlignment(Qt.AlignTop)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.scrollArea)
        self.setLayout(self.v_layout)
        
    def iconClickedEvent(self,icon:IconsWidget):
        """图标点击事件"""
        try:
            self.nodewidget.close()#防止从节点直接进入页面的重叠bug
        except:pass
        self.nodewidget = NodeWidget(self,icon)
        self.nodewidget.resize(self.width(), self.height())
        self.nodewidget.show()
        
    def setingClickedEvent(self):
        """点击设置按钮"""
        self.setwidget = SetingWidget()
        self.setwidget.save.connect(self.initNodeIconPath)
        self.setwidget.show()
    
    def selectNode(self):
        """点击搜索"""
        self.scrollArea.removeAllItem()
        num_x = 0
        num_y = 0
        for i in self.nodeiconpath.paths:
            if i[0].find(self.line_edit.text()) != -1:
                label_widget = IconsWidget(self,i)
                label_widget.click.connect(self.iconClickedEvent)
                self.scrollArea.addItem(label_widget,num_x,num_y)
                label_widget.show()
                num_y = num_y+1
                if num_y>6:
                    num_y = 0
                    num_x = num_x+1

        self.scrollArea.updateAutomaticSize()
        
    def resizeEvent(self, a0):
        self.scrollArea.updateAutomaticSize()
        try:
            self.nodewidget.resize(self.width(), self.height())
        except:pass
    