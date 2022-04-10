#coding=utf-8
#节点的滚动框
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class NodeScrollArea(QScrollArea):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)#无边框
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)#隐藏横向滚动条
        self.nodeswidget = QWidget(self)
        self.setWidget(self.nodeswidget)#显示滚动条必须的
        self.g_layout = QGridLayout(self.nodeswidget)
        self.g_layout.setAlignment(Qt.AlignTop)#居左对齐
        self.g_layout.setContentsMargins(2,0,10,0)
        self.g_layout.setSpacing(0)
    
    def addItem(self,item,x,y):
        """添加子项"""
        self.g_layout.addWidget(item,x,y)
    
    def removeAllItem(self):
        """删除所有子项"""
        items = []
        for i in range(self.g_layout.count()):
            item = self.g_layout.itemAt(i).widget()
            items.append(item)
        for item in items:
            self.g_layout.removeWidget(item)
    
    def updateAutomaticSize(self):
        """自动设置节点所需要的尺寸"""
        self.nodeswidget.setMinimumSize(self.width(),self.nodeswidget.sizeHint().height())#设置滚动条的尺寸
        self.nodeswidget.resize(self.width(),self.nodeswidget.sizeHint().height())