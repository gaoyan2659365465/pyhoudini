from PYBP.window.widget.PYBP_Widget import *
from PYBP.window.PYBP_System import *

#此窗口为透明-只显示其子控件

class PYBP_Window(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()
        self.initValue()
        self.initQss()
        self.initTitle()
        
    def initQss(self):
        """初始化Qss"""
        class CommonHelper:
            """加载样式"""
            @staticmethod
            def readQss(style):
                with open(style,'r',encoding='utf-8') as f:
                    return f.read()
        styleFile = './PYBP/qss/style.qss'
        self.qssStyle = CommonHelper.readQss(styleFile)
        QApplication.instance().setStyleSheet(self.qssStyle)
    
    def initTitle(self):
        """无边框"""
        self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)    #无边框|置顶
        self.resize(800,600)
    
    def initUI(self):
        """初始化UI"""
        self.v_layout = QVBoxLayout()
        
        self.show_widget = self.createWidget()
        self.show_widget.show()
        self.setCentralWidget(self.show_widget)
        self.v_layout.addWidget(self.show_widget)
        #self.setLayout(self.v_layout)
        
    def initValue(self):
        """初始化属性"""
        self.poor = 0
        self.System = System(self)
    
    def createWidget(self):
        """创建窗体"""
        return PYBP_Widget(self)
    
    def nativeEvent(self, eventType, message):
        try:
            any = self.System.nativeEvent(eventType, message)
        except:
            self.System = System(self)
            any = self.System.nativeEvent(eventType, message)
        return any
        
    def resizeEvent(self,event):#窗口改变大小时触发
        ww = self.width()
        hh = self.height()
        try:
            self.show_widget.resize(ww,hh)
        except:
            pass
    
    def mousePressEvent(self,event):
        """鼠标按下"""
        if event.button()==Qt.LeftButton:#左键
            self.poor = QCursor.pos()-self.pos()
            if self.poor.y()>40:#标题栏宽度
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
    
    def selectItemClick(self,obj,is_click):
        """选项卡的点击槽函数"""
        pass