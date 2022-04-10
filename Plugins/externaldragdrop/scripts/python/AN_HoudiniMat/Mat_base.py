#coding:utf-8
import hou

def connect(nodeA,nodeB,port):
    nodeB.setInput(port,nodeA)

class texMap(object):
    def __init__(self,parent = None,name = None,path = None,space = None):
        self.path = path
        self.colorSpace = space
        self.name = name
        self.parent = parent
        self.node = None
        self.type = None

    def createNode(self):
        if self.name == None:
            self.node = self.parent.createNode(self.type)
        else:
            self.node = self.parent.createNode(self.type,self.name)

    def create(self):
        pass

    def connectTo(self,node,port):
        connect(self.node,node,port)

class material(object):
    def __init__(self):
        self.diffuseMap = None
        self.specularMap = None
        self.roughnessMap = None
        self.glossMap = None
        self.metalMap = None
        self.normalMap = None
        self.bumpMap = None
        self.displacementMap = None
        self.aoMap = None
        self.emissionMap = None
        self.opacityMap = None
        self.sssColorMap = None
        self.sssStrengthMap = None
        self.anisotropyMap = None
        self.anisotropy_rotMap = None
        

        self.diffuseNode = None
        self.specularNode = None
        self.roughnessNode = None
        self.glossNode = None
        self.metalNode = None
        self.normalNode = None
        self.bumpNode = None
        self.displacementNode = None
        self.aoNode = None
        self.emissionNode = None
        self.opacityNode = None
        self.sssColorNode = None
        self.sssStrengthNode = None
        self.anisotropyNode = None
        self.anisotropy_rotNode = None
        

        self.bumpScale = 1.0
        self.displacementAmount = 0.1
        self.name = None
        self.path = None
        self.mainMat = None

    def update(self):
        if not self.path.endswith("/"):
            self.path += "/"  
        node = hou.node(self.path+self.name)
        if node != None:
            node.cook()

    def removeSameNode(self):
        if not self.path.endswith("/"):
            self.path += "/"  
        node = hou.node(self.path+self.name)
        if node != None:
            node.destroy()

    def create(self):
        pass

