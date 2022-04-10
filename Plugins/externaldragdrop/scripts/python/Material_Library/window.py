import sys
import os
from PySide2 import QtGui,QtCore,QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import json
import hou
import AN_HoudiniMat as HM


def importMaterial(path,name,renderer):
    mat = None
    if renderer == "Redshift":
        mat = HM.rsMaterial(name)
    elif renderer == "Arnold":
        mat = HM.arMaterial(name)
    elif renderer == "Octane":
        mat = HM.orMaterial(name)
    elif renderer == "Mantra":
        mat = HM.mrMaterial(name)
    elif renderer == "Renderman":
        mat = HM.rmMaterial(name)

    if mat != None:
        HM.createFromFolder(mat,path)
        mat.create()
        mat_path = mat.mainMat.parent().path()
        nodes = hou.selectedNodes()
        for node in nodes:
            if node.type().name() == "geo":
                node.parm("shop_materialpath").set(mat_path)

class Window(QMainWindow):
    def __init__(self):
        super(Window,self).__init__()
        
        self.setWindowTitle('AN Material Link')
        pth = os.path.split(os.path.realpath(__file__))[0] + "/src/MatLIB.tif"
        self.setWindowIcon(QIcon(pth))
        self.resize(800,500)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        color = QColor(58, 58, 58).name()
        self.setStyleSheet("QLabel{background-color:%s;color:rgb(200,200,200)}"
                    "QWidget{background-color:%s;color:rgb(200,200,200)}"
                   "QLabel{color:rgb(170,160,150,250);font-size:20px;font-family:Vegur Bold;}"
                   "QLabel:hover{color:rgb(100,100,100,250);}" % (color,color))

        #create other label
        self.initAttrib()

        #create MAT LIB
        sizex = 150
        sizey = 150
        self.HL = QListWidget()
        self.HL.setStyleSheet("border: none;")
        self.HL.setMovement(QListView.Static)
        self.HL.setGridSize(QtCore.QSize(sizex+10,sizey+20))
        self.HL.setViewMode(QListWidget.IconMode)
        self.HL.doubleClicked.connect(self.LoadResource)
        self.HL.setIconSize(QtCore.QSize(sizex,sizey))

        #add to layout
        self.layout = QVBoxLayout()
        self.addMenu()
        self.layout.addWidget(self.HL)
        self.layout.setAlignment(Qt.AlignTop)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(self.layout)

        self.setList(self.HLpath)
        self.setHL()

        #houdini style
        self.setStyleSheet(hou.qt.styleSheet())
        self.setProperty("houdiniStyle",True)

    def initAttrib(self):     
        oriPath = os.path.split(os.path.realpath(__file__))[0] + "/src"
        oriPath = oriPath.replace("\\","/")

        #HDRI LINK env
        self.HLpath = "C:/"
        self.HLenv = oriPath + "/AN_MaterialLIB.json"
        self.onLoad()
    
    def onLoad(self):
        file = self.HLenv
        try:
            with open(file, "r") as f:
                info = json.loads(f.read())
                self.HLpath = info["Library_Path"]
                self.RDindex = int(info["Renderer"])
                self.IconScale = int(info["Scale"])
                if not os.path.exists(self.HLpath):
                    self.HLpath = "C:/"
        except:
            self.HLpath = "C:/"
            self.RDindex = 0
            self.IconScale = 150
            info = {}
            info["Library_Path"] = self.HLpath
            info["Renderer"] = self.RDindex
            info["Scale"] = self.IconScale
            with open(file, "w") as f:
                f.write(json.dumps(info, indent=4))

    def addMenu(self):
        self.hbox = QHBoxLayout()
        style = "color: rgb(150,150,150);font-size:16px;font-family:Vegur Bold;padding:2px 4px;"#;background-color:rgb(10,10,10);border:2px groove gray;border-radius:10px;

        #folder list
        self.HLlist = QComboBox()
        self.HLlist.currentIndexChanged.connect(self.setHL)
        self.HLlist.setStyleSheet("color: rgb(200,200,200);font-size:16px;font-family:Vegur Bold;selection-background-color:rgb(60,60,60);")
        self.HLlist.setMaximumWidth(200)
        self.HLlist.setMaxVisibleItems(25)
        self.hbox.addWidget(self.HLlist)

        #render list
        self.RDlist = QComboBox()
        self.initRDlist()
        self.hbox.addWidget(self.RDlist)

        #set path
        self.set = QPushButton("P")
        self.set.clicked.connect(self.setPath)
        self.set.setStyleSheet(style)
        self.set.setMaximumWidth(30)
        self.hbox.addWidget(self.set)

        #open folder
        openfolder = QPushButton("O")
        openfolder.clicked.connect(self.openFolder)
        openfolder.setStyleSheet(style)
        openfolder.setMaximumWidth(30)
        self.hbox.addWidget(openfolder)

        spacer = QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Maximum)
        self.hbox.addItem(spacer)
        #scale
        spinbox = QSpinBox()
        self.hbox.addWidget(spinbox)
        spinbox.setMaximumWidth(80)
        spinbox.setRange(10, 1000)
        spinbox.valueChanged.connect(self.setScale)
        spinbox.setValue(self.IconScale)

        self.layout.addLayout(self.hbox)


    def initRDlist(self):
        self.RDlist.setStyleSheet("color: rgb(200,200,200);font-size:16px;font-family:Vegur Bold;selection-background-color:rgb(60,60,60);")
        self.RDlist.currentIndexChanged.connect(self.saveRDlist)
        self.RDlist.setMaximumWidth(140)
        self.RDlist.addItems(["Redshift","Arnold","Octane","Mantra","Renderman"])
        self.RDlist.setCurrentIndex(self.RDindex)

    def setScale(self,value):
        self.HL.setGridSize(QtCore.QSize(value+10,value+20))
        self.HL.setIconSize(QtCore.QSize(value,value))
        file = self.HLenv
        info = None
        with open(file, "r") as f:
            info = json.loads(f.read())
    
        if info != None:
            info["Scale"] = value
            with open(file, "w") as f:
                f.write(json.dumps(info, indent=4))

    def saveRDlist(self):
        file = self.HLenv
        info = None
        with open(file, "r") as f:
            info = json.loads(f.read())
    
        if info != None:
            info["Renderer"] = self.RDlist.currentIndex()
            with open(file, "w") as f:
                f.write(json.dumps(info, indent=4))

    def openFolder(self):
        os.startfile(self.HLpath+"/"+ self.HLlist.currentText())

    def setPath(self):
        dirname = QFileDialog.getExistingDirectory(self, 'Open file', './')
        file = self.HLenv
        if len(dirname)>0:
            info = {}
            with open(file, "r") as f:
                info = json.loads(f.read())
            info["Library_Path"] = dirname
            with open(file, "w") as f:
                f.write(json.dumps(info, indent=4))
                self.HLpath = dirname
                self.setList(self.HLpath)
                self.setHL()

    def resizeEvent(self,size):
        self.setHL()

    def setList(self,path):
        self.HLlist.clear()
        pathList = os.listdir(path)
        self.HLlist.addItems(pathList)

    def setHL(self):
        path = str(self.HLpath + "/"+ self.HLlist.currentText()+"/")
        path = path.replace("\\","/")
        if os.path.exists(path):
            self.HL.clear()
            for file in os.listdir(path):
                if file.endswith('.png') or file.endswith('.jpg'):
                    fn = file.split(".")
                    del fn[-1]
                    name = str(".".join(fn))
                    #add icon
                    tex = str(path + file)
                    icon = QIcon(tex)
                    item = QListWidgetItem(icon,name)
                    self.HL.addItem(item)

    def LoadResource(self,item):
        filename = item.data()
        folderpath = self.HLpath + "/"+ self.HLlist.currentText() + "/"
        for folder in os.listdir(folderpath):
            if folder.endswith(filename):
                if "metal" in self.HLlist.currentText().lower() and "metal" not in filename.lower():
                    filename = filename+"_metal"
                importMaterial(folderpath + folder,filename,self.RDlist.currentText())
                break


