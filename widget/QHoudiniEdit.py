from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import requests
import webbrowser
import sys

from widget.StyleTool import *
from widget.FlowLayout import FlowLayout
from widget.Translation import ActionText


class QHWUrlWeb(QCommandLinkButton):
    resized = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.url = "http://www.baidu.com"
        
        #-----------------------------------
        self.setObjectName(u"commandLinkButton")
        self.setCursor(QCursor(Qt.PointingHandCursor))
        addStyleIcon(self,"cil-link.png")
        self.setText(QCoreApplication.translate("MainWindow", u"Link Button", None))
        self.setDescription(QCoreApplication.translate("MainWindow", u"Link description", None))
        self.resize(168,54)
        
        self.parent().createRightmenu = self.createRightmenu
        
    def resizeEvent(self, a0: QResizeEvent):
        self.resized.emit()#把尺寸事件转发给包裹框
    
    def setWebUrl(self):
        """保存url"""
        self.url = self.linew.text()
        self.selectw.close()
        self.setText(QCoreApplication.translate("MainWindow", self.linewA.text(), None))
        self.setDescription(QCoreApplication.translate("MainWindow", self.linewB.text(), None))
    
    def mousePressEvent(self, event: QMouseEvent):
        """鼠标按下"""
        if event.buttons() == Qt.RightButton:
            return
        webbrowser.open(self.url)
    
    def close(self):
        try:
            self.selectw.close()
        except:pass
        return super().close()

    def saveWidget(self):
        """序列化保存控件"""
        list0 = []
        list0.append(self.text())
        list0.append(self.description())
        list0.append(self.url)
        data = {'QHWUrlWeb':list0}
        return data
    
    def loadWidget(self,data):
        """序列化加载控件"""
        self.setText(QCoreApplication.translate("MainWindow", data[0], None))
        self.setDescription(QCoreApplication.translate("MainWindow", data[1], None))
        self.url = data[2]
    
    def openURLWidget(self):
        """打开设置界面"""
        #-----------------------------------
        self.selectw = QWidget()
        self.selectw.resize(300,150)
        self.selectw.setWindowFlags(Qt.WindowStaysOnTopHint)    #置顶
        self.selectw.setAttribute(Qt.WA_TranslucentBackground,True)#背景透明
        self.selectw.setStyleSheet(QHWUrlWebselectw)
        self.selectw_ = QWidget(self.selectw)
        self.selectw_.resize(self.selectw.size())
        self.selectw_.setStyleSheet("background-color: rgb(33, 37, 43);border-radius: 5px;")
        h_layout = QHBoxLayout()
        h_layout.setSpacing(0)
        h_layout.setContentsMargins(5, 0, 5, 0)
        v_layout = QVBoxLayout()
        v_layout.setSpacing(0)
        v_layout.setContentsMargins(0, 0, 0, 0)
        v_layout.addLayout(h_layout)
        self.selectw_.setLayout(v_layout)
        
        self.linew = QLineEdit(self.selectw_)
        self.linew.setText(self.url)
        buttonw = QPushButton("",self.selectw_)
        buttonw.clicked.connect(self.setWebUrl)
        buttonw.setCursor(QCursor(Qt.PointingHandCursor))
        buttonw.setStyleSheet("border: none;border-radius: 15px;")
        addStyleIcon(buttonw,"cil-save.png")
        h_layout.addWidget(self.linew)
        h_layout.addWidget(buttonw)
        
        self.linewA = QLineEdit(self.selectw_)
        self.linewA.setText(self.text())
        self.linewB = QLineEdit(self.selectw_)
        self.linewB.setText(self.description())
        v_layout.addWidget(self.linewA)
        v_layout.addWidget(self.linewB)
        
        self.selectw.show()
    
    def createRightmenu(self):
        """创建右键菜单函数"""
        parent = self.parent()
        parent.groupBox_menu = QMenu(parent)
        
        parent.actionA = QAction(u'更换连接',parent)#创建菜单选项对象
        parent.groupBox_menu.addAction(parent.actionA)
        parent.actionA.triggered.connect(self.openURLWidget)
        
        parent.actionC = QAction(u'删除',parent)#创建菜单选项对象
        parent.groupBox_menu.addAction(parent.actionC)
        parent.actionC.triggered.connect(parent.RightMenuEvent)
        
        parent.groupBox_menu.popup(QCursor.pos())

