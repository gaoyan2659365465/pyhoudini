from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from .BP_Json import BP_Json

IMAGEPATH = __file__[:-14] + "images/"

IMAGE_ICON = IMAGEPATH+"Node_09.png"
IMAGE_ICON2 = IMAGEPATH+"Node_08.png"
IMAGE_ICON3 = IMAGEPATH+"Node_07.png"
IMAGE_SHADOW = IMAGEPATH+"未标题-2.png"

    
    
class W_TitleBase(QGraphicsItem,BP_Json):
    def __init__(self,parent=None,width=0,height=0):
        super().__init__(parent)
        self.initUI()
        self.width = width
        self.height = height
        self.initColor()
        
    def initUI(self):
        self.initSizes()
        
    
    def initSizes(self):
        self.roundnes = 10.0#发亮边缘圆角度数
    
    def initColor(self):
        self.color = QColor("#4c748d")      #标题栏左边颜色#4c748d
        self.color2 = QColor("#4D4c748d")   #标题栏右边颜色#FF424342
        self.color_GaoGuang = QColor("#C8FFFFFF")   #白色高光
        self.color_roundness = QColor("#FF000000")  #黑色描边
        self.pen_GaoGuang = QPen(self.color_GaoGuang)
        self.pen_GaoGuang.setWidthF(1.0)
        self.pen_roundness = QPen(self.color_roundness)
        self.pen_roundness.setWidthF(1.0)
        self.pen_Text = QPen(QColor("#eeeeee"))#文字颜色
        self.font = QFont("SimHei", 13, QFont.Bold)
        self.pix = QPixmap(IMAGE_ICON).scaled(18,18,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.pix1 = QPixmap(IMAGE_SHADOW).scaled(150,39,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.setNodeTitleName("HelloWorld")
        
    
    def boundingRect(self) -> QRectF:
        """定义Qt的边框"""
        return QRectF(0,0,self.width,self.height).normalized()
    
    def getNodeTitleName(self):
        """获得节点标题栏文字"""
        return self.title_text
    
    def setNodeTitleName(self,Name:str=''):
        """设置节点标题栏文字"""
        self.title_text = Name

    def setNodeTitlePix(self,pix:int=0):
        """设置节点标题栏图标"""
        if pix == 0:
            IMAGE = IMAGE_ICON
        elif pix == 1:
            IMAGE = IMAGE_ICON2
        elif pix == 2:
            IMAGE = IMAGE_ICON3
        self.pix = QPixmap(IMAGE).scaled(18,18,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
    
    def setNodeTitleColor(self,color):
        """设置标题栏颜色"""
        self.color = QColor(color)#标题栏蓝色

    def setAutomaticSize(self,width,height):
        """自动设置节点所需要的尺寸"""
        self.width = width
        self.height = height
        self.update()
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """重载-绘制"""
        lg = QLinearGradient(0, -70, self.width, 70)
        lg.setColorAt(0, self.color)
        lg.setColorAt(0.6, self.color)
        lg.setColorAt(0.9, self.color2)
        lg.setColorAt(1, self.color2)
        
        path_content1 = QPainterPath()
        path_content1.setFillRule(Qt.WindingFill)
        path_content1.addRoundedRect(3, 2, self.width-6, self.height-1, self.roundnes, self.roundnes)
        path_content1.addRect(3, self.roundnes+2, self.width-6, self.height-self.roundnes)
        painter.setPen(Qt.NoPen)
        painter.setBrush(lg)
        painter.drawPath(path_content1.simplified())
        
        #绘制高光
        painter.setClipRegion(QRegion(0,2,self.width,self.roundnes-5))
        path_content = QPainterPath()
        path_content.addRoundedRect(3, 2, self.width-6, self.height-1, self.roundnes+2, self.roundnes+2)
        painter.setPen(self.pen_GaoGuang)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_content.simplified())
        painter.setClipRegion(QRegion(0,0,self.width,self.height))
        #绘制图片
        painter.drawPixmap(12, 8, 18, 18, self.pix)
        painter.drawPixmap(12, 0, 150, 39, self.pix1)
        
        #绘制文字
        painter.setFont(self.font)
        painter.setPen(self.pen_Text)
        painter.drawText(35,23,self.title_text)
    
    #region 序列化
    def dump(self):
        """保存"""
        data = {'title_text':self.title_text}
        return data
    def load(self,obj):
        """加载"""
        title_text = obj['title_text']
        self.title_text = title_text
        return
    #endregion