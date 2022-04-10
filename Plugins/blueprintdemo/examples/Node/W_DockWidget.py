from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

IMAGEPATH = __file__[:-15] + "images/"
IMAGE_DOCK_TITLE_ICON = IMAGEPATH+"未标题-1.png"

class W_DockTitleWidgetItem(QWidget):
    click=Signal(object)#自定义点击信号
    
    def __init__(self,title_text='', parent=None):
        super().__init__(parent)
        self.initSize()
        self.initBackground()
        self.initPenAndBrush()
        self.roundnes = 2
        self.is_click = False#是否点击
        self.is_select_x = False#是否悬浮X号
        self.title_text = title_text
        
    def initSize(self):
        """初始化尺寸"""
        self.setMinimumWidth(150)
        self.setMinimumHeight(20)
        self.setMaximumWidth(150)
        self.setGeometry(8,0,150,20)
    
    def initBackground(self):
        """初始化背景颜色"""
        self.setAutoFillBackground(True) #自动填充背景
        self.setPalette(QPalette(QColor("#003c3c3c"))) #着色区分背景
    
    def initPenAndBrush(self):
        """初始化笔和画刷"""
        self.font1 = QFont("SimHei", 9)
        self.font2 = QFont("SimHei", 8)
        self.pen_text  = QPen(QColor("#ffffff"))#文字颜色
        self.pen_Text3  = QPen(QColor("#1b1b1b"))#叉号颜色
        self.pen_3  = QPen(QColor("#c0b119"))#选中金线颜色
        self.brush_background = QBrush(QColor(44, 49, 57))#默认颜色
        self.pix = QPixmap(IMAGE_DOCK_TITLE_ICON).scaled(14,14,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
    
    def enterEvent(self, a0: QEvent):#进入事件
        """重载-鼠标进入"""
        self.setMouseTracking(True)
        color = QColor(33, 37, 43)
        self.brush_background = QBrush(color)#默认颜色
        self.update()
    
    def leaveEvent(self, a0: QEvent):#离开事件
        """重载-鼠标离开"""
        self.setMouseTracking(False)
        self.is_select_x = False
        color = QColor(44, 49, 57)
        self.brush_background = QBrush(color)#默认颜色
        self.update()
        
    def mousePressEvent(self, a0: QMouseEvent):
        """重载-鼠标按下"""
        color = QColor(33, 37, 43)
        self.brush_background = QBrush(color)#默认颜色
        self.update()
        self.is_click = not self.is_click
        self.click.emit(self.is_click)
        super().mousePressEvent(a0)
    
    def mouseMoveEvent(self, a0: QMouseEvent):
        """重载-鼠标移动"""
        x = a0.pos().x()
        if x>132 and x<142:
            self.is_select_x = True
            self.update()
        else:
            self.is_select_x = False
            self.update()
        super().mouseMoveEvent(a0)
        
    def paintEvent(self, a0: QPaintEvent):
        """重载-绘制"""
        painter = QPainter(self)
        
        path_content1 = QPainterPath()
        path_content1.setFillRule(Qt.WindingFill)
        path_content1.addRoundedRect(0, 0, self.width(), self.height(), self.roundnes, self.roundnes)
        path_content1.addRect(0, self.roundnes, self.width(), self.height()-self.roundnes)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_content1.simplified())
        #绘制文字
        painter.setFont(self.font1)
        painter.setPen(self.pen_text)
        painter.drawText(30,15,self.title_text)
        #绘制图片
        painter.drawPixmap(10, 3, 14, 14, self.pix)
        #绘制选中金线
        if self.is_click:
            lg = QLinearGradient(0, 0, self.width(), 0)
            lg.setColorAt(0, QColor("#00c0b119"))
            lg.setColorAt(0.05, QColor("#c0b119"))
            lg.setColorAt(0.95, QColor("#c0b119"))
            lg.setColorAt(1, QColor("#00c0b119"))
            
            brush = QBrush(lg)
            self.pen_3 = QPen(brush,1)
            painter.setPen(self.pen_3)
            painter.drawLine(self.roundnes,0,self.width()-2*self.roundnes,0)
        #绘制叉号
        if self.is_select_x:
            #白色叉号
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor('#b50202')))
            painter.drawEllipse(self.width()-20-0,15-11,12,12)
            painter.setPen(QPen(QColor('#ffffff')))
        else:
            painter.setPen(self.pen_Text3)
            painter.setBrush(Qt.NoBrush)
        painter.setFont(self.font2)
        painter.drawText(self.width()-20,15,'×')
        
class W_DockTitleWidget(QWidget):
    click_signal=Signal(object,object)#自定义点击信号
    click_signal_close=Signal(object)#自定义点击信号
    
    def __init__(self,title_text='详细面板', parent=None):
        super().__init__(parent)
        self.initLayout()
        self.initBackground()
        self.title_text = title_text
        
        self.item = W_DockTitleWidgetItem(self.title_text)
        self.item.click.connect(self.click)
        self.h_layout.addWidget(self.item)
    
    def initLayout(self):
        """初始化布局"""
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(0)
        self.h_layout.setAlignment(Qt.AlignLeft)
        self.h_layout.setContentsMargins(8,0,0,0)
        self.setLayout(self.h_layout)#设置布局
    
    def initBackground(self):
        """初始化背景颜色"""
        self.setAutoFillBackground(True) #自动填充背景
        self.setPalette(QPalette(QColor("#00000000"))) #着色区分背景
    
    def click(self,is_click):
        """槽函数-点击"""
        self.click_signal.emit(self,is_click)
        
    def cancelSelected(self):
        """槽函数-取消选中"""
        self.item.is_click = False
        self.item.update()
    
    def mousePressEvent(self, a0: QMouseEvent):
        """重载-鼠标点击"""
        if a0.x()>8 and a0.x()<150:
            self.selected = True#是否选中
            super().mousePressEvent(a0)
        if a0.x()>142 and a0.x()<149:
            self.click_signal_close.emit(self)
            
class W_DockWidget(QDockWidget):
    def __init__(self, parent=None,item=None,title_text='详细面板'):
        super().__init__(parent)
        self.setParent(parent)
        self.initItem(item)
        self.initBackground()
        self.setWindowTitle("添加节点")
        self.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.title_widget = W_DockTitleWidget(title_text)
        self.title_widget.click_signal.connect(self.clickSignal)
        self.title_widget.click_signal_close.connect(self.close)
        self.setTitleBarWidget(self.title_widget)
    
    def initBackground(self):
        """初始化背景颜色"""
        self.setAutoFillBackground(True) #自动填充背景
        self.setPalette(QPalette(QColor("#1c1c1c"))) #着色区分背景
    
    def initItem(self,item):
        """初始化子项"""
        self.item_widget = item
        self.setWidget(self.item_widget)
    
    def clickSignal(self,widget,is_click):
        """槽函数-点击选项卡"""
        self.docks = self.parent().findChildren(QDockWidget)
        for dock in self.docks:
            widget_ = dock.titleBarWidget()
            if widget_ != widget:
                widget_.cancelSelected()
    
    def resizeEvent(self, a0: QResizeEvent):
        """重载-尺寸缩放"""
        try:
            self.item_widget.setAutomaticSize(a0)
        except:pass