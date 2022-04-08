# -*- coding: utf-8 -*-
from .W_NodeBase import *
from .W_Edge import W_Edge,EDGE_POS_SOURCE,EDGE_POS_DESTINATION
from .BP_Json import BP_Json
import uuid


class BP_NodeBase(BP_Json):
    def __init__(self,scene=None):
        self.scene = scene#父控件容器
        self.w_node = None#节点控件
        self.w_edges = {}#连接线
        self.socket_num = 0#插槽数
        self.mouse_pos = QPointF()#鼠标位置
        self.socket_offect = QPointF()
        self.socket_base_offect = QPointF()
        self.createNode()
        self.uuid = str(uuid.uuid1())#生成唯一ID
        self.new_socket_num = 0#默认下一个连接节点的插槽编号
        
    def createNode(self):
        """创建一个W_NodeBase"""
        self.w_node = W_NodeBase(self)
        self.scene.addItem(self.w_node)
    
    def removeNode(self):
        """删除这个Node"""
        nodes=[]
        for i in self.w_edges:
            a = 0
            for o in self.w_edges[i]:
                edge = o[0]
                nodes.append(edge.getNewNode(self))#获取另一个node
                self.scene.removeItem(o[0])
                self.w_edges[i][a][0] = None
                a = a+1
        nodes = list(set(nodes))#去除重复项
        for node in nodes:
            if node == None:continue
            for i in node.w_edges:
                b = 0
                for o in node.w_edges[i]:
                    edge = o[0]
                    if edge.nodes[0] == self or edge.nodes[1] == self:
                        node.w_edges[i][b][0] = None
                    b = b+1
            node.updateEdges()
        self.updateEdges()
        return self
    
    def removeEdgeBySocket(self,socket):
        """删除指定插槽的所有连接线"""
        key = self.getSocketIndex(socket)
        nodes=[]
        edges=[]
        a=0
        try:
            for o in self.w_edges[key]:
                edge = o[0]
                self.scene.removeItem(edge)
                nodes.append(edge.getNewNode(self))#获取另一个node
                edges.append(self.w_edges[key][a][0])
                self.w_edges[key][a][0] = None
                a+=1
            nodes = list(set(nodes))
            for node in nodes:
                if node == None:continue
                for key1 in node.w_edges:
                    b = 0
                    for o in node.w_edges[key1]:
                        edge = o[0]
                        if edge.nodes[0] == self or edge.nodes[1] == self:
                            if node.w_edges[key1][b][0] in edges:#防止删多了
                                node.w_edges[key1][b][0] = None
                        b+=1
                node.updateEdges()
            self.updateEdges()
        except:pass
    
    def updateEdges(self):
        """更新连接线列表并且设置socket状态"""
        #清除所有插槽的连接状态
        sockets = self.getAllSocket()
        for socket in sockets:
            socket.setSocketState(False)
        #清除edges内的None值
        new_edges = {}
        for i in self.w_edges:
            list01 = []
            for o in self.w_edges[i]:#o表示插槽
                edge = o[0]
                if edge != None:
                    list01.append(o)
                    self.setSocketState(i,True)
            new_edges[i] = list01
        self.w_edges = new_edges
        self.w_node.update()
        #print(self.w_edges)
    
    def getNodeTitleName(self):
        """获得节点标题栏文字"""
        return self.w_node.getNodeTitleName()
    
    def setNewSocketNum(self,num):
        """设置下一个节点连接端默认编号"""
        self.new_socket_num = num
    
    def setNodeTitleName(self,Name:str=''):
        """设置节点标题栏文字"""
        self.w_node.setNodeTitleName(Name)
    
    def setNodeTitlePix(self,pix:int=0):
        """设置节点标题栏图标"""
        self.w_node.setNodeTitlePix(pix)
    
    def setNodeTitleColor(self,color:str=''):
        """设置标题栏颜色"""
        self.w_node.setNodeTitleColor(color)
    
    def addSocket(self,data_type:int=0,direction:int=0,logic_type:int=0):
        """给节点内容增加端口
        :param data_type: 节点表示的变量的数据类型（整型/字符串）
        :param direction: 需要在节点输(入/出)侧添加端口
        :param logic_type: 节点表示的变量的逻辑类型（数据/逻辑）
        """
        self.socket_num = self.socket_num +1
        socket=self.w_node.addSocket(data_type,direction,logic_type)
        self.setAutomaticSize()
        return socket
    
    def addDemoSocket(self):
        """测试代码-添加默认插槽"""
        self.addSocket(-1,0,0)#逻辑
        self.addSocket(-1,1,0)#逻辑
        #---------------------------
        self.addSocket(0,0,1)#值
        self.addSocket(2,0,1)#值
        self.addSocket(1,1,1)#值
        self.addSocket(1,0,1)#值
        self.addSocket(3,0,1)#值
    
    def getAllSocket(self):
        """获取此节点所有插槽"""
        return self.w_node.getAllSocket()
    
    def getSocketIndex(self,socket):
        """查询socket的编号"""
        sockets = self.getAllSocket()
        return sockets.index(socket)
    
    def getSocketLocation(self,socket_num:int=0):
        """获取插槽的绝对位置
        :param socket_num:次节点的插槽端口编号
        return 插槽的绝对位置
        """
        return self.w_node.pos() + self.w_node.getSocketLocation(socket_num)
    
    def getSocketColor(self,socket_num:int=0):
        """获取插槽的颜色"""
        return self.w_node.getSocketColor(socket_num)
    
    def setSocketState(self,socket_num:int=0,isLink:bool=False):
        """设置端口状态是否已连接"""
        self.w_node.setSocketState(socket_num,isLink)
    
    def getSocketDirection(self,socket_num:int=0)->bool:
        """获取插槽是左边还是右边"""
        return self.w_node.getSocketDirection(socket_num)
    
    def setAutomaticSize(self):
        """自动设置节点所需要的尺寸"""
        self.w_node.setAutomaticSize()
    
    def connection(self,new_node,x1,x2):
        """建立一个连接线"""
        point = self.getSocketLocation(x1)
        point1 = new_node.getSocketLocation(x2)
        color = self.getSocketColor(x1)
        self.w_edge = W_Edge()
        self.w_edge.setEdgeColor(color)
        self.w_edge.setNodes(self,new_node)                 #存入Node引用
        self.scene.addItem(self.w_edge)#将连接线让场景显示出来
        try:
            list01 = self.w_edges[x1]
        except:
            list01 = []
        try:
            list02 = new_node.w_edges[x2]
        except:
            list02 = []
        direction = self.getSocketDirection(x1)#获取插槽是左边还是右边
        if direction == VALUE_INPUT:
            list01.append([self.w_edge,EDGE_POS_DESTINATION])
            list02.append([self.w_edge,EDGE_POS_SOURCE])
            self.w_edge.setSource(point1.x(),point1.y())          #设置起点
            self.w_edge.setDestination(point.x(),point.y())   #设置终点
        elif direction == VALUE_OUTPUT:
            list01.append([self.w_edge,EDGE_POS_SOURCE])
            list02.append([self.w_edge,EDGE_POS_DESTINATION])
            self.w_edge.setSource(point.x(),point.y())          #设置起点
            self.w_edge.setDestination(point1.x(),point1.y())   #设置终点
        
        self.w_edges[x1] = list01
        new_node.w_edges[x2] = list02
        self.setSocketState(x1,True)
        new_node.setSocketState(x2,True)
        return self.w_edge
    
    def node_connection(self,my_socket,new_socket,new_node):
        """此函数被view调用-连接两个节点"""
        point = self.getSocketIndex(my_socket)
        edges=[]
        try:
            for i in self.w_edges[point]:
                edges.append(i[0])
        except:pass
        point1 = new_node.getSocketIndex(new_socket)
        edges1=[]
        try:
            for i in new_node.w_edges[point1]:
                edges1.append(i[0])
        except:pass
        set_c = set(edges) & set(edges1)#判断两list有无重复项
        list_c = list(set_c)
        if len(list_c)==0:#两个插槽不能存在多条线
            self.connection(new_node,point,point1)#有BUG。两个节点如果有一条线的话不能再创建线
    
    def nodeMove(self):
        """节点被移动了"""
        self.updateAllEdgeLocation()
    
    def updateAllEdgeLocation(self):
        """更新此节点上连接的所有线的位置"""
        for key in self.w_edges:
            a = self.w_edges[key]
            point = self.getSocketLocation(key)
            for i in a:
                i[0].setLocation(i[1],point.x(),point.y())
    
    #region socket拖拽事件
    def socket_mouse_press(self,socket,event,isXuanFu):
        """事件调度-socket"""
        if self.scene.isAltKey == True:
            self.removeEdgeBySocket(socket)
        
        if not isXuanFu:
            return
        
        key = self.getSocketIndex(socket)
        point = self.getSocketLocation(key)
        
        sc_pos = event.screenPos()
        self.socket_offect = point - sc_pos
        
        self.w_edge_ = W_Edge()
        self.w_edge_.setSource(point.x(),point.y())         #设置起点
        self.w_edge_.setDestination(point.x(),point.y())  #设置终点
        self.w_edge_.hovered = True#鼠标悬浮
        color = self.getSocketColor(key)#设置线条颜色
        self.w_edge_.setEdgeColor(color)
        self.scene.addItem(self.w_edge_)#将连接线让场景显示出来
        
    def socket_mouse_move(self,socket,event):
        """事件调度-socket"""
        sc_pos = event.screenPos()
        sc_pos = sc_pos + self.socket_offect.toPoint() + self.socket_base_offect.toPoint()
        try:
            self.w_edge_.setDestination(sc_pos.x(),sc_pos.y())    #设置终点
            self.w_edge_.update()
        except:pass
        
    def socket_mouse_release(self,socket,event):
        """事件调度-socket"""
        try:
            self.scene.removeItem(self.w_edge_)
            self.w_edge_ = None
        except:pass
    #endregion
    
    def runBlueprint(self):
        """运行节点蓝图函数"""
        sockets = self.getAllSocket()
        key = None
        for socket in sockets:
            index = self.getSocketIndex(socket)
            direction = self.getSocketDirection(index)
            if direction == VALUE_OUTPUT:
                key = index
                break
        #根据key获取edge
        try:
            for i in self.w_edges[key]:
                edge = i[0]
                new_node = edge.getNewNode(self)
                new_node.runBlueprint()
        except:pass

    def getAttributeList(self):
        """获取节点的属性列表"""
        data = {}
        data['node_name'] = self.getNodeTitleName()
        data['node_uuid'] = self.uuid
        data['node_socket'] = self.socket_num
        return data
    
    #region 序列化
    def dump(self):
        """保存"""
        data_edges = {}#所有插槽的所有线
        for key in self.w_edges:
            data_edge={}#一个插槽的所有线
            data_edge_={}#{edge,开始还是结尾}
            a=0
            for i in self.w_edges[key]:
                edge = i[0]
                data_edge_[0] = edge.dump()
                data_edge_[1] = {'source':i[1]}
                data_edge[a] = data_edge_.copy()
                a=a+1
                
            data_edges[key] = data_edge.copy()
        data = {'uuid':self.uuid,
                'new_socket_num':self.new_socket_num,
                'w_node':self.w_node.dump(),
                'data_edges':data_edges,
                }
        return data
    def load(self,obj):
        """加载"""
        self.uuid = obj['uuid']
        self.new_socket_num = obj['new_socket_num']
        data = obj['w_node']
        self.w_node.load(data)
        self.json = obj#存储序列化json
        
        return
    def load_edge(self,obj):
        """加载连线"""
        data = obj['data_edges']
        for key in data:#这个key表示线的socket位置编号
            for key2 in data[key]:#这个key表示一个socket上面多个连线
                edge_node0 = data[key][key2]['0']['edge_node0']
                edge_node1 = data[key][key2]['0']['edge_node1']
                edge_uuid = data[key][key2]['0']['edge_uuid']
                if edge_node0 == self.uuid:
                    edge_node = edge_node1#取出另一个节点的uuid
                elif edge_node1 == self.uuid:
                    edge_node = edge_node0#取出另一个节点的uuid
                else:
                    print("反序列化时连接线未知错误")
                new_node = self.scene.getNodeByUUID(edge_node)
                mysocket = self.getAllSocket()[int(key)]#取出socket
                for i in new_node.json['data_edges']:
                    for n in new_node.json['data_edges'][i]:
                        try:
                            new_edge_uuid = new_node.json['data_edges'][i][n]['0']['edge_uuid']
                        except:new_edge_uuid = 0
                        if edge_uuid == new_edge_uuid:
                            new_socket = new_node.getAllSocket()[int(i)]#取出socket
                            try:
                                self.node_connection(mysocket,new_socket,new_node)
                            except:pass
    #endregion

