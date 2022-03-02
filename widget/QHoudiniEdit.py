from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class QHWNode(QLabel):
    resized = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap(__file__[:-15] + "image/node.jpg")\
            .scaled(100,50,Qt.IgnoreAspectRatio,Qt.SmoothTransformation))
        self.setMinimumSize(100,50)
        self.setMaximumSize(100,50)
        self.setScaledContents(True)
        self.resize(100,50)
        
        self.datatext = ""#用于保持节点代码
    
    def setDataText(self,text):
        """设置节点代码"""
        self.datatext = text
    
    def resizeEvent(self, a0: QResizeEvent):
        self.resized.emit()#把尺寸事件转发给包裹框
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下"""
        if event.buttons() == Qt.LeftButton:
            if self.datatext != "":
                try:
                    exec(self.datatext)
                except:pass
        

class QHTWTextEdit(QTextEdit):
    resized = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet(u"background-color: rgb(44, 49, 57);")
        self.setMinimumSize(400,150)
        self.setMaximumSize(400,150)
        self.textedit_width = 24
        self.textedit_height = 42
        self.document_ = self.document()
        self.document_.contentsChanged.connect(self.textAreaChanged)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setContextMenuPolicy(Qt.CustomContextMenu)#右键菜单
    
    def resizeEvent(self, a0: QResizeEvent):
        self.resized.emit()#把尺寸事件转发给包裹框
    
    def textAreaChanged(self):
        """文本框内容自适应尺寸"""
        self.document_.adjustSize()
        newWidth = self.document_.size().width() + 10
        newHeight = self.document_.size().height() + 20
        if newWidth != self.width():
            self.setFixedWidth(newWidth)
            self.setMaximumWidth(newWidth)
        if newHeight != self.height():
            self.setFixedHeight(newHeight)
            self.setMaximumHeight(newHeight)

class QHoudiniWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("QHoudiniWidget")
        self.styledata = u"#QHoudiniWidget { background-color: rgb(44, 49, 57); border: none;  border-radius: 5px; }\
                             #QHoudiniWidget:hover { background-color: rgb(44, 49, 57); border: 2px solid rgb(52, 59, 72); border-radius: 4px; }"
        self.setStyleSheet(self.styledata)
        self.setFixedSize(50,50)
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)#右键菜单
        self.customContextMenuRequested.connect(self.createRightmenu)  # 连接到菜单显示函数
    
    def addHoudiniWidget(self,widget:QWidget):
        """把其他控件添加进来"""
        self.houdiniwidget = widget
        widget.setParent(self)
        widget.move(5,5)
        def resize_():
            self.setFixedSize(widget.width()+10,widget.height()+10)
        widget.resized.connect(resize_)
        widget.customContextMenuRequested.connect(self.createRightmenu)  # 连接到菜单显示函数
    
    def paintEvent(self, event):
        """重载-绘制"""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下"""
        self.setStyleSheet(u"#QHoudiniWidget { \
            background-color: rgb(44, 49, 57); \
            border: none;  border-radius: 5px;}")
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):#鼠标松开
        self.setStyleSheet(self.styledata)
        super().mouseReleaseEvent(event)
    
    def createRightmenu(self):
        """创建右键菜单函数"""
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'删除',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionA)
        self.actionA.triggered.connect(self.RightMenuEvent)
        self.groupBox_menu.popup(QCursor.pos())
    
    def RightMenuEvent(self):
        """右键菜单点击事件"""
        self.close()

    def leaveEvent(self, QEvent):
       """鼠标离开事件"""
       self.setStyleSheet(self.styledata)
        
class QHoudiniEdit(QScrollArea):
    """自定义框可以加自绘控件"""
    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)#无边框
        self.setAcceptDrops(True)#设置B可以接受拖动
        self.setContextMenuPolicy(Qt.CustomContextMenu)#右键菜单
        self.customContextMenuRequested.connect(self.createRightmenu)  # 连接到菜单显示函数
        
        self.topFiller = QWidget()
        self.topFiller.setObjectName("QHoudiniEdit")
        self.topFiller.setAcceptDrops(True)
        self.topFiller.setMinimumSize(250, 2000)#设置滚动条的尺寸
        self.topFiller.setStyleSheet(u"#QHoudiniEdit{background-color: rgb(33, 37, 43);}")
        self.topFiller.dragEnterEvent = self.dragEnterEvent#拖拽事件
        self.topFiller.dropEvent = self.dropEvent#拖拽事件
        #self.topFiller.setCursor(QCursor(Qt.IBeamCursor))
        self.setWidget(self.topFiller)
        
        self.vlayout = QVBoxLayout(self.topFiller)
        self.topFiller.setLayout(self.vlayout)
        self.vlayout.setAlignment(Qt.AlignTop)
    
    def createRightmenu(self):
        """创建右键菜单函数"""
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'新建',self)#创建菜单选项对象
        #self.actionA.setShortcut('Ctrl+S')#设置动作A的快捷键
        self.groupBox_menu.addAction(self.actionA)
        def RightMenuEvent():
            """右键菜单点击事件"""
            textedit = QHTWTextEdit()
            houdiniwidget = QHoudiniWidget(self.topFiller)
            houdiniwidget.addHoudiniWidget(textedit)
            self.vlayout.addWidget(houdiniwidget)
        self.actionA.triggered.connect(RightMenuEvent)
        self.groupBox_menu.popup(QCursor.pos())#声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，
    
    def resizeEvent(self, a0: QResizeEvent):
        self.topFiller.setGeometry(0,0,self.width()-10,self.height())
    
    # def dragEnterEvent(self,e):
    #     print("拖动成功1:")
    #     print(e)
        
    def dropEvent(self, event):
        source = event.source()
        print("拖动成功:")
        if source and source != self:
            nodename = event.mimeData().text()
            print(nodename)
            import toolutils
            data = toolutils.generateToolScriptForNode(nodename)
            a = "kwargs = {'toolname': 'geo', 'panename': '', 'altclick': False, 'ctrlclick': False,\
                'shiftclick': False, 'cmdclick': False, 'pane': None, 'viewport': None, 'inputnodename': '',\
                'outputindex': -1, 'inputs': [], 'outputnodename': '', 'inputindex': -1, 'outputs': [],\
                'branch': False, 'autoplace': False, 'requestnew': False}"
            b = "import hou"
            node = QHWNode()
            node.setDataText(a+'\n'+b+'\n'+data)
            houdiniwidget = QHoudiniWidget(self.topFiller)
            houdiniwidget.addHoudiniWidget(node)
            self.vlayout.addWidget(houdiniwidget)

