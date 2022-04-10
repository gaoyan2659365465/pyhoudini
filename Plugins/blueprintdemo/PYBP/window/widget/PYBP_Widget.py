from PYBP.window.PYBP_Button import *

class PYBP_Widget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initValue()
        self.initUI()
        
    def initUI(self):
        """初始化UI"""
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(0)#各控件间距
        self.h_layout.setAlignment(Qt.AlignTop)
        self.h_layout.setContentsMargins(4,4,4,4)#layout边缘
        self.setLayout(self.h_layout)
        
        self.title = QLabel()
        self.title.setPixmap(QPixmap("./PYBP/images/未标题-6.png"))
        self.title.setMaximumHeight(self.title_height)
        self.title.setScaledContents(True)
        
        self.h_layout.addWidget(self.title)
        
        self.logo = QLabel(self)
        logo_pixmap = QPixmap("./PYBP/images/未标题-5.png")
        logo_pixmap = logo_pixmap.scaled(25,25,Qt.IgnoreAspectRatio,Qt.SmoothTransformation)
        self.logo.setPixmap(logo_pixmap)
        self.logo.move(5,5)
        self.logo.setMaximumSize(25,25)
        
        self.h_button_layout = QHBoxLayout()
        self.h_button_layout.setSpacing(0)#各控件间距
        self.h_button_layout.setAlignment(Qt.AlignLeft)
        self.h_button_layout.setContentsMargins(0,0,0,0)#layout边缘
        self.button_widget = QWidget(self)
        self.button_widget.setLayout(self.h_button_layout)
        self.button1 = PYBP_Button(self.button_widget)
        self.button2 = PYBP_Button(self.button_widget)
        self.button3 = PYBP_Button(self.button_widget)
        self.button1.setButtonType(0)
        self.button2.setButtonType(1)
        self.button3.setButtonType(2)
        
        self.h_button_layout.addWidget(self.button1)
        self.h_button_layout.addWidget(self.button2)
        self.h_button_layout.addWidget(self.button3)
        
        self.button1.clicked.connect(self.parent().showMinimized)
        self.button2.clicked.connect(self.customMaximized)
        self.button3.clicked.connect(self.parent().close)
        
        self.setAttribute(Qt.WA_StyledBackground, True)#开启qss
    
    def initValue(self):
        """初始化变量"""
        self.title_height = 43
    
    def resizeEvent(self,event):
        """窗口改变大小时触发"""
        self.button_widget.move(self.width()-100,-2)
    
    def customMaximized(self):
        """自定义最大化"""
        if self.parent().isMaximized()==False:
            self.button2.setButtonType(3)
            self.parent().showMaximized()
        elif self.parent().isMaximized()==True:
            self.button2.setButtonType(1)
            self.parent().showNormal()