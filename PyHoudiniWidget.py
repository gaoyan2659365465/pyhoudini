#coding=utf-8

import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import pyHoudini
import PyDracula.main as main
import widget.miniWidget as mini


class PyHoudiniWidget(main.MainWindow):
    def __init__(self):
        main.MainWindow.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)    #置顶
        self.houdinihelp=pyHoudini.HoudiniHelp()
        self.houdinihelp.setWindows(self)#将自己发过去备用
        self.ui.stackedWidget.addWidget(self.houdinihelp)
        
        self.miniw = mini.MiniWidget(None,self)
        self.miniw.setMaxWidget(self)
        self.isminiw = False#是否迷你模式
        # MINI
        def openMiniWidget():
            self.miniw.show()
            self.isminiw = True
            self.miniw.setMaxWidget(self)
            self.hide()
        self.ui.miniBtn.clicked.connect(openMiniWidget)
    
    def show(self):
        try:
            if self.isminiw:
                self.miniw.show()
                self.miniw.setMaxWidget(self)
                self.hide()
                self.miniw.move(QCursor.pos())
            else:
                super().show()
        except:pass
    
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.home)
            main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(main.UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            print("")
            #self.ui.stackedWidget.setCurrentWidget(self.ui.widgets)
            #main.UIFunctions.resetStyle(self, btnName)
            #btn.setStyleSheet(main.UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            print("")

        if btnName == "btn_save":
            print("Save BTN clicked!")
        
        if btnName == "btn_my":
            self.ui.stackedWidget.setCurrentWidget(self.houdinihelp)
            main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(main.UIFunctions.selectMenu(btn.styleSheet()))
            #修复回到主界面不显示icon问题
            self.houdinihelp.updateNodeWidget()
            #--------------------------

if __name__ == "__main__":
    app=QApplication(sys.argv)
    pyhwidget=PyHoudiniWidget()
    pyhwidget.show()
    sys.exit(app.exec_())
else:
    pyhwidget=PyHoudiniWidget()