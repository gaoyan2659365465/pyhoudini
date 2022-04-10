#废弃代码

# self.htmljschannel = self.HtmlJsChannel(self)
# self.htmlview = HtmlView.HtmlView(self)
# path = "file:///"+PATH.replace("\\", "/")+"/widget/wangEditor.html"
# url = QUrl(path)
# self.htmlview.load(url)
# self.htmlview.setGeometry(10,70,self.width()-20,self.height()-100)
# self.htmlview.lower()

#self.htmlview.setGeometry(10,70,self.width()-20,self.height()-100)

# try:
#     with open(PATH + '/data/'+SORT+"/"+ self.icon.icon_name + ".html", encoding="utf-8") as file_obj:
#         contents = file_obj.read()
#         #print(contents)
#         jscode = "editor.dangerouslyInsertHtml('"+contents+"');"
#         self.htmlview.page().runJavaScript(jscode)
        
#         jscode = "var div = document.getElementById('editor-container');\
#             div.setAttribute('style','height: 0px;');"
#         self.htmlview.page().runJavaScript(jscode)
# except:pass

# with open(PATH + '/data/'+SORT+"/"+ self.icon.icon_name + ".json", 'w', encoding="utf-8") as file_obj:
#     file_obj.write(str(data))

#jscode = "backend.foo(editor.getHtml());"
#self.htmlview.page().runJavaScript(jscode)

# from PySide2.QtWebEngineWidgets import *
# from PySide2.QtWebChannel import QWebChannel
 
#https://cdn.jsdelivr.net/npm/wangeditor@latest/dist/wangEditor.min.js
# url = QUrl("file:///C:/Users/26593/Desktop/pyhoudini/data/GeometryNodes/adaptiveprune.html")
# view = HtmlView(self)
# view.load(url)
 
# class HtmlView(QWebEngineView):
#     def __init__(self, *args, **kwargs):
#         QWebEngineView.__init__(self, *args, **kwargs)
#         self.channel = QWebChannel()
#         self.channel.registerObject('backend', self.parent().htmljschannel)
#         self.page().setWebChannel(self.channel)

# class HtmlJsChannel(QObject):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.icon = parent.icon
        
#     @Slot(str)
#     def foo(self,data):
#         #print(data)
#         if os.path.isdir(PATH + '/data/'+SORT+"/") == False:
#             os.makedirs(PATH + '/data/'+SORT+"/")
#         with open(PATH + '/data/'+SORT+"/"+ self.icon.icon_name + ".html", 'w', encoding="utf-8") as file_obj:
#             file_obj.write(data)
            
#     @Slot()
#     def gethtml(self):
#         """html初始化时获取内容"""
#         self.parent().initTextEdit()

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
9、快捷键呼出悬浮小搜索栏直接快速查找(已解决)
10、收藏栏点爱心、默认屏蔽无笔记节点
11、内容加入视频控件、图片控件(待优化)
12、全局搜索内容
13、笔记的序列化保存(已解决)
14、能直接切换节点类型vop sop等(已解决)
15、内置vex代码段
16、字太小
17、文本框适配md语法
18、取消所有的print模式
"""
# self._color_white_output = QColor("#282c34")
# self._brush3 = QBrush(self._color_white_output)
# def paintEvent(self, event):
#     """重载-绘制"""
#     painter = QPainter(self)
#     painter.setBrush(self._brush3)
#     painter.setPen(Qt.NoPen)
#     painter.drawRect(0,0,self.width(),self.height())

#import configparser#此处如果错误就改成ConfigParser

#self.setWindowFlags(Qt.WindowStaysOnTopHint)    #置顶

#self.initBackground()
# def initBackground(self):
#     """初始化背景颜色"""
#     self.setAutoFillBackground(True) #自动填充背景
#     self.setPalette(QPalette(QColor('#ffffff'))) #着色区分背景

#self.updateNodeWidget()
# def updateNodeWidget(self):
#     """更新节点界面修复不显示BUG"""
#     a = self.size()
#     self.adjustSize()
#     self.resize(a)


# self.num_x = 0
# self.num_y = 0
# self.num_ = 0
# #初始化一个定时器
# self.timer=QTimer()
# self.timer.timeout.connect(self.initIconWidget)
# #设置时间间隔并启动定时器
# self.timer.start(10)
#self.timer.stop()

# def initIconWidget(self):
#     """用于生成图标"""
#     label_widget = IconsWidget(self,self.nodeiconpath.paths[self.num_])
#     label_widget.click.connect(self.iconClickedEvent)
#     self.scrollArea.addItem(label_widget,self.num_x,self.num_y)
#     label_widget.show()
#     self.num_y = self.num_y+1
#     if self.num_y>6:
#         self.num_y = 0
#         self.num_x = self.num_x+1
#     self.scrollArea.updateAutomaticSize()
    
#     if self.num_+1 == len(self.nodeiconpath.paths):
#         self.num_x = 0
#         self.num_y = 0
#         self.num_ = 0
#         self.timer.stop()
#     else:
#         self.num_ = self.num_+1