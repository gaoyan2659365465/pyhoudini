#Houdini商店界面
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from widget.StyleTool import *
from widget.FlowLayout import FlowLayout
import requests
from widget.Sign.Sign import getStoreAssetData
from widget.ThreadReadImage import ReadWebImages

class HoudiniStoreTopWidget(QWidget):
    """Houdini商店顶部控件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.v_layout)
        
        self.imagelabel = QLabel()#顶部广告图片
        self.thread_1 = ReadWebImages()  # 创建线程
        self.thread_1.image_url = "https://cdn2.unrealengine.com/unreal-engine-marketplace-sale-march-2022-banner-1340x180-8b684d14c9b4.png"
        self.thread_1.imagelabel = self.imagelabel
        self.thread_1.mode = 1#不缩放图片
        self.thread_1.start()  # 开始线程
        
        self.imagelabel.setMinimumWidth(900)
        self.imagelabel.setMaximumWidth(1300)
        self.v_layout.addWidget(self.imagelabel)
        
        self.h_layout = QHBoxLayout()
        self.v_layout.addLayout(self.h_layout)
        
        self.textA = QLabel("Houdini商城")
        self.textA.setFont(QFont("Lucida Console"))
        self.textA.setStyleSheet("color: #f3f3f3;font-size: 28px;")
        self.h_layout.addWidget(self.textA)
        self.h_layout.addStretch()
        
        self.buttonA = QPushButton("首页")
        self.buttonA.setStyleSheet(HoudiniStoreTopWidgetButton)
        self.h_layout.addWidget(self.buttonA)
        
        self.buttonB = QPushButton("浏览")
        self.buttonB.setStyleSheet(HoudiniStoreTopWidgetButton)
        self.h_layout.addWidget(self.buttonB)
        
        self.buttonC = QPushButton("行业")
        self.buttonC.setStyleSheet(HoudiniStoreTopWidgetButton)
        self.h_layout.addWidget(self.buttonC)
        
        self.buttonD = QPushButton("免费")
        self.buttonD.setStyleSheet(HoudiniStoreTopWidgetButton)
        self.h_layout.addWidget(self.buttonD)
        
        self.buttonE = QPushButton("特价")
        self.buttonE.setStyleSheet(HoudiniStoreTopWidgetButton)
        self.h_layout.addWidget(self.buttonE)
        
        self.buttonF = QPushButton("3月特卖")
        self.buttonF.setStyleSheet(HoudiniStoreTopWidgetButton)
        self.h_layout.addWidget(self.buttonF)
        
        self.buttonG = QPushButton("保管库")
        self.buttonG.setStyleSheet(HoudiniStoreTopWidgetButton)
        self.h_layout.addWidget(self.buttonG)
        
        self.buttonH = QPushButton("帮助")
        self.buttonH.setStyleSheet(HoudiniStoreTopWidgetButton)
        self.h_layout.addWidget(self.buttonH)
        
        self.select_layout = QHBoxLayout()
        self.select_layout.setContentsMargins(0,8,0,0)
        self.h_layout.addLayout(self.select_layout)
        
        self.line_edit = QLineEdit()
        self.line_edit.setObjectName("HoudiniStoreTopWidgetLineEdit")
        self.line_edit.setFixedHeight(38)
        self.line_edit.setStyleSheet(HoudiniStoreTopWidget_edit)
        self.line_edit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"搜索内容...", None))
        #self.line_edit.returnPressed.connect(self.selectNode)
        self.selectbutton = QPushButton("")
        #self.selectbutton.clicked.connect(self.selectNode)
        self.selectbutton.setCursor(QCursor(Qt.PointingHandCursor))
        #self.selectbutton.setFixedSize(self.selectheight-4,self.selectheight-4)
        self.selectbutton.setStyleSheet(HoudiniHelpselectbutton)
        addStyleIcon(self.selectbutton,"cil-magnifying-glass.png")
        self.select_hlayout = QHBoxLayout()
        self.select_hlayout.setSpacing(0)
        self.select_hlayout.setContentsMargins(0,0,5,0)
        self.select_hlayout.addStretch()
        self.select_hlayout.addWidget(self.selectbutton)
        self.line_edit.setLayout(self.select_hlayout)
        
        self.select_layout.addWidget(self.line_edit)
        
        
        
        self.linelable = QLabel(self)
        self.linelable.setFixedSize(1300,1)
        self.linelable.setStyleSheet("background-color: #3b3c3d;")
        self.v_layout.addWidget(self.linelable)
        
        self.setMaximumWidth(1300)

class HoudiniStoreAssetShoppingTrolleyWidget(QWidget):
    """Houdini商店显示商品控件——的购物车控件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(248,35)
        
        self.linelable = QLabel(self)
        self.linelable.setFixedSize(248,1)
        self.linelable.move(-14,0)
        self.linelable.setStyleSheet("background-color: #3b3c3d;")
        
        self.h_layout = QHBoxLayout()
        self.h_layout.setAlignment(Qt.AlignVCenter)#居中
        self.h_layout.setSpacing(0)
        self.h_layout.setContentsMargins(7, 5, 21, 5)
        self.setLayout(self.h_layout)
        
        self.sortsrt = QLabel("Characters")
        self.sortsrt.setStyleSheet("color: #dca100;font-size: 12px;")
        self.h_layout.addWidget(self.sortsrt)
        self.h_layout.addStretch()
        
        self.buttonA = QPushButton("添加到购物车")
        self.buttonA.setFixedSize(84,24)
        self.buttonA.setStyleSheet(HoudiniStoreAssetShoppingTrolleyWidgetButton)
        self.h_layout.addWidget(self.buttonA)
        
        self.linelableB = QLabel(self)
        self.linelableB.setFixedSize(1,24)
        self.linelableB.setStyleSheet("background-color: #3b3c3d;")
        self.h_layout.addWidget(self.linelableB)
        
        self.buttonB = QPushButton()
        self.buttonB.setFixedSize(30,24)
        self.buttonB.setStyleSheet(HoudiniStoreAssetShoppingTrolleyWidgetButton)
        icon2 = QIcon()
        icon2.addFile(FilePath + "image/xin.png", QSize(40,40), QIcon.Normal, QIcon.Off)
        self.buttonB.setIcon(icon2)
        self.h_layout.addWidget(self.buttonB)
        
