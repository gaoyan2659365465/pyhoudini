#Houdini内容浏览器可以显示文件夹和笔记
import os
import json
import textwrap
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from widget.FlowLayout import FlowLayout
from widget.StyleTool import *

ContentBrowserFilePath = FilePath[:-7] + "data/ContentBrowser"

def getJsonData(path):
    """获取json文件"""
    try:
        with open(path, 'r',encoding='utf-8') as json_file:
            data = json_file.read()
            result = json.loads(data)
    except:
        with open(path, 'r',encoding='gbk') as json_file:
            data = json_file.read()
            result = json.loads(data)
    return result

class QBrowserItemBase(QWidget):
    """内容浏览器图片的基类"""
    def __init__(self, parent = None):
        super().__init__(parent)
        #鼠标变成小手形状
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.folderPath = ""
        self.initWidget()
        
        self.setContextMenuPolicy(Qt.CustomContextMenu)#右键菜单
        self.customContextMenuRequested.connect(self.createRightmenu)  # 连接到菜单显示函数
    
    def RightMenuEvent(self):
        """右键重命名点击事件"""
        self.lineedit = QLineEdit(self)
        self.lineedit.focusOutEvent = self.focusOutEvent
        self.lineedit.setText(self.label_text.text())
        self.lineedit.setFocus()#焦点
        self.v_layout.addWidget(self.lineedit)
        self.label_text.hide()
        
    def initWidget(self):
        """初始化生成子控件"""
        self.lable_image = QLabel(self)#图片
        self.setImagePath(FilePath + "image/T_folder.png")
        self.label_text = QLabel(self)#文字
        self.setLabelText("新建文件夹")
        self.label_text.setFont(QFont("Microsoft YaHei",15,QFont.Bold))#文字尺寸默认10
        self.label_text.setStyleSheet("color: #a4a4a4 ")
        
        self.v_layout = QVBoxLayout(self)
        self.v_layout.setSpacing(0)#各控件间距
        self.v_layout.setContentsMargins(4,4,4,4)#layout边缘
        self.v_layout.addWidget(self.lable_image,0,Qt.AlignHCenter)
        self.v_layout.addWidget(self.label_text,0,Qt.AlignHCenter)
    
    def setImagePath(self,path,imagescale=2.5,scale_w=264,scale_h=177):
        """设置图片路径"""
        self.lable_image.setPixmap(QPixmap(path)\
            .scaled(scale_w/imagescale,scale_h/imagescale,Qt.IgnoreAspectRatio,Qt.SmoothTransformation))
        self.lable_image.setFixedSize(scale_w/imagescale,scale_h/imagescale)
    
    def setLabelText(self,text):
        """设置图标文字"""
        self.label_text.setText(text)

    def createRightmenu(self):
        """创建右键菜单函数"""
        pass
    
    def setFilePath(self,path):
        """设置文件路径"""
        self.folderPath = path

