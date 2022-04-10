from PYBP.window.PYBP_Window import *
from PYBP.window.PYBP_Tool import *
from PYBP.window.select.PYBP_SelectItem import *
from PYBP.window.select.PYBP_SelectLayout import *
from PYBP.window.widget.PYBP_MainWidget import PYBP_MainWidget

class PYBP_WindowItem(PYBP_Window):
    move_signal=Signal(object,object)#自定义点击信号
    
    def __init__(self, parent):
        super().__init__(parent)
        
    def initValue(self):
        self.tool = PYBP_Tool(self)
        self.s_layout = PYBP_SelectLayout(self)
        self.main_window:PYBP_WindowItem = None
        return super().initValue()
    
    def setMainWindow(self,obj):
        """设置main_window"""
        self.main_window = obj
    
    def resizeEvent(self,event):
        """窗口改变大小时触发"""
        self.tool.resize(self.width()-10,20)
        super().resizeEvent(event)
    
    def mouseMoveEvent(self,event):
        """鼠标移动"""
        if self.s_layout.isborder:
            press_pos = self.s_layout.getPressPos()
            self.move(QCursor.pos() - press_pos - QPoint(35,15))
            self.move_signal.emit(self,self)
            self.setWindowOpacity(0.85)#窗体颜色虚化
            return
        if self.getSelectItemClickState():
            self.s_layout.moveItem(event.x(),event.y())
            return
        super().mouseMoveEvent(event)
    
    def getSelectItemClickState(self):
        """获取浏览页点击状态"""
        return self.s_layout.getSelectItemClickState()
    
    def showMaximized(self):
        """窗口最大化"""
        super().showMaximized()
        self.tool.move(5,30)
        self.s_layout.setY(5)
    
    def showNormal(self):
        """还原窗口"""
        super().showNormal()
        self.tool.move(5,40)
        self.s_layout.setY(15)
        
    def selectItemClick(self,obj,is_click):
        """选项卡的点击槽函数"""
        super().selectItemClick(obj,is_click)
        self.s_layout.setSelectItemClickState(is_click)
        self.s_layout.setClickItem(obj)
        self.s_layout.moveAnim()
        self.s_layout.setAllColor(obj)
    
    def addAllWindow(self,obj):
        """需要子类重载"""
        self.main_window.addAllWindow(self)
    def subAllWindow(self,obj):
        """需要子类重载"""
        try:
            self.main_window.subAllWindow(self)
        except:pass
    
    def border(self,obj:PYBP_SelectItem):
        """当鼠标拖拽浏览页超出当前边界时"""
        self.addWindow(obj)#创建新界面
        obj.click.disconnect(self.selectItemClick)
        self.s_layout.setSelectItemClickState(False)
        self.s_layout.isborder = False#取消拖拽状态
        self.s_layout.remove(obj)#从原列表删除
        self.s_layout.setY(self.s_layout.y)#刷新一下老界面
        self.visiable()#隐藏自己
        
    
    def visiable(self):
        """隐藏自己"""
        if len(self.s_layout.widgets) == 0:
            self.subAllWindow(self)
            self.setWindowOpacity(0)
            
    
    def closeWin(self):
        """关闭自己"""
        if len(self.s_layout.widgets) == 0:
            self.subAllWindow(self)
            self.close()
    
    def close(self):
        """重载-关闭函数"""
        self.subAllWindow(self)
        super().close()
    
    def event(self,event):
        #print(str(self) + "    " + str(event.type()))
        if event.type() == 10:
            self.setWindowOpacity(1)#设置透明度
            self.s_layout.setY(self.s_layout.y)
        if event.type() == 11:#原窗体触发
            self.closeWin()
        return super().event(event)
    
    def mouseReleaseEvent(self,event):
        super().mouseReleaseEvent(event)
        self.setWindowOpacity(1)#设置透明度
        self.s_layout.setY(self.s_layout.y)
        self.releaseMouse()#取消全局鼠标
        self.s_layout.isborder = False
        self.s_layout.setSelectItemClickState(False)
    
    def addWindow(self,select_item:PYBP_SelectItem):
        """主窗体添加额外窗体"""
        self.win = PYBP_WindowItem(None)
        self.win.setMainWindow(self.main_window)
        self.win.addSelectItem(select_item,self.pos())
        self.win.show()
        return self.win
    
    def getSelectSize(self):
        """获取浏览页条尺寸"""
        x = self.x() + self.s_layout.x
        y = self.y() + self.s_layout.y
        w = self.width() - 2*self.s_layout.x
        h = 25#PYBP_SelectItem  w_height
        return QRect(x,y,w,h)
    
    def addNewSelectItem(self,name):
        """添加新的选项卡"""
        w_select = PYBP_SelectItem(self)
        w_select.setText(name)
        w_select.click.connect(self.selectItemClick)
        self.s_layout.addWidget(w_select)
        
    def addSelectItem(self,select_item:PYBP_SelectItem,pos:QPoint):
        """添加浏览页并初始化窗体"""
        self.setWindowOpacity(0.85)#窗体颜色虚化
        self.move(pos)#设置位置
        select_item.setParent(self)#移植到新界面
        select_item.click.connect(self.selectItemClick)
        select_item.show()
        self.addAllWindow(self)
        self.s_layout.addWidget(select_item)
        self.s_layout.setClickItem(select_item)
        self.s_layout.setSelectItemClickState(True)
        self.s_layout.setY(self.s_layout.y)#刷新一下新界面
        self.s_layout.isborder = True#正在拖拽状态
        m_event = QMouseEvent(QEvent.MouseButtonPress, QCursor.pos() - self.pos(),
                                Qt.LeftButton,Qt.LeftButton, Qt.NoModifier)
        self.grabMouse()#开启全局鼠标
        QApplication.sendEvent(self,m_event)
        
        
        
        