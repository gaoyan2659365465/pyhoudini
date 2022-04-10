#代码补全类
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from Plugins.Tools import *


class CodeAC:
    #代码自动补全功能
    def __init__(self, input_line):
        self.completer = QCompleter()
        self.completer.popup().setFrameShape(QFrame.NoFrame)#无边框
        self.completer.popup().setStyleSheet(CodeACcompleter)
        self.completer.setFilterMode(Qt.MatchStartsWith)# Qt::MatchStartsWith只匹配开头Qt.MatchContains
        input_line.setCompleter(self.completer)
        self.model = QStandardItemModel()

    def active_script(self,result):
        for cmd in result:
            item = QStandardItem(cmd)
            self.model.insertRow(0, item)
        self.completer.setModel(self.model)