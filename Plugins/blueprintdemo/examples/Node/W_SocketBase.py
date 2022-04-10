from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import typing

#单纯指小圆插槽
SOCKET_TYPE_FLOAT = 0   #浮点类型
SOCKET_TYPE_INT = 1     #整数类型
SOCKET_TYPE_BOOL = 2    #布尔类型
SOCKET_TYPE_STRING = 3  #字符串类型
VALUE_INPUT = 0     #需要在节点输入侧添加端口
VALUE_OUTPUT = 1    #需要在节点输出侧添加端口

SOCKET_TYPE_LOGIC = 0#插槽-逻辑类型
SOCKET_TYPE_VALUE = 1#插槽-数值类型

class W_SocketBase(QGraphicsItem):
    def __init__(self,parent=None,data_type:int=0,direction:int=0,logic_type:int=0):
        super().__init__(parent)
        self.width = 26
        self.height = 20
        self.data_type = data_type
        self.direction = direction      #插槽方向(0/1)左右
        self.logic_type = logic_type
        self.socket_state = False       #插槽状态-是否连接
        self.initUI()
        self.initAssets()
        self.setAcceptHoverEvents(True)#接受悬停事件
    
    def initUI(self):
        self.radius = 6.5               #插槽圆圈半径
        self.white_output_width = 3.0   #插槽白色多边形绘制步长
    
    def initAssets(self):   
        self._color_outline = QColor("#0A0C0A")         # 插槽端口周围轮廓颜色
        self._color_background = QColor("#41f702")      # 插槽端口颜色-可变
        self._color_background2 = QColor("#0A0C0A")     # 插槽端口小圈黑色
        self._color_white_output = QColor("#ffffffff")    #白色连接端口颜色

        self._pen = QPen(self._color_outline)
        self._pen.setWidthF(0.5)#插槽轮廓线宽度
        self._white_pen = QPen(self._color_white_output)
        self._white_pen.setWidthF(1)
        self._brush = QBrush(self._color_background)    # 插槽端口颜色-可变
        self._brush2 = QBrush(self._color_background2)  # 插槽端口小圈黑色
        self._brush3 = QBrush(self._color_white_output) # 白色连接端口颜色
    
    def setGeometry(self,x,y,width,height):
        """设置位置尺寸"""
        self.setPos(x,y)
        self.width = width
        self.height = height
    
    def boundingRect(self) -> QRectF:
        """定义Qt的边框"""
        return QRectF(0,0,self.width,self.height).normalized()
    
    def getSocketColor(self)-> QColor:
        """获取插槽的颜色"""
        if self.logic_type == SOCKET_TYPE_VALUE:
            return self._color_background
        elif self.logic_type == SOCKET_TYPE_LOGIC:
            return self._color_white_output
    
    def getSocketLocation(self):
        """获取插槽的绝对位置"""
        w = self.white_output_width
        if self.direction == VALUE_INPUT:
            point = 4
        elif self.direction == VALUE_OUTPUT:
            point = self.width-3.3*w-4
            
        return self.pos() + QPointF(13,10) + QPointF(point,0)
    
    def setSocketColor(self,color:str='#000000'):
        """设置端口颜色
        :param color: 不同颜色表示不同数据类型
        """
        if self.data_type == SOCKET_TYPE_FLOAT:#float
            color = "#41f702"
        elif self.data_type == SOCKET_TYPE_INT:#int
            color = "#00effe"
        elif self.data_type == SOCKET_TYPE_BOOL:#bool
            color = "#fe0000"
        elif self.data_type == SOCKET_TYPE_STRING:#string
            color = "#ee02f7"
        
        self._color_background = QColor(color)  #确定套接字的颜色
        self._brush = QBrush(self._color_background)
        return color
    
    def setSocketState(self,isLink:bool=False):
        """设置端口状态是否已连接"""
        self.socket_state = isLink
    
    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent'):
        """重载-鼠标离开"""
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(event)
        
    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent'):
        """重载-鼠标进入"""
        self.setCursor(Qt.CrossCursor)
        super().hoverEnterEvent(event)
    
    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):
        """重载-鼠标点击"""
        socket_content = self.parentItem()
        node_content = socket_content.parentItem()
        w_node = node_content.parentItem()
        self.input_offect = QPointF(0,0)
        if self.direction == VALUE_INPUT:
            self.input_offect = QPointF(6,0)
        w_node.bp_node.socket_base_offect = event.pos()-QPointF(25,10)+self.input_offect
        #鼠标拖拽时位置偏移
        super().mousePressEvent(event)
    
    def drawValueType(self,painter):
        """绘制插槽变量圆圈"""
        #分左右进行绘制两侧位置不同
        if self.direction == VALUE_INPUT:
            painter.translate(9.5, 10)
        elif self.direction == VALUE_OUTPUT:
            painter.translate(14.5, 10)
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        #绘制底层三角和圆形
        polygon = QPolygon()
        polygon.append(QPoint(4,self.radius*0.9))
        polygon.append(QPoint(self.radius*1.7,0))
        polygon.append(QPoint(4,-self.radius*0.9))
        painter.drawPolygon(polygon)
        painter.drawEllipse(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
        #如果此端口已经被连接的话绘制中部小圆形
        if not self.socket_state:
            painter.setBrush(self._brush2)
            painter.drawEllipse(-self.radius*1.2/2, -self.radius*1.2/2, 1.2 * self.radius, 1.2 * self.radius)
    
    def drawLogicType(self,painter):
        """绘制白色多边形"""
        w = self.white_output_width
        #分左右进行绘制两侧位置不同
        if self.direction == VALUE_INPUT:
            painter.translate(4, self.height/2-1)
        elif self.direction == VALUE_OUTPUT:
            painter.translate(self.width-3.3*w-4, self.height/2-1)
        path_content = QPainterPath()
        list01 = [0,-2*w, 2*w-1,-2*w, 4*w-1,0, 4*w-1,1, 2*w-1,2*w+1 ,0,2*w+1]
        list02: typing.List[QPoint] = []

        for i in range(0,len(list01),2):
            list02.append(QPoint(list01[i],list01[i+1]))
            
        path_content.addPolygon(QPolygonF(QPolygon(list02)))
        painter.setPen(self._white_pen)
        painter.setRenderHint(QPainter.Antialiasing, False)#反走样
        #如果此端口已经被连接的话
        if self.socket_state:
            painter.setBrush(self._brush3)
            painter.setRenderHint(QPainter.Antialiasing, True)#反走样
        painter.drawPath(path_content.simplified())
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """重载-绘制"""
        """
        self.brush_background = QBrush(QColor("#FF000000"))
        path_content1 = QPainterPath()
        path_content1.setFillRule(Qt.WindingFill)
        path_content1.addRect(0, 0, self.width, self.height)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.brush_background)
        painter.drawPath(path_content1.simplified())
        """
        if self.logic_type == SOCKET_TYPE_VALUE:
            self.drawValueType(painter)
        elif self.logic_type == SOCKET_TYPE_LOGIC:
            self.drawLogicType(painter)
    
        
    