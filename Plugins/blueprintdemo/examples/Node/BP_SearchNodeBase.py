from examples.Node.W_SearchNodeBase import *
from examples.Node.BP_NodeBase import *
from examples.Plugins.Plugins import *

# 创建信号类
class QSearchNodeBaseSigner(QObject):
    widget_rem=Signal(object)#删除连接线信号
    widget_add=Signal(object)#将连接线添加到scene
    def __init__(self):
        super(QSearchNodeBaseSigner, self).__init__()
    def scene_add_run(self,item):
        self.widget_add.emit(item)
    def scene_remove_run(self,item):
        self.widget_rem.emit(item)


class BP_SearchNodeBase():
    def __init__(self,scene=None):
        self.scene = scene
        self.initAssets()
        self.createSearch()
    
    def initAssets(self):
        self.signer = QSearchNodeBaseSigner()
        #print(list_section)
        
    def createSearch(self):
        """创建一个SearchNodeBase"""
        self.w_search = W_SearchNodeBase()
        self.w_search.signer.addNode.connect(self.addNode)
        self.signer.widget_add.connect(self.scene.addItem)
        self.signer.scene_add_run(self.w_search)
        self.w_search.hide()
        
    def removeSearch(self):
        """从scene里面删除该界面"""
        self.signer.scene_remove_run(self.w_search)
        
    def setSearchNodeWidgetLocation(self,x,y):
        """设置界面位置"""
        self.w_search.show()
        self.w_search.setPos(x,y)
    
    def addNode(self,obj):
        """向场景中添加节点"""
        if obj == 'BeginPlay':
            self.node = BP_Node_BeginPlay(self.scene)
        elif obj == 'PrintString':
            self.node = BP_Node_PrintString(self.scene)
        elif obj == 'Branch':
            self.node = BP_Node_Branch(self.scene)
        elif obj == 'ForLoop':
            self.node = BP_Node_ForLoop(self.scene)
        elif obj == 'IntToString':
            self.node = BP_Node_IntToString(self.scene)
        self.node.addDemoSocket()
        pos = self.w_search.pos()
        self.node.w_node.setPos(pos.x(),pos.y())
        self.scene.addNodes(self.node)
        self.setSearchNodeWidgetLocation(10000,10000)
        self.w_search.isOk = False
        
        