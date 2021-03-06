#coding=utf-8

import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import PyDracula.main as main
from Plugins import *

class PyHoudiniWidget(main.MainWindow):
    def __init__(self):
        main.MainWindow.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)    #置顶
        self.houdinihelp=HoudiniHelp(self)
        self.ui.stackedWidget.addWidget(self.houdinihelp)
        
        self.miniw = MiniWidget(None,self)
        self.miniw.setMaxWidget(self)
        self.isminiw = False#是否迷你模式
        # MINI
        def openMiniWidget():
            self.miniw.show()
            self.isminiw = True
            self.miniw.setMaxWidget(self)
            self.hide()
        self.ui.miniBtn.clicked.connect(openMiniWidget)
        
        self.ui.settingsTopBtn.clicked.connect(self.htmlShow)
        
        try:
            #点击按钮，将选中的节点输出到json文件，用来给UE5生成场景
            self.ui.ue5Btn.clicked.connect(getNodeData)
        except:pass
    
    def htmlShow(self):
        """创建网页登录"""
        try:
            self.ui.stackedWidget.setCurrentWidget(self.htmlwidget)
        except:
            self.htmlwidget = HtmlView()
            #self.htmlwidget.resize(self.ui.stackedWidget.sizeHint())
            self.ui.stackedWidget.addWidget(self.htmlwidget)
        
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
            try:
                self.ui.stackedWidget.setCurrentWidget(self.translation)
            except:
                self.translation = TranslationWidget()
                self.ui.stackedWidget.addWidget(self.translation)
                self.ui.stackedWidget.setCurrentWidget(self.translation)
            main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(main.UIFunctions.selectMenu(btn.styleSheet()))
        
        if btnName == "btn_store":
            try:
                self.ui.stackedWidget.setCurrentWidget(self.storewidget)
            except:
                self.storewidget = HoudiniStoreScrollArea()#商店界面
                self.ui.stackedWidget.addWidget(self.storewidget)
                self.ui.stackedWidget.setCurrentWidget(self.storewidget)
            main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(main.UIFunctions.selectMenu(btn.styleSheet()))
        
        if btnName == "btn_browser":
            try:
                self.ui.stackedWidget.setCurrentWidget(self.contentBrowser)
            except:
                self.contentBrowser = ContentBrowserScrollArea()#内容浏览器界面
                self.ui.stackedWidget.addWidget(self.contentBrowser)
                self.ui.stackedWidget.setCurrentWidget(self.contentBrowser)
            main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(main.UIFunctions.selectMenu(btn.styleSheet()))
        
        if btnName == "btn_blueprint":
            try:
                self.ui.stackedWidget.setCurrentWidget(self.blueprintWindow)
            except:
                self.blueprintWindow = BlueprintWindow()#蓝图
                self.ui.stackedWidget.addWidget(self.blueprintWindow)
                self.ui.stackedWidget.setCurrentWidget(self.blueprintWindow)
            main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(main.UIFunctions.selectMenu(btn.styleSheet()))
        
        if btnName == "btn_weslib":
            try:
                self.ui.stackedWidget.setCurrentWidget(self.proj)
            except:
                self.proj = ProjBrowser()#项目管理
                self.ui.stackedWidget.addWidget(self.proj)
                self.ui.stackedWidget.setCurrentWidget(self.proj)
            main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(main.UIFunctions.selectMenu(btn.styleSheet()))
                
                

if __name__ == "__main__":
    app=QApplication(sys.argv)
    pyhwidget=PyHoudiniWidget()
    pyhwidget.show()
    if tagv != "tag1.1" and tagv != "":
        pro = UpdateGitHub()
        pro.show()
    sys.exit(app.exec_())
else:
    pyhwidget=PyHoudiniWidget()
    if tagv != "tag1.1" and tagv != "":
        pro = UpdateGitHub()
        pro.show()