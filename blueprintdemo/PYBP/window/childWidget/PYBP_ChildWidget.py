from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class PYBP_ChildWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.initQss()
        self.splitter = QSplitter(Qt.Horizontal)#水平
        self.splitter = QSplitter(Qt.Vertical)#垂直
        self.paintrect = QRect(10,10,200,150)
        self.pen1 = QPen(QColor("#6e562f"))
        self.pen1.setWidthF(10)
        
    def initQss(self):
        """初始化Qss"""
        class CommonHelper:
            """加载样式"""
            @staticmethod
            def readQss(style):
                with open(style,'r',encoding='utf-8') as f:
                    return f.read()
        styleFile = './PYBP/qss/style.qss'
        self.qssStyle = CommonHelper.readQss(styleFile)
        QApplication.instance().setStyleSheet(self.qssStyle)
    
    def getPaintRect(self):
        """计算需要绘制的坐标"""
        p = self.paintrect
        w = p.width()/2
        h = p.height()/2
        x = p.x() + w - w/2
        y = p.y() + h - h/2
        
        line1 = QLine(QPoint(p.x(),p.y()),QPoint(x,y))
        line2 = QLine(QPoint(p.x()+p.width(),p.y()),QPoint(x+w,y))
        line3 = QLine(QPoint(p.x(),p.y()+p.height()),QPoint(x,y+h))
        line4 = QLine(QPoint(p.x()+p.width(),p.y()+p.height()),QPoint(x+w,y+h))
        lines = [line1,line2,line3,line4]
        return QRect(x,y,w,h),lines
    
    def getPaintRect2(self):
        """计算边缘黄色条坐标"""
        line1 = QLine(QPoint(0,0),QPoint(self.width(),0))
        line2 = QLine(QPoint(self.width(),0),QPoint(self.width(),self.height()))
        line3 = QLine(QPoint(0,0),QPoint(0,self.height()))
        line4 = QLine(QPoint(0,self.height()),QPoint(self.width(),self.height()))
        lines = [line1,line2,line3,line4]
        return lines
    
    def paintEvent(self, a0):
        """重载绘制事件"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)#反走样
        painter.setPen(QColor(255, 255, 255))
        painter.drawRect(self.paintrect)
        paintrect2,lines = self.getPaintRect()
        painter.drawRect(paintrect2)
        for i in lines:
            painter.drawLine(i)
        
        painter.setPen(self.pen1)
        lines2 = self.getPaintRect2()
        for i in lines2:
            painter.drawLine(i)
        return super().paintEvent(a0)