#复制节点数据表
import hou
import json
import os
from Plugins.Tools import *

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
    
    path = FilePath + 'UE5/'
    path_json = path + "HoudiniNodeData.json"
    if not os.path.isdir(path):
        os.makedirs(path)
    json.dump(list1, open(path_json,'w'),ensure_ascii=False,indent=4)