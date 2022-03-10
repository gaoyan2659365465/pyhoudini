#coding=utf-8

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


from widget.googletrans.google_trans_new import google_translator
from widget.StyleTool import *

class ActionText(QTextEdit):
    isEdit = False
    signal = Signal()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def mouseReleaseEvent(self, event):
        if self.isEdit == False:
            textCursor = self.textCursor()
            index = textCursor.position()
            # self.action_text.find(txt, QTextDocument.FindWholeWords)
            #self.signal.indexTrigger.emit(index)
    def setColumnPos(self, index):
        textCursor = self.action_text.textCursor()
        textCursor.select(QTextCursor.LineUnderCursor)
        self.action_text.setTextCursor(textCursor)
    def insertFromMimeData(self, soc):
        if soc.hasText():
            self.textCursor().insertText(soc.text())  #去除粘贴格式

class TranslationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        v_layout = QVBoxLayout()
        v_layout.setSpacing(10)
        v_layout.setContentsMargins(10,10,10,0)#layout边缘
        self.setLayout(v_layout)
        
        self.textedit = ActionText()
        v_layout.addWidget(self.textedit)
        self.textedit.setFrameShape(QFrame.NoFrame)
        self.textedit.setStyleSheet(u"background-color: rgb(44, 49, 57);")
        
        self.texteditB = QTextEdit()
        v_layout.addWidget(self.texteditB)
        self.texteditB.setFrameShape(QFrame.NoFrame)
        self.texteditB.setStyleSheet(u"background-color: rgb(44, 49, 57);")
        
        h_layout_text = QHBoxLayout()
        button = QPushButton("",self.textedit)
        button.clicked.connect(self.startTranslation)
        button.setCursor(QCursor(Qt.PointingHandCursor))
        button.setFixedSize(28,28)
        button.setStyleSheet(TranslationWidgetButton)
        addStyleIcon(button,"cil-text-size.png")
        
        buttonB = QPushButton("",self.textedit)
        buttonB.clicked.connect(self.removeText)
        buttonB.setCursor(QCursor(Qt.PointingHandCursor))
        buttonB.setFixedSize(28,28)
        buttonB.setStyleSheet(TranslationWidgetButton)
        addStyleIcon(buttonB,"cil-x.png")
        
        self.textedit.setLayout(h_layout_text)
        h_layout_text.addStretch()
        h_layout_text.addWidget(button,0,Qt.AlignBottom)
        h_layout_text.addWidget(buttonB,0,Qt.AlignBottom)
        #v_layout.addWidget(button)
        
        #-----------
        self.labelB = QLabel("翻译结果已经复制",self.texteditB)
        self.labelB.setStyleSheet("color: rgb(111, 111, 111);")
        h_layout_textB = QHBoxLayout()
        self.texteditB.setLayout(h_layout_textB)
        h_layout_textB.addStretch()
        h_layout_textB.addWidget(self.labelB,0,Qt.AlignBottom)
        self.labelB.hide()
        #-----------
        
        self.search_result = google_translator(timeout=10)#翻译类
    
    def startTranslation(self):
        """开始翻译"""
        sample1 = self.textedit.toPlainText()
        data =  self.search_result.translate(sample1, lang_tgt='zh-cn')
        self.texteditB.setText(data)
        clipboard = QApplication.clipboard()
        clipboard.setText(data)
        self.labelB.show()
        self.timer=QTimer()
        self.timer.timeout.connect(self.initLabelB)
        #设置时间间隔并启动定时器
        self.timer.start(2000)
    
    def initLabelB(self):
        """隐藏文字"""
        self.labelB.hide()
        self.timer.stop()
    
    def removeText(self):
        """删除文本"""
        self.textedit.setText("")
        self.texteditB.setText("")