class BP_Node_BeginPlay(BP_NodeBase):
    def __init__(self,scene=None):
        super().__init__(scene)
        self.setNodeTitleName("BeginPlay")
        self.setNodeTitleColor("#ff8e1214")
        self.setNewSocketNum(0)
    
    def addDemoSocket(self):
        """测试代码-添加默认插槽"""
        self.addSocket(0,1,0)#逻辑
    
    def runBlueprint(self):
        """运行节点蓝图函数"""
        super().runBlueprint()

class BP_Node_PrintString(BP_NodeBase):
    def __init__(self,scene=None):
        super().__init__(scene)
        self.setNodeTitleName("PrintString")
        self.setNodeTitlePix(1)
        self.setNewSocketNum(1)
    
    def addDemoSocket(self):
        """测试代码-添加默认插槽"""
        self.addSocket(0,0,0)#逻辑
        self.addSocket(0,1,0)#逻辑
        s1 = self.addSocket(3,0,1)#字符串
        s1.setSocketText('String')
    
    def runBlueprint(self):
        """运行节点蓝图函数"""
        super().runBlueprint()

class BP_Node_Branch(BP_NodeBase):
    def __init__(self,scene=None):
        super().__init__(scene)
        self.setNodeTitleName("Branch")
        self.setNodeTitleColor("#808080")
        self.setNewSocketNum(3)
    
    def addDemoSocket(self):
        """测试代码-添加默认插槽"""
        self.addSocket(0,0,0)#逻辑
        s0 = self.addSocket(2,0,1)#布尔
        s0.setSocketText('Condition')
        s1 = self.addSocket(0,1,0)#逻辑
        s1.setSocketText('True')
        s2 = self.addSocket(0,1,0)#逻辑
        s2.setSocketText('False')
    
    def runBlueprint(self):
        """运行节点蓝图函数"""
        super().runBlueprint()

