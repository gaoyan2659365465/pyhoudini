from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class QHoudiniTextEdit(QScrollArea):
    """自定义文本框可以加自绘控件"""
    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        self.setAcceptDrops(True)#设置B可以接受拖动
        
        self.topFiller = QWidget()
        self.topFiller.setAcceptDrops(True)
        #self.topFiller.setCursor(QCursor(Qt.IBeamCursor))
        self.topFiller.setMinimumSize(250, 2000)#######设置滚动条的尺寸
        self.topFiller.setStyleSheet(u"background-color: rgb(33, 37, 43);")
        self.topFiller.dragEnterEvent = self.dragEnterEvent
        self.topFiller.dropEvent = self.dropEvent
        self.setWidget(self.topFiller)
        
        self.vlayout = QVBoxLayout(self.topFiller)
        self.topFiller.setLayout(self.vlayout)
        self.vlayout.setAlignment(Qt.AlignTop)
        
        self.textedit = QTextEdit("123456",self.topFiller)
        self.textedit.setFrameShape(QFrame.NoFrame)
        self.textedit.setStyleSheet(u"background-color: rgb(0, 0, 0);")
        self.textedit.setMinimumSize(400,150)
        self.textedit.setMaximumSize(400,150)
        
        self.textedit_width = 24
        self.textedit_height = 42
        self.document = self.textedit.document()
        self.document.contentsChanged.connect(self.textAreaChanged)
        self.textedit.setLineWrapMode(QTextEdit.NoWrap)
        
        self.b = QPushButton("你好呀!",self.topFiller)
        self.b.setMinimumSize(50,30)
        self.b.setMaximumSize(50,30)
        def runNodeData():
            data = self.textedit.toPlainText()
            exec(data)
        self.b.clicked.connect(runNodeData)
        
        self.vlayout.addWidget(self.textedit)
        self.vlayout.addWidget(self.b)
    
    def textAreaChanged(self):
        """文本框内容自适应尺寸"""
        self.document.adjustSize()
        newWidth = self.document.size().width() + 10
        newHeight = self.document.size().height() + 20
        if newWidth != self.textedit.width():
            self.textedit.setFixedWidth(newWidth)
            self.textedit.setMaximumWidth(newWidth)
        if newHeight != self.textedit.height():
            self.textedit.setFixedHeight(newHeight)
            self.textedit.setMaximumHeight(newHeight)
    
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
            a = "kwargs = {'toolname': 'geo', 'panename': '', 'altclick': False, 'ctrlclick': False, 'shiftclick': False, 'cmdclick': False, 'pane': None, 'viewport': None, 'inputnodename': '', 'outputindex': -1, 'inputs': [], 'outputnodename': '', 'inputindex': -1, 'outputs': [], 'branch': False, 'autoplace': False, 'requestnew': False}"
            b = "import hou"
            self.textedit.setText(a+'\n'+b+'\n'+data)