class HoudiniStoreAssetPriceWidget(QWidget):
    """Houdini商店显示商品控件——的价格控件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(232,24)
        
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(0)
        self.h_layout.setContentsMargins(0, 4, 0, 4)
        self.setLayout(self.h_layout)
        
        self.discount_percentage = QLabel("50%OFF")
        self.discount_percentage.setFont(QFont("Microsoft YaHei",16,QFont.Bold))
        self.discount_percentage.setStyleSheet("background-color: #4f802d;\
            padding-left: 6px;padding-right: 6px;color: #f5f5f5;font-size: 16px;")
        self.h_layout.addWidget(self.discount_percentage)
        self.h_layout.addStretch()
        
        self.price = QLabel("$22.49")
        self.price.setFont(QFont("Microsoft YaHei",16))
        self.price.setStyleSheet("color: #ffffff;font-size: 16px;")
        self.h_layout.addWidget(self.price)
    
    def setPriceText(self,data):
        """设置价格标签文字"""
        self.price.setText(data)

class HoudiniStoreAssetScoreWidget(QWidget):
    """Houdini商店显示商品控件——的评分星星控件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(232,24)
        
        self.h_layout = QHBoxLayout()
        self.h_layout.setSpacing(0)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.h_layout)
        
        self.scorestr = QLabel("尚未评分")
        self.scorestr.setFont(QFont("Microsoft YaHei",16,QFont.Bold))
        self.scorestr.setStyleSheet("color: #ffffff;font-size: 16px;")
        self.scorestr.setFixedSize(232,24)
        self.h_layout.addWidget(self.scorestr)
    
    def setScoreText(self,data):
        """设置评分标签文字"""
        if data == '0':
            return
        self.scorestr.setText(data)

