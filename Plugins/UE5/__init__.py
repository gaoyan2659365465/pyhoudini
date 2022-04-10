# -*- coding: utf-8 -*-

__name__ = 'UE5'
__author__ = '柯哀的眼'
__version__ = '0.1'

#此文件由UE5调用
#from UE5.CreateMesh import *

#其中有hou模块需要Houdini运行时才能正常加载
try:
    from UE5.CopyHoudiniNodeData import *
except:pass