from .Node.W_View import *
from .Node.W_Scene import *
from examples.Node.W_DockWidget import *
from .W_Attributes import W_Attributes
import os
import shutil


class BlueprintWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initQss()
        self.initUI()
        self.initBackground()

    def initQss(self):
        """初始化Qss"""
        class CommonHelper:
            """加载样式"""
            @staticmethod
            def readQss(style):
                with open(style,'r',encoding='utf-8') as f:
                    return f.read()
        styleFile = __file__[:-12] + 'style.qss'
        self.qssStyle = CommonHelper.readQss(styleFile)
        QApplication.instance().setStyleSheet(self.qssStyle)
    
    def initUI(self):
        self.setTitle()
        self.setGeometry(0,50,1024,720)
        self.setContentsMargins(4,4,4,4)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)    #置顶
        
        self.scene = W_Scene()
        self.scene.click_node.connect(self.clickNode)
        
        self.view = W_View(self.scene)
        self.view_dock = W_DockWidget(self,self.view,'事件图表')
        self.view_dock.dockLocationChanged.connect(self.dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.view_dock)
        
        self.attributes = W_Attributes(self)
        self.attributes_dock = W_DockWidget(self,self.attributes)
        self.attributes_dock.dockLocationChanged.connect(self.dock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.attributes_dock)
        #self.splitDockWidget(self.w_attributes,self.view,Qt.Horizontal)
        
        self.createButton()
        self.createMenu()
    
    def initBackground(self):
        """初始化背景颜色"""
        self.setAutoFillBackground(True) #自动填充背景
        self.setPalette(QPalette(QColor('#1c1c1c'))) #着色区分背景
        
    def setTitle(self):
        """函数，负责设置窗口标题"""
        title = "Blueprint Editor"
        self.setWindowTitle(title)
    
    def createMenu(self):
        """创建菜单栏"""
        self.menubar = QMenuBar(self)
        self.menubar.setFixedHeight(25)
        self.setMenuBar(self.menubar)
        self.menu = QMenu(self.menubar)
        self.menu_2 = QMenu(self.menubar)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        
        
        self.action1 = QAction(self)#保存
        self.menu.addAction(self.action1)#保存
        self.action3 = QAction(self)#加载
        self.menu.addAction(self.action3)#加载
        self.action2 = QAction(self)#运行
        self.menu_2.addAction(self.action2)#运行
        
        
        _translate = QCoreApplication.translate
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "编辑"))
        self.action1.setText(_translate("MainWindow", "保存"))
        self.action3.setText(_translate("MainWindow", "加载"))
        self.action2.setText(_translate("MainWindow", "运行"))
        
        self.action1.triggered.connect(self.btnstate1)#保存
        self.action3.triggered.connect(self.btnstate2)#加载
        self.action2.triggered.connect(self.btnstate)#运行
    
    def createButton(self):
        """创建按钮"""
        pass
    
    def btnstate(self):
        self.scene.runBlueprint()
        path = __file__[:-22]
        os.system(path +"/tcc/tcc.exe "+ \
            path +"/cDemo/demo2.c "+ \
            path +"/cDemo/cJSON.c" + \
            " -o "+ path +"\\build\\demo2.exe")
        #创建build目录
        path_build = path + "/build"
        #isExists = os.path.exists(path_build)
        #if isExists:
        #    shutil.rmtree(path_build)
        #os.makedirs(path_build)
        #shutil.move(path[:-13] +"/demo2.exe", path_build)
        #shutil.move(path +"/test.json", path_build)
        self.btnstate1()
        os.system("cd Plugins/blueprintdemo/build && " + path_build +"/demo2.exe")
    
    def btnstate1(self):
        self.scene.dump()
    
    def btnstate2(self):
        self.scene.load()
    
    def dock(self):
        self.tabs = self.findChildren(QTabBar)
        #self.setTabPosition(self.w_attributes.allowedAreas(), QTabWidget.North)#标签页放上面
        for i in self.tabs:
            #widget = i.tabButton(0,QTabBar.ButtonPosition.LeftSide)
            #self.tab.setTabButton(0,QTabBar.ButtonPosition.LeftSide,QPushButton("123"))
            i.setDrawBase(False)#去除Tabbar白色分割线
    
    def clickNode(self,bp_node):
        """槽函数-点击Node"""
        self.attributes.setAttributeList(bp_node.getAttributeList())