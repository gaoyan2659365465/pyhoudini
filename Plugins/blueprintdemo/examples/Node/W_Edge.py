# -*- coding: utf-8 -*-
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import math
from .BP_Json import BP_Json
import uuid

EDGE_POS_SOURCE = 0         #线连接端-起点
EDGE_POS_DESTINATION = 1    #线连接端-终点

EDGE_CP_ROUNDNESS = 0     #: 贝塞尔控制点在直线上的距离
class GraphicsEdgePathBezier():
    """三次线连接图形边"""
    def __init__(self, owner:QGraphicsPathItem=None):
        # 保持对所有者GraphicsEdge类的引用
        self.owner = owner
    def calcPath(self) -> QPainterPath:
        """计算三次Bezier线连接与2个控制点

        :returns: ``QPainterPath`` of the cubic Bezier line
        :rtype: ``QPainterPath``
        """
        s = self.owner.posSource
        d = self.owner.posDestination
        dist = (d[0] - s[0]) * 0.5
        if dist>0:
            dist = dist * -1

        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        if (s[0] > d[0] and True) or (s[0] < d[0] and True):
            cpx_d *= -1
            cpx_s *= -1

            cpy_d = (
                (s[1] - d[1]) / math.fabs(
                    (s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.00001
                )
            ) * EDGE_CP_ROUNDNESS
            cpy_s = (
                (d[1] - s[1]) / math.fabs(
                    (d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.00001
                )
            ) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(self.owner.posSource[0], self.owner.posSource[1]))
        path.cubicTo( s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.owner.posDestination[0], self.owner.posDestination[1])

        return path

class W_Edge(QGraphicsPathItem,BP_Json):
    """图形边缘的基类"""
    def __init__(self, parent:QWidget=None):
        super().__init__(parent)
        # 我们初始化变量
        self.posSource = [0, 0]
        self.posDestination = [200, 100]
        self.hovered = False    #鼠标悬停
        self.pathCalculator = GraphicsEdgePathBezier(self)
        self.initAssets()
        self.initUI()
        self.nodes = []#只是存一下
        self.uuid = str(uuid.uuid1())#生成唯一ID

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.setZValue(-1)
        
    def initAssets(self):
        self._color = QColor("#ffffff")
        self._color_hovered = QColor("#ffffffff")
        self._pen = QPen(self._color)
        self._pen_hovered = QPen(self._color_hovered)
        self._pen.setWidthF(3.0)
        self._pen_hovered.setWidthF(5.0)
    
    def setSource(self, x:float, y:float):
        """设置连接线的开始点坐标"""
        self.posSource = [x, y]
    def setDestination(self, x:float, y:float):
        """设置连接线的目的地坐标"""
        self.posDestination = [x, y]
    
    def setLocation(self,EDGE_POS,x:float, y:float):
        """设置连接线两端位置"""
        if EDGE_POS == EDGE_POS_SOURCE:
            self.setSource(x, y)
        elif EDGE_POS == EDGE_POS_DESTINATION:
            self.setDestination(x, y)
        
    def setEdgeColor(self,color):
        """设置连接线颜色"""
        self._color = color
        self._pen = QPen(self._color)
        self._pen.setWidthF(3.0)
        self._color_hovered = color
        self._pen_hovered = QPen(self._color_hovered)
        self._pen_hovered.setWidthF(5.0)
        
        
    def setNodes(self,x,y):
        """设置Nodes列表用于存储"""
        self.nodes.append(x)
        self.nodes.append(y)
    
    def getNewNode(self,node):
        """传入一个node获取另外一个node"""
        if self.nodes[0] == node:
            return self.nodes[1]
        if self.nodes[1] == node:
            return self.nodes[0]
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        self.setPath(self.calcPath())
        painter.setBrush(Qt.NoBrush)
        if self.hovered == False:
            painter.setPen(self._pen)
        else:
            painter.setPen(self._pen_hovered)
        painter.drawPath(self.path())
    
    def hoverEnterEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """处理悬停效果"""
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event: 'QGraphicsSceneHoverEvent') -> None:
        """处理悬停效果"""
        self.hovered = False
        self.update()
    
    def calcPath(self) -> QPainterPath:
        return self.pathCalculator.calcPath()
    
    def boundingRect(self) -> QRectF:
        """定义Qt的边框"""
        return self.calcPath().boundingRect()

    #region 序列化
    def dump(self):
        """保存"""
        self.nodes[0].uuid
        self.nodes[1].uuid
        data = {'edge_node0':self.nodes[0].uuid,
                'edge_node1':self.nodes[1].uuid,
                'edge_uuid':self.uuid,
                }
        return data
    def load(self,obj):
        """加载"""
        return
    #endregion