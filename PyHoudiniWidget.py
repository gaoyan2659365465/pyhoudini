from importlib import reload
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import PyDracula.main
#reload(PyDracula.main)
import pyHoudini
#reload(pyHoudini)
import sys


class PyHoudiniWidget(PyDracula.main.MainWindow):
    def __init__(self):
        PyDracula.main.MainWindow.__init__(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)    #置顶
        self.houdinihelp=pyHoudini.HoudiniHelp()
        #self.houdinihelp=QWidget()
        self.ui.stackedWidget.addWidget(self.houdinihelp)
    
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW HOME PAGE
        if btnName == "btn_home":
            self.ui.stackedWidget.setCurrentWidget(self.ui.home)
            PyDracula.main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(PyDracula.main.UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW WIDGETS PAGE
        if btnName == "btn_widgets":
            self.ui.stackedWidget.setCurrentWidget(self.ui.widgets)
            PyDracula.main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(PyDracula.main.UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW NEW PAGE
        if btnName == "btn_new":
            self.ui.stackedWidget.setCurrentWidget(self.ui.new_page) # SET PAGE 
            PyDracula.main.UIFunctions.resetStyle(self, btnName) # RESET ANOTHERS BUTTONS SELECTED
            btn.setStyleSheet(PyDracula.main.UIFunctions.selectMenu(btn.styleSheet())) # SELECT MENU

        if btnName == "btn_save":
            print("Save BTN clicked!")
            self.ui.stackedWidget.setCurrentWidget(self.ui.page)
            PyDracula.main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(PyDracula.main.UIFunctions.selectMenu(btn.styleSheet()))
        
        if btnName == "btn_my":
            self.ui.stackedWidget.setCurrentWidget(self.houdinihelp)
            PyDracula.main.UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(PyDracula.main.UIFunctions.selectMenu(btn.styleSheet()))
            

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')

if __name__ == "__main__":
    app=QApplication(sys.argv)
    pyhwidget=PyHoudiniWidget()
    pyhwidget.show()
    sys.exit(app.exec_())
else:
    pyhwidget=PyHoudiniWidget()
    #pyhwidget.show()