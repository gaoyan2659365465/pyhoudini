from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class PYBP_Button(QPushButton):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)#开启qss
        self.button_type = 0
        self._color_outline = QColor("#000000")
        self._pen = QPen(self._color_outline)
        self._color_background = QColor("#ffffff")
        self._color_background2 = QColor("#2f2f2f")
        self._brush = QBrush(self._color_background)
        self._brush2 = QBrush(self._color_background2)
        self.qsscore="PYBP_Button:hover{\
                                background-color: #9a4e34;\
                                border-style:solid;/* 边框风格 */\
                                border-width:6px;/* 边框宽度 */\
                                border-top-color:qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #000000, stop:0.333 #66dddddd,stop:1 #00b2b2b2);/* 上边框颜色 */\
                                border-bottom-color:qlineargradient(x1:0, y1:1, x2:0, y2:0, stop:0 #000000, stop:0.333 #66dddddd,stop:1 #00b2b2b2);/* 下边框颜色 */\
                                border-left-color:qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #000000, stop:0.333 #66dddddd,stop:1 #00b2b2b2);/* 左边框颜色 */\
                                border-right-color:qlineargradient(x1:1, y1:0, x2:0, y2:0, stop:0 #000000, stop:0.333 #66dddddd,stop:1 #00b2b2b2);/* 右边框颜色 */\
                                }\
                    PYBP_Button:pressed{\
                                background-color:qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #804d4d4d,stop:1 #222222);/* 背景色 */\
                                border-style:solid;/* 边框风格 */\
                                border-width:2px;/* 边框宽度 */\
                                border-top-color:qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #ff000000,stop:1 #B3828282);/* 上边框颜色 */\
                                border-bottom-color:qlineargradient(x1:0, y1:0, x2:0, y2:1,stop:0 #B3828282,stop:1 #ff000000);/* 下边框颜色 */\
                                border-left-color:qlineargradient(x1:0, y1:0, x2:1, y2:0,stop:0 #ff000000,stop:1 #B3828282);/* 左边框颜色 */\
                                border-right-color:qlineargradient(x1:0, y1:0, x2:1, y2:0,stop:0 #B3828282,stop:1 #ff000000);/* 右边框颜色 */\
                            }"
    
    def setButtonColor(self,num):
        """设置按钮的背景颜色"""
        if num==0:#白色
            color = "#b2b2b2"
        elif num==1:#红色
            color = "#9a4e34"
        self.qsscore = self.qsscore.replace("#9a4e34", color)
        self.setStyleSheet(self.qsscore)
    
    def setButtonType(self,num):
        """设置按钮类型"""
        if num==0:#最小化
            self.button_type = 0
            self.setMaximumSize(27,17)
            self.setMinimumSize(27,17)
        elif num==1:#最大化
            self.button_type = 1
            self.setMaximumSize(24,17)
            self.setMinimumSize(24,17)
        elif num==2:#关闭
            self.button_type = 2
            self.setMaximumSize(43,17)
            self.setMinimumSize(43,17)
            self.setButtonColor(1)
        elif num==3:#还原最大化
            self.button_type = 3
            self.setMaximumSize(24,17)
            self.setMinimumSize(24,17)
        
    def paintEvent(self, event):
        """重载-绘制"""
        super().paintEvent(event)
        if self.button_type == 0:
            painter = QPainter(self)
            painter.setBrush(self._brush)
            painter.setPen(self._pen)
            painter.drawRect(7, 8, 11, 4)
        elif self.button_type == 1:
            painter = QPainter(self)
            painter.setBrush(self._brush)
            painter.setPen(self._pen)
            painter.drawRect(5, 4, 13, 9)
            painter.setBrush(self._brush2)
            painter.setPen(self._pen)
            painter.drawRect(8, 8, 7, 3)
        elif self.button_type == 2:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, False)#反走样
            path_content = QPainterPath()
            path_content.setFillRule(Qt.WindingFill)
            painter.translate(20, 8)
            painter.rotate(-45)
            path_content.addRect(-6,-2,11,3)
            path_content.addRect(-2,-6,3,11)
            painter.setBrush(self._brush)
            painter.setPen(self._pen)
            painter.drawPath(path_content.simplified())
        elif self.button_type == 3:
            painter = QPainter(self)
            painter.setBrush(self._brush)
            painter.setPen(self._pen)
            painter.drawRect(8, 2, 9, 9)
            painter.setBrush(self._brush2)
            painter.setPen(self._pen)
            painter.drawRect(11, 5, 3, 3)
            #----------------------------------
            painter.setBrush(self._brush)
            painter.setPen(self._pen)
            painter.drawRect(6, 4, 9, 9)
            painter.setBrush(self._brush2)
            painter.setPen(self._pen)
            painter.drawRect(9, 7, 3, 3)