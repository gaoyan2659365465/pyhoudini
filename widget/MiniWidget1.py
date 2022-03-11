#迷你模式的搜索框界面
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from widget.CodeActive import CodeAC
from widget.pathjson.NodeIconPath import NodeIconPath
from widget.StyleTool import *


class MiniWidget(QWidget):
    def __init__(self, parent=None,p=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)    #置顶
        self.setAttribute(Qt.WA_TranslucentBackground,True)#背景透明
        self.setMaxWidget(p)
        self.selectheight = 40
        
        self.line_edit = QLineEdit(self)
        self.line_edit.setFixedSize(500,self.selectheight)
        self.line_edit.setAttribute(Qt.WA_InputMethodEnabled, False)#屏蔽输入法
        self.line_edit.setStyleSheet(MiniWidgetline_edit)
        self.line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"搜索节点..", None))
        def selectNode():
            class icon():
                pass
            icon_path = '/icons/OBJ/geo1.svg'
            icon.icon_path = icon_path
            icon.icon_name = self.line_edit.text()
            self.maxwidget.isminiw = False
            self.maxwidget.show()
            self.maxwidget.houdinihelp.iconClickedEvent(icon)
            self.hide()
            self.maxwidget.isminiw = True
        self.line_edit.returnPressed.connect(selectNode)
        
        #代码补全-------------------------
        self.nodeiconpath = NodeIconPath(self.maxwidget.houdinihelp.sort)
        self.extention = CodeAC(self.line_edit)
        self.extention.active_script(self.nodeiconpath.names)
        #---------------------------------------
        
        self.maxbutton = QPushButton("",self)
        def maxshow():
            self.maxwidget.isminiw = False
            self.maxwidget.show()
            self.hide()
        self.maxbutton.clicked.connect(maxshow)
        self.maxbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.maxbutton.setFixedSize(self.selectheight-4,self.selectheight-4)
        self.maxbutton.setStyleSheet("border: none;border-radius: 15px;")
        addStyleIcon(self.maxbutton,"cil-pin.png")
        
        
        self.closebutton = QPushButton("",self)
        self.closebutton.clicked.connect(self.close)
        self.closebutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.closebutton.setFixedSize(self.selectheight-4,self.selectheight-4)
        self.closebutton.setStyleSheet("border: none;border-radius: 15px;")
        addStyleIcon(self.closebutton,"icon_close.png")
        
        self.select_hlayout = QHBoxLayout()
        self.select_hlayout.addStretch()
        self.select_hlayout.addWidget(self.maxbutton)
        self.select_hlayout.addWidget(self.closebutton)
        self.select_hlayout.setSpacing(0)
        self.select_hlayout.setContentsMargins(0, 0, 2, 0)
        self.line_edit.setLayout(self.select_hlayout)
    
    def setMaxWidget(self,widget):
        """保存大窗体"""
        self.maxwidget = widget
    
    def initNodeIconPath(self,name):
        self.nodeiconpath = NodeIconPath(name)
        self.extention = CodeAC(self.line_edit)
        self.extention.active_script(self.nodeiconpath.names)
        