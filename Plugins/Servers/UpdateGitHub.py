#从github下载最新的版本
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from Servers.py_circular_progress import PyCircularProgress

import json
import requests
from contextlib import closing

#如果断网
try:
    res = requests.get("https://api.github.com/repos/gaoyan2659365465/pyhoudini/releases")
    data = json.loads(res.text)
    fs = []
    for item in data:
        str1 = item["tag_name"]
        f1 = float(str1[3:])#去掉tag
        fs.append(f1)

    #数组排序,找出最新的版本
    fs.sort(reverse=True)
    tagv = "tag"+str(fs[0])

    file_url = "https://api.github.com/repos/gaoyan2659365465/pyhoudini/zipball/" + tagv
except:
    tagv = ""

class ProgressBar(object):
    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        #print(self.__get_info(), end=end_str)

#下载
class DownloadUpdateFile(QThread):
    porg = Signal(object)#进度条事件
    def __init__(self,parent=None,path=""):
        super().__init__(parent)
        self.path = path

    def run(self):
        with closing(requests.get(file_url, stream=True)) as response:
            chunk_size = 1024 # 单次请求最大值
            try:
                content_size = int(response.headers['content-length']) # 内容体总大小
            except:
                content_size = 1024*30
            progress = ProgressBar(self.path+"/pyhoudini_"+ tagv +".zip", total=content_size,
                                            unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
            with open(self.path+"/pyhoudini_"+ tagv +".zip", "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    progress.refresh(count=len(data)/1000)#kb是千字节
                    kbdata = progress.count/progress.chunk_size
                    self.porg.emit(kbdata)
                self.porg.emit(30)
                    

class UpdateGitHub(QWidget):
    def __init__(self):
        super(UpdateGitHub, self).__init__()
        self.setWindowTitle("更新")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)    #置顶
        
        #Load UI File
        uiloader = QUiLoader()
        self.ui = uiloader.load(__file__[:-15]+"update.ui")
        self.v_layout = QVBoxLayout(self)
        self.v_layout.addWidget(self.ui)
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        
        #Find Widgets
        self.getpathbutton = self.ui.findChild(QPushButton, "getpath")
        self.installbutton = self.ui.findChild(QPushButton, "install")
        self.cancelbutton = self.ui.findChild(QPushButton, "cancel")
        self.filepathlineedit = self.ui.findChild(QLineEdit, "filepath")
        self.updatewidget_2 = self.ui.findChild(QWidget, "updatewidget_2")
        self.updatelabel = self.ui.findChild(QWidget, "updatelabel")
        self.version = self.ui.findChild(QLabel, "version")#版本号
        self.version.setText('PyHoudini '+tagv)
        
        self.closeAppBtn = self.ui.findChild(QPushButton, "closeAppBtn")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Normal, QIcon.Off)
        self.closeAppBtn.setIcon(icon)
        
        self.getpathbutton.clicked.connect(self.getPathEvent)
        self.closeAppBtn.clicked.connect(self.close)
        self.cancelbutton.clicked.connect(self.close)
        self.installbutton.clicked.connect(self.installEvent)
        
    def getPathEvent(self):
        """弹出窗口选择要放置插件的路径"""
        self.fileDirectory = QFileDialog.getExistingDirectory(QMainWindow(), "选择文件夹")
        self.filepathlineedit:QLineEdit
        self.filepathlineedit.setText(self.fileDirectory)
    
    def installEvent(self):
        """点击安装按钮事件"""
        if self.filepathlineedit.text() == "":
            QMessageBox.information(self, "提示", "请选择文件夹")
            return
        self.progress = PyCircularProgress(max_value=30)
        
        self.h_layout = QHBoxLayout(self.updatelabel)
        self.h_layout.setAlignment(Qt.AlignRight)
        self.updatelabel.layout().addWidget(self.progress)
        self.progress.setMinimumSize(80,80)
        self.progress.setMaximumSize(80,80)
        
        #禁用按钮
        self.installbutton.setEnabled(False)
        self.cancelbutton.setEnabled(False)
        #设置按钮禁用样式
        style = 'background-color: #3c3c3c;\
                        font: 10pt "Microsoft YaHei UI";'
        self.installbutton.setStyleSheet(style)
        self.cancelbutton.setStyleSheet(style)
        
        self.download = DownloadUpdateFile(path=self.filepathlineedit.text())
        self.download.start()
        self.download.porg.connect(self.downloadEvent)
    
    def downloadEvent(self, data):
        """下载事件"""
        data = round(data, 1)#保留一位小数
        self.progress.set_value(data)
        
    def mousePressEvent(self,event):
        """鼠标按下"""
        if event.button()==Qt.LeftButton:#左键
            self.poor = QCursor.pos()-self.pos()
            if self.poor.y()>45:#标题栏宽度
                self.poor = 0    #poor存在说明鼠标在标题栏里面
        super().mousePressEvent(event)

    def mouseMoveEvent(self,event):#鼠标移动
        if self.poor:
            self.startPoint = QCursor.pos()
            self.move(self.startPoint-self.poor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self,event):
        self.poor = 0
        if self.pos().y()<0 :#标题栏动画
            self.location2 = self.pos()
            self.location2.setY(0)
            self.qanimation2 = QPropertyAnimation(self, b"pos")
            self.qanimation2.setDuration(100)
            self.qanimation2.setStartValue(self.pos())#起点
            self.qanimation2.setEndValue(self.location2)
            self.qanimation2.start()
        super().mouseReleaseEvent(event)