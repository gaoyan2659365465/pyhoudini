from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from importlib import reload
import setWidget
import os
import sys
import zipfile
import configparser#读取ini配置文件
from threading import Thread
import server.Check.UpdateCheck
from widget.W_ScrollArea import W_ScrollArea
import widget.pathjson.NodeIconPath as NodeIconPath
import widget.HtmlView as HtmlView
from widget.QHoudiniEdit import QHoudiniEdit
from widget.CodeActive import CodeAC


PATH = ""
SORT = ""
SCRPATH=""

class NodeWidget(QWidget):
    def __init__(self,p,icon):
        super().__init__(p)
        self.resize(p.width(),p.height())
        self.p = p
        self.icon = icon
        self._color_white_output = QColor("#282c34")
        self._brush3 = QBrush(self._color_white_output)
        self.v_layout = QVBoxLayout(self)
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setSpacing(10)
        self.h_layout.setContentsMargins(10,0,0,0)#layout边缘
        self.v_layout.setContentsMargins(0,10,0,0)#layout边缘
        self.h_layout.setAlignment(Qt.AlignLeft)
        
        self.button = QPushButton("返回",self)
        self.button.clicked.connect(self.p.nodeCloseEvent)
        self.button.setMinimumSize(QSize(100, 30))
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        self.button2 = QPushButton("保存",self)
        self.button2.clicked.connect(self.saveTextEdit)
        self.button2.setMinimumSize(QSize(100, 30))
        self.button2.setCursor(QCursor(Qt.PointingHandCursor))
        self.button2.setStyleSheet(u"background-color: rgb(52, 59, 72);")
        
        
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(icon.icon_path))
        self.label.setFixedSize(48,48)
        
        self.h_layout.addWidget(self.button)
        self.h_layout.addWidget(self.button2)
        self.h_layout.addWidget(self.label)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.setAlignment(Qt.AlignTop)
        
        self.text_Edit = QHoudiniEdit(self)#QPlainTextEdit QTextEdit
        self.text_Edit.setGeometry(10,70,self.width()-20,self.height()-100)
        
        # self.htmljschannel = self.HtmlJsChannel(self)
        # self.htmlview = HtmlView.HtmlView(self)
        # path = "file:///"+PATH.replace("\\", "/")+"/widget/wangEditor.html"
        # url = QUrl(path)
        # self.htmlview.load(url)
        # self.htmlview.setGeometry(10,70,self.width()-20,self.height()-100)
        # self.htmlview.lower()
    
    def resizeEvent(self, a0: QResizeEvent):
        if self.text_Edit:
            self.text_Edit.setGeometry(10,70,self.width()-20,self.height()-100)
        #self.htmlview.setGeometry(10,70,self.width()-20,self.height()-100)
    
    def initTextEdit(self):
        """初始化富文本"""
        try:
            with open(PATH + '/data/'+SORT+"/"+ self.icon.icon_name + ".html", encoding="utf-8") as file_obj:
                contents = file_obj.read()
                #print(contents)
                jscode = "editor.dangerouslyInsertHtml('"+contents+"');"
                self.htmlview.page().runJavaScript(jscode)
                
                jscode = "var div = document.getElementById('editor-container');\
                    div.setAttribute('style','height: 0px;');"
                self.htmlview.page().runJavaScript(jscode)
        except:pass
    
    def saveTextEdit(self):
        """保存富文本"""
        jscode = "backend.foo(editor.getHtml());"
        self.htmlview.page().runJavaScript(jscode)

    def paintEvent(self, event):
        """重载-绘制"""
        painter = QPainter(self)
        painter.setBrush(self._brush3)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0,0,self.width(),self.height())
    
    class HtmlJsChannel(QObject):
        def __init__(self, parent):
            super().__init__(parent)
            self.icon = parent.icon
            
        @Slot(str)
        def foo(self,data):
            #print(data)
            if os.path.isdir(PATH + '/data/'+SORT+"/") == False:
                os.makedirs(PATH + '/data/'+SORT+"/")
            with open(PATH + '/data/'+SORT+"/"+ self.icon.icon_name + ".html", 'w', encoding="utf-8") as file_obj:
                file_obj.write(data)
                
        @Slot()
        def gethtml(self):
            """html初始化时获取内容"""
            self.parent().initTextEdit()
        
