# -*- coding: utf-8 -*-
import math
from examples.Node.W_Scene import *
from examples.Node.W_DockWidget import *
import typing

#QRubberBand
class W_RubberBand(QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.hide()
        self.pen = QPen(QColor('#ffffff'),1,Qt.DashLine)
        self.pen.setDashPattern([6.0,4.0])
    def paintEvent(self, a0: QPaintEvent):
        painter = QPainter(self)
        painter.setPen(self.pen)
        painter.drawRect(0, 0, self.width()-2, self.height()-2)

class W_View(QGraphicsView):
    def __init__(self, graphic_scene, parent=None):
        super().__init__(parent)
        self.gr_scene = graphic_scene  # 将scene传入此处托管，方便在view中维护
        self.parent = parent
        self.setGeometry(0,0,800,700)

        self.init_ui()
        self.init_data()
        
        self.zoom = 10
        self.zoomStep = 1
        self.zoomClamp = True
        self.zoomRange = [0, 10]
        self.zoomInFactor = 1.25
        
        self.socket_content = None
        
        self.rb = W_RubberBand(self)
        self.gr_scene.addWidget(self.rb)
        self.rb_size = QPoint()
        

    def init_ui(self):
        self.setScene(self.gr_scene)
        # 设置渲染属性
        self.setRenderHints(QPainter.Antialiasing |                    # 抗锯齿
                            QPainter.HighQualityAntialiasing |         # 高品质抗锯齿
                            QPainter.TextAntialiasing |                # 文字抗锯齿
                            QPainter.SmoothPixmapTransform |           # 使图元变换更加平滑
                            QPainter.LosslessImageRendering)           # 不失真的图片渲染
        # 视窗更新模式
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        # 设置水平和竖直方向的滚动条不显示
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(self.AnchorUnderMouse)
        # 设置拖拽模式
        self.setDragMode(self.NoDrag)#QRubberBand ScrollHandDrag RubberBandDrag NoDrag
        self.setAcceptDrops(True)
    
    def init_data(self):
        """初始化类成员数据"""
        # 一些关于网格背景的设置
        self.grid_size = 16     # 一块网格的大小 （正方形的）
        self.grid_squares = 8   # 网格中正方形的区域个数
		# 一些颜色
        self._color_dark = QColor('#151515')
        self._color_light = QColor('#313131')
        self._color_background = QColor('#262626')
        # 设置画背景的画笔
        self.setBackgroundBrush(self._color_background)
		# 一些画笔
        self._pen_dark = QPen(self._color_dark)
        self._pen_light = QPen(self._color_light)
        self._pen_dark.setWidth(1)
        self._pen_light.setWidth(1)
        #设置Scene尺寸
        self.setGrSceneRect(64000, 64000)
    
    def wheelEvent(self, event:QWheelEvent):
        """重载-处理缩放"""
        # 计算缩放因子
        zoomOutFactor = 1 / self.zoomInFactor
        # 计算放大
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep
        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True
        # 设置场景规模
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
    
    def setGrSceneRect(self, width:int, height:int):
        """设置Scene尺寸"""
        self.setSceneRect(-width // 2, -height // 2, width, height)
    
    def drawBackground(self, painter, rect):
        """重载-绘制网格"""
        super().drawBackground(painter, rect)
        painter.setRenderHint(QPainter.Antialiasing, False)#反走样
		# 获取背景矩形的上下左右的长度，分别向上或向下取整数
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))
		# 从左边和上边开始
        first_left = left - (left % self.grid_size)  # 减去余数，保证可以被网格大小整除
        first_top = top - (top % self.grid_size)
		# 分别收集明、暗线
        lines_light: typing.List[QLine] = []
        lines_dark: typing.List[QLine] = []
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))
        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))
		# 最后把收集的明、暗线分别画出来
        painter.setPen(self._pen_light)
        if lines_light:
            painter.drawLines(lines_light)
        painter.setPen(self._pen_dark)
        if lines_dark:
            painter.drawLines(lines_dark)
    
    def mousePressEvent(self, event:QMouseEvent):
        """重载-鼠标按下"""
        #scene
        item = self.getItemAtClick(event)
        self.gr_scene.setClickItem(item)
        self.gr_scene.setStartPos(event.pos())
        
        if event.button() == Qt.MiddleButton:
            pass
            #self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
            pass
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: 'QMouseEvent'):
        """重载-鼠标移动"""
        item = self.getItemAtClick(event)
        if isinstance(item, W_SocketBase) or isinstance(item, W_SocketContent):
            if isinstance(item, W_SocketBase):
                socket_content = item.parentItem()
            elif isinstance(item, W_SocketContent):
                socket_content = item
            if self.socket_content == socket_content:
                socket_content.mouse_stay = True
            else:
                if self.socket_content != None:
                    self.socket_content.mouse_stay = False
                self.socket_content = socket_content
                socket_content.mouse_stay = True
        else:
            if self.socket_content != None:
                self.socket_content.mouse_stay = False
        super().mouseMoveEvent(event)
        #拖拽框尺寸
        self.NewPos = event.pos()
        NewRect = QRect(self.rb_size,self.NewPos)
        self.rb.setGeometry(NewRect.normalized())
        self.NewRect = NewRect.normalized()#保存区域用于检测
        if self.rb.isVisible():
            self.rb.update()
            for w_node in self.gr_scene.selectedItems():#所有选中的都取消选择
                w_node.setSelected(False)
            items = self.items(self.NewRect)
            for i in items:
                if isinstance(i, W_NodeBase):
                    i.setSelected(True)
        
    def mouseReleaseEvent(self, event:QMouseEvent):
        """重载-鼠标松开"""
        #scene
        sc_pos = self.mapToScene(event.pos())
        self.gr_scene.setEndPos(event.pos(),sc_pos)
        item = self.getItemAtClick(event)
        self.gr_scene.setClickItem(item)
        
        if event.button() == Qt.MiddleButton:
            pass
            #self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
            pass
        else:
            super().mouseReleaseEvent(event)

    def leftMouseButtonPress(self, event:QMouseEvent):
        """当鼠标左键被按下时"""
        # 获取我们点击的项目
        self.setDragMode(self.NoDrag)
        item = self.getItemAtClick(event)
        if isinstance(item, W_TitleBase):
            self.setDragMode(self.ScrollHandDrag)
            releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
            self.mouseReleaseEvent(releaseEvent)
            fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                    Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
            super().mousePressEvent(fakeEvent)
            self.setDragMode(self.NoDrag)
            return
        if isinstance(item, W_SocketBase):
            self.setCursor(Qt.ArrowCursor)
            self.setDragMode(self.NoDrag)
        super().mousePressEvent(event)
        #拖拽框尺寸
        if not item:
            self.rb.show()
            self.rb_size = event.pos()
            self.rb.setGeometry(QRect(self.rb_size,QSize()))
    
    def leftMouseButtonRelease(self, event:QMouseEvent):
        """当鼠标左键被释放"""
        super().mouseReleaseEvent(event)
        self.rb.hide()#隐藏拖拽框
    
    def rightMouseButtonPress(self, event:QMouseEvent):
        """当鼠标右键被按下"""
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def rightMouseButtonRelease(self, event:QMouseEvent):
        """当鼠标右键被释放"""
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())
        super().mouseReleaseEvent(releaseEvent)
        super().mouseReleaseEvent(event)
        self.setDragMode(QGraphicsView.NoDrag)
    
    def getItemAtClick(self, event:QEvent)-> 'QGraphicsItem':
        """返回鼠标位置的对象"""
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    
