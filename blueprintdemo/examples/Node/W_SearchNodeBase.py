#蓝图中鼠标右键会创建一个用于搜索节点创建节点的界面
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# 创建信号类
class QSearchNodeBaseSigner(QObject):
    addNode=Signal(object)#添加节点
    def __init__(self):
        super(QSearchNodeBaseSigner, self).__init__()
    def addNode_run(self,obj):
        self.addNode.emit(obj)



class W_SearchNodeBase(QGraphicsItem):
    def __init__(self,parent:QWidget=None):
        super().__init__(parent)
        self.initSizes()
        self.initAssets()
        self.initUI()
        self.isOk = False#只能创建一次
        self.setZValue(10000.0)#置顶

    def initSizes(self):
        self.width = 350
        self.height = 450
    
    def initAssets(self):
        self.signer = QSearchNodeBaseSigner()
        
        self.edge_roundness = 2.0#发亮边缘圆角度数
        self._color = QColor("#00000000")
        self._color_roundness = QColor("#FF000000")
        self._pen_roundness = QPen(self._color_roundness)
        self._pen_roundness.setWidthF(2.0)
        #节点背景颜色
        self._brush_background = QBrush(QColor("#0f110f"))
    
    def initUI(self):
        """初始化UI子控件"""
        
        #self.h_layoput = QHBoxLayout()
        #self.h_layoput.addWidget()
        
        
        self.push_button = QPushButton("BeginPlay")
        self.node_widget = QGraphicsProxyWidget(self)
        self.node_widget.setWidget(self.push_button)
        self.push_button.clicked.connect(self.addNode)
        
        self.push_button2 = QPushButton("PrintString")
        self.node_widget2 = QGraphicsProxyWidget(self)
        self.node_widget2.setWidget(self.push_button2)
        self.push_button2.clicked.connect(self.addNode2)
        self.node_widget2.setY(30)
        self.push_button3 = QPushButton("Branch")
        self.node_widget3 = QGraphicsProxyWidget(self)
        self.node_widget3.setWidget(self.push_button3)
        self.push_button3.clicked.connect(self.addNode3)
        self.node_widget3.setY(60)
        self.push_button4 = QPushButton("ForLoop")
        self.node_widget4 = QGraphicsProxyWidget(self)
        self.node_widget4.setWidget(self.push_button4)
        self.push_button4.clicked.connect(self.addNode4)
        self.node_widget4.setY(90)
        self.push_button5 = QPushButton("IntToString")
        self.node_widget5 = QGraphicsProxyWidget(self)
        self.node_widget5.setWidget(self.push_button5)
        self.push_button5.clicked.connect(self.addNode5)
        self.node_widget5.setY(120)
    
    def boundingRect(self) -> QRectF:
        """定义Qt的边框"""
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()
    
    def addNode(self):
        """向场景中添加节点"""
        if self.isOk:return
        self.isOk = True
        self.signer.addNode_run('BeginPlay')
    
    def addNode2(self):
        """向场景中添加节点"""
        if self.isOk:return
        self.isOk = True
        self.signer.addNode_run('PrintString')
    
    def addNode3(self):
        """向场景中添加节点"""
        if self.isOk:return
        self.isOk = True
        self.signer.addNode_run('Branch')
    
    def addNode4(self):
        """向场景中添加节点"""
        if self.isOk:return
        self.isOk = True
        self.signer.addNode_run('ForLoop')
    
    def addNode5(self):
        """向场景中添加节点"""
        if self.isOk:return
        self.isOk = True
        self.signer.addNode_run('IntToString')
    
    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        # 节点主体背景，没有这个节点主体会变成透明
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, 0, self.width, self.height, self.edge_roundness, self.edge_roundness)
        painter.setPen(self._pen_roundness)
        painter.setBrush(self._brush_background)
        painter.drawPath(path_content.simplified())