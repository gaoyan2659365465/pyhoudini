#Houdini商店界面
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from widget.StyleTool import *
from widget.FlowLayout import FlowLayout
import requests

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

class HoudiniStoreAssetWidget(QWidget):
    """Houdini商店显示商品控件"""
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.v_layout = QVBoxLayout()#主布局
        self.v_layout.setContentsMargins(10,0,10,16)
        self.setLayout(self.v_layout)
        
        self.imagelabel = QLabel()#商品展示图片
        res = requests.get("https://cdn1.epicgames.com/ue/product/Thumbnail/RetroPlantsandTreespack_thumb-284x284-14cd1044a384d8c2b493482bd8db6341.png?resize=1&w=300")
        img = QImage.fromData(res.content)
        self.imagelabel.setPixmap(QPixmap.fromImage(img)\
            .scaled(248,248,Qt.IgnoreAspectRatio,Qt.SmoothTransformation))
        self.imagelabel.setFixedSize(248,248)
        self.v_layout.addWidget(self.imagelabel)
        
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
        
        self.assetprice = HoudiniStoreAssetShoppingTrolleyWidget()#购物车控件
        self.v_layout_info.addWidget(self.assetprice)
        
        self.setObjectName("HoudiniStoreAssetWidget")
        self.setStyleSheet(HoudiniStoreAssetWidgetStyle)
    
    def paintEvent(self, event):
        """重载-绘制"""
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
        
class HoudiniStoreAssetsBlockWidget(QWidget):
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
        
        #self.g_layout = QGridLayout()
        self.g_layout = FlowLayout()
        #self.g_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        
        self.v_layout.addLayout(self.g_layout)
        
        
        self.demo()
        
    def addAssetWidget(self,widget:HoudiniStoreAssetWidget,x,y):
        """添加商品展示控件"""
        #self.g_layout.addWidget(widget,x,y)
        self.g_layout.addWidget(widget)

    def demo(self):
        """测试"""
        for i in range(5):
            saw = HoudiniStoreAssetWidget()
            self.addAssetWidget(saw,0,i)

class HoudiniStoreScrollArea(QScrollArea):
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
        
        self.assetswidgetA = HoudiniStoreAssetsBlockWidget()
        self.v_layout.addWidget(self.assetswidgetA)
        self.assetswidgetA.show()
        
        self.nodeswidget.setStyleSheet(HoudiniStoreScrollAreaStyle)

    def resizeEvent(self, e):
        self.nodeswidget.resize(self.width(),self.nodeswidget.sizeHint().height())
