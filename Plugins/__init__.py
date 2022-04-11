# -*- coding: utf-8 -*-

__name__ = 'Plugins'
__author__ = '柯哀的眼'
__version__ = '0.1'

import sys
path = __file__[:-11]
sys.path.append(path)

#翻译页面
from Translation import *

#登录页面
from Sign import *

#内容浏览器页面
from ContentBrowser import *

#商店页面
from Stores import *

#UE5链接功能
from UE5 import *

#节点笔记页面
from NodeBook import *

#迷你模式页面
from MiniMode import *

#蓝图页面
from blueprintdemo import *

#版本管理页面
from WesLib import *