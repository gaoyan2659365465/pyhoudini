from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

#瀑布流布局

class FlowLayout(QLayout):
    resized = Signal()
    def __init__(self, parent=None, margin=0, spacing=-1):
        super(FlowLayout, self).__init__(parent)

        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)

        self.setSpacing(spacing)

        self.itemList = []
        
        self.flowheight = 0

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.itemList.append(item)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList[index]

        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.itemList):
            return self.itemList.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.doLayout(QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        flowheight = self.doLayout(rect, False)
        if flowheight != 0:
            self.flowheight = flowheight
            self.resized.emit()#发送尺寸改变信号
        else:
            if self.count() == 0:
                self.flowheight = 0
                self.resized.emit()#发送尺寸改变信号
    
    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())

        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def doLayout(self, rect, testOnly):
        x = rect.x()
        y = rect.y()
        lineHeight = 0

        for item in self.itemList:
            wid = item.widget()
            #可能会引起崩溃
            # spaceX = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton,
            #                                                     QSizePolicy.PushButton, Qt.Horizontal)
            # spaceY = self.spacing() + wid.style().layoutSpacing(QSizePolicy.PushButton,
            #                                                     QSizePolicy.PushButton, Qt.Vertical)
            spaceX = -1
            spaceY = -1
            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > rect.right() and lineHeight > 0:
                x = rect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))
                #打印黄色
                #print("\033[1;33m",QRect(QPoint(x, y), item.sizeHint()),"\033[0m")

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())
        return y + lineHeight - rect.y()

