#多线程加载图片防止卡顿
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import requests

class ReadWebImages(QThread):
    def __init__(self):
        super().__init__()
        self.image_url = ''
        self.imagelabel = None
        self.mode = 0#0缩放图片，1不缩放图片

    def run(self):
        res = requests.get(self.image_url)
        img = QImage.fromData(res.content)
        if self.mode == 0:
            self.imagelabel.setPixmap(QPixmap.fromImage(img)\
                .scaled(248,248,Qt.IgnoreAspectRatio,Qt.SmoothTransformation))
        elif self.mode == 1:
            self.imagelabel.setPixmap(QPixmap.fromImage(img))