class HoudiniStoreAssetWidget(QWidget):
    """Houdini商店显示商品控件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.v_layout = QVBoxLayout()#主布局
        self.v_layout.setContentsMargins(10,0,10,16)
        self.setLayout(self.v_layout)
        
        self.imagelayout = QHBoxLayout()
        self.imagelayout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.imagelabel = QLabel()#商品展示图片
        self.imagelabel.setFixedSize(248,248)
        self.imagelayout.addWidget(self.imagelabel)
        self.v_layout.addLayout(self.imagelayout)
        
        self.v_layout_info = QVBoxLayout()#商品大致信息
        self.v_layout_info.setContentsMargins(8,8,8,0)
        self.v_layout.addLayout(self.v_layout_info)
        
        self.assetname = QLabel("这是一个商品")#商品名字
        self.assetname.setFont(QFont("Lucida Console",16))
        self.assetname.setStyleSheet("color: #f3f3f3;font-size: 16px;")
        self.assetname.setFixedSize(232,24)
        self.v_layout_info.addWidget(self.assetname)
        
        self.assetauthor = QLabel("柯哀的眼")#作者名字
        self.assetauthor.setFont(QFont("Lucida Console",14))
        self.assetauthor.setStyleSheet("color: #dca100;font-size: 14px;")
        self.assetauthor.setFixedSize(232,24)
        self.v_layout_info.addWidget(self.assetauthor)
        
        self.assetscore = HoudiniStoreAssetScoreWidget()#评分控件
        self.v_layout_info.addWidget(self.assetscore)
        
        self.assetprice = HoudiniStoreAssetPriceWidget()#价格控件
        self.v_layout_info.addWidget(self.assetprice)
        
        self.assetshopping = HoudiniStoreAssetShoppingTrolleyWidget()#购物车控件
        self.v_layout_info.addWidget(self.assetshopping)
        
        self.setObjectName("HoudiniStoreAssetWidget")
        self.setStyleSheet(HoudiniStoreAssetWidgetStyle)
    
    def paintEvent(self, event):
        """重载-绘制"""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
    
    def initWidget(self,data):
        """初始化商品控件"""
        for n in data['fields']:
            if n == 'assetName':
                self.assetname.setText(str(data['fields'][n]))
            elif n == 'authorName':
                self.assetauthor.setText(str(data['fields'][n]))
            elif n == 'assetPrice':
                self.assetprice.setPriceText('$'+str(data['fields'][n]))
            elif n == 'assetScore':
                self.assetscore.setScoreText(str(data['fields'][n]))
            elif n == 'imagePath':
                self.thread_1 = ReadWebImages()  # 创建线程
                self.thread_1.image_url = str(data['fields'][n])
                self.thread_1.imagelabel = self.imagelabel
                self.thread_1.start()  # 开始线程
        
class HoudiniStoreAssetsBlockWidget(QWidget):
    """Houdini商店显示商品分区"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(900)
        self.setMaximumWidth(1300)
        
        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(30,32,30,0)
        self.v_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.setLayout(self.v_layout)
        
        self.name_layout = QHBoxLayout()
        self.v_layout.addLayout(self.name_layout)
        
        self.nametitleA = QLabel("新内容")#文字标题左
        self.nametitleA.setStyleSheet("color: #f3f3f3;font-size: 28px;")
        self.name_layout.addWidget(self.nametitleA)
        self.name_layout.addStretch()
        
        self.nametitleB = QLabel("查看所有新发布的商品")#文字标题右
        self.nametitleB.setStyleSheet("color: #dca100;font-size: 16px;")
        self.name_layout.addWidget(self.nametitleB)
        
        self.g_layout = FlowLayout()
        self.v_layout.addLayout(self.g_layout)
        
    def addAssetWidget(self,widget:HoudiniStoreAssetWidget):
        """添加商品展示控件"""
        self.g_layout.addWidget(widget)

    def demo(self):
        """测试"""
        for i in range(5):
            saw = HoudiniStoreAssetWidget()
            self.addAssetWidget(saw)
    
    def addAssetForData(self,data):
        """根据数据添加商品"""
        if not data:
            self.demo()
            return#没服务器就获取不到数据
        for i in data:
            saw = HoudiniStoreAssetWidget()
            self.addAssetWidget(saw)
            saw.initWidget(i)
            self.demo()
    
    def resizeEvent(self, e):
        h = self.name_layout.sizeHint().height()
        self.setMinimumHeight(self.g_layout.flowheight+h+60)
        self.resize(self.width(),self.g_layout.flowheight+h+60)

class HoudiniStoreScrollArea(QScrollArea):
    """Houdini商店滚动区域"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)#无边框
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)#隐藏横向滚动条
        self.nodeswidget = QWidget(self)
        self.nodeswidget.setObjectName("HoudiniStoreScrollArea")
        self.nodeswidget.resize(self.size())
        self.setWidget(self.nodeswidget)#显示滚动条必须的
        
        self.v_layout = QVBoxLayout(self.nodeswidget)
        self.v_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.v_layout.setContentsMargins(2,0,10,0)
        self.v_layout.setSpacing(0)
        
        self.topwidget = HoudiniStoreTopWidget()
        self.v_layout.addWidget(self.topwidget)
        
        self.assetswidgetA = HoudiniStoreAssetsBlockWidget()
        self.v_layout.addWidget(self.assetswidgetA)
        self.assetswidgetA.show()
        
        self.nodeswidget.setStyleSheet(HoudiniStoreScrollAreaStyle)
        self.addAssetForData()#网络加载资源

    def resizeEvent(self, e):
        self.nodeswidget.resize(self.width(),self.nodeswidget.sizeHint().height())
    
    def addAssetForData(self):
        """根据数据添加商品"""
        data = getStoreAssetData()
        self.assetswidgetA.addAssetForData(data)
        
