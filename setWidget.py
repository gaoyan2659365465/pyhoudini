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
        self.line_edit3 = QLineEdit()
        self.h_layout3.addWidget(self.label3)
        self.h_layout3.addWidget(self.line_edit3)
        
        self.h_layout2 = QHBoxLayout()
        self.label2 = QLabel("展示类型:")
        self.combo_box = QComboBox()
        list01 = ["VOP","SOP"]
        self.combo_box.addItems(list01)
        self.h_layout2.addWidget(self.label2)
        self.h_layout2.addWidget(self.combo_box)
        
        self.h_layout4 = QHBoxLayout()
        self.label4 = QLabel("默认尺寸:")
        self.line_edit4_1 = QLineEdit()
        self.line_edit4_2 = QLineEdit()
        self.h_layout4.addWidget(self.label4)
        self.h_layout4.addWidget(self.line_edit4_1)
        self.h_layout4.addWidget(self.line_edit4_2)
        
        self.h_layout5 = QHBoxLayout()
        self.label5 = QLabel("图标尺寸:")
        self.line_edit5 = QLineEdit()
        self.h_layout5.addWidget(self.label5)
        self.h_layout5.addWidget(self.line_edit5)
        
        self.h_layout6 = QHBoxLayout()
        self.label6 = QLabel("文字尺寸:")
        self.line_edit6 = QLineEdit()
        self.h_layout6.addWidget(self.label6)
        self.h_layout6.addWidget(self.line_edit6)
        
        self.h_layout7 = QHBoxLayout()
        self.label7 = QLabel("搜索栏尺寸:")
        self.line_edit7 = QLineEdit()
        self.h_layout7.addWidget(self.label7)
        self.h_layout7.addWidget(self.line_edit7)
        
        self.v_layout.addLayout(self.h_layout3)
        self.v_layout.addLayout(self.h_layout2)
        self.v_layout.addLayout(self.h_layout4)
        self.v_layout.addLayout(self.h_layout5)
        self.v_layout.addLayout(self.h_layout6)
        self.v_layout.addLayout(self.h_layout7)
        
        self.updatebutton = QPushButton("打印最新版网址",self)
        self.updatebutton.clicked.connect(self.updateEvent)
        self.v_layout.addWidget(self.updatebutton)
        
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
        self.line_edit3.setText(SCRPATH)
        SORT  = conf.get("config","SORT")
        
        for i in range(self.combo_box.count()):
            if self.combo_box.itemText(i) == SORT:
                self.combo_box.setCurrentIndex(i)   # 设置默认值
        
        default_size = conf.get("config","DefaultSize")
        default_size = default_size.split(',')#字符串转列表
        self.line_edit4_1.setText(default_size[0])
        self.line_edit4_2.setText(default_size[1])
        
        iconsize = conf.get("config","iconsize")
        self.line_edit5.setText(iconsize)
        
        iconfontsize = conf.get("config","iconfontsize")
        self.line_edit6.setText(iconfontsize)
        
        selectheight = conf.get("config","selectheight")
        self.line_edit7.setText(selectheight)
    
    def saveEvent(self):
        """点击保存按钮"""
        conf = configparser.ConfigParser()
        conf.read(__file__[:-12]+"config.ini")
        
        conf.set('config', 'SCRPATH', self.line_edit3.text())
        
        conf.set('config', 'SORT', self.combo_box.currentText())
        
        size_1 = self.line_edit4_1.text()
        size_2 = self.line_edit4_2.text()
        conf.set('config', 'DefaultSize', size_1+','+size_2)
        
        conf.set('config', 'iconsize', self.line_edit5.text())
        
        conf.set('config', 'iconfontsize', self.line_edit6.text())
        
        conf.set('config', 'selectheight', self.line_edit7.text())
        
        conf.write(open(__file__[:-12]+"config.ini", 'w'))
        
        print("已保存请重新打开插件^-^")
    
    def updateEvent(self):
        """打开更新网页"""
        print("-------------------------------")
        print("最新版更新网址:https://gitee.com/seerhugan/py-houdini")
        print("与开发者交流:QQ:2659365465")
        print("-------------------------------")

# [config]
# PATH = C:\Users\26593\Desktop\pyhoudini\
# SCRPATH = C:/Program Files/Side Effects Software/Houdini 19.0.383/houdini/config/Icons/icons.zip
# SORT = VOP