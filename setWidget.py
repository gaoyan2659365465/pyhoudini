from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import configparser#读取ini配置文件

#设置界面


class SetWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.v_layout = QVBoxLayout()
        
        self.h_layout3 = QHBoxLayout()
        self.label3 = QLabel("图标目录:")
        self.line_edit2 = QLineEdit()
        self.h_layout3.addWidget(self.label3)
        self.h_layout3.addWidget(self.line_edit2)
        
        self.h_layout2 = QHBoxLayout()
        self.label2 = QLabel("展示类型:")
        self.combo_box = QComboBox()
        list01 = ["VOP","SOP"]
        self.combo_box.addItems(list01)
        self.h_layout2.addWidget(self.label2)
        self.h_layout2.addWidget(self.combo_box)
        
        self.v_layout.addLayout(self.h_layout3)
        self.v_layout.addLayout(self.h_layout2)
        
        self.savebutton = QPushButton("保存",self)
        self.savebutton.clicked.connect(self.saveEvent)
        self.v_layout.addWidget(self.savebutton)
        self.setLayout(self.v_layout)
        
        self.initIniFlie()
    
    def initIniFlie(self):
        """初始化配置文件"""
        conf = configparser.ConfigParser()
        # 读取.ini文件
        conf.read(__file__[:-12]+"config.ini")
        # get()函数读取section里的参数值
        SCRPATH  = conf.get("config","SCRPATH")
        self.line_edit2.setText(SCRPATH)
        SORT  = conf.get("config","SORT")
        
        for i in range(self.combo_box.count()):
            if self.combo_box.itemText(i) == SORT:
                self.combo_box.setCurrentIndex(i)   # 设置默认值
    
    def saveEvent(self):
        """点击保存按钮"""
        conf = configparser.ConfigParser()
        conf.read(__file__[:-12]+"config.ini")
        conf.set('config', 'SORT', self.combo_box.currentText())
        conf.write(open(__file__[:-12]+"config.ini", 'w'))

# [config]
# PATH = C:\Users\26593\Desktop\pyhoudini\
# SCRPATH = C:/Program Files/Side Effects Software/Houdini 19.0.383/houdini/config/Icons/icons.zip
# SORT = VOP