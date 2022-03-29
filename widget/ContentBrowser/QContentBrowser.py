#Houdini内容浏览器可以显示文件夹和笔记

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from widget.FlowLayout import FlowLayout
from widget.StyleTool import *

class QFolderWidget(QWidget):
    """内容浏览器的文件夹"""
    def __init__(self, parent = None):
        super().__init__(parent)
        label = QLabel(self)
        imagescale = 2.5
        label.setPixmap(QPixmap(FilePath + "image/T_folder.png")\
            .scaled(264/imagescale,177/imagescale,Qt.IgnoreAspectRatio,Qt.SmoothTransformation))
        label.setFixedSize(264/imagescale,177/imagescale)
        self.label_text = QLabel(self)
        self.label_text.setText("新建文件夹")
        self.label_text.setFont(QFont("Microsoft YaHei",15,QFont.Bold))#文字尺寸默认10
        self.label_text.setStyleSheet("color: #a4a4a4 ")
        v_layout = QVBoxLayout(self)
        v_layout.setSpacing(0)#各控件间距
        v_layout.setContentsMargins(4,4,4,4)#layout边缘
        v_layout.addWidget(label,0,Qt.AlignHCenter)
        v_layout.addWidget(self.label_text,0,Qt.AlignHCenter)

class QContentBrowserWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.g_layout = FlowLayout()
        self.setLayout(self.g_layout)
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)#右键菜单
        self.customContextMenuRequested.connect(self.createRightmenu)  # 连接到菜单显示函数
        
    def addWidget(self,widget):
        """添加新项"""
        self.g_layout.addWidget(widget)
    
    def initWidgets(self):
        """初始化所有子控件"""
        pass

    def createRightmenu(self):
        """创建右键菜单函数"""
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'新建文件夹',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionA)
        def RightMenuEvent():
            """右键新建文件夹点击事件"""
            folderWidget = QFolderWidget()
            self.addWidget(folderWidget)
        self.actionA.triggered.connect(RightMenuEvent)
        
        self.actionB = QAction(u'新建笔记',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionB)
        def RightMenuBEvent():
            """右键新建笔记点击事件"""
            folderWidget = QFolderWidget()
            self.addWidget(folderWidget)
        self.actionB.triggered.connect(RightMenuBEvent)
        #声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，
        self.groupBox_menu.popup(QCursor.pos())