class QHWUrlImage(QLabel):
    """加载网络图片"""
    resized = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.url = "https://tse3-mm.cn.bing.net/th/id/OIP-C.Tq_jFLCrIeR5cIWDqWVArQHaLP?pid=ImgDet&rs=1"
        self.initImage()
        self.parent().createRightmenu = self.createRightmenu
    
    def initImage(self):
        """初始化图片"""
        res = requests.get(self.url)
        img = QImage.fromData(res.content)
        self.setPixmap(QPixmap.fromImage(img))
        self.setScaledContents(True)
        self.resize(img.width(),img.height())
    
    def resizeEvent(self, a0: QResizeEvent):
        self.resized.emit()#把尺寸事件转发给包裹框
    
    def close(self) -> bool:
        try:
            self.selectw.close()
        except:pass
        return super().close()
    
    def setImage(self):
        self.selectw = QWidget()
        self.selectw.resize(300,40)
        self.selectw.setWindowFlags(Qt.WindowStaysOnTopHint)    #置顶
        self.selectw.setStyleSheet(u'QWidget {color: rgb(221, 221, 221);\
	                                font: 10pt "Segoe UI";}\
                                    QLineEdit {\
                                    background-color: rgb(33, 37, 43);\
                                    border-radius: 5px;\
                                    border: 2px solid rgb(33, 37, 43);\
                                    padding-left: 10px;\
                                    selection-color: rgb(255, 255, 255);\
                                    selection-background-color: rgb(255, 121, 198);}\
                                    QLineEdit:hover {\
                                        border: 2px solid rgb(64, 71, 88);}\
                                    QLineEdit:focus {\
                                        border: 2px solid rgb(91, 101, 124);}')
        self.selectw_ = QWidget(self.selectw)
        self.selectw_.resize(self.selectw.size())
        self.selectw_.setStyleSheet("background-color: rgb(33, 37, 43);border-radius: 5px;")
        h_layout = QHBoxLayout()
        h_layout.setSpacing(5)
        h_layout.setContentsMargins(5, 0, 5, 0)
        self.selectw_.setLayout(h_layout)
        
        self.linew = QLineEdit(self.selectw_)
        self.linew.setText(self.url)
        buttonw = QPushButton("",self.selectw_)
        buttonw.clicked.connect(self.setImageUrl)
        buttonw.setCursor(QCursor(Qt.PointingHandCursor))
        buttonw.setStyleSheet("border: none;border-radius: 15px;")
        addStyleIcon(buttonw,"cil-save.png")
        h_layout.addWidget(self.linew)
        h_layout.addWidget(buttonw)
        self.selectw.show()
            
    def setImageUrl(self):
        """保存图片url"""
        self.url = self.linew.text()
        self.initImage()
        self.selectw.close()
    
    def saveWidget(self):
        """序列化保存控件"""
        data = {'QHWUrlImage':self.url}
        return data
    
    def loadWidget(self,data):
        """序列化加载控件"""
        self.url = data
        self.initImage()
    
    def createRightmenu(self):
        """创建右键菜单函数"""
        parent = self.parent()
        parent.groupBox_menu = QMenu(parent)
        
        parent.actionA = QAction(u'更换图片',parent)#创建菜单选项对象
        parent.groupBox_menu.addAction(parent.actionA)
        parent.actionA.triggered.connect(self.setImage)
        
        parent.actionC = QAction(u'删除',parent)#创建菜单选项对象
        parent.groupBox_menu.addAction(parent.actionC)
        parent.actionC.triggered.connect(parent.RightMenuEvent)
        
        parent.groupBox_menu.popup(QCursor.pos())

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
        
        self.datatext = ""#用于保存节点代码
    
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
    
    def saveWidget(self):
        """序列化保存控件"""
        data = {'QHWNode':self.datatext}
        return data
    
    def loadWidget(self,data):
        """序列化加载控件"""
        self.datatext = data

class QHTWMarkdown(ActionText):
    """支持markdown语法的文本框"""
    resized = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setStyleSheet(u"background-color: rgb(44, 49, 57);")
        self.setMinimumSize(400,150)
        self.setMaximumSize(400,150)
        self.document_ = self.document()
        self.document_.contentsChanged.connect(self.textAreaChanged)
        self.markdowncore = ''
        self.setLineWrapMode(QTextEdit.NoWrap)#不自动换行
        self.setContextMenuPolicy(Qt.CustomContextMenu)#右键菜单
        
        self.parent().createRightmenu = self.createRightmenu
        
        
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
    
    def toTextEditEvent(self):
        self.setText(self.toMarkdown())
        self.markdowncore = self.toMarkdown()#记录一下代码
    
    def toMarkdownEvent(self):
        if self.markdowncore == "":
            self.markdowncore = self.toPlainText()#记录一下代码
        self.setMarkdown(self.markdowncore)
    
    def createRightmenu(self):
        """创建右键菜单函数"""
        parent = self.parent()
        parent.groupBox_menu = QMenu(parent)
        
        parent.actionA = QAction(u'Markdown代码',parent)#创建菜单选项对象
        parent.groupBox_menu.addAction(parent.actionA)
        parent.actionA.triggered.connect(self.toTextEditEvent)
        
        parent.actionB = QAction(u'最终效果',parent)#创建菜单选项对象
        parent.groupBox_menu.addAction(parent.actionB)
        parent.actionB.triggered.connect(self.toMarkdownEvent)
        
        parent.actionC = QAction(u'删除',parent)#创建菜单选项对象
        parent.groupBox_menu.addAction(parent.actionC)
        parent.actionC.triggered.connect(parent.RightMenuEvent)
        
        parent.groupBox_menu.popup(QCursor.pos())
            
    def saveWidget(self):
        """序列化保存控件"""
        data = {'QHTWMarkdown':self.toHtml()}
        return data
    
    def loadWidget(self,data):
        """序列化加载控件"""
        self.setHtml(data)

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
        self.setLineWrapMode(QTextEdit.NoWrap)#不自动换行
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
    
    def saveWidget(self):
        """序列化保存控件"""
        data = {'QHTWTextEdit':self.toHtml()}
        return data
    
    def loadWidget(self,data):
        """序列化加载控件"""
        self.setHtml(data)

class QHoudiniWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName("QHoudiniWidget")
        self.styledata = QHoudiniWidgetStyle
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
        self.houdiniwidget.close()
        self.close()

    def leaveEvent(self, QEvent):
       """鼠标离开事件"""
       self.setStyleSheet(self.styledata)
    
    def saveWidget(self):
        """序列化保存控件"""
        return self.houdiniwidget.saveWidget()

    def loadWidget(self,data):
        """序列化加载控件"""
        return self.houdiniwidget.loadWidget(data)
        
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
        self.topFiller.setContentsMargins(7, 7, 7, 7)
        self.topFiller.dragEnterEvent = self.dragEnterEvent#拖拽事件
        self.topFiller.dropEvent = self.dropEvent#拖拽事件
        #self.topFiller.setCursor(QCursor(Qt.IBeamCursor))
        self.setWidget(self.topFiller)
        
        #self.vlayout = QVBoxLayout(self.topFiller)
        self.vlayout = FlowLayout(self.topFiller)
        self.topFiller.setLayout(self.vlayout)
        self.vlayout.setAlignment(Qt.AlignTop)
    
    def createRightmenu(self):
        """创建右键菜单函数"""
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'新建文本框',self)#创建菜单选项对象
        #self.actionA.setShortcut('Ctrl+S')#设置动作A的快捷键
        self.groupBox_menu.addAction(self.actionA)
        def RightMenuEvent():
            """右键菜单点击事件"""
            textedit = QHTWTextEdit()
            houdiniwidget = QHoudiniWidget(self.topFiller)
            houdiniwidget.addHoudiniWidget(textedit)
            self.vlayout.addWidget(houdiniwidget)
        self.actionA.triggered.connect(RightMenuEvent)
        
        self.actionB = QAction(u'新建网络图片',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionB)
        def RightMenuBEvent():
            """右键菜单点击事件"""
            houdiniwidget = QHoudiniWidget(self.topFiller)
            textedit = QHWUrlImage(houdiniwidget)
            houdiniwidget.addHoudiniWidget(textedit)
            self.vlayout.addWidget(houdiniwidget)
        self.actionB.triggered.connect(RightMenuBEvent)
        
        self.actionC = QAction(u'新建网址链接',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionC)
        def RightMenuCEvent():
            """右键菜单点击事件"""
            houdiniwidget = QHoudiniWidget(self.topFiller)
            textedit = QHWUrlWeb(houdiniwidget)
            houdiniwidget.addHoudiniWidget(textedit)
            self.vlayout.addWidget(houdiniwidget)
        self.actionC.triggered.connect(RightMenuCEvent)
        
        self.actionD = QAction(u'新建Markdown',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionD)
        def RightMenuDEvent():
            """右键菜单点击事件"""
            houdiniwidget = QHoudiniWidget(self.topFiller)
            textedit = QHTWMarkdown(houdiniwidget)
            houdiniwidget.addHoudiniWidget(textedit)
            self.vlayout.addWidget(houdiniwidget)
        self.actionD.triggered.connect(RightMenuDEvent)
        #声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，
        self.groupBox_menu.popup(QCursor.pos())
    
    def resizeEvent(self, a0: QResizeEvent):
        self.topFiller.setGeometry(0,0,self.width()-10,self.height())
    
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

    def saveWidget(self):
        """序列化保存控件"""
        items = []
        for i in range(self.vlayout.count()):
            item = self.vlayout.itemAt(i).widget()
            items.append(item)
        itemdata = []
        for item in items:
            if item.isVisible():
                item:QHoudiniWidget
                itemdata.append(item.saveWidget())#获取数据到列表
        return itemdata
    
    def loadWidget(self,data):
        """序列化加载控件"""
        for key in data:
            for key_name in key:
                houdiniwidget = QHoudiniWidget(self.topFiller)
                #print(key_name)
                AClass = getattr(sys.modules[__name__],key_name)
                textedit = AClass(houdiniwidget)
                houdiniwidget.addHoudiniWidget(textedit)
                self.vlayout.addWidget(houdiniwidget)
                #print(key[key_name])
                houdiniwidget.loadWidget(key[key_name])