#Houdini内容浏览器可以显示文件夹和笔记
import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from widget.FlowLayout import FlowLayout
from widget.StyleTool import *

ContentBrowserFilePath = FilePath[:-7] + "data/ContentBrowser"

class QFolderWidget(QWidget):
    """内容浏览器的文件夹"""
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.folderPath = ""
        
        label = QLabel(self)
        imagescale = 2.5
        label.setPixmap(QPixmap(FilePath + "image/T_folder.png")\
            .scaled(264/imagescale,177/imagescale,Qt.IgnoreAspectRatio,Qt.SmoothTransformation))
        label.setFixedSize(264/imagescale,177/imagescale)
        self.label_text = QLabel(self)
        self.label_text.setText("新建文件夹")
        self.label_text.setFont(QFont("Microsoft YaHei",15,QFont.Bold))#文字尺寸默认10
        self.label_text.setStyleSheet("color: #a4a4a4 ")
        self.v_layout = QVBoxLayout(self)
        self.v_layout.setSpacing(0)#各控件间距
        self.v_layout.setContentsMargins(4,4,4,4)#layout边缘
        self.v_layout.addWidget(label,0,Qt.AlignHCenter)
        self.v_layout.addWidget(self.label_text,0,Qt.AlignHCenter)
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)#右键菜单
        self.customContextMenuRequested.connect(self.createRightmenu)  # 连接到菜单显示函数
    
    def setFolderName(self,name,path):
        """设置文件夹名字"""
        self.label_text.setText(name)
        print(path)
        self.folderPath = path
    
    def focusOutEvent(self, arg__1):
        """失去焦点"""
        name = self.label_text.text()
        newname = self.lineedit.text()
        self.label_text.setText(newname)
        self.label_text.show()
        self.lineedit.close()
        
        #print("name:" + name)
        #print("newname:" + newname)
        #print("folderPath:" + self.folderPath)
        #print("folderPath[:-len(name)]:" + self.folderPath[:-len(name)])
        #print(-len(name))
        #print(self.folderPath[:-len(name)]+newname)
        os.rename(self.folderPath,self.folderPath[:-len(name)]+newname)#修改文件夹名
        self.folderPath = self.folderPath[:-len(name)]+newname
    
    def RightMenuEvent(self):
        """右键重命名点击事件"""
        self.lineedit = QLineEdit(self)
        self.lineedit.focusOutEvent = self.focusOutEvent
        self.lineedit.setText(self.label_text.text())
        self.lineedit.setFocus()#焦点
        self.v_layout.addWidget(self.lineedit)
        self.label_text.hide()
        
    def createRightmenu(self):
        """创建右键菜单函数"""
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'重命名',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionA)
        self.actionA.triggered.connect(self.RightMenuEvent)
        
        self.actionB = QAction(u'删除',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionB)
        def RightMenuBEvent():
            """右键删除点击事件"""
            for root, dirs, files in os.walk(self.folderPath, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.folderPath)
            self.parent().initWidgets()#刷新
        self.actionB.triggered.connect(RightMenuBEvent)
        #声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，
        self.groupBox_menu.popup(QCursor.pos())
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.buttons() == Qt.LeftButton:
            #把路径传递给父控件
            self.parent().openFolder(self.folderPath)
        super().mousePressEvent(event)

class QContentBrowserWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(0)
        self.v_layout.setContentsMargins(0,0,0,0)#layout边缘
        self.v_layout.setAlignment(Qt.AlignTop)
        self.h_layout = QHBoxLayout()
        self.button = QPushButton("",self)
        self.button.clicked.connect(self.previous)
        self.button.setMinimumSize(QSize(30, 30))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet(NodeWidgetButtonStyle)
        addStyleIcon(self.button,"cil-chevron-circle-left-alt.png")
        
        self.h_layout.addWidget(self.button)
        self.h_layout.addStretch()
        self.g_layout = FlowLayout()
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addLayout(self.g_layout)
        self.setLayout(self.v_layout)
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)#右键菜单
        self.customContextMenuRequested.connect(self.createRightmenu)  # 连接到菜单显示函数
        
        self.BrowserPath = ""#这个路径是根路径的相对路径
        
        self.initWidgets()#初始化
        
    def addWidget(self,widget):
        """添加新项"""
        self.g_layout.addWidget(widget)
    
    def removeAllItem(self):
        """删除所有子项"""
        items = []
        for i in range(self.g_layout.count()):
            item = self.g_layout.itemAt(i).widget()
            items.append(item)
        for item in items:
            self.g_layout.removeWidget(item)
            item.close()
    
    def initWidgets(self):
        """初始化所有子控件"""
        self.removeAllItem()
        path = ContentBrowserFilePath + self.BrowserPath
        
        if os.path.isdir(path) == True:
            for dir in os.listdir(path):#获取路径下所有文件名/文件夹名
                if os.path.isdir(path+"/"+dir):
                    folderWidget = QFolderWidget(self)
                    folderWidget.setFolderName(dir,path+"/"+dir)
                    self.addWidget(folderWidget)
                elif os.path.isfile(path+"/"+dir):
                    pass
        else:
            os.makedirs(path)
            
    def createRightmenu(self):
        """创建右键菜单函数"""
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'新建文件夹',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionA)
        def RightMenuEvent():
            """右键新建文件夹点击事件"""
            FolderName = "新建文件夹"
            path_ = self.BrowserPath+"/"+FolderName
            num = 2
            while True:
                if os.path.isdir(ContentBrowserFilePath + path_) == True:
                    #如果目录存在
                    path_ = self.BrowserPath[:-(len(FolderName)+1)]
                    FolderName = "新建文件夹" + " (" + str(num) + ")"
                    path_ = self.BrowserPath+"/"+FolderName
                    num = num + 1
                else:
                    os.makedirs(ContentBrowserFilePath + path_)
                    break
            folderWidget = QFolderWidget(self)
            folderWidget.setFolderName(FolderName,ContentBrowserFilePath + path_)
            self.addWidget(folderWidget)
        self.actionA.triggered.connect(RightMenuEvent)
        
        self.actionB = QAction(u'新建笔记',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionB)
        def RightMenuBEvent():
            """右键新建笔记点击事件"""
            pass
        self.actionB.triggered.connect(RightMenuBEvent)
        
        self.actionC = QAction(u'刷新',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionC)
        def RightMenuCEvent():
            """右键刷新点击事件"""
            self.initWidgets()#初始化
        self.actionC.triggered.connect(RightMenuCEvent)
        
        #声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，
        self.groupBox_menu.popup(QCursor.pos())
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        self.setFocus()#焦点
        super().mousePressEvent(event)
    
    def openFolder(self,path):
        """打开文件夹"""
        self.BrowserPath = path[len(ContentBrowserFilePath):]
        self.initWidgets()#初始化
    
    def previous(self):
        """上一步"""
        path = ""
        list0 = self.BrowserPath.split("/")
        if len(list0)>0:
            for i in range(len(list0)-1):
                if list0[i] != "":
                    path = path +"/"+ list0[i]
        self.BrowserPath = path
        self.initWidgets()#初始化