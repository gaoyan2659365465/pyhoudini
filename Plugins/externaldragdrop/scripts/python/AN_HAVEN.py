#coding:utf-8
from PySide2 import (QtWebEngineWidgets,QtWidgets,QtGui,QtCore)
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import requests
import zipfile
import shutil
import os 
import hou
import json

class Download(QThread):
    error = Signal()
    
    def __init__(self):
        super(Download,self).__init__()
        self.url = None
        self.path = None
        self.render = None
        self.createMode =None
        self.name = None
        self.exist = None
        self.cachePath =None
        self.file_total = 1
        self.re = None

    def getsize(self):
        try:
            self.file_total=float(self.re.headers['Content-Length'])
            return self.file_total
        except:
            print('get size error')

    def run(self):
        print ("Start")
    
        url = self.url
        path = self.path
        exist = self.exist
        msg = "Download Successfully"
        print(url)
        self.re=requests.head(url,allow_redirects=True)
        self.file_total=self.getsize()
        if not exist:
            r = requests.get(url,stream=True)
            try:
                with open(path, "wb") as code:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            code.write(chunk)
                print("Downlaod Succeed")
            except:
                self.error.emit()
                msg = "Download ERROR!!!"
            
        print (msg)
        
        cachePath = self.cachePath
        name = self.name
        idx = self.render    
        #create domelight
        if self.createMode == 0:
            obj = hou.node("/obj/")
            
            ns = hou.selectedNodes()
            has = len(ns)>0
            type =""
            
            if has:
                dome = ns[0]
                type = dome.type().name()
                
            if idx == 0:
                if not has or type != 'rslightdome::2.0':
                    dome = obj.createNode('rslightdome::2.0',"rs_Dome")
                parm = dome.parm("env_map")
                
            if idx == 1:
                if not has or type != 'arnold_light':
                    dome = obj.createNode('arnold_light')
                dome.parm("ar_light_type").set(6)
                dome.parm("ar_light_color_type").set(1)
                dome.parm("ar_format").set(2)
                dome.parm("ar_color_space").set("linear")
                parm = dome.parm("ar_light_color_texture")
                
            if idx == 2:
                shop = hou.node("/shop/")
                if not has or type != 'octane_rendertarget_dl':
                    dome = shop.createNode('octane_rendertarget_dl')
                dome.parm("gamma3").set(1)
                dome.parm("parmEnvironment").set(1)
                parm = dome.parm("A_FILENAME")
                shop.layoutChildren()
                
            if idx == 3:
                if not has or type != 'envlight':
                    dome = obj.createNode('envlight')
                parm = dome.parm("env_map")
                
            if idx == 4:
                if not has or type != 'pxrdomelight':
                    dome = obj.createNode('pxrdomelight')
                parm = dome.parm("lightColorMap")
            if idx == 5:
                if not has or type != 'VRayNodeLightDome':
                    dome = obj.createNode('VRayNodeLightDome')
                parm = dome.parm("dome_tex")
                dome.parm("dome_spherical").set(1)
                
            obj.layoutChildren()
            parm.set(path)
            
            
        if self.createMode == 1:
            name = name.split(".zip")[0]
            dir = cachePath + name
            if not os.path.exists(dir):
                os.makedirs(dir)
            
            if not exist:
                #unzip
                f = zipfile.ZipFile(path,'r')
                for file in f.namelist():
                    f.extract(file,dir)
                f.close()
                
                #remove zip file
                os.remove(path) 
            
            #save textures
            dic = {"ao":"","bump":"","diff":"","disp":"","nor":"","rough":"","spec":"","matel":""}
            list = os.listdir(dir)
            for i in list:
                path = dir+"/"+i
                if "ao" in i or "Ao" in i:
                    dic["ao"] = path
                if "bump" in i or "Bump" in i:
                    dic["bump"] = path
                if "diff" in i or "Diff" in i:
                    dic["diff"] = path
                if "disp" in i or "Disp" in i:
                    dic["disp"] = path
                if "nor" in i or "Nor" in i:
                    dic["nor"] = path
                if "rough" in i or "Rough" in i:
                    dic["rough"] = path
                if "spec" in i or "Spec" in i:
                    dic["spec"] = path
                    
            if idx == 0:
                self.rsMat(dic,name)
            if idx == 1:
                self.arMat(dic,name)
            if idx == 2:
                self.orMat(dic,name)
            if idx == 3:
                self.mtMat(dic,name)
            if idx == 4:
                self.risMat(dic,name)
                
                
    def rsMat(self,dic,name):
        #create rs material network
        shop = hou.node("/shop/")
        rsNet = shop.createNode("redshift_vopnet","RS_"+name)
        root = rsNet.children()[0]
        #material node
        mat = rsNet.createNode("Material","Material")
        root.setInput(0,mat)
        mat.setParms({"refl_brdf":"1"})#set parm
          
        #diffuse
        if dic["diff"] != "":
            diffuse = rsNet.createNode("TextureSampler","Diffuse_map")
            mat.setInput(0,diffuse)
            diffuse.setParms({"tex0":dic["diff"],"tex0_gammaoverride":1,"tex0_srgb":1})#setparm
        
        
        #roughness
        if dic["rough"] != "":
            roughness = rsNet.createNode("TextureSampler","Roughness_map")
            mat.setInput(7,roughness)
            roughness.setParms({"tex0":dic["rough"],"tex0_gammaoverride":1})#setparm
        
        #metallic
        if dic["matel"] != "":
            mat.setParms({"refl_fresnel_mode":"2"})#set parm
            metallic = rsNet.createNode("TextureSampler","Metallic_map")
            mat.setInput(14,metallic)
            metallic.setParms({"tex0":dic["matel"],"tex0_gammaoverride":1})#setparm
            
        #specular
        if dic["spec"] != "":
            specular = rsNet.createNode("TextureSampler","Specular_map")
            mat.setInput(6,specular)
            specular.setParms({"tex0":dic["spec"],"tex0_gammaoverride":1})#setparm
                
        #normalMap
        if dic["nor"] != "":
            normalMap = rsNet.createNode("NormalMap","NormalMap")
            mat.setInput(49,normalMap)
            normalMap.setParms({"tex0":dic["nor"],"flipY":1})#setparm
        
        #bump
        if dic["bump"] != "":
            bump = rsNet.createNode("BumpMap","BumpMap")
            mat.setInput(49,bump)
       
            #bump tex
            bumpMap = rsNet.createNode("TextureSampler","Bump_map")
            bump.setInput(0,bumpMap)
            bumpMap.setParms({"tex0":dic["bump"],"tex0_gammaoverride":1})#setparm
        
        #bump blender
        if dic["bump"] != "" and dic["nor"] != "":
            blend = rsNet.createNode("BumpBlender")
            blend.setParms({"additive":1,"bumpWeight0":1})#setparm
            blend.setInput(0,normalMap)
            blend.setInput(1,bump)
            mat.setInput(49,blend)
            
        #displacement
        if dic["disp"] != "":
            disp = rsNet.createNode("Displacement","Displacement")
            root.setInput(1,disp)
            disp.setParms({"scale":0.1})#setparm
        
            #height
            height = rsNet.createNode("TextureSampler","Height_map")
            disp.setInput(0,height)
            height.setParms({"tex0":dic["disp"],"tex0_gammaoverride":1})#setparm
        
        #ao
        if dic["ao"] != "":
            ao = rsNet.createNode("TextureSampler","AO_map")
            diffuse.setInput(3,ao)
            ao.setParms({"tex0":dic["ao"],"tex0_gammaoverride":1})#setparm
            
        shop.layoutChildren()
        rsNet.layoutChildren()
        
        nds = hou.selectedNodes()
        if len(nds) > 0:
            nd = nds[0]
            type = nd.type().name()
            if type == "geo":
                nd.parm("shop_materialpath").set(rsNet.path())
            
    def arMat(self,dic,name):
        #create ar material network
        shop = hou.node("/shop/")
        arNet = shop.createNode("arnold_vopnet","AR_"+name)
        root = arNet.children()[0]
        #material node
        mat = arNet.createNode("arnold::standard_surface")
        root.setInput(0,mat)
          
        #diffuse
        if dic["diff"] != "":
            diffuse = arNet.createNode("arnold::image","Diffuse_map")
            mat.setInput(1,diffuse)
            diffuse.setParms({"filename":dic["diff"],"color_space":"sRGB"})#setparm
        
        #roughness
        if dic["rough"] != "":
            roughness = arNet.createNode("arnold::image","Roughness_map")
            mat.setInput(6,roughness)
            roughness.setParms({"filename":dic["rough"],"color_space":"linear"})#setparm
        
        #metallic
        if dic["matel"] != "":
            metallic = arNet.createNode("arnold::image","Metallic_map")
            mat.setInput(3,metallic)
            metallic.setParms({"filename":dic["matel"],"color_space":"linear"})#setparm
            
        #specular
        if dic["spec"] != "":
            specular = arNet.createNode("arnold::image","Specular_map")
            mat.setInput(4,specular)
            specular.setParms({"filename":dic["spec"],"color_space":"linear"})#setparm
                
        #normalMap
        if dic["nor"] != "":
            normalMap = arNet.createNode("arnold::normal_map","NormalMap")
            mat.setInput(39,normalMap)
            
            #tex
            normal = arNet.createNode("arnold::image","Normal_map")
            normalMap.setInput(0,normal)
            normal.setParms({"filename":dic["nor"],"color_space":"linear"})#setparm
        
        #displacement
        if dic["disp"] != "":
            disp = arNet.createNode("arnold::vector_map","Displacement")
            root.setInput(1,disp)
            disp.setParms({"scale":0.1})#setparm
        
            #height
            height = arNet.createNode("arnold::image","Height_map")
            disp.setInput(0,height)
            height.setParms({"filename":dic["disp"],"color_space":"linear"})#setparm
        
        #ao
        #if dic["ao"] != "":
        #    ao = arNet.createNode("arnold::image","AO_map")
        #    diffuse.setInput(1,ao)
        #   ao.setParms({"filename":dic["ao"],"color_space":"linear"})#setparm
            
        shop.layoutChildren()
        arNet.layoutChildren()
        
        nds = hou.selectedNodes()
        if len(nds) > 0:
            nd = nds[0]
            type = nd.type().name()
            if type == "geo":
                nd.parm("shop_materialpath").set(arNet.path())
                
    def orMat(self,dic,name):
        #create ris material network
        shop = hou.node("/shop/")
        orNet = shop.createNode("octane_vopnet","OR_vopnet_"+name)
        root = orNet.children()[0]
        
        #material node
        mat = orNet.createNode("NT_MAT_UNIVERSAL","ORMaterial")
        root.setInput(0,mat)
        
        #diffuse  only diffuse
        if dic["diff"] != "":
            diffuse = orNet.createNode("NT_TEX_IMAGE","Diffuse_map")
            mat.setInput(1,diffuse)
            diffuse.setParms({"A_FILENAME":dic["diff"],})#setparm
        #ao
        #if dic["ao"] != "":
        #    ao = orNet.createNode("NT_TEX_FLOATIMAGE","AO_map")
        #    diffuse.setInput(0,ao)
        #    ao.setParms({"A_FILENAME":dic["ao"],"gamma":1})#setparm

        #roughness
        if dic["rough"] != "":
            roughness = orNet.createNode("NT_TEX_FLOATIMAGE","Roughness_map")
            mat.setInput(5,roughness)
            roughness.setParms({"A_FILENAME":dic["rough"],"gamma":1})#setparm

        #metallic
        if dic["matel"] != "":
            metallic = orNet.createNode("NT_TEX_FLOATIMAGE","Metallic_map")
            mat.setInput(2,metallic)
            metallic.setParms({"A_FILENAME":dic["matel"],"gamma":1})#setparm
         
        #specular
        if dic["spec"] != "":
            specular = orNet.createNode("NT_TEX_FLOATIMAGE","Specular_map")
            mat.setInput(4,specular)
            specular.setParms({"A_FILENAME":dic["spec"],"gamma":1})#setparm

        #normalMap
        if dic["nor"] != "":
            normalMap = orNet.createNode("NT_TEX_IMAGE","Normal_Map")
            mat.setInput(27,normalMap)
            normalMap.setParms({"A_FILENAME":dic["nor"],"gamma":1})#setparm
        
        #displacement
        if dic["disp"] != "":
            disp = orNet.createNode("NT_DISPLACEMENT","Displacement")
            mat.setInput(28,disp)
            disp.setParms({"black_level":0.5,})#setparm
        
        #height
            height = orNet.createNode("NT_TEX_FLOATIMAGE","Height_map")
            disp.setInput(0,height)
            height.setParms({"A_FILENAME":dic["disp"],"gamma":1})#setparm
        
        shop.layoutChildren()
        orNet.layoutChildren()

        
    def mtMat(self,dic,name):
        #create ris material network
        shop = hou.node("/shop/")
        MtNet = shop.createNode("vopmaterial","MT_vopnet_"+name)
        
        for i in MtNet.children():#delet default node
            i.destroy()

        root = MtNet.createNode("collect","out")
        
        #material node
        mat = MtNet.createNode("principledshader","MtMaterial")
        root.setInput(0,mat)
        
        #diffuse
        if dic["diff"] != "":
            mat.setParms({"basecolor_useTexture":1,"basecolor_texture":dic["diff"],})
        #rough
        if dic["rough"] != "":
            mat.setParms({"rough_useTexture":1,"rough_texture":dic["rough"],"rough_textureColorSpace":"Linear"})
        #metallic
        if dic["matel"] != "":
            mat.setParms({"metallic_useTexture":1,"metallic_texture":dic["matel"],"metallic_textureColorSpace":"Linear"})
        #specular
        if dic["spec"] != "":
            mat.setParms({"reflect_useTexture":1,"reflect_texture":dic["spec"],"reflect_textureColorSpace":"Linear"})
        #normalMap
        if dic["nor"] != "":
            mat.setParms({"baseBumpAndNormal_enable":1,"baseNormal_texture":dic["nor"],"baseNormal_flipY":1})            
        #disp_height
        if dic["disp"] != "":
            mat.setParms({"dispTex_enable":1,"dispTex_texture":dic["disp"]})              
            
        shop.layoutChildren()
        MtNet.layoutChildren()
        
    def risMat(self,dic,name):
        #create ris material network
        shop = hou.node("/shop/")
        risNet = shop.createNode("risnet","RIS_shader_"+name)
        mat = risNet.createNode("pxrdisney","material_"+name)
        root = risNet.createNode("collect","collect_"+name)
        
        root.setInput(0,mat)
        
        #diffuse  only diffuse
        if dic["diff"] != "":
            diffuse = risNet.createNode("pxrtexture","Diffuse_map")
            mat.setInput(0,diffuse)
            diffuse.setParms({"filename":dic["diff"],})#setparm
            
        #ao
        #if dic["ao"] != "":
        #    ao = risNet.createNode("pxrtexture","Ao_map")
        #    ao.setParms({"filename":dic["ao"],"linearize":1})#setparm
        #    blend = risNet.createNode("pxrblend")
        #    blend.parm("operation").set(18)
        #    mat.setInput(0,blend)
        #    blend.setInput(0,ao)
        #    blend.setInput(2,diffuse)     

        #roughness
        if dic["rough"] != "":
            roughness = risNet.createNode("pxrtexture","Roughness_map")
            mat.setInput(7,roughness,1)
            roughness.setParms({"filename":dic["rough"],"linearize":1})#setparm

        #metallic
        if dic["matel"] != "":
            metallic = risNet.createNode("pxrtexture","Metallic_map")
            mat.setInput(4,metallic,1)
            metallic.setParms({"filename":dic["matel"],"linearize":1})#setparm
         
        #specular
        if dic["spec"] != "":
            specular = risNet.createNode("pxrtexture","Specular_map")
            mat.setInput(5,specular,1)
            specular.setParms({"filename":dic["spec"],"linearize":1})#setparm

        #normalMap
        if dic["nor"] != "":
            normalMap = risNet.createNode("pxrtexture","Normal_Map")
            mat.setInput(13,normalMap)
            normalMap.setParms({"filename":dic["nor"],"linearize":1})#setparm

        #displacement
        if dic["disp"] != "":
            disp = risNet.createNode("pxrdisplace","Displacement")
            root.setInput(1,disp)
            disp.setParms({"dispScalar":0.1,})#setparm
        
        #height
            height = risNet.createNode("pxrtexture","Height_map")
            disp.setInput(0,height)
            height.setParms({"filename":dic["disp"],"linearize":1})#setparm
        
            
        shop.layoutChildren()
        risNet.layoutChildren()
        

