# -*- coding: utf-8 -*-

__name__ = 'BlueprintEditor'
__author__ = '柯哀的眼'
__version__ = '0.1'

import sys
path = __file__[:-11]
path2 = path[:-9]
sys.path.append(path2)#C:\Users\26593\Desktop\pyhoudini\blueprintdemo\
sys.path.append(path)#C:\Users\26593\Desktop\pyhoudini\blueprintdemo\examples

from  .BP_Window import *
from  .W_Attributes import *
from  .W_ScrollArea import *
#----------------------------------
from  .Node.W_View import *
from  .Node.W_Edge import *
from  .Node.W_Scene import *
from  .Node.BP_Json import *
from  .Node.W_NodeBase import *
from  .Node.W_TitleBase import *
from  .Node.BP_NodeBase import *
from  .Node.W_DockWidget import *
from  .Node.W_SocketBase import *
from  .Node.W_NodeContent import *
from  .Node.W_SocketContent import *
from  .Node.W_SearchNodeBase import *
from  .Node.BP_SearchNodeBase import *

#----------------------------------
from  .Plugins.Plugins import *

"""
BP_Window程序的开始入口
    W_DockWidget各个悬浮窗
        W_View视口类负责显示网格、缩放
        W_Scene场景类负责处理场景中逻辑
            BP_NodeBase节点的抽象基类
                W_NodeBase节点的界面基类
                    W_TitleBase节点的标题栏
                    W_NodeContent节点内容
                        W_SocketContent节点插槽(端口、文字、输入控件)
                            W_SocketBase节点连接端小圆圈
            W_Edge节点之间连接线类
            BP_SearchNodeBase鼠标右键搜索抽象类
                W_SearchNodeBase鼠标右键搜索界面类
        W_Attributes属性栏
            W_ScrollArea滚动条窗口
"""