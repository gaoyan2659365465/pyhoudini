#coding=utf-8

import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from widget.pyHoudini import HoudiniHelp
import PyDracula.main as main
import widget.MiniWidget as mini
import widget.Translation as tran
from widget.Sign.Sign import HtmlView,isLogin
from widget.store.HoudiniStore import HoudiniStoreScrollArea
from widget.CopyHoudiniNodeData import getNodeData

class PyHoudiniWidget(main.MainWindow):
    def __init__(self):
        main.MainWindow.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)    #置顶
        self.houdinihelp=HoudiniHelp(self)
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
        
        self.translation = tran.TranslationWidget()
        self.ui.stackedWidget.addWidget(self.translation)

        self.ui.settingsTopBtn.clicked.connect(self.htmlShow)
        
        self.storewidget = HoudiniStoreScrollArea()#商店界面
        self.ui.stackedWidget.addWidget(self.storewidget)
        
        self.htmlwidget = HtmlView()
        #self.htmlwidget.resize(self.ui.stackedWidget.sizeHint())
        self.ui.stackedWidget.addWidget(self.htmlwidget)
        
        #点击按钮，将选中的节点输出到json文件，用来给UE5生成场景
        self.ui.ue5Btn.clicked.connect(getNodeData)
    
    def htmlShow(self):
        """创建网页登录"""
        # if not isLogin():
        #     try:
        #         if self.htmlwidget.isVisible:
        #             self.htmlwidget.close()
        #             del self.htmlwidget
        #             return
        #     except:pass
        self.ui.stackedWidget.setCurrentWidget(self.htmlwidget)
        
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
        
        if btnName == "btn_translation":
            self.ui.stackedWidget.setCurrentWidget(self.translation)
            main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(main.UIFunctions.selectMenu(btn.styleSheet()))
        
        if btnName == "btn_store":
            self.ui.stackedWidget.setCurrentWidget(self.storewidget)
            main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(main.UIFunctions.selectMenu(btn.styleSheet()))

if __name__ == "__main__":
    app=QApplication(sys.argv)
    pyhwidget=PyHoudiniWidget()
    pyhwidget.show()
    sys.exit(app.exec_())
else:
    pyhwidget=PyHoudiniWidget()