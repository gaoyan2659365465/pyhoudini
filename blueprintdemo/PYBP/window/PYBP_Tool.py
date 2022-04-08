from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class PYBP_Tool(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)#开启qss
        self.initLayout()
        self.initUI()
        
    def initLayout(self):
        """初始化布局"""
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(0)#各控件间距
        self.h_layout.setAlignment(Qt.AlignLeft)
        self.h_layout.setContentsMargins(0,0,0,0)#layout边缘
        self.setLayout(self.h_layout)
    
    def initUI(self):
        """初始化UI"""
        self.addButton("文件")
        self.addButton("编辑")
        self.addButton("资产")
        self.addButton("查看")
        self.move(5,40)
    
    def addButton(self,name):
        """工具栏添加按钮"""
        self.button = QPushButton()
        self.button.setMinimumSize(44,20)
        self.button.setMaximumSize(44,20)
        self.button.setText(name)
        self.button.setObjectName("PYBP_Tool_Button")
        self.h_layout.addWidget(self.button)
        