from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
#自定义滚动框

class W_ScrollBar(QScrollBar):
    """自定义滚动条"""
    def __init__(self,parent=None):
        super().__init__(Qt.Vertical,parent)
        self.setPageStep(100)  #此时滚动条 约占 1/3
        self._white_pen = QPen(QColor("#ff6e6e6e"))
        self._white_pen.setWidthF(1)
        self._white_pen2 = QPen(QColor("#ff5e5d5d"))
        self._white_pen2.setWidthF(1)
        self.is_enter = False
    
    def leaveEvent(self, a0: QEvent):
        """重载-离开"""
        self.is_enter = False
        
    def enterEvent(self, a0: QEvent):
        """重载-进入"""
        self.is_enter = True
    
    def paintEvent(self, a0: QPaintEvent):
        """重载-绘制"""
        painter = QPainter(self)
        if self.is_enter:
            painter.setPen(self._white_pen)
        else:
            painter.setPen(self._white_pen2)
        painter.drawLine(5,0,5,self.height())
        super().paintEvent(a0)
    
class W_ScrollArea(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.g_layout = QGridLayout()
        self.g_layout.setAlignment(Qt.AlignTop)#居左对齐
        self.g_layout.setContentsMargins(2,0,10,0)
        self.g_layout.setSpacing(0)
        
        self.item_widget = QWidget(self)
        self.item_widget.setLayout(self.g_layout)
        
        self.w_scroll_bar = W_ScrollBar(self)
        self.w_scroll_bar.valueChanged.connect(self.valueChanged)

        self.setAutoFillBackground(True)                #自动填充背景
        self.setPalette(QPalette(QColor('#3c3c3c')))    #着色区分背景
        
    def addItem(self,item,x,y):
        """添加子项"""
        self.g_layout.addWidget(item,x,y)
        self.w_scroll_bar.raise_()      #置顶
        try:
            item.toolBoxSize.connect(self.toolBoxSizeEvent)#绑定子控件尺寸改变信号
            item.paint.connect(self.toolBoxPaintEvent)
        except:pass
        widget = self.item_widget
        widget.setGeometry(0,0,widget.width(), widget.height()+item.height())
    
    def removeAllItem(self):
        """删除所有子项"""
        items = []
        for i in range(self.g_layout.count()):
            item = self.g_layout.itemAt(i).widget()
            items.append(item)
        for item in items:
            self.g_layout.removeWidget(item)
            item.setParent(None)
        widget = self.item_widget
        widget.setGeometry(0,0,widget.width(), 100)
            
    
    def wheelEvent(self, event:QWheelEvent):
        """重载-滚轮"""
        if event.angleDelta().y()<0:
            value = self.w_scroll_bar.value() + 20
        else:
            value = self.w_scroll_bar.value() - 20
        self.w_scroll_bar.setSliderPosition(value)
    
    def valueChanged(self):
        """槽函数-滚动条改变"""
        value = self.w_scroll_bar.value()
        widget = self.item_widget
        widget.setGeometry(0,0-value,widget.width(), widget.height())
    
    def setAutomaticSize(self,ax: int, ay: int, aw: int, ah: int):
        """自动设置节点所需要的尺寸"""
        self.setGeometry(ax,ay,aw, ah)
        widget = self.item_widget
        widget.setGeometry(ax,ay,aw, widget.sizeHint().height())
        self.w_scroll_bar.setGeometry(self.width()-15,0,10,ah-20)
        self.w_scroll_bar.setRange(0, widget.sizeHint().height()-ah+20)
        max_value = widget.sizeHint().height()-ah+20
        if max_value<0:
            self.w_scroll_bar.hide()
        elif max_value>=0 and not self.w_scroll_bar.isVisible():
            self.w_scroll_bar.show()
    
    def toolBoxSizeEvent(self):
        """子控件尺寸改变"""
        self.setAutomaticSize(0,0,self.width(),self.height())
    
    def toolBoxPaintEvent(self):
        """子控件重绘"""
        self.w_scroll_bar.raise_()      #置顶
        self.w_scroll_bar.update()