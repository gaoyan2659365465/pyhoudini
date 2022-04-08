from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from .W_SocketContent import *
from .BP_Json import BP_Json



"""自定义布局类"""
class BP_Layout():
    def __init__(self,parent:QGraphicsItem=None):
        self.widget = parent
    def getSize(self,widget_list):
        """获取控件预计尺寸"""
        heights1 = 0#总高度
        heights2 = 0#总高度
        width1 = 0#总宽度
        width2 = 0#总宽度
        maxWidth = 0#最长宽度
        maxHeight = 0#最长宽度
        for i in widget_list:
            if i.direction == VALUE_INPUT:
                heights1 = heights1 + i.height + 8
                if i.width>width1:
                    width1 = i.width
            elif i.direction == VALUE_OUTPUT:
                heights2 = heights2 + i.height + 8
                if i.width>width2:
                    width2 = i.width
            maxHeight = heights2
            if heights1>heights2:
                maxHeight = heights1
            maxWidth = width1+width2
        return maxWidth,maxHeight
    def setLocation(self,widget_list):
        """将控件设置到预计位置"""
        height1 = 0#总高度
        height2 = 0#总高度
        i:W_SocketContent
        for i in widget_list:
            if i.direction == VALUE_INPUT:
                i.setGeometry(0,height1,i.width,i.height)
                height1 = height1 + i.height + 8
            elif i.direction == VALUE_OUTPUT:
                a = self.widget.width - i.width
                i.setGeometry(a,height2,i.width,i.height)
                height2 = height2 + i.height + 8

class W_NodeContent(QGraphicsItem,BP_Json):
    def __init__(self,parent=None,width=0,height=0,title_height=0):
        super().__init__(parent)
        self.initUI()
        self.marginX = 8#边缘留白
        self.marginY = 7#边缘留白
        self.width = width-self.marginX*2
        self.title_height = title_height
        self.height = height-title_height-self.marginY*2
        
        self.setPos(self.marginX,self.title_height+self.marginY)
        self.bp_layout = BP_Layout(self)#自定义布局类
        
    
    def initUI(self):
        self.sockets = []
    
    def boundingRect(self) -> QRectF:
        """定义Qt的边框"""
        return QRectF(0,0,self.width,self.height).normalized()

    def addSocket(self,data_type:int=0,direction:int=0,logic_type:int=0):
        """给节点内容增加端口
        :param data_type: 节点表示的变量的数据类型（整型/字符串）
        :param direction: 需要在节点输(入/出)侧添加端口
        :param logic_type: 节点表示的变量的逻辑类型（数据/逻辑）
        """
        socket_content = W_SocketContent(self,data_type,direction,logic_type)
        self.sockets.append(socket_content)
        self.bp_layout.setLocation(self.sockets)
        socket_content.setSocketColor()
        return socket_content
    
    def getAllSocket(self):
        """获取此节点所有插槽"""
        return self.sockets
    
    def getSocketLocation(self,socket_num:int=0):
        """获取插槽的绝对位置"""
        socket_content = self.sockets[socket_num]
        socket_content:W_SocketContent
        #返回的坐标是基于屏幕的
        return socket_content.getSocketLocation()
    
    def getSocketDirection(self,socket_num:int=0)->bool:
        """获取插槽是左边还是右边"""
        socket_content = self.sockets[socket_num]
        socket_content:W_SocketContent
        return socket_content.getSocketDirection()
    
    def setSocketState(self,socket_num:int=0,isLink:bool=False):
        """设置端口状态是否已连接"""
        socket_content = self.sockets[socket_num]
        socket_content:W_SocketContent
        socket_content.setSocketState(isLink)
    
    def getSocketColor(self,socket_num:int=0):
        """获取插槽的颜色"""
        socket_content = self.sockets[socket_num]
        socket_content:W_SocketContent
        return socket_content.getSocketColor()
    
    def getRequiredSize(self):
        """获取所需尺寸用来让父控件延展"""
        width,height = self.bp_layout.getSize(self.sockets)
        width = width+self.marginX*2
        height = height+self.marginY*2+self.title_height
        return width,height
    
    def setAutomaticSize(self,width,height):
        """自动设置节点所需要的尺寸"""
        self.width = width-self.marginX*2
        self.height = height-self.title_height-self.marginY*2
        self.bp_layout.setLocation(self.sockets)
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """重载-绘制"""
        self.brush_background = QBrush(QColor("#0041f702"))
        
        path_content1 = QPainterPath()
        path_content1.setFillRule(Qt.WindingFill)
        path_content1.addRect(0, 0, self.width, self.height)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_content1.simplified())
    
    #region 序列化
    def dump(self):
        """保存"""
        data = {}
        a=0
        for socket_content in self.sockets:
            data[a] = socket_content.dump()
            a=a+1
        return data
    def load(self,obj):
        """加载"""
        for key in obj:
            self.sockets[int(key)].load(obj[key])
        return
    #endregion