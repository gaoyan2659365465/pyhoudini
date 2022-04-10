#coding:utf-8
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from FL_utils import *
from FL_server import *
from globalvar import get_value
import hou

class window(QWidget):
    def __init__(self):
        super(window,self).__init__()
        self.setWindowTitle('AN FileLink')
        initPorts("Houdini")
        self.initUI()
        self.initServer()
        self.resize(250,100)

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(hou.qt.styleSheet())
        self.setProperty("houdiniStyle",True)
        self.setWindowFlags(Qt.WindowStaysOnTopHint) 
        softLayout = QHBoxLayout()
        exportLayout = QHBoxLayout()

        #create items
        softLable = QLabel("Software")
        self.softwareList = QComboBox()
        self.softwareList.addItems(get_value("ports").keys())
        export = QPushButton("Send Mesh")
        loadMesh = QPushButton("Load Mesh")
        loadTex = QPushButton("Load Tex")

        #set style
        softLable.setMaximumWidth(50)
        #add to layout
        self.layout.addLayout(softLayout)
        softLayout.addWidget(softLable)
        softLayout.addWidget(self.softwareList)
        self.layout.addWidget(export)
        self.layout.addLayout(exportLayout)
        exportLayout.addWidget(loadMesh)
        exportLayout.addWidget(loadTex)

        #connect
        export.clicked.connect(self.exportAssets)
        loadMesh.clicked.connect(importMesh)
        loadTex.clicked.connect(importTex)

    def initServer(self):
        self.bgExport = bgExport()
        try:
            self.server = bgServer()
            self.server.start()
        except:
            pass
            #print("Can not Satrt Server!!!")
            
    def exportAssets(self):
        self.bgExport.setTargetSoftware(self.softwareList.currentText())
        self.bgExport.start()

    def closeEvent(self, event):
        #self.server.remove()
        self.bgExport.remove()
        event.accept()
    
    def loadAssets(self):
        importMesh()
        importTex()
        
def LoadWindow():
    win = window()
    hou.session.an_FE = win
    win.show()