class QHoudiniNodeWidget(QBrowserItemBase):
    """内容浏览器的节点"""
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setImagePath(FilePath + "image/Houdini3D_icon.png",scale_w=177)
        self.setMinimumWidth(264/2.5)
    
    def setNodeName(self,name,path):
        """设置节点名字"""
        self.setLabelText(name)
        self.setFilePath(path)
    
    def focusOutEvent(self, arg__1):
        """失去焦点"""
        name = self.label_text.text()
        newname = self.lineedit.text()
        self.label_text.setText(newname)
        self.label_text.show()
        self.lineedit.close()
        
        os.rename(self.folderPath,self.folderPath[:-(len(name)+5)]+newname+".json")#修改文件夹名
        self.folderPath = self.folderPath[:-(len(name)+5)]+newname+".json"
    
    def RightMenuEvent(self):
        """右键重命名点击事件"""
        self.lineedit = QLineEdit(self)
        self.lineedit.focusOutEvent = self.focusOutEvent
        self.lineedit.setText(self.label_text.text())
        self.lineedit.setFocus()#焦点
        self.v_layout.addWidget(self.lineedit)
        self.label_text.hide()
        
    def createRightmenu(self):
        """创建右键菜单函数"""
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'重命名',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionA)
        self.actionA.triggered.connect(self.RightMenuEvent)
        
        self.actionB = QAction(u'删除',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionB)
        def RightMenuBEvent():
            """右键删除点击事件"""
            os.remove(self.folderPath)
            self.parent().initWidgets()#刷新
        self.actionB.triggered.connect(RightMenuBEvent)
        #声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，
        self.groupBox_menu.popup(QCursor.pos())
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.buttons() == Qt.LeftButton:
            #把路径传递给父控件
            self.runNode(self.folderPath)
        super().mousePressEvent(event)
    
    def runNode(self,path):
        """运行节点代码生成节点"""
        path = path# + ".json"
        if os.path.exists(path) == False:
            return
        result = getJsonData(path)
        try:
            exec(result["data"])
        except:pass
    
    def setCore(self,nodename):
        """设置节点代码"""
        import toolutils
        data = toolutils.generateToolScriptForNode(nodename)
        a = "kwargs = {'toolname': 'geo', 'panename': '', 'altclick': False, 'ctrlclick': False,\
            'shiftclick': False, 'cmdclick': False, 'pane': None, 'viewport': None, 'inputnodename': '',\
            'outputindex': -1, 'inputs': [], 'outputnodename': '', 'inputindex': -1, 'outputs': [],\
            'branch': False, 'autoplace': False, 'requestnew': False}"
        b = "import hou"
        self.core = a+'\n'+b+'\n'+data
    
    def saveWidget(self,nodeName):
        """序列化保存控件"""
        path = self.folderPath
        path_json = path + "/" + nodeName + ".json"
        if not os.path.isdir(path):
            os.makedirs(path)
        data = {"type":"QHoudiniNodeWidget",
            "data":self.core}
        json.dump(data, open(path_json,'w'),ensure_ascii=False,indent=4)

class QFolderWidget(QBrowserItemBase):
    """内容浏览器的文件夹"""
    def __init__(self, parent = None):
        super().__init__(parent)
    
    def setFolderName(self,name,path):
        """设置文件夹名字"""
        self.setLabelText(name)
        self.setFilePath(path)
    
    def focusOutEvent(self, arg__1):
        """失去焦点"""
        name = self.label_text.text()
        newname = self.lineedit.text()
        self.label_text.setText(newname)
        self.label_text.show()
        self.lineedit.close()
        
        #print("name:" + name)
        #print("newname:" + newname)
        #print("folderPath:" + self.folderPath)
        #print("folderPath[:-len(name)]:" + self.folderPath[:-len(name)])
        #print(-len(name))
        #print(self.folderPath[:-len(name)]+newname)
        os.rename(self.folderPath,self.folderPath[:-len(name)]+newname)#修改文件夹名
        self.folderPath = self.folderPath[:-len(name)]+newname
        
    def createRightmenu(self):
        """创建右键菜单函数"""
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'重命名',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionA)
        self.actionA.triggered.connect(self.RightMenuEvent)
        
        self.actionB = QAction(u'删除',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionB)
        def RightMenuBEvent():
            """右键删除点击事件"""
            for root, dirs, files in os.walk(self.folderPath, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(self.folderPath)
            self.parent().initWidgets()#刷新
        self.actionB.triggered.connect(RightMenuBEvent)
        #声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，
        self.groupBox_menu.popup(QCursor.pos())
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.buttons() == Qt.LeftButton:
            #把路径传递给父控件
            self.parent().openFolder(self.folderPath)
        super().mousePressEvent(event)

class QHoudiniTextWidget(QBrowserItemBase):
    """内容浏览器的笔记资产"""
    def __init__(self, parent = None):
        super().__init__(parent)
        self.textData = ""
        
        self.setImagePath(FilePath + "image/Text_icon.png",scale_w=177)
        self.setMinimumWidth(264/2.5)
    
    def newName(self,path):
        """构造不重复的新名字"""
        nodeName = "新建笔记"
        num = 2
        path_ = path + "/" + nodeName + ".json"
        while True:
            if os.path.exists(path_) == True:
                #如果文件存在
                path_ = path[:-(len(nodeName)+5+1)]#5个正好是.json 加1是/
                nodeName = "新建笔记" + " (" + str(num) + ")"
                path_ = path+"/"+nodeName + ".json"
                num = num + 1
            else:
                break
        return nodeName
    
    def focusOutEvent(self, arg__1):
        """失去焦点"""
        name = self.label_text.text()
        newname = self.lineedit.text()
        self.label_text.setText(newname)
        self.label_text.show()
        self.lineedit.close()
        
        os.rename(self.folderPath,self.folderPath[:-(len(name)+5)]+newname+".json")#修改文件夹名
        self.folderPath = self.folderPath[:-(len(name)+5)]+newname+".json"
        
    def createRightmenu(self):
        """创建右键菜单函数"""
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'重命名',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionA)
        self.actionA.triggered.connect(self.RightMenuEvent)
        
        self.actionB = QAction(u'删除',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionB)
        def RightMenuBEvent():
            """右键删除点击事件"""
            os.remove(self.folderPath)
            self.parent().initWidgets()#刷新
        self.actionB.triggered.connect(RightMenuBEvent)
        #声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，
        self.groupBox_menu.popup(QCursor.pos())
    
    def saveWidget(self):
        """序列化保存控件"""
        data = {"type":"QHoudiniTextWidget",
                "data":self.textData}
        json.dump(data, open(self.folderPath,'w'),ensure_ascii=False,indent=4)
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        if event.buttons() == Qt.LeftButton:
            #把路径传递给父控件
            pass
        super().mousePressEvent(event)
    
