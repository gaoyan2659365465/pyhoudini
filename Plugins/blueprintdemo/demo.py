import sys
from PYBP.window.PYBP_WindowItem import *
from PYBP.window.widget.PYBP_MainWidget import *

class PYBP_MainWindow(PYBP_WindowItem):
    def __init__(self, parent):
        self.createWidget = lambda:PYBP_MainWidget(self)
        super().__init__(parent)
        self.addNewSelectItem("1")
        self.addNewSelectItem("2")
        self.addNewSelectItem("3")
        self.closeWin = lambda:None
        self.visiable = lambda:None
        self.move_signal.connect(self.ItemWinMove)
        self.addAllWindow(self)
    
    def initValue(self):
        self.allWindow = []#专门存储所有外置窗口
        return super().initValue()
    
    def initTitle(self):
        """无边框"""
        super().initTitle()
        self.setWindowFlags(Qt.FramelessWindowHint)
        
    def close(self):
        """重载-关闭函数"""
        self.allWindow.remove(self)
        for win in reversed(self.allWindow):
            win.close()
        super().close()
    
    def addAllWindow(self,obj):
        """需要子类重载"""
        self.allWindow.append(obj)
        obj.move_signal.connect(self.ItemWinMove)
    
    def subAllWindow(self,obj):
        """需要子类重载"""
        try:
            self.allWindow.remove(obj)
        except:pass
        
    def ItemWinMove(self,obj0:PYBP_WindowItem,obj:PYBP_WindowItem):
        """所有子窗体的移动槽函数
        obj0:拖动之前的窗体，被隐藏
        obj:正在被拖动的窗体，半透明
        """
        def ItemWinMove_Ture(ww):
            obj.releaseMouse()#取消全局鼠标
            try:
                obj.subAllWindow(obj)
            except:pass
            obj_select = obj.s_layout.click_widget
            obj_select.setParent(ww)#移植到新界面
            try:
                obj_select.click.disconnect(obj.selectItemClick)
            except:pass
            obj_select.click.connect(ww.selectItemClick)
            obj_select.show()
            ww.s_layout.addWidget(obj_select)
            ww.s_layout.setClickItem(obj_select)
            ww.s_layout.setY(15)#刷新一下新界面
            obj.s_layout.remove(obj_select)#从原列表删除
            obj.s_layout.setY(15)#刷新一下老界面
            obj.close()
            ww.s_layout.isborder = False#正在拖拽状态
            ww.s_layout.setSelectItemClickState(True)
            m_event = QMouseEvent(QEvent.MouseButtonPress, QCursor.pos() - ww.pos(),
                                Qt.LeftButton,Qt.LeftButton, Qt.NoModifier)
            ww.grabMouse()#开启全局鼠标
            QApplication.sendEvent(ww,m_event)
            
        for w in self.allWindow:
            if w == obj:continue
            w_size:QRect = w.getSelectSize()
            if w_size.contains(QCursor.pos()):
                ItemWinMove_Ture(w)
                return
    
    def border(self,obj):
        """当鼠标拖拽浏览页超出当前边界时"""
        self.main_window = self
        super().border(obj)

if __name__ == "__main__":
    app=QApplication(sys.argv)
    widget=PYBP_MainWindow(None)
    widget.show()
    sys.exit(app.exec_())