class IconsWidget(QWidget):
    click=Signal(object)#自定义点击信号
    def __init__(self,p,i):
        super().__init__(p)
        self._color_white_output = QColor("#282c34")
        self._brush3 = QBrush(self._color_white_output)
        v_layout = QVBoxLayout(self)
        v_layout.setSpacing(0)#各控件间距
        #v_layout.setAlignment(Qt.AlignTop)
        v_layout.setContentsMargins(4,4,4,4)#layout边缘
        
        self.icon_path = PATH+i[1][5:]
        if self.icon_path[-3:] != 'svg':
            self.icon_path = PATH+'/icons/OBJ/geo.svg'
        if os.path.exists(self.icon_path) == False:
            self.icon_path = PATH+'/icons/OBJ/geo.svg'
        self.icon_name = i[0]#0是名字
        label = QLabel(self)
        label.setPixmap(QPixmap(self.icon_path).scaled(p.iconsize,p.iconsize,Qt.IgnoreAspectRatio,Qt.SmoothTransformation))
        label.setFixedSize(p.iconsize,p.iconsize)#图标尺寸默认48
        self.label_text = QLabel(self)
        self.label_text.setText(self.icon_name)
        self.label_text.setFont(QFont("Microsoft YaHei",p.iconfontsize,QFont.Bold))#文字尺寸默认10
        self.label_text.setStyleSheet("color: #a4a4a4 ")
        
        v_layout.addWidget(label,0,Qt.AlignHCenter)
        v_layout.addWidget(self.label_text,0,Qt.AlignHCenter)
    
    def mousePressEvent(self, a0: QMouseEvent):#鼠标按下
        self.click.emit(self)
    
    def paintEvent(self, event):
        """重载-绘制"""
        painter = QPainter(self)
        painter.setBrush(self._brush3)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0,0,self.width(),self.height())
    
class HoudiniHelp(QWidget):
    def __init__(self):
        super().__init__()
        self.initIniFlie()
        self.initIconsDir()
        self.initBackground()
        self.initSize()
        self.nodeiconpath = NodeIconPath.NodeIconPath(SORT)
        self.initWidget()
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)    #置顶
        
        self.num_x = 0
        self.num_y = 0
        self.num_ = 0
        #初始化一个定时器
        self.timer=QTimer()
        self.timer.timeout.connect(self.initIconWidget)
        #设置时间间隔并启动定时器
        self.timer.start(10)
        
        
    def initIconWidget(self):
        """用于生成图标"""
        label_widget = IconsWidget(self,self.nodeiconpath.paths[self.num_])
        label_widget.click.connect(self.click)
        self.scrollArea.addItem(label_widget,self.num_x,self.num_y)
        label_widget.show()
        self.num_y = self.num_y+1
        if self.num_y>6:
            self.num_y = 0
            self.num_x = self.num_x+1
        self.scrollArea.toolBoxSizeEvent()
        
        if self.num_+1 == len(self.nodeiconpath.paths):
            self.num_x = 0
            self.num_y = 0
            self.num_ = 0
            self.timer.stop()
        else:
            self.num_ = self.num_+1
                
    def initIniFlie(self):
        """初始化配置文件"""
        global SCRPATH
        global PATH
        global SORT
        conf = configparser.ConfigParser()
        # 读取.ini文件
        conf.read(__file__[:-12]+"config.ini")
        # get()函数读取section里的参数值
        SCRPATH  = conf.get("config","SCRPATH")
        PATH = __file__[:-13]
        SORT  = conf.get("config","SORT")
        self.default_size = conf.get("config","DefaultSize")
        self.iconsize = int(conf.get("config","iconsize"))
        self.iconfontsize = int(conf.get("config","iconfontsize"))
        self.selectheight = int(conf.get("config","selectheight"))
    
    def initSize(self):
        """初始化窗口尺寸"""
        self.default_size = self.default_size.split(',')#字符串转列表
        self.resize(int(self.default_size[0]),int(self.default_size[1]))
    
    def initIconsDir(self):
        """判断图标文件夹是否存在"""
        if os.path.isdir(PATH + "/icons") == True:
            print("存在icons目录")
        else:
            print("不存在icons目录,正在解压...")
            try:
                z = zipfile.ZipFile(SCRPATH, 'r')
                z.extractall(path=PATH + "/icons")
                z.close()
            except:
                print("第一次运行请手动修改此处的图标zip路径并重新打开")
                os.system(r'notepad '+__file__[:-12]+"config.ini")
    
    def initWidget(self):
        """初始化子控件"""
        self.h_layout = QHBoxLayout()#横向
        self.h_layout.setSpacing(0)
        self.h_layout.setContentsMargins(0,0,0,0)
        self.h_layout.setAlignment(Qt.AlignLeft)
        
        self.setbutton = QPushButton("",self)
        self.setbutton.setFixedSize(self.selectheight,self.selectheight)
        self.setbutton.clicked.connect(self.clickSetButton)
        self.setbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.setbutton.setStyleSheet(u"QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\
                                        QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\
                                        QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }")
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_settings.png", QSize(), QIcon.Normal, QIcon.Off)
        self.setbutton.setIcon(icon2)
        self.setbutton.setIconSize(QSize(20, 20))
        
        self.line_edit = QLineEdit(self)
        self.line_edit.setFixedHeight(self.selectheight)
        self.line_edit.setAttribute(Qt.WA_InputMethodEnabled, False)#屏蔽输入法
        self.line_edit.setStyleSheet(u"background-color: rgb(33, 37, 43);\
                                     border-radius: 17px;")
        self.line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"搜索节点..", None))
        self.line_edit.returnPressed.connect(self.lineEdit_function)
        self.extention = CodeAC(self.line_edit)
        #代码补全-------------------------
        self.extention.active_script(self.nodeiconpath.names)
        #---------------------------------------

        self.selectbutton = QPushButton("",self)
        self.selectbutton.clicked.connect(self.selectNode)
        self.selectbutton.setCursor(QCursor(Qt.PointingHandCursor))
        self.selectbutton.setFixedSize(self.selectheight-4,self.selectheight-4)
        self.selectbutton.setStyleSheet("border: none;border-radius: 15px;")
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/cil-magnifying-glass.png", QSize(), QIcon.Normal, QIcon.Off)
        self.selectbutton.setIcon(icon1)
        self.select_hlayout = QHBoxLayout()
        self.select_hlayout.addStretch()
        self.select_hlayout.addWidget(self.selectbutton)
        self.select_hlayout.setSpacing(0)
        self.select_hlayout.setContentsMargins(0, 0, 2, 0)
        self.line_edit.setLayout(self.select_hlayout)
        
        self.h_layout.addWidget(self.setbutton)
        self.h_layout.addWidget(self.line_edit)
        
        
        self.v_layout = QVBoxLayout()
        self.v_layout.setSpacing(0)
        self.v_layout.setContentsMargins(0,0,0,0)
        self.v_layout.setAlignment(Qt.AlignTop)
        self.v_layout.addLayout(self.h_layout)
        
        self.w = QWidget(self)
        self.scrollArea = W_ScrollArea(self.w)
        self.v_layout.addWidget(self.w)
        self.setLayout(self.v_layout)
        
    def click(self,icon:IconsWidget):
        """点击"""
        try:
            self.nodeCloseEvent()#防止从节点直接进入页面的重叠bug
        except:pass
        self.nodewidget = NodeWidget(self,icon)
        self.nodewidget.show()
        
    def clickSetButton(self):
        """点击设置按钮"""
        self.setwidget = setWidget.SetWidget()
        self.setwidget.show()
    
    def selectNode(self):
        """点击搜索"""
        self.scrollArea.removeAllItem()
        num_x = 0
        num_y = 0
        for i in self.nodeiconpath.paths:
            if i[0].find(self.line_edit.text()) != -1:
                label_widget = IconsWidget(self,i)
                label_widget.click.connect(self.click)
                self.scrollArea.addItem(label_widget,num_x,num_y)
                label_widget.show()
                num_y = num_y+1
                if num_y>6:
                    num_y = 0
                    num_x = num_x+1

        self.scrollArea.toolBoxSizeEvent()
        self.timer.stop()
    
    def lineEdit_function(self):
        """搜索框按下回车"""
        self.selectNode()
    
    def initBackground(self):
        """初始化背景颜色"""
        self.setAutoFillBackground(True) #自动填充背景
        self.setPalette(QPalette(QColor('#ffffff'))) #着色区分背景
    
    def resizeEvent(self, a0: QResizeEvent):
        self.w.setGeometry(0, self.selectheight, self.width(), self.height()-self.selectheight)
        self.scrollArea.setAutomaticSize(0, 0, self.width(), self.height()-self.selectheight)
        try:
            self.nodewidget.resize(self.width(), self.height())
        except:pass

    def nodeCloseEvent(self):
        """nodeWidget关闭事件"""
        self.nodewidget.close()
        a = self.size()
        self.adjustSize()
        self.resize(a)

    