class QContentBrowserWidget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(0)
        self.v_layout.setContentsMargins(0,0,0,0)#layout边缘
        self.v_layout.setAlignment(Qt.AlignTop)
        self.h_layout = QHBoxLayout()
        self.button = QPushButton("",self)
        self.button.clicked.connect(self.previous)
        self.button.setMinimumSize(QSize(30, 30))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet(NodeWidgetButtonStyle)
        addStyleIcon(self.button,"cil-chevron-circle-left-alt.png")
        
        self.h_layout.addWidget(self.button)
        self.h_layout.addStretch()
        self.g_layout = FlowLayout()
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addLayout(self.g_layout)
        self.setLayout(self.v_layout)
        
        self.setAcceptDrops(True)#设置B可以接受拖动
        self.setContextMenuPolicy(Qt.CustomContextMenu)#右键菜单
        self.customContextMenuRequested.connect(self.createRightmenu)  # 连接到菜单显示函数
        
        self.BrowserPath = ""#这个路径是根路径的相对路径
        
        self.initWidgets()#初始化
        
    def addWidget(self,widget):
        """添加新项"""
        self.g_layout.addWidget(widget)
    
    def removeAllItem(self):
        """删除所有子项"""
        items = []
        for i in range(self.g_layout.count()):
            item = self.g_layout.itemAt(i).widget()
            items.append(item)
        for item in items:
            self.g_layout.removeWidget(item)
            item.close()
    
    def initWidgets(self):
        """初始化所有子控件"""
        self.removeAllItem()
        path = ContentBrowserFilePath + self.BrowserPath
        
        if os.path.isdir(path) == True:
            for dir in os.listdir(path):#获取路径下所有文件名/文件夹名
                if os.path.isdir(path+"/"+dir):
                    folderWidget = QFolderWidget(self)
                    folderWidget.setFolderName(dir,path+"/"+dir)
                    self.addWidget(folderWidget)
                elif os.path.isfile(path+"/"+dir):
                    data = getJsonData(path+"/"+dir)
                    if data["type"]=="QHoudiniTextWidget":
                        textw = QHoudiniTextWidget(self)
                        textw.setFilePath(path+"/"+dir)
                        textw.setLabelText(dir[:-5])
                        textw.saveWidget()
                        self.addWidget(textw)
                    if data["type"]=="QHoudiniNodeWidget":
                        nodeWidget = QHoudiniNodeWidget(self)
                        nodeWidget.setNodeName(dir[:-5],path+"/"+dir)#.json
                        self.addWidget(nodeWidget)
        else:
            os.makedirs(path)
            
    def createRightmenu(self):
        """创建右键菜单函数"""
        self.groupBox_menu = QMenu(self)
        self.actionA = QAction(u'新建文件夹',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionA)
        def RightMenuEvent():
            """右键新建文件夹点击事件"""
            FolderName = "新建文件夹"
            path_ = self.BrowserPath+"/"+FolderName
            num = 2
            while True:
                if os.path.isdir(ContentBrowserFilePath + path_) == True:
                    #如果目录存在
                    path_ = self.BrowserPath[:-(len(FolderName)+1)]
                    FolderName = "新建文件夹" + " (" + str(num) + ")"
                    path_ = self.BrowserPath+"/"+FolderName
                    num = num + 1
                else:
                    os.makedirs(ContentBrowserFilePath + path_)
                    break
            folderWidget = QFolderWidget(self)
            folderWidget.setFolderName(FolderName,ContentBrowserFilePath + path_)
            self.addWidget(folderWidget)
        self.actionA.triggered.connect(RightMenuEvent)
        
        self.actionB = QAction(u'新建笔记',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionB)
        def RightMenuBEvent():
            """右键新建笔记点击事件"""
            textw = QHoudiniTextWidget(self)
            path_ = ContentBrowserFilePath + self.BrowserPath
            newname = textw.newName(path_)
            textw.setFilePath(path_ +'/'+ newname + '.json')
            textw.setLabelText(newname)
            textw.saveWidget()
            self.addWidget(textw)
        self.actionB.triggered.connect(RightMenuBEvent)
        
        self.actionC = QAction(u'刷新',self)#创建菜单选项对象
        self.groupBox_menu.addAction(self.actionC)
        def RightMenuCEvent():
            """右键刷新点击事件"""
            self.initWidgets()#初始化
        self.actionC.triggered.connect(RightMenuCEvent)
        
        #声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，
        self.groupBox_menu.popup(QCursor.pos())
    
    def mousePressEvent(self, event):
        """鼠标点击事件"""
        self.setFocus()#焦点
        super().mousePressEvent(event)
    
    def openFolder(self,path):
        """打开文件夹"""
        self.BrowserPath = path[len(ContentBrowserFilePath):]
        self.initWidgets()#初始化
    
    def previous(self):
        """上一步"""
        path = ""
        list0 = self.BrowserPath.split("/")
        if len(list0)>0:
            for i in range(len(list0)-1):
                if list0[i] != "":
                    path = path +"/"+ list0[i]
        self.BrowserPath = path
        self.initWidgets()#初始化
    
    def dropEvent(self, event):
        """拖动事件"""
        source = event.source()
        if source and source != self:
            nodename = event.mimeData().text()
            
            nodeFileName = "新建节点"
            path_ = self.BrowserPath+"/"+nodeFileName + ".json"
            num = 2
            while True:
                if os.path.exists(ContentBrowserFilePath + path_) == True:
                    #如果文件存在
                    path_ = self.BrowserPath[:-(len(nodeFileName)+5+1)]
                    nodeFileName = "新建节点" + " (" + str(num) + ")"
                    path_ = self.BrowserPath+"/"+nodeFileName + ".json"
                    num = num + 1
                else:
                    break
            nodeWidget = QHoudiniNodeWidget(self)
            nodeWidget.setNodeName(nodeFileName,ContentBrowserFilePath + path_)
            nodeWidget.setCore(nodename)
            nodeWidget.saveWidget(nodeFileName)
            self.addWidget(nodeWidget)
            
            