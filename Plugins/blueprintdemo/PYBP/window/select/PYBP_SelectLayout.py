from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

#负责存放浏览页的布局类

class PYBP_SelectLayout():
    def __init__(self,window):
        self.window = window
        self.widgets = []
        self.click_widget = None
        self.isclick = False
        self.isborder = False
        self.x = 35
        self.y = 15
    
    def setClickItem(self,obj:QWidget):
        """设置点击的子项"""
        self.click_widget = obj
    
    def addWidget(self,widget:QWidget):
        """添加子项"""
        self.widgets.append(widget)
        self.setY(15)
    
    def setY(self,y):
        """设置Y值"""
        self.y = y
        self.move(self.x,y)
    
    def move(self,x,y):
        """移动所有子项"""
        for w in self.widgets:
            w:QWidget
            w.move(x,y)
            x=x+w.width()-30
        for i in reversed(self.widgets):#反着遍历
            i.raise_()#置顶
        if self.click_widget:
            self.click_widget.raise_()
    
    def moveItem(self,x,y):
        """移动一个子项"""
        if self.click_widget == None:return
        self.moveAnim()
        press_pos = self.click_widget.press_pos
        if y>self.y and y<self.y+self.click_widget.w_height:
            self.click_widget.move(x-press_pos.x(),self.y)#y-press_pos.y()
        else:
            if not self.isborder:
                self.border(self.click_widget)
    
    def moveAnim(self):
        """位置排序"""
        list0 = []
        list1 = []
        for w in self.widgets:
            w:QWidget
            w_x = w.pos().x()
            list0.append(w_x)
            list0.append(w)
            list1.append(list(list0))
            list0 = []
        list1 = sorted(list1,key=lambda x: x[0])
        for i in range(len(list1)):
            self.widgets[i] = list1[i][1]
        self.move(self.x,self.y)

    def border(self,obj):
        """当鼠标拖拽浏览页超出当前边界时"""
        if self.click_widget == None:return
        self.window.border(obj)
            
    def remove(self,obj):
        """删除指定浏览卡"""
        try:
            self.click_widget = None
            self.widgets.remove(obj)
        except:pass
    
    def setAllColor(self,obj):
        """关闭所有选项卡的颜色"""
        for i in self.widgets:
            i.setColor(False)
        obj.setColor(True)
    
    def getPressPos(self):
        """获得浏览页偏移"""
        return self.click_widget.press_pos
    
    def getSelectItemClickState(self):
        """获取浏览页点击状态"""
        return self.isclick
    
    def setSelectItemClickState(self,is_click):
        """设置浏览页点击状态"""
        self.isclick = is_click
    
#点一下到最前面，遮挡