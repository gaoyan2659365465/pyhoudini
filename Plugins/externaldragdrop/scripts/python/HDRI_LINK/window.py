import sys
import os
from PySide2 import QtGui,QtCore,QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import json
import hou

def importHDRI(path):
    try:
        node = hou.selectedNodes()[0]
        gen = node.parm('env_map')
    except:
        return
        
    if gen == None:
        gen = node.parm('ar_light_color_texture')
    elif gen == None:
        gen = node.parm('A_FILENAME')
        #gen = node.parm('A_FILENAME2')
    elif gen == None:
        gen = node.parm("dome_tex")
    
    if node.type().name() == 'octane_rendertarget_dl':
        gen = node.parm('A_FILENAME')
        
    if gen != None:
        gen.set(path)

class Window(QMainWindow):
    def __init__(self):
        super(Window,self).__init__()
        
        self.setWindowTitle('AN Link')
        pth = os.path.split(os.path.realpath(__file__))[0] + "/src/LINK.tif"
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

        #create HDRI Link
        sizex = 240
        sizey = 120
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
        self.HLenv = oriPath + "/AN_HDRILINK.json"
        self.onLoad()
    
    def onLoad(self):
        file = self.HLenv
        try:
            with open(file, "r") as f:
                info = json.loads(f.read())
                self.HLpath = info["HDRI_Path"]
                self.IconScale = int(info["Scale"])
                if not os.path.exists(self.HLpath):
                    self.HLpath = "C:/"
        except:
            self.HLpath = "C:/"
            self.IconScale = 150
            info = {}
            info["HDRI_Path"] = self.HLpath
            info["Scale"] = self.IconScale
            with open(file, "w") as f:
                f.write(json.dumps(info, indent=4))

    def addMenu(self):
        self.hbox = QHBoxLayout()
        style = "color: rgb(150,150,150);font-size:16px;font-family:Vegur Bold;padding:2px 4px;"#;background-color:rgb(10,10,10);border:2px groove gray;border-radius:10px;

        self.HLlist = QComboBox()
        self.HLlist.currentIndexChanged.connect(self.setHL)
        self.HLlist.setStyleSheet("color: rgb(200,200,200);font-size:16px;font-family:Vegur Bold;selection-background-color:rgb(60,60,60);")
        self.HLlist.setMaximumWidth(200)
        self.hbox.addWidget(self.HLlist)

        self.set = QPushButton("P")
        self.set.clicked.connect(self.setPath)
        self.set.setStyleSheet(style)
        self.set.setMaximumWidth(30)

        self.hbox.addWidget(self.set)
        self.hbox.setAlignment(QtCore.Qt.AlignTop)
        self.layout.addLayout(self.hbox)

        spacer = QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Maximum)
        self.hbox.addItem(spacer)
        #scale
        spinbox = QSpinBox()
        self.hbox.addWidget(spinbox)
        spinbox.setMaximumWidth(80)
        spinbox.setRange(10, 1000)
        spinbox.valueChanged.connect(self.setScale)
        spinbox.setValue(self.IconScale)

    def setScale(self,value):
        self.HL.setGridSize(QtCore.QSize(value*2+10,value+20))
        self.HL.setIconSize(QtCore.QSize(value*2,value))
        file = self.HLenv
        info = None
        with open(file, "r") as f:
            info = json.loads(f.read())
    
        if info != None:
            info["Scale"] = value
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
            info["HDRI_Path"] = dirname
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
        path = str(self.HLpath + "/"+ self.HLlist.currentText() + "/Thumbnails/")
        # path = str(self.HLpath + "/"+ self.HLlist.currentText() )
        # path = r"E:\Megascans Library\Downloaded\3d\3d_Nature_vepnebc\Thumbs\1k"
        path = path.replace("\\","/")
        if os.path.exists(path):
            self.HL.clear()
            for file in os.listdir(path):
                if file.endswith('.jpg'):
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
        texpath = self.HLpath + "/"+ self.HLlist.currentText() + "/HDRIs/"
        # texpath = self.HLpath + "/"+ self.HLlist.currentText() 
        #iconpath = self.HLpath + "/"+ self.HLlist.currentText() + "/Thumbnails/"

        for texture in os.listdir(texpath):
            if filename in texture and ".tx" not in texture and ".tex" not in texture:
                #name = filename+".jpg"
                filename = texture
                path = str(texpath + filename)
                path = path.replace("\\","/")
                
                importHDRI(path)
                break


