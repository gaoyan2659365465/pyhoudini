from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from .W_ScrollArea import W_ScrollArea
import typing

#region 无用
class W_ToolBox_Title(QWidget):
    click=Signal(object)#自定义点击信号
    def __init__(self,parent=None,text=''):
        super().__init__(parent)
        self.parent_widget= parent
        self.is_click = False#是否点击
        self.title_text = text#抽屉栏文字
        self.setMinimumHeight(30)
        self.setMaximumHeight(30)
        self.setAutoFillBackground(True) #自动填充背景
        self.setPalette(QPalette(QColor('#313131'))) #着色区分背景
        self.leave_color = QColor('#313131')#离开颜色
        self.enter_color = QColor('#202020')#进入颜色
        self._font = QFont("SimHei", 11)
        self._brush3    = QBrush(QColor("#ffffff"))
        self.pen_Text   = QPen(QColor("#eeeeee"))#文字颜色
        self.pen_Text2  = QPen(QColor("#000000"))#文字颜色
        self._white_pen = QPen(QColor("#ffffff"))
        self._white_pen.setWidthF(1)
        
    def leaveEvent(self, a0: QEvent):#离开事件
        self.setPalette(QPalette(self.leave_color)) #着色区分背景
    def enterEvent(self, a0: QEvent):#进入事件
        self.setPalette(QPalette(self.enter_color)) #着色区分背景
    def mousePressEvent(self, a0: QMouseEvent):#鼠标按下
        self.is_click = not self.is_click
        self.click.emit(self.is_click)
    def paintEvent(self, event):
        """重载-绘制"""
        painter = QPainter(self)
        painter.translate(4, self.height()/2)
        path_content = QPainterPath()
        if not self.is_click:
            list01 = [0,4, 6,4, 6,-3]
            painter.setBrush(self._brush3)
            painter.setPen(Qt.NoPen)
        else:
            list01 = [0,-4, 4,0, 0,4]
            painter.setPen(self._white_pen)
            painter.setBrush(Qt.NoBrush)
        path_content.addPolygon(QPolygonF(QPolygon(list01)))
        painter.setRenderHint(QPainter.Antialiasing, False)#反走样
        painter.drawPath(path_content.simplified())
        
        #绘制文字
        painter.setFont(self._font)
        painter.setPen(self.pen_Text2)
        painter.drawText(10,6,self.title_text)
        painter.setFont(self._font)
        painter.setPen(self.pen_Text)
        painter.drawText(10,5,self.title_text)        

class W_ToolBox(QWidget):
    """能展开收缩的抽屉控件"""
    paint=Signal()#自定义点击信号
    toolBoxSize=Signal()#自定义尺寸改变信号
    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent_widget= parent
        self.is_click = False
        self.title_text = '外观' 
        self.setAutoFillBackground(True)                #自动填充背景
        self.setPalette(QPalette(QColor('#3c3c3c')))    #着色区分背景
        
        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(0)
        self.v_layout.setAlignment(Qt.AlignTop)
        self.v_layout.setContentsMargins(0, 0, 0, 2)
        
        self.v_layout_1 = QVBoxLayout()
        self.v_layout_1.setSpacing(0)
        self.v_layout_1.setAlignment(Qt.AlignTop)
        self.v_layout_1.setContentsMargins(0, 0, 0, 0)
        self.v_layout_1.setGeometry(QRect(0,30,self.width()+10,self.sizeHint().height()))
        
        self.button_widget = W_ToolBox_Title(self,self.title_text)
        self.button_widget.click.connect(self.click)
        
        self.setLayout(self.v_layout)
        self.v_layout.addWidget(self.button_widget)
        self.v_layout.addLayout(self.v_layout_1)
        
    def addItem(self,item):
        """添加子项"""
        self.v_layout_1.addWidget(item)
        try:
            item.paint.connect(self.toolBoxPaintEvent)
        except:pass
    
    def toolBoxPaintEvent(self):
        """子控件重绘"""
        self.paint.emit()
        
    def click(self,is_click):
        """点击"""
        self.is_click = is_click
        if self.is_click:
            self.setMaximumHeight(30)
            self.v_layout_1.setGeometry(QRect(0,0,0,0))
        else:
            height = self.sizeHint().height()
            self.setMaximumHeight(height)
            self.v_layout_1.setGeometry(QRect(0,30,self.width()+10,height))
        self.toolBoxSize.emit()

