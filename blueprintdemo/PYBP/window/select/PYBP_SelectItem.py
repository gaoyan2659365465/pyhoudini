from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *


class PYBP_SelectItem(QWidget):
    click=Signal(object,object)#自定义点击信号
    
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)#开启qss
        self.initValue()
        self.resize(self.w_width,self.w_height)
    
    def initValue(self):
        """初始化变量"""
        self.w_width = 211#整体长度
        self.w_width_b = 25#贝塞尔曲线的长度
        self.w_height = 25#整体高度
        self.is_select = False#是否选择当前选项卡，变白色
        self._color_outline = QColor("#303030")
        self._pen = QPen(self._color_outline)
        self._color_background = QColor("#595959")
        self._brush = QBrush(self._color_background)
        
        self.is_click = False#是否点击
        self.is_select_x = False#是否悬浮X号
        self.pen_Text3  = QPen(QColor("#1b1b1b"))#叉号颜色
        self.font2 = QFont("SimHei", 8)
        
        self.press_pos = QPoint()#按下鼠标时的相对位置
        self.text = ""#浏览选项卡文字
    
    def setText(self,text):
        """设置选项卡文字"""
        self.text = text
    
    def setColor(self,is_select):
        """设置选项卡颜色"""
        if is_select:
            self._color_background = QColor("#7c7c7c")
        else:
            self._color_background = QColor("#595959")
        self._brush = QBrush(self._color_background)
        self.update()
    
    def bezier(self,x,y,x1,y1):
        """计算贝塞尔曲线"""
        x2 = (x+x1)/2
        return x2
    
    def enterEvent(self, a0: QEvent):#进入事件
        """重载-鼠标进入"""
        self.setMouseTracking(True)
        color = QColor("#363636")
        self.update()
    
    def leaveEvent(self, a0: QEvent):#离开事件
        """重载-鼠标离开"""
        self.setMouseTracking(False)
        self.is_select_x = False
        self.update()
    
    def mouseMoveEvent(self, a0: QMouseEvent):
        """重载-鼠标移动"""
        x = a0.pos().x()
        ww = self.w_width-self.w_width_b-9
        if x>ww and x<ww+10:
            self.is_select_x = True
            self.update()
        else:
            self.is_select_x = False
            self.update()
        super().mouseMoveEvent(a0)
    
    def mousePressEvent(self, a0: QMouseEvent):
        """重载-鼠标按下"""
        self.update()
        self.is_click = True
        self.click.emit(self,self.is_click)
        self.press_pos = a0.pos()
        super().mousePressEvent(a0)
    
    def mouseReleaseEvent(self,event):
        """重载-鼠标松开"""
        self.is_click = False
        self.click.emit(self,self.is_click)
        super().mouseReleaseEvent(event)
    
    def paintEvent(self, event):
        """重载-绘制"""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)#反走样
        self.bezierPath = QPainterPath()
        self.bezierPath.setFillRule(Qt.WindingFill)#封闭图形
        self.bezierPath.moveTo(0, self.w_height)
        x2 = self.bezier(0,self.w_height,self.w_width_b,0)
        self.bezierPath.cubicTo(x2, self.w_height, x2, 0, self.w_width_b, 0)
        self.bezierPath.cubicTo(self.w_width_b, 0, self.w_width_b, self.w_height, self.w_width_b, self.w_height)
        
        self.bezierPath.addRect(self.w_width_b,0,self.w_width-self.w_width_b*2,self.w_height)
        
        self.bezierPath.moveTo(self.w_width-self.w_width_b, 0)
        x3 = self.bezier(self.w_width-self.w_width_b,0, self.w_width,self.w_height)
        self.bezierPath.cubicTo(x3, 0, x3, self.w_height, self.w_width,self.w_height)
        self.bezierPath.cubicTo(self.w_width,self.w_height, self.w_width-self.w_width_b,self.w_height, self.w_width-self.w_width_b,self.w_height)
        
        
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawPath(self.bezierPath.simplified())
        
        #绘制叉号
        if self.is_select_x:
            #白色叉号
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor('#b50202')))
            painter.drawEllipse(self.w_width-self.w_width_b-10,17-11,12,12)
            painter.setPen(QPen(QColor('#ffffff')))
        else:
            painter.setPen(self.pen_Text3)
            painter.setBrush(Qt.NoBrush)
        painter.setFont(self.font2)
        painter.drawText(self.w_width-self.w_width_b-9,16,'×')
        
        painter.drawText(25,16,self.text)
