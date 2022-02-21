from imp import reload

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from widget.W_ScrollArea import W_ScrollArea
import pathjson.NodeIconPath
reload(pathjson.NodeIconPath)
import setWidget
reload(setWidget)
import os
import zipfile
import configparser#读取ini配置文件

PATH = ""
SORT = ""
SCRPATH=""

class NodeWidget(QWidget):
    def __init__(self,p,icon):
        super().__init__(p)
        self.initBackground()
        self.resize(p.width(),p.height())
        self.p = p
        self.icon = icon
        self.v_layout = QVBoxLayout(self)
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setSpacing(0)
        self.h_layout.setContentsMargins(50,0,0,0)#layout边缘
        self.v_layout.setContentsMargins(0,10,0,0)#layout边缘
        self.h_layout.setAlignment(Qt.AlignLeft)
        self.button = QPushButton("返回",self)
        self.button.clicked.connect(self.close)
        
        self.button2 = QPushButton("保存",self)
        self.button2.clicked.connect(self.saveTextEdit)
        
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap(icon.icon_path))
        self.label.setFixedSize(48,48)
        
        self.h_layout.addWidget(self.button)
        self.h_layout.addWidget(self.button2)
        self.h_layout.addWidget(self.label)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.setAlignment(Qt.AlignTop)
        
        self.text_Edit = QTextEdit(self)
        self.text_Edit.setGeometry(50,70,self.width()-100,self.height()-100)
        self.initTextEdit()
    
    def initBackground(self):
        """初始化背景颜色"""
        self.setAutoFillBackground(True) #自动填充背景
        self.setPalette(QPalette(QColor('#3c3c3c'))) #着色区分背景
    
    def resizeEvent(self, a0: QResizeEvent):
        self.text_Edit.setGeometry(50,70,self.width()-100,self.height()-100)
    
    def initTextEdit(self):
        """初始化富文本"""
        try:
            with open(PATH + '/data/'+SORT+"/"+ self.icon.icon_name + ".html", encoding="gbk") as file_obj:
                contents = file_obj.read()
                print(contents)
                self.text_Edit.setHtml(contents)
        except:pass
    
    def saveTextEdit(self):
        """保存富文本"""
        data = self.text_Edit.toHtml()
        if os.path.isdir(PATH + '/data/'+SORT+"/") == False:
            os.makedirs(PATH + '/data/'+SORT+"/")
        with open(PATH + '/data/'+SORT+"/"+ self.icon.icon_name + ".html", 'w', encoding="gbk") as file_obj:
            file_obj.write(data)
        

class IconsWidget(QWidget):
    click=Signal(object)#自定义点击信号
    def __init__(self,p,i):
        super().__init__(p)
        v_layout = QVBoxLayout(self)
        v_layout.setSpacing(0)#各控件间距
        v_layout.setAlignment(Qt.AlignTop)
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
        
        v_layout.addWidget(label)
        v_layout.addWidget(self.label_text)
    
    def mousePressEvent(self, a0: QMouseEvent):#鼠标按下
        self.click.emit(self)

class CodeAC:
    #代码自动补全功能
    def __init__(self, input_line):
        self.completer = QCompleter()
        input_line.setCompleter(self.completer)
        self.model = QStandardItemModel()
            
    def active_script(self,result):
        for cmd in result:
            item = QStandardItem(cmd)
            self.model.insertRow(0, item)
        self.completer.setModel(self.model)

class HoudiniHelp(QWidget):
    def __init__(self):
        super().__init__()
        self.initIniFlie()
        self.initIconsDir()
        self.initBackground()
        self.initQss()
        self.initSize()
        self.initWidget()
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)    #置顶
        
        self.nodeiconpath = pathjson.NodeIconPath.NodeIconPath(SORT)
        num_x = 0
        num_y = 0
        for i in self.nodeiconpath.paths:
            label_widget = IconsWidget(self,i)
            label_widget.click.connect(self.click)
            self.scrollArea.addItem(label_widget,num_x,num_y)
            num_y = num_y+1
            if num_y>6:
                num_y = 0
                num_x = num_x+1
        
        #代码补全-------------------------
        name = []
        for i in self.nodeiconpath.paths:
            name.append(i[0])
        self.extention.active_script(name)
        #---------------------------------------
        
    
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
        
        self.setbutton = QPushButton("设置",self)
        self.setbutton.setFixedSize(self.selectheight,self.selectheight)
        self.setbutton.clicked.connect(self.clickSetButton)
        
        self.line_edit = QLineEdit(self)
        self.line_edit.setFixedHeight(self.selectheight)
        self.line_edit.setAttribute(Qt.WA_InputMethodEnabled, False)#屏蔽输入法
        self.line_edit.returnPressed.connect(self.lineEdit_function)
        self.extention = CodeAC(self.line_edit)
        
        
        self.selectbutton = QPushButton("搜索",self)
        self.selectbutton.setFixedSize(self.selectheight,self.selectheight)
        self.selectbutton.clicked.connect(self.selectNode)
        
        self.h_layout.addWidget(self.setbutton)
        self.h_layout.addWidget(self.line_edit)
        self.h_layout.addWidget(self.selectbutton)
        
        
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
        print(icon.label_text.text())
        self.nodewidget = NodeWidget(self.w,icon)
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
                num_y = num_y+1
                if num_y>6:
                    num_y = 0
                    num_x = num_x+1
    
    def lineEdit_function(self):
        """搜索框按下回车"""
        self.selectNode()
        
    def initQss(self):
        """初始化Qss"""
        class CommonHelper:
            """加载样式"""
            @staticmethod
            def readQss(style):
                with open(style,'r',encoding='utf-8') as f:
                    return f.read()
        styleFile = PATH+'/qss/style.qss'
        self.qssStyle = CommonHelper.readQss(styleFile)
        QApplication.instance().setStyleSheet(self.qssStyle)
    
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

import sys

if __name__ == "__main__":
    app=QApplication(sys.argv)
    widget=HoudiniHelp()
    widget.show()
    sys.exit(app.exec_())
else:
    widget=HoudiniHelp()
    widget.show()


"""
1、快捷键呼出
2、自动补全(已解决)(效果有待优化)
3、节点上按快捷键,直接可以跳转到写笔记的界面
4、搜索栏按回车搜索(已解决)
5、收藏栏点爱心
6、快捷键呼出悬浮小搜索栏直接快速查找
7、笔记能创建例子,方便学习
8、笔记框加图片
9、加自动更新功能
10、搜索框禁用中文输入法(已解决)
"""