class HDRI_HAVEN(QWidget):
    def __init__(self):
        super(HDRI_HAVEN,self).__init__()
        
        #win = QtWidgets.QWidget()
        self.setWindowTitle('AN HAVEN')
        #self.setMinimumSize(1500,880)
        self.resize(1300,800)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)  
        
        color = QtGui.QColor(QtGui.QColor(58, 58, 58)).name()
        self.setStyleSheet("QLabel{background-color:%s}""QWidget{background-color:%s}"  
                   "QLabel{color:rgb(170,160,150,250);font-size:20px;font-family:Vegur Bold;}"  
                   "QLabel:hover{color:rgb(100,100,100,250);}" % (color,color))  
                   
        self.HDRIHAVEN=0              
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.thread = Download()     
        self.thread.error.connect(self.proceeError)

        #create webview
        self.webview = QtWebEngineWidgets.QWebEngineView()
        url = "https://hdrihaven.com/hdris/category/?c=all"
        self.webview.setUrl(url)
        self.webview.urlChanged.connect(self.changeLink)
        
        #create other label
        self.initAttrib()
        
        #create HDRI Link
        sizex = 300
        sizey = 150
        self.HL = QListWidget()
        self.HL.setMovement(QtWidgets.QListView.Static)
        self.HL.setGridSize(QtCore.QSize(sizex+10,sizey+20))
        self.HL.setViewMode(QtWidgets.QListView.IconMode)
        self.HL.doubleClicked.connect(self.LoadResource)
        self.HL.setIconSize(QSize(sizex,sizey))
        
        #add to layout
        self.addMenu()
        self.layout.addWidget(self.webview)
        self.layout.addWidget(self.HL)
        self.HideHL(True)
        self.setML()#function
        
        
        self.mode.setCurrentIndex(3)
        
    def initAttrib(self):     
        self.onLoad()

        self.filename = None
        self.percent = 0

        self.render = 0
        self.createMode = 0
        self.dllkin =""
        
    def onLoad(self):
        folder = os.getenv("HOUDINI_USER_PREF_DIR") + "/"
        self.env = folder + "AN_HAVEN.json"
        self.cache = os.environ['temp']+"/HavenCache"
        self.HLpath = "C:/" 
        self.MLpath = "C:/" 
        self.PRpath = "C:/" 
        file = self.env

        if not os.path.exists(folder):
            os.makedirs(oriPath)

        try:
            with open(file, "r") as f:
                info = json.loads(f.read())
                self.cache = info["CACHE_Path"]
                self.HLpath = info["HDRI_Path"]
                self.MLpath = info["MODEL_Path"]
                self.PRpath = info["PROJECT_Path"]
        except:
            pass

    def addMenu(self):
        self.hbox = QHBoxLayout()
        self.timer = QBasicTimer()

        style = "color: rgb(150,150,150);font-size:16px;font-family:Vegur Bold;padding:2px 4px;"#;background-color:rgb(10,10,10);border:2px groove gray;border-radius:10px;
        icon = "F:/FFOutput/Download/Compressed/C4D Icon/icon/"
        size = 50
        
        
        self.mode = QComboBox()
        self.mode.addItems(["HDRI", "Material","Link","Model","Project"])
        self.mode.currentIndexChanged.connect(self.changeMode)
        self.mode.setStyleSheet("color: rgb(200,200,200);font-size:16px;font-family:Vegur Bold;selection-background-color:rgb(60,60,60);")
        self.mode.setMaximumWidth(100)
        self.hbox.addWidget(self.mode)
        
        
        self.back = QPushButton("<")
        self.back.clicked.connect(self.webview.back)
        self.back.setStyleSheet(style)
        self.back.setMaximumSize(QtCore.QSize(size, size))
        #pixMap = QPixmap(icon+"back.jpg").scaled(100,100)
        #back.setPixmap(pixMap)
        
        #jpg1 = QtGui.QPixmap(icon+"back.jpg").scaled(50, 50)
        #back.setIcon(QIcon(pixMap))
        self.hbox.addWidget(self.back)
        
        self.forward = QPushButton(">")
        self.forward.clicked.connect(self.webview.forward)
        self.forward.setStyleSheet(style)
        self.forward.setMaximumWidth(80)
        self.forward.setMaximumSize(QtCore.QSize(size, size))
        self.hbox.addWidget(self.forward)
        
        self.refresh = QPushButton("R")
        self.refresh.clicked.connect(self.webview.reload)
        self.refresh.setStyleSheet(style)
        self.refresh.setMaximumWidth(80)
        self.refresh.setMaximumSize(QtCore.QSize(size, size))
        self.hbox.addWidget(self.refresh)
                    
        self.rd = QComboBox()
        self.rd.addItems(["Redsfhit", "Arnold", "Octane", "Mantra","RenderMan","Vray"])
        self.rd.currentIndexChanged.connect(self.changeRender)
        self.rd.setStyleSheet("color: rgb(200,200,200);font-size:16px;font-family:Vegur Bold;selection-background-color:rgb(60,60,60);") 
        self.rd.setMaximumWidth(110)
        self.hbox.addWidget(self.rd)
        
        
        self.res = QComboBox()
        self.res.addItems(["1k", "2k", "4k", "8k","16k"])
        self.res.setStyleSheet("color: rgb(200,200,200);font-size:16px;font-family:Vegur Bold;selection-background-color:rgb(60,60,60);") 
        self.res.setMaximumWidth(50)
        self.hbox.addWidget(self.res)
        
        self.format = QComboBox()
        self.format.addItems(["hdr", "exr"])
        self.format.setStyleSheet("color: rgb(200,200,200);font-size:16px;font-family:Vegur Bold;selection-background-color:rgb(60,60,60);") 
        self.format.setMaximumWidth(50)
        self.hbox.addWidget(self.format)
        
        self.create = QPushButton("Import")
        self.create.clicked.connect(self.createSource)
        self.create.setStyleSheet("color: rgb(200,200,200);font-size:16px;font-family:Vegur Bold;background-color:rgb(50,50,50);")
        self.create.setMinimumWidth(200)
        self.create.setMaximumSize(QtCore.QSize(size, size))
        self.hbox.addWidget(self.create)
        
        self.link = QLineEdit()
        self.link.setStyleSheet("color: rgb(200,200,200);font-size:16px;font-family:Vegur Bold;background-color:rgb(50,50,50);")
        self.hbox.addWidget(self.link)
        self.link.returnPressed.connect(self.changeWebview)
        
        self.HLlist = QComboBox()
        #self.HLlist.addItems(["HDRI", "Material","Link"])
        self.HLlist.currentIndexChanged.connect(self.changeListLink)
        self.HLlist.setStyleSheet("color: rgb(200,200,200);font-size:16px;font-family:Vegur Bold;selection-background-color:rgb(60,60,60);")
        self.HLlist.setMaximumWidth(200)        
        self.hbox.addWidget(self.HLlist)
        
        self.save = QPushButton("Save")
        self.save.clicked.connect(self.SaveFile)
        self.save.setStyleSheet(style)
        self.save.setMaximumWidth(150)
        #clear.setMaximumSize(QtCore.QSize(size, size))
        self.hbox.addWidget(self.save)
        
        

        self.open = QPushButton("Open Folder")
        self.open.clicked.connect(self.openFolder)
        self.open.setStyleSheet(style)
        self.open.setMaximumWidth(150)
        #clear.setMaximumSize(QtCore.QSize(size, size))
        self.hbox.addWidget(self.open)
        
        self.clear = QPushButton("Clear Cache")
        self.clear.clicked.connect(self.clearFolder)
        self.clear.setStyleSheet(style)
        self.clear.setMaximumWidth(150)
        #clear.setMaximumSize(QtCore.QSize(size, size))
        self.hbox.addWidget(self.clear)
        
        self.set = QPushButton("P")
        self.set.clicked.connect(self.setPath)
        self.set.setStyleSheet(style)
        self.set.setMaximumWidth(50)
        #clear.setMaximumSize(QtCore.QSize(size, size))
        self.hbox.addWidget(self.set)
        
        self.process = QProgressBar()
        self.process.setMaximumWidth(150) 
        self.process.setTextVisible(False)
        self.hbox.addWidget(self.process)
        
        self.hbox.setAlignment(QtCore.Qt.AlignTop)  
        self.layout.addLayout(self.hbox)          
        
    def changeMode(self,mode):
        if self.mode.currentText() == "HDRI":
            url = "https://hdrihaven.com/hdris/category/?c=all"
            self.createMode = 0
            self.format.clear()
            self.format.addItems(["hdr", "exr"])
            self.res.clear()
            self.res.addItems(["1k", "2k", "4k", "8k","16k"])
            self.webview.setUrl(url)
            self.HideWeb(False)
            self.HideHL(True)
            
        if self.mode.currentText() == "Material":        
            url = "https://texturehaven.com/textures/"
            self.createMode = 1
            self.format.clear()
            self.format.addItems(["jpg", "png"])
            self.res.clear()
            self.res.addItems(["1k", "2k", "4k", "8k"])
            self.webview.setUrl(url)
            self.HideWeb(False)
            self.HideHL(True)
            
        if self.mode.currentText() == "Link":
            sizex = 300
            sizey = 150
            self.HL.setGridSize(QtCore.QSize(sizex+10,sizey+20))
            self.HL.setIconSize(QSize(sizex,sizey))
            
            self.HideWeb(True)
            self.HideHL(False)
            self.setList(self.HLpath)
            self.setHL()
            
        if self.mode.currentText() == "Model":
            sizex = 300
            sizey = 300
            self.HL.setGridSize(QtCore.QSize(sizex+10,sizey+20))
            self.HL.setIconSize(QSize(sizex,sizey))
            
            self.HideWeb(True)
            self.HideHL(False)
            self.setList(self.MLpath)
            self.setML()
            
        if self.mode.currentText() == "Project":
            sizex = 300
            sizey = 300
            self.HL.setGridSize(QtCore.QSize(sizex+10,sizey+20))
            self.HL.setIconSize(QSize(sizex,sizey))
            
            self.HideWeb(True)
            self.HideHL(False)
            self.setList(self.PRpath)
            self.setPR()
            
    def changeRender(self,render):
        self.render = render
            
    def clearFolder(self):
        def  del_file(path):
            for i in os.listdir(path):
                path_file = os.path.join(path,i)
                if os.path.isfile(path_file):
                    os.remove(path_file)
                else:
                    del_file(path_file)
                    
        del_file(self.cache)  
        shutil.rmtree(self.cache)
        if not os.path.exists(self.cache):
            os.makedirs(self.cache)
            
    def openFolder(self):
        if self.mode.currentText() == "HDRI" or self.mode.currentText() == "Material":
            os.startfile(self.cache)
        if self.mode.currentText() == "Link":
            os.startfile(self.HLpath+"/"+ self.HLlist.currentText())
        if self.mode.currentText() == "Model":
            os.startfile(self.MLpath+"/"+ self.HLlist.currentText())
        if self.mode.currentText() == "Project":
            os.startfile(self.PRpath+"/"+ self.HLlist.currentText())
            
    def setPath(self):
        dirname = QFileDialog.getExistingDirectory(self, 'Open file', './')
        dirname = str(dirname)

        if len(dirname) == 0:
            return

        if self.mode.currentText() == "Link":
            self.HLpath = dirname
            self.setList(self.HLpath)
            self.setHL()
                
        if self.mode.currentText() == "Model":
            self.MLpath = dirname
            self.setList(self.MLpath)
            self.setHL()
                
        if self.mode.currentText() == "Project":
            self.PRpath = dirname
            self.setList(self.PRpath)
            self.setHL()
                
        if self.mode.currentText() == "HDRI" or self.mode.currentText() == "Material":
            self.cache = dirname

        file = self.env
        info = {}
        info["CACHE_Path"] = self.cache
        info["HDRI_Path"] = self.HLpath
        info["MODEL_Path"] = self.MLpath
        info["PROJECT_Path"] = self.PRpath
        with open(file, "w") as f:
            f.write(json.dumps(info, indent=4))
            print("Save Successfully!")
            
    def changeWebview(self):
        if self.webview is not None:
            q = QUrl(self.link.text())
            if q.scheme() == '':
                q.setScheme('http')
            self.webview.setUrl(q)
        
    def changeLink(self):
        u = self.webview.url()    
        page = u.toDisplayString()
        self.link.setText(page)
        
    def resizeEvent(self,size):
        if self.mode.currentText() == "Link":
            self.setHL()
        if self.mode.currentText() == "Model":
            self.setML()
    
    def changeListLink(self):
        if self.mode.currentText() == "Link":
            self.setHL()
        if self.mode.currentText() == "Model":
            self.setML()
        if self.mode.currentText() == "Project":
            self.setPR()
            
    def setList(self,path):
        self.HLlist.clear()
        pathList = os.listdir(path)
        self.HLlist.addItems(pathList)
        
    def setHL(self):        
        path = self.HLpath + "/"+ self.HLlist.currentText() + "/Thumbnails/"
        if os.path.exists(path):
            self.HL.clear()
            for file in os.listdir(path):
                if file.endswith('.jpg'):
                    fn = file.split(".")
                    del fn[-1]
                    name = ".".join(fn)
                    #add icon
                    tex = path + file
                    tex = tex.replace("\\","/")
                    icon = QtGui.QIcon(tex)
                    item = QListWidgetItem(icon,name)
                    self.HL.addItem(item)    

    def LoadResource(self,item):
        filename = item.data()
        
        if self.mode.currentText() == "Link":
            texpath = self.HLpath + "/"+ self.HLlist.currentText() + "/HDRIs/"
            
            for texture in os.listdir(texpath):
                if filename in texture and ".tx" not in texture:
                    filename = texture
    
            path = texpath + filename
            node = hou.selectedNodes()[0]
            gen = node.parm('env_map')
            
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
            
        if self.mode.currentText() == "Model":
            geoFile = self.MLpath +"/"+ self.HLlist.currentText() +"/"+ filename+".bgeo"
            name = geoFile.split("/")[-1]
    
            obj  = hou.node("/obj/").createNode("geo",name)
    
            chs = obj.children()
            if len(chs)>0:
                file = chs[0]
            else:
                file = obj.createNode("file")
            file.parm("file").set(geoFile)
    
            xform = file.createOutputNode("xform")
            null = xform.createOutputNode("null","OUT_OBJ")
    
            null.setDisplayFlag(1)
            null.setRenderFlag(1)
            hou.node("/obj/").layoutChildren()
            
        if self.mode.currentText() == "Project":
            filename = item.data()
            hipFile = self.PRpath +"/"+ self.HLlist.currentText() +"/"+filename+".hip"
            hou.hipFile.load(hipFile)
            
    def setML(self):
        path = self.MLpath + "/"+ self.HLlist.currentText()+"/"
        if os.path.exists(path):
            self.HL.clear()
            for file in os.listdir(path):
                #print file
                if file.endswith('.jpg'):
                    fn = file.split(".")
                    del fn[-1]
                    name = ".".join(fn)
                    #add icon
                    tex = path + file
                    icon = QtGui.QIcon(tex)
                    item = QListWidgetItem(icon,name)
                    self.HL.addItem(item)    

    def setPR(self):
        path = self.PRpath + "/"+ self.HLlist.currentText()+"/"
        if os.path.exists(path):
            self.HL.clear()
            for file in os.listdir(path):
                #print file
                if file.endswith('.jpg'):
                    fn = file.split(".")
                    del fn[-1]
                    name = ".".join(fn)
                    #add icon
                    tex = path + file
                    icon = QtGui.QIcon(tex)
                    item = QListWidgetItem(icon,name)
                    self.HL.addItem(item)   
                    
    def SaveFile(self):
        if self.mode.currentText() == "Model":
            def savePicture(path,name):
                # get view port
                cur_desktop = hou.ui.curDesktop()
                scene = cur_desktop.paneTabOfType(hou.paneTabType.SceneViewer)
                
                f = hou.frame()
                
                filepath = path + name + ".jpg"
                
                #getFlipbook
                flip_options = scene.flipbookSettings().stash()
                
                #SetFlipbook
                flip_options.frameRange((f, f))
                flip_options.outputToMPlay(0)
                flip_options.useResolution(1)
                flip_options.resolution((500,500))
                flip_options.output(filepath)
                
                #RunFlipbook
                scene.flipbook(scene.curViewport(), flip_options)
                
                
    
            selNode = hou.selectedNodes()[0]
            path = self.MLpath+"/"+ self.HLlist.currentText()+"/"
            selNode.geometry().saveToFile(path + selNode.name() + ".bgeo")
    
            savePicture(path,selNode.name())
    
            self.setML()
            
        if self.mode.currentText() == "Project":
            # get view port
            cur_desktop = hou.ui.curDesktop()
            scene = cur_desktop.paneTabOfType(hou.paneTabType.SceneViewer)
    
            #save HIP
            a = hou.hipFile.name()
            k = a.split("/")
            hip = ''
            if len(k)==1:
                hip = hou.ui.selectFile(title='Save',file_type=hou.fileType.Hip)
                if hip!='':
                    hou.hipFile.save(file_name = hip)
            else:
                 hou.hipFile.save()
                 hip = '1'
    
            if hip!='':
                #set name and path
                f = hou.frame()
                fn = hou.hipFile.basename().split(".")
                del fn[-1]
                filename = ".".join(fn)
                
                path=hou.hipFile.path().split("/")
                del path[-1]
                filepath = "/".join(path)+"/"+filename+".jpg"
                
                #getFlipbook
                flip_options = scene.flipbookSettings().stash()
                
                #SetFlipbook
                flip_options.frameRange((f, f))
                flip_options.outputToMPlay(0)
                flip_options.useResolution(1)
                flip_options.resolution((500,500))
                flip_options.output(filepath)
                
                #RunFlipbook
                scene.flipbook(scene.curViewport(), flip_options)
                
            self.setPR()            
            
    def createSource(self):
        #download
        cachePath = self.cache+"/"
                
        u = self.webview.url()    
        page = u.toDisplayString()
        n = page.split("=")[-1]
        form = self.format.currentText()
        res = self.res.currentText()

        if self.createMode == 0:
            #https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/4k/sandsloot_4k.hdr
            #https://dl.polyhaven.org/file/ph-assets/HDRIs/exr/4k/studio_small_09_4k.exr
            
            # url = "https://hdrihaven.com/files/hdris/" + n + "_"+res+"." + form
            
            name = n.split("/")[-1]
            url = "https://dl.polyhaven.org/file/ph-assets/HDRIs/" + form + "/" + res + "/" + name + "_"+res+"." + form
            name = url.split("/")[-1]
            path = cachePath + name
            f = path
            
        if self.createMode == 1:    
            #https://polyhaven.com/__download__/20220409120544/river_small_rocks_4k.blend.zip
            
            url = "https://texturehaven.com/files/textures/zip/"+res+"/"+n+"/"+n+"_"+res+"_"+form+".zip"            
            name = url.split("/")[-1]
            path = cachePath + name
            f = name.split(".zip")[0]
            f = cachePath + f
        
        exist = os.path.exists(f)
          
        self.percent = 0
        self.process.setValue(self.percent)
        self.onStartDL()
        self.filename = path
        self.onStart()

        self.timer.start(100,self)
        self.thread.url = url
        self.thread.path = path
        self.thread.render = self.render
        self.thread.createMode =self.createMode
        self.thread.name = name
        self.thread.exist = exist
        self.thread.cachePath = cachePath
        # self.thread.setDaemon(True)
        self.thread.start()
            

    def timerEvent(self, event):
        if self.percent>=100:
           self.timer.stop()
           return

        file_total=self.thread.file_total
        if os.path.exists(self.filename):
            print(file_total)
            print(self.filename)
            self.percent = 100*float(os.path.getsize(self.filename))/float(file_total)
            print(str(self.percent) + " %")
            self.process.setValue(self.percent)

    def onStart(self):
        if self.timer.isActive(): 
            self.timer.stop()
        else:
            self.timer.start(1000,self)


    def proceeError(self):
        #self.timer.stop()
        #danger = "QProgressBar::chunk {background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,stop: 0 #FF0350,stop: 0.4999 #FF0020,stop: 0.5 #FF0019,stop: 1 rgb(0,150,0) );border-bottom-right-radius: 5px;border-bottom-left-radius: 5px;border: .px solid black;}"
        #self.process.setStyleSheet(danger)
        self.process.setStyleSheet("QProgressBar::chunk {background-color:rgb(250,0,0);border:0px}")

    
    def onStartDL(self):
        # safe= "QProgressBar::chunk {background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,stop: 0 #78d,stop: 0.4999 #46a,stop: 0.5 #45a,stop: 1 #238 );border-bottom-right-radius: 7px;border-bottom-left-radius: 7px;border: 1px solid black;}"
        # self.process.setStyleSheet(safe)
        self.process.setStyleSheet("QProgressBar::chunk {background-color:rgb(0,250,0);border:0px}")


    def closeEvent(self, event = None):
        #self.thread.stop()
        pass

    def HideWeb(self,mode):
        self.webview.setHidden(mode)
        self.back.setHidden(mode)
        self.forward.setHidden(mode)
        self.refresh.setHidden(mode)
        self.rd.setHidden(mode)
        self.res.setHidden(mode)
        self.format.setHidden(mode)
        self.create.setHidden(mode)
        self.process.setHidden(mode)
        #self.open.setHidden(mode)
        self.clear.setHidden(mode)
        self.link.setHidden(mode)
        
    def HideHL(self,mode):
        self.HL.setHidden(mode)
        self.HLlist.setHidden(mode)
        if self.mode.currentText() != "Link":
            self.save.setHidden(mode)
    
def LoadWindow():
    window = HDRI_HAVEN()
    hou.session.hdri_haven = window 
    window.show()        
    