class BP_Node_ForLoop(BP_NodeBase):
    def __init__(self,scene=None):
        super().__init__(scene)
        self.setNodeTitleName("ForLoop")
        self.setNodeTitleColor("#808080")
        self.setNewSocketNum(3)
    
    def addDemoSocket(self):
        """测试代码-添加默认插槽"""
        self.addSocket(0,0,0)#逻辑
        s0 = self.addSocket(1,0,1)#整数
        s0.setSocketText('First Index')
        s1 = self.addSocket(1,0,1)#整数
        s1.setSocketText('Last Index')
        
        s2 = self.addSocket(0,1,0)#逻辑
        s2.setSocketText('Loop Body')
        s3 = self.addSocket(1,1,1)#整数
        s3.setSocketText('Index')
        s4 = self.addSocket(0,1,0)#逻辑
        s4.setSocketText('Completed')
    
    def runBlueprint(self):
        """运行节点蓝图函数"""
        super().runBlueprint()

class BP_Node_IntToString(BP_NodeBase):
    def __init__(self,scene=None):
        super().__init__(scene)
        self.setNodeTitleName("IntToString")
        self.setNodeTitlePix(2)
        self.setNodeTitleColor("#4d804d")
        self.setNewSocketNum(1)
    
    def addDemoSocket(self):
        """测试代码-添加默认插槽"""
        s0 = self.addSocket(1,0,1)#整数
        s0.setSocketText('Int')
        s1 = self.addSocket(3,1,1)#字符串
        s1.setSocketText('String')
    
    def runBlueprint(self):
        """运行节点蓝图函数"""
        super().runBlueprint()

class BP_Node(BP_NodeBase):
    def __init__(self,scene=None):
        super().__init__(scene)
        self.setNodeTitleName("NewNode")
        self.setNodeTitlePix(1)
        self.setNewSocketNum(1)
    
    def addDemoSocket(self):
        """测试代码-添加默认插槽"""
        self.addSocket(0,0,0)#逻辑
        self.addSocket(0,1,0)#逻辑