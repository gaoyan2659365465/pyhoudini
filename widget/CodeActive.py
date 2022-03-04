#代码补全类
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class CodeAC:
    #代码自动补全功能
    def __init__(self, input_line):
        self.completer = QCompleter()
        self.completer.popup().setFrameShape(QFrame.NoFrame)#无边框
        self.completer.popup().setStyleSheet('QWidget{background-color: rgb(33, 37, 43);\
            color: rgb(221, 221, 221);\
	        font: 10pt "Segoe UI";}\
            QScrollBar:horizontal {\
    border: none;\
    background: rgb(52, 59, 72);\
    height: 8px;\
    margin: 0px 21px 0 21px;\
	border-radius: 0px;\
}\
QScrollBar::handle:horizontal {\
    background: rgb(189, 147, 249);\
    min-width: 25px;\
	border-radius: 4px\
}\
QScrollBar::add-line:horizontal {\
    border: none;\
    background: rgb(55, 63, 77);\
    width: 20px;\
	border-top-right-radius: 4px;\
    border-bottom-right-radius: 4px;\
    subcontrol-position: right;\
    subcontrol-origin: margin;\
}\
QScrollBar::sub-line:horizontal {\
    border: none;\
    background: rgb(55, 63, 77);\
    width: 20px;\
	border-top-left-radius: 4px;\
    border-bottom-left-radius: 4px;\
    subcontrol-position: left;\
    subcontrol-origin: margin;\
}\
QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\
{\
     background: none;\
}\
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\
{\
     background: none;\
}\
 QScrollBar:vertical {\
	border: none;\
    background: rgb(52, 59, 72);\
    width: 8px;\
    margin: 21px 0 21px 0;\
	border-radius: 0px;\
 }\
 QScrollBar::handle:vertical {	\
	background: rgb(189, 147, 249);\
    min-height: 25px;\
	border-radius: 4px\
 }\
 QScrollBar::add-line:vertical {\
     border: none;\
    background: rgb(55, 63, 77);\
     height: 20px;\
	border-bottom-left-radius: 4px;\
    border-bottom-right-radius: 4px;\
     subcontrol-position: bottom;\
     subcontrol-origin: margin;\
 }\
 QScrollBar::sub-line:vertical {\
	border: none;\
    background: rgb(55, 63, 77);\
     height: 20px;\
	border-top-left-radius: 4px;\
    border-top-right-radius: 4px;\
     subcontrol-position: top;\
     subcontrol-origin: margin;\
 }\
 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\
     background: none;\
 }\
 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\
     background: none;\
 }')
        self.completer.setFilterMode(Qt.MatchStartsWith)# Qt::MatchStartsWith只匹配开头Qt.MatchContains
        input_line.setCompleter(self.completer)
        self.model = QStandardItemModel()

    def active_script(self,result):
        for cmd in result:
            item = QStandardItem(cmd)
            self.model.insertRow(0, item)
        self.completer.setModel(self.model)