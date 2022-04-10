import examples.Node.BP_NodeBase
from examples.Node.W_NodeBase import *
from examples.Node.BP_SearchNodeBase import *
import random
from .BP_Json import BP_Json

class W_Scene(QGraphicsScene):
    click_node=Signal(object)#自定义点击信号
    def __init__(self, parent=None):
        super().__init__(parent)
        self.select_node1 = None#被点击且拖拽的Node
        self.select_socket = None#被悬浮的socket
        self.create_nodes = []#动态创建的节点列表
        self.isAltKey = False
        self.bp_search = BP_SearchNodeBase(self)#鼠标右键点击弹出的窗口

    def addNodes(self,node):
        """动态添加节点到列表由Search调用"""
        self.create_nodes.append(node)
    
    def removeNodes(self):
        """删除选中的Node"""
        for w_node in self.selectedItems():
            if type(w_node) == W_NodeBase:
                bp_node = w_node.bp_node.removeNode()
                self.removeItem(w_node)
                try:
                    self.create_nodes.remove(bp_node)
                except:pass
    
    #region 获取选中Node
    def getSelectNode(self):
        """获取选中的Node"""
        return self.select_node1,self.select_socket
    
    def setSelectNode(self,node,socket):
        """设置选中的Node"""
        self.select_node1 = node
        self.select_socket = socket
    #endregion
    
    #region 鼠标坐标
    def getStartPos(self):
        """获得鼠标点击时view视口的鼠标坐标"""
        return self.start_pos
    
    def setStartPos(self,pos):
        """设置鼠标点击时view视口的鼠标坐标"""
        self.start_pos = pos
    
    def getEndPos(self):
        """获得鼠标点击时view视口的鼠标坐标"""
        return self.end_pos,self.sc_pos
    
    def setEndPos(self,pos,sc_pos):
        """设置鼠标点击时view视口的鼠标坐标"""
        self.end_pos = pos
        self.sc_pos = sc_pos
    #endregion
    
    #region 鼠标点击的项
    def getClickItem(self):
        """获得鼠标点击的项"""
        try:
            self.click_item
        except:
            self.click_item=None
        return self.click_item
    
    def setClickItem(self,item):
        """设置鼠标点击的项"""
        self.click_item = item
    #endregion
    
    #region 鼠标坐标
    def getDragMousePos(self):
        """获得拖拽时view视口的鼠标坐标"""
        return self.drag_mouse_pos
    
    def setDragMousePos(self,pos):
        """设置拖拽时view视口的鼠标坐标"""
        self.drag_mouse_pos = pos
    #endregion
    
    def keyPressEvent(self, event):
        """重载键盘事件"""
        if event.key() == 16777223:#删除键
            self.removeNodes()
        if event.key() == 16777251:#Alt键
            self.isAltKey = True
        super().keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        """重载键盘事件"""
        if event.key() == 16777251:#Alt键
            self.isAltKey = False
        super().keyReleaseEvent(event)
    
    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        """重载-鼠标移动"""
        for i in self.selectedItems():
            if type(i) == W_NodeBase:
                i.bp_node.nodeMove()#节点移动
        item = self.getClickItem()
        #print("移动:" + str(event.screenPos()))
        if isinstance(item, W_SocketBase):
            socket_content = item.parentItem()
            node_content = socket_content.parentItem()
            w_node = node_content.parentItem()
            w_node.bp_node.socket_mouse_move(socket_content,event)
            return
        super().mouseMoveEvent(event)
    
    def mousePressEvent(self, event:QMouseEvent):
        """重载-鼠标按下"""
        item = self.getClickItem()
        #按下鼠标时点击到别处则隐藏Search界面
        if item is None or hasattr(item.parentItem(), "w_title"):
            self.bp_search.setSearchNodeWidgetLocation(10000,10000)
        #------------------------------------
        if isinstance(item, W_SocketBase):
            socket_content = item.parentItem()
            node_content = socket_content.parentItem()
            w_node = node_content.parentItem()
            w_node.bp_node.socket_mouse_press(socket_content,event,True)
            self.setSelectNode(w_node,socket_content)#设置选中Node
        if isinstance(item, W_TitleBase) or isinstance(item, W_NodeContent):
            w_node = item.parentItem()
            self.click_node.emit(w_node.bp_node)#点击Node发射信号
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event:QMouseEvent):
        """重载-鼠标松开"""
        start_pos = self.getStartPos()
        end_pos,sc_pos = self.getEndPos()
        if start_pos == end_pos:
            if event.button() == Qt.RightButton:
                #设置搜索面板位置
                self.bp_search.setSearchNodeWidgetLocation(sc_pos.x(),sc_pos.y())
                self.bp_search.w_search.isOk = False
        #-----------------------------
        item = self.getClickItem()
        if isinstance(item, W_SocketBase):
            socket_content = item.parentItem()
            node_content = socket_content.parentItem()
            w_node = node_content.parentItem()
            
            node1,socket = self.getSelectNode()
            node2 = w_node
            if node1 != None and node2 != None:
                if node1 != node2:
                    node1.bp_node.node_connection(socket,socket_content,node2.bp_node)
            try:
                node1.bp_node.socket_mouse_release(socket_content,event)
            except:pass
            self.setSelectNode(None,None)
        else:
            #松开鼠标使连接线删除
            node1,socket = self.getSelectNode()
            if node1 != None:
                node1.bp_node.socket_mouse_release(socket,event)
                self.setSelectNode(None,None)
            
        super().mouseReleaseEvent(event)
   
    def runBlueprint(self):
        """运行蓝图"""
        print("开始运行")
        for w_node in self.items():
            if type(w_node) == W_NodeBase:
                if type(w_node.bp_node) == BP_Node_BeginPlay:
                    w_node.bp_node.runBlueprint()
    
    def getNodeByUUID(self,uuid):
        """通过uuid获取node"""
        for item in self.items():
            if isinstance(item, W_NodeBase):
                if item.bp_node.uuid == uuid:
                    return item.bp_node
    
    #region 序列化
    def dump(self):
        """保存"""
        data = {}
        data2 = {}
        a=0
        for item in self.items():
            if isinstance(item, W_NodeBase):
                data['class_name'] = item.bp_node.__class__.__name__
                data['bp_node'] = item.bp_node.dump()
                data2[a] = data.copy()
                a=a+1
        data3 = {}
        data3['node_num'] = a#所有节点总数
        data2['bp_data'] = data3
        
        json = BP_Json()
        json.dumpFile(data2)
        return
    def load(self):
        """加载"""
        json = BP_Json()
        data = json.loadFile()
        for key in data:
            #根据类名创建相应节点
            if key == 'bp_data':
                continue
            AClass = getattr(examples.Node.BP_NodeBase, data[key]['class_name'])
            node = AClass(self)
            node.addDemoSocket()
            self.addNodes(node)
            node.load(data[key]['bp_node'])
        for item in self.items():
            if isinstance(item, W_NodeBase):
                for key in data:
                    if key == 'bp_data':
                        continue
                    if data[key]['bp_node']['uuid'] == item.bp_node.uuid:
                        item.bp_node.load_edge(data[key]['bp_node'])
        return
    #endregion