#样式工具
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

FilePath = __file__[:-12]

NodeWidgetStyle = "background-color: #282c34;"

NodeWidgetButtonStyle = "QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\
         QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\
         QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }"

HoudiniHelpSetingButton = "QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\
                                        QPushButton:hover { background-color: rgb(44, 49, 57); border-style: solid; border-radius: 4px; }\
                                        QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }"

HoudiniHelpline_edit = "background-color: rgb(33, 37, 43);\
                                     border-radius: 17px;"
                                     
HoudiniHelpselectbutton = "border: none;border-radius: 15px;"

IconsWidgetStyle = "background-color: #282c34;"

def addStyleIcon(button,path):
    """创建Icon"""
    icon0 = QIcon()
    icon0.addFile(u":/icons/images/icons/" + path, QSize(48,48), QIcon.Normal, QIcon.Off)
    button.setIcon(icon0)

MiniWidgetline_edit = 'QWidget {color: rgb(221, 221, 221);\
	                                font: 10pt "Segoe UI";}\
                                    QLineEdit {\
                                    background-color: rgb(33, 37, 43);\
                                    border-radius: 5px;\
                                    border: 2px solid rgb(33, 37, 43);\
                                    padding-left: 10px;\
                                    selection-color: rgb(255, 255, 255);\
                                    selection-background-color: rgb(255, 121, 198);}\
                                    QLineEdit:hover {\
                                        border: 2px solid rgb(64, 71, 88);}\
                                    QLineEdit:focus {\
                                        border: 2px solid rgb(91, 101, 124);}'