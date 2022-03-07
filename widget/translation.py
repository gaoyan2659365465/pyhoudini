#coding=utf-8

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


from widget.googletrans.google_trans_new import google_translator

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
        #button.setStyleSheet("border: none;border-radius: 15px;")
        button.setStyleSheet(u"QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\
                                QPushButton:hover { background-color: rgb(40, 44, 52); border-style: solid; border-radius: 4px; }\
                                QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/cil-text-size.png", QSize(), QIcon.Normal, QIcon.Off)
        button.setIcon(icon1)
        
        buttonB = QPushButton("",self.textedit)
        buttonB.clicked.connect(self.removeText)
        buttonB.setCursor(QCursor(Qt.PointingHandCursor))
        buttonB.setFixedSize(28,28)
        #button.setStyleSheet("border: none;border-radius: 15px;")
        buttonB.setStyleSheet(u"QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\
                                QPushButton:hover { background-color: rgb(40, 44, 52); border-style: solid; border-radius: 4px; }\
                                QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/cil-x.png", QSize(), QIcon.Normal, QIcon.Off)
        buttonB.setIcon(icon2)
        
        self.textedit.setLayout(h_layout_text)
        h_layout_text.addStretch()
        h_layout_text.addWidget(button,0,Qt.AlignBottom)
        h_layout_text.addWidget(buttonB,0,Qt.AlignBottom)
        #v_layout.addWidget(button)
        
        self.search_result = google_translator(timeout=10)#翻译类
    
    def startTranslation(self):
        """开始翻译"""
        sample1 = self.textedit.toPlainText()
        print(sample1)
        data =  self.search_result.translate(sample1, lang_tgt='zh-cn')
        self.texteditB.setText(data)
    
    def removeText(self):
        """删除文本"""
        self.textedit.setText("")
        self.texteditB.setText("")