class W_AttributeItem(W_ToolBox):
    """属性面板子项"""
    paint=Signal()#自定义点击信号
    def __init__(self,text='',parent=None):
        super().__init__(parent)
        self.title_text = text#属性文字
        self.v_layout.removeWidget(self.button_widget)
        
        self.button_widget = W_ToolBox_Title(self,self.title_text)
        self.button_widget.click.connect(self.click)
        self.button_widget._font = QFont("SimHei", 9)
        self.button_widget.leave_color = QColor('#3e3e3e')#离开颜色
        self.button_widget.enter_color = QColor('#494949')#进入颜色
        self.button_widget.setPalette(QPalette(QColor('#3e3e3e'))) #着色区分背景
        
        self.setLayout(self.v_layout)
        self.v_layout.insertWidget(0,self.button_widget)
        #self.initUI()
        
    # def initUI(self):
    #     """初始化UI"""
    #     self.setMinimumHeight(30)
    #     self.setPalette(QPalette(QColor('#3e3e3e'))) #着色区分背景
    #     self.setAutoFillBackground(True) #自动填充背景
    #     self.pen_Text = QPen(QColor("#eeeeee"))#文字颜色
    #     self.font = QFont("SimHei", 9)
    # def leaveEvent(self, a0: QEvent):#离开事件
    #     self.setPalette(QPalette(QColor('#3e3e3e'))) #着色区分背景
    # def enterEvent(self, a0: QEvent):#进入事件
    #     self.setPalette(QPalette(QColor('#494949'))) #着色区分背景
    #     self.paint.emit()
    # def paintEvent(self, event):
    #     """重载-绘制"""
    #     painter = QPainter(self)
    #     painter.setRenderHint(QPainter.Antialiasing, False)#反走样
    #     #绘制文字
    #     painter.setFont(self.font)
    #     painter.setPen(self.pen_Text)
    #     painter.drawText(15,20,self.title_text)
#endregion

class W_ToolAttributeItemTitle(QWidget):
    """属性面板子项标题"""
    click=Signal(object)#自定义点击信号
    def __init__(self,parent=None):
        super().__init__(parent)
        self._font = QFont("SimHei", 11)
        self.offset = 0#三角形偏移
        self.pen_text = QPen(QColor("#eeeeee"))#文字颜色
        self.pen_text_shadow = QPen(QColor("#000000"))#文字颜色
        self._white_pen = QPen(QColor("#ffffff"))
        self._white_pen.setWidthF(1)
        self._brush3    = QBrush(QColor("#ffffff"))
        self.setEnterColor(QColor('#313131'),QColor('#202020'))
        self.setIsHaveChildren(True)
        self.setAutoFillBackground(True) #自动填充背景
        self.setPalette(QPalette(self.leave_color)) #着色区分背景
    
    def setText(self,text:str):
        """设置标题文字"""
        self.title_text = text
    
    def setTextFont(self,font:QFont):
        """设置文字字体"""
        self._font = font
    
    def setEnterColor(self,leave_color,enter_color):
        """设置进入离开颜色"""
        self.leave_color = leave_color#离开颜色
        self.enter_color = enter_color#进入颜色
        self.setPalette(QPalette(self.leave_color)) #着色区分背景
    
    def setIsHaveChildren(self,is_have:bool):
        """设置是否拥有子项"""
        self.is_have_children = is_have#是否拥有子项
        self.is_click = False
    
    #region 进入离开事件
    def leaveEvent(self, a0: QEvent):
        """重载-离开事件"""
        self.setPalette(QPalette(self.leave_color)) #着色区分背景
        
    def enterEvent(self, a0: QEvent):
        """重载-进入事件"""
        self.setPalette(QPalette(self.enter_color)) #着色区分背景
    #endregion
    
    def mousePressEvent(self, a0: QMouseEvent):
        """重载-鼠标按下"""
        self.is_click = not self.is_click
        self.update()
        self.click.emit(self.is_click)
        if a0.x()>3 and a0.x()<12:
            self.offset = 3
        super().mousePressEvent(a0)
    
    def mouseReleaseEvent(self, a0: QMouseEvent):
        """重载-鼠标松开"""
        self.offset = 0
        self.update()
        super().mouseReleaseEvent(a0)
    
    def paintEvent(self, event):
        """重载-绘制"""
        painter = QPainter(self)
        painter.translate(4, self.height()/2 + self.offset)
        
        if self.is_have_children:
            path_content = QPainterPath()
            if not self.is_click:
                list01 = [0,4, 6,4, 6,-3]
                painter.setBrush(self._brush3)
                painter.setPen(Qt.NoPen)
            else:
                list01 = [0,-4, 4,0, 0,4]
                painter.setPen(self._white_pen)
                painter.setBrush(Qt.NoBrush)
            
            list02: typing.List[QPoint] = []
            for i in range(0,len(list01),2):
                list02.append(QPoint(list01[i],list01[i+1]))
            
            path_content.addPolygon(QPolygonF(QPolygon(list02)))
            painter.setRenderHint(QPainter.Antialiasing, False)#反走样
            painter.drawPath(path_content.simplified())
            
        painter.translate(0, -self.offset)
        #绘制文字
        # painter.setFont(self._font)
        # painter.setPen(self.pen_text_shadow)
        # painter.drawText(10,6,self.title_text)
        painter.setFont(self._font)
        painter.setPen(self.pen_text)
        painter.drawText(10,5,self.title_text) 