if __name__ == "__main__":
    # 创建线程01，不指定参数
    #thread_01 = Thread(target=server.Check.UpdateCheck.run)
    #thread_01.start()
    app=QApplication(sys.argv)
    pyhwidget=HoudiniHelp()
    pyhwidget.show()
    sys.exit(app.exec_())
else:
    pass
    # 创建线程01，不指定参数
    #thread_01 = Thread(target=server.Check.UpdateCheck.run)
    #thread_01.start()
    #import hou
    #a=HoudiniHelp()
    #a.show()
    
    # nodes = list(hou.selectedNodes())
    # if nodes:
    #     string = nodes[0].type().name()
    #     icon_path = PATH+'/icons/OBJ/geo1.svg'
    #     string = ''.join(e for e in string if e.isalnum())
    #     icon_name = ''.join([i for i in string if not i.isdigit()])
    #     print(icon_name)
    #     class icon():
    #         pass
    #     icon.icon_path = icon_path
    #     icon.icon_name = icon_name
    #     a.click(icon)
        
    


"""
1、快捷键呼出(已解决)
2、自动补全(已解决)
3、节点上按快捷键,直接可以跳转到写笔记的界面(已解决)
4、搜索栏按回车搜索(已解决)
5、笔记能创建例子,方便学习(已解决)
6、加自动更新功能(待优化)
7、搜索框禁用中文输入法(已解决)
8、加载插件太慢(已解决)
9、收藏栏点爱心、默认屏蔽无笔记节点
10、快捷键呼出悬浮小搜索栏直接快速查找
11、内容加入视频控件、图片控件
12、全局搜索内容
13、笔记的序列化保存
14、能直接切换节点类型vop sop等
15、内置vex代码段
16、字太小
17、
"""