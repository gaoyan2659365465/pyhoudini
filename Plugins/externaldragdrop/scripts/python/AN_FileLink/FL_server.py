#coding:utf-8
import os
import hou
import socket
import SocketServer
from FL_utils import *
from globalvar import get_value
from PySide2.QtCore import QThread


def evalMessage(message):
    data = message.split("#")
    tp = data[0]
    data.remove(data[0])
    message = "#".join(data)

    if tp == "mesh":
        importMesh()
        print("Import Mesh from " + message)
    elif tp == "tex":
        importTex(message)
        print("Import materials from substance painter")

class myServer(SocketServer.BaseRequestHandler):
    def handle(self):
        while True:
            data=self.request.recv(1024).decode("utf-8")
            if not data:
                continue
            else:
                evalMessage(data)

class bgServer(QThread):
    def __init__(self):
        super(bgServer,self).__init__()
        self.server = None
        
    def stop(self):
        try:
            self.server.shutdown()
            self.server.close()
        except:
            pass

    def remove(self):
        self.stop()
        try:
            self.quit()
            #self.wait()
            self.destroyed()
        except:
            pass

    def run(self):
        try:
            print("Start File Link Server")
            self.server = SocketServer.ThreadingTCPServer(("localhost",get_value("myPort")),myServer)
            self.server.serve_forever()
        except:
            pass
            #print("Port has been used")

class bgExport(QThread):
    def __init__(self):
        super(bgExport,self).__init__()
        self.targetSoftware = None

    def setPort(self,port):
        self.client = socket.socket()
        try:
            self.client.connect(("localhost",port))
            return True
        except:
            print("Can not connect to " + self.targetSoftware)
            return False

    def setTargetSoftware(self,software):
        self.targetSoftware = software

    def remove(self):
        try:
            self.client.close()
            self.quit()
            self.wait()
            self.destroyed()
        except:
            pass

    def export(self):
        nodes = hou.selectedNodes()
        if len(nodes) > 0:
            node = nodes[0]
            if node.type().name() == "geo":
                exportMesh(node.displayNode())
            elif node.type().category().name() == "Sop":
                exportMesh(node)
        else:
            print("No Sop Node Selected!!!")

    def run(self):
        if self.setPort(get_value("ports")[self.targetSoftware]):
            msg = "mesh#Houdini"
            self.export()
            self.client.send(msg.encode("utf-8"))