class W_ToolAttributeItem(QWidget):
    """属性面板子项"""
    toolBoxSize=Signal()#自定义尺寸改变信号
    def __init__(self,title_text="外观",parent=None):
        super().__init__(parent)
        self.title_text = title_text            #标题文字
        self.title_height = 30              #标题高度
        self.is_have_children = False       #是否拥有子项
        self.initUI()
        self.setMinimumHeight(30)
        self.setAutoFillBackground(True)                #自动填充背景
        self.setPalette(QPalette(QColor('#3c3c3c')))    #着色区分背景
        
        self.title = W_ToolAttributeItemTitle(self)
        self.title.setText(self.title_text)
        self.title.setIsHaveChildren(self.is_have_children)
        self.title.click.connect(self.titleClick)
    
    def initUI(self):
        """初始化UI"""
        if self.is_have_children:
            self.v_layout = QVBoxLayout()
            self.v_layout.setSpacing(0)
            self.v_layout.setAlignment(Qt.AlignTop)
            self.v_layout.setContentsMargins(0, self.title_height, 0, 2)
            self.setLayout(self.v_layout)
        self.titleClick(False)
    
    def setIsHaveChildren(self,is_have:bool):
        """设置是否拥有子项"""
        self.is_have_children = is_have       #是否拥有子项
        self.title.setIsHaveChildren(self.is_have_children)
        self.initUI()
    
    def setEnterColor(self,leave_color,enter_color):
        """设置进入离开颜色"""
        self.title.setEnterColor(leave_color,enter_color)
    
    def setTextFont(self,font:QFont):
        """设置文字字体"""
        self.title.setTextFont(font)
    
    def addItem(self,item):
        """添加子项"""
        self.is_have_children = True
        self.title.setIsHaveChildren(True)
        self.v_layout.addWidget(item)
        self.titleClick(False)
        try:
            item.toolBoxSize.connect(self.toolBoxSizeEvent)
            self.toolBoxSize.emit()
        except:pass
    
    def toolBoxSizeEvent(self):
        """槽函数-子控件尺寸改变"""
        self.setGeometry(0,0,self.sizeHint().width(),self.sizeHint().height())
        self.setMaximumHeight(self.sizeHint().height())
        self.toolBoxSize.emit()
    
    def titleClick(self,is_click):
        """槽函数-标题栏点击"""
        if not self.is_have_children:return
        if is_click:
            self.setGeometry(QRect(0,0,self.width(),self.title_height))
            self.v_layout.setGeometry(QRect(0,0,0,0))
            self.setMaximumHeight(self.title_height)
        else:
            width = self.width()
            height = self.sizeHint().height()
            self.setGeometry(QRect(0,0,self.width(),height))
            self.v_layout.setGeometry(QRect(0,0,width,height))
            self.setMaximumHeight(height)
        self.toolBoxSize.emit()
    
    def resizeEvent(self, a0: QResizeEvent):
        """重载-尺寸缩放"""
        self.title.setGeometry(0,0,self.width(),self.title_height)
        
class W_Attributes(QWidget):
    """属性面板控件"""
    def __init__(self,parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        """初始化UI"""
        self.setMinimumWidth(300)
        self.scrollArea = W_ScrollArea(self)
    
    def setAttributeList(self,data):
        """设置属性列表"""
        self.scrollArea.removeAllItem()
        toolBox = W_ToolAttributeItem('基础')
        toolBox.setIsHaveChildren(True)#用于子项
        for key in data:
            toolBox2 = W_ToolAttributeItem(key+':'+str(data[key]))
            #二级颜色
            toolBox2.setEnterColor(QColor('#3e3e3e'),QColor('#494949'))
            toolBox2.setTextFont(QFont("SimHei", 11))
            toolBox.addItem(toolBox2)#一级添加二级
        self.scrollArea.addItem(toolBox)
    
    def setAutomaticSize(self,event):
        """自动设置节点所需要的尺寸"""
        w = event.size()
        self.scrollArea.setAutomaticSize(0, 0, w.width(), w.height())
    
    