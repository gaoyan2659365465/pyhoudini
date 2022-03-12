#复制节点数据表
import hou
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

def getNodeData():
    list1 = {}
    nodes = hou.selectedNodes()
    if nodes:
        geo = nodes[0].geometry()
        points = geo.points()
        Attribsname = geo.pointAttribs()

        for n in Attribsname:
            list2 = []
            for i in points:
                list2.append(i.attribValue(n))
            print(n.name())
            list1[n.name()] = list(list2)
    
    clipboard = QApplication.clipboard()
    clipboard.setText(str(list1))