#样式工具
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

FilePath = __file__[:-12]#带斜杠

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

TranslationWidgetButton = "QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\
                                QPushButton:hover { background-color: rgb(40, 44, 52); border-style: solid; border-radius: 4px; }\
                                QPushButton:pressed { background-color: rgb(23, 26, 30); border-style: solid; border-radius: 4px; }"

CodeACcompleter = 'QWidget{background-color: rgb(33, 37, 43);\
            color: rgb(221, 221, 221);\
	        font: 10pt "Segoe UI";}\
            QScrollBar:horizontal {\
    border: none;\
    background: rgb(52, 59, 72);\
    height: 8px;\
    margin: 0px 21px 0 21px;\
	border-radius: 0px;\
}\
QScrollBar::handle:horizontal {\
    background: rgb(189, 147, 249);\
    min-width: 25px;\
	border-radius: 4px\
}\
QScrollBar::add-line:horizontal {\
    border: none;\
    background: rgb(55, 63, 77);\
    width: 20px;\
	border-top-right-radius: 4px;\
    border-bottom-right-radius: 4px;\
    subcontrol-position: right;\
    subcontrol-origin: margin;\
}\
QScrollBar::sub-line:horizontal {\
    border: none;\
    background: rgb(55, 63, 77);\
    width: 20px;\
	border-top-left-radius: 4px;\
    border-bottom-left-radius: 4px;\
    subcontrol-position: left;\
    subcontrol-origin: margin;\
}\
QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\
{\
     background: none;\
}\
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\
{\
     background: none;\
}\
 QScrollBar:vertical {\
	border: none;\
    background: rgb(52, 59, 72);\
    width: 8px;\
    margin: 21px 0 21px 0;\
	border-radius: 0px;\
 }\
 QScrollBar::handle:vertical {	\
	background: rgb(189, 147, 249);\
    min-height: 25px;\
	border-radius: 4px\
 }\
 QScrollBar::add-line:vertical {\
     border: none;\
    background: rgb(55, 63, 77);\
     height: 20px;\
	border-bottom-left-radius: 4px;\
    border-bottom-right-radius: 4px;\
     subcontrol-position: bottom;\
     subcontrol-origin: margin;\
 }\
 QScrollBar::sub-line:vertical {\
	border: none;\
    background: rgb(55, 63, 77);\
     height: 20px;\
	border-top-left-radius: 4px;\
    border-top-right-radius: 4px;\
     subcontrol-position: top;\
     subcontrol-origin: margin;\
 }\
 QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\
     background: none;\
 }\
 QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\
     background: none;\
 }'
 
QHWUrlWebselectw = 'QWidget {color: rgb(221, 221, 221);\
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

QHoudiniWidgetStyle = "#QHoudiniWidget { background-color: rgb(44, 49, 57); border: none;  border-radius: 5px; }\
                             #QHoudiniWidget:hover { background-color: rgb(44, 49, 57); border: 2px solid rgb(52, 59, 72); border-radius: 4px; }"

HoudiniStoreScrollAreaStyle = "#HoudiniStoreScrollArea {background-color: rgb(33, 37, 43);}"

HoudiniStoreAssetWidgetStyle = "#HoudiniStoreAssetWidget {background-color: rgb(38, 38, 38);\
    padding-left: 10px;\
    border: 10px solid rgb(33, 37, 43);}"

HoudiniStoreAssetShoppingTrolleyWidgetButton = "QPushButton { background-color: #dca100; border: none;color: #000000;font-size: 12px;padding-left: 6px;padding-right: 6px;}\
                                        QPushButton:hover { background-color: #ffbb00; border-style: solid;color: #000000;font-size: 12px;padding-left: 6px;padding-right: 6px;}\
                                        QPushButton:pressed { background-color: #dca100; border-style: solid;color: #000000;font-size: 12px;padding-left: 6px;padding-right: 6px;}"

HoudiniStoreTopWidgetButton = "QPushButton { background-color: #00000000; border: none;color: #f3f3f3;font-family: SimHei;font-size: 16px;padding-left: 9.6px;padding-right: 9.6px;padding-top: 16px;padding-bottom: 16px;}\
                                        QPushButton:hover { background-color: rgb(44, 49, 57); border: none;color: #f3f3f3;font-family: SimHei;font-size: 16px;padding-left: 9.6px;padding-right: 9.6px;padding-top: 16px;padding-bottom: 16px;}\
                                        QPushButton:pressed { background-color: rgb(44, 49, 57); border: none;color: #f3f3f3;font-family: SimHei;font-size: 16px;padding-left: 9.6px;padding-right: 9.6px;padding-top: 16px;padding-bottom: 16px;}"

HoudiniStoreTopWidget_edit = "#HoudiniStoreTopWidgetLineEdit {background-color: rgb(33, 37, 43);\
                                    border: 2px solid rgb(44, 49, 57);\
                                    color: #f3f3f3;font-size: 16px;}"