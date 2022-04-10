from PYBP.window.widget.PYBP_Widget import *

#子项-主界面控件-唯一


class PYBP_MainWidget(PYBP_Widget):
    def __init__(self, parent):
        super().__init__(parent)
        
    
    def initValue(self):
        """初始化变量"""
        super().initValue()
        self._color_outline = QColor("#252525")
        self._pen = QPen(self._color_outline)
        self._pen.setWidth(15)
    
    def paintEvent(self, event):
        """重载-绘制"""
        painter = QPainter(self)
        painter.setClipRect(5,5,self.width()-10,self.height()-10)
        painter.rotate(45)
        painter.setRenderHint(QPainter.Antialiasing, True)#反走样
        painter.setPen(self._pen)
        painter.translate(0, -2000)
        x=0
        for i in range(100):
            painter.drawLine(x,0,x,3000)
            x = i * 26
        super().paintEvent(event)
            