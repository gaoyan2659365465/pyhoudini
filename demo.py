from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import hou
import json

def getQtClass(data):
    listclass=[]
    list0 = data.children()#获取子空间列表
    listclass.append(list0)
    for i in list0:
        #print(i.__class__.__name__)
        if i.__class__.__name__ == 'QVBoxLayout':
            for a in range(i.count()):
                item = i.itemAt(a).widget()
                #print(item.__class__.__name__)
                listclass.append(getQtClass(item))
        else:
            listclass.append(getQtClass(i))
    return listclass


w = hou.qt.mainWindow()
w:QWidget
a = w.children()[1]
#print(w.children()[1].move(0,0))
b = a.children()[0]
#print(a.children()[0].move(0,0))
c1 = b.children()[0]#视口
c2 = b.children()[1]#属性界面
c3 = b.children()[2]#时间滑块

d = a.children()[1]
e = d.itemAt(0).widget()

f1 = e.children()[0]
f2 = e.children()[1]
f3 = e.children()[2]

g = w.children()[0]
# for i in range(g.count()):
#     item = g.itemAt(i).widget()
#     print(item)
h = g.itemAt(0).widget()
h1 = h.children()[0]#整体

#print(a.children()[1].move(100,0))
#print(w.children()[1].children()[0])
#a = QPushButton("你好",w)
#a.close()
#listdata = getQtClass(w)
#json.dump(str(listdata), open(__file__[:-7]+"/aaa.json",'w'),ensure_ascii=False,indent=4)
#print(listdata)