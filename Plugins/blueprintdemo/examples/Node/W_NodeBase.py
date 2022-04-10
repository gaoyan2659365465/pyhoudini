# -*- coding: utf-8 -*-
from .W_TitleBase import W_TitleBase
from .W_NodeContent import *
from .BP_Json import BP_Json



class W_NodeBase(QGraphicsItem,BP_Json):
    def __init__(self,bp_node=None):
        super().__init__()
        self.bp_node = bp_node
        self.initUI()
        
    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)# ***设置图元是可以被选择的
        self.setFlag(QGraphicsItem.ItemIsMovable)   # ***设置图元是可以被移动的
        self.setAcceptHoverEvents(True)#接受悬停事件
        self.initSizes()
        self.initAssets()
        #节点背景
        self.w_background = W_NodeContent(self,self.width,self.height,self.title_height)
        #标题栏
        self.w_title = W_TitleBase(self,self.width,self.title_height)
        
    def initSizes(self):
        self.width = 200
        self.height = 100
        self.min_width = 200#节点的最小宽度
        self.title_height = 38#标题栏高度
        self.edge_roundness = 10.0#发亮边缘圆角度数
    
    def initAssets(self):
        self._color = QColor("#00000000")
        self._color_selected = QColor("#FFFFA637")
        self._color_roundness = QColor("#FF000000")
        self._pen_default = QPen(self._color)
        self._pen_default.setWidthF(2.0)
        self._pen_selected = QPen(self._color_selected)
        self._pen_selected.setWidthF(3.2)
        self._pen_roundness = QPen(self._color_roundness)
        self._pen_roundness.setWidthF(2.0)
        #节点背景颜色
        self._brush_background = QBrush(QColor("#0f110f"))
    
    def boundingRect(self) -> QRectF:
        """定义Qt的边框"""
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()
    
    def getNodeTitleName(self):
        """获得节点标题栏文字"""
        return self.w_title.getNodeTitleName()
    
    def setNodeTitleName(self,Name:str=''):
        """设置节点标题栏文字"""
        self.w_title.setNodeTitleName(Name)
    
    def setNodeTitlePix(self,pix:int=0):
        """设置节点标题栏图标"""
        self.w_title.setNodeTitlePix(pix)
    
    def setNodeTitleColor(self,color):
        """设置标题栏颜色"""
        self.w_title.setNodeTitleColor(color)
    
    def addSocket(self,data_type:int=0,direction:int=0,logic_type:int=0):
        """给节点内容增加端口
        :param data_type: 节点表示的变量的数据类型（整型/字符串）
        :param direction: 需要在节点输(入/出)侧添加端口
        :param logic_type: 节点表示的变量的逻辑类型（数据/逻辑）
        """
        return self.w_background.addSocket(data_type,direction,logic_type)
    
    def getAllSocket(self):
        """获取此节点所有插槽"""
        return self.w_background.getAllSocket()
    
    def getSocketLocation(self,socket_num:int=0):
        """获取插槽的绝对位置"""
        return self.w_background.pos() + self.w_background.getSocketLocation(socket_num)
    
    def getSocketDirection(self,socket_num:int=0)->bool:
        """获取插槽是左边还是右边"""
        return self.w_background.getSocketDirection(socket_num)
    
    def setSocketState(self,socket_num:int=0,isLink:bool=False):
        """设置端口状态是否已连接"""
        self.w_background.setSocketState(socket_num,isLink)
    
    def getSocketColor(self,socket_num:int=0):
        """获取插槽的颜色"""
        return self.w_background.getSocketColor(socket_num)
    
    def setAutomaticSize(self):
        """自动设置节点所需要的尺寸"""
        width,height = self.w_background.getRequiredSize()#获取子控件合适的尺寸
        if self.min_width>width:#设置尺寸不小于self.width
            self.width = self.min_width
            self.height = height
            self.w_background.setAutomaticSize(self.width,height)
            self.w_title.setAutomaticSize(self.width,self.w_title.height)#设置标题栏大小
            return
        self.width = width
        self.height = height
        self.w_background.setAutomaticSize(width,height)
        self.w_title.setAutomaticSize(width,self.w_title.height)#设置标题栏大小
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        """重载-绘制"""
        # 节点主体背景，没有这个节点主体会变成透明
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
        painter.setPen(self._pen_roundness)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())
        
        # 节点被点击以后会周围发光
        path_outline = QPainterPath()
        path_outline.addRoundedRect(-2, -2, self.width+4, self.height+4, self.edge_roundness, self.edge_roundness)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.drawPath(path_outline.simplified())
    
    def setIsMovable(self,isMovable:bool=True):
        """设置节点是否可以拖动"""
        self.setFlag(QGraphicsItem.ItemIsMovable,isMovable)   # ***设置图元是可以被移动的
    
    #region 序列化
    def dump(self):
        """保存"""
        title_data = self.w_title.dump()
        node_data = self.w_background.dump()
        data = {'x':self.x(),
                'y':self.y(),
                'w_title':title_data,
                'node_data':node_data,
                }
        return data
    def load(self,obj):
        """加载"""
        x = obj['x']
        y = obj['y']
        self.setX(x)
        self.setY(y)
        #---------------
        w_title = obj['w_title']
        node_data = obj['node_data']
        self.w_title.load(w_title)
        self.w_background.load(node_data)
        return
    #endregion