#coding:utf-8
import os
import shutil
import hou
from globalvar import *
import AN_HoudiniMat as HM

def getJsonPath():
    doc = os.path.expanduser('~')
    doc = doc.replace("\\","/")
    if not doc.endswith("Documents"):
        doc += "/Documents"
    path = doc + "/Allegorithmic/Substance Painter/plugins/an_FileLink/config/export_data.json"
    return path

def getAllPorts():
    ports = {"Cinema 4D" :8801,
             "Blender" : 8802,
             "Houdini" : 8803}
            #  "SP" : 1004,
            #  "SD" : 1005
    return ports

def getMyPort(myName):
    ports = getAllPorts()
    return ports[myName]

def getPorts(myName):
    ports = getAllPorts()
    ports.pop(myName)
    return ports

def initPorts(myName):
    gv_init()
    set_value("myName",myName)
    set_value("myPort",getMyPort(myName))
    set_value("ports",getPorts(myName))
    
def getTempPath():
    tmp = os.environ["temp"]
    path = tmp.split("houdini_temp")[0] + "FileLink/"
    path = path.replace("\\","/")
    return path

def remove(path):
    if os.path.exists(path):
        os.remove(path)

def removeFile(path):
    if not os.path.exists(path):
        return

    ap = open(path + "temp.txt","w")
    ap.write("")
    ap.close()

    path += "modle_temp/"
    if not os.path.exists(path):
        return

    for i in os.listdir(path):
        file = path + i
        try:
            os.remove(file)
        except:
            shutil.rmtree(file)
                
    
def exportMesh(node):
    name = node.name()
    path = getTempPath()
    env = path + "temp.txt"
    removeFile(path)
    path += "modle_temp/"
    mesh = path+name+".fbx"
    
    if not os.path.exists(path):
        os.makedirs(path)
    
    #print os.path.isfile(env)
    fp = open(env,"w")
    fp.write(mesh+"\n" + get_value("myName"))
    fp.close()
    
    fbx_rop = node.createOutputNode('rop_fbx')
    fbx_rop.parm('sopoutput').set(mesh)
    fbx_rop.parm("exportkind").set(0)
    fbx_rop.render()
    fbx_rop.destroy()
    print("Export Mesh Successfully")

def importMesh():
    path = getTempPath()
    env = path + "temp.txt"
    
    ep = open(env,"r")
    geo = ep.readline()
    geo = geo.strip('\n')
    soft = ep.readline()
    ep.close()
    
    name = os.path.basename(geo)
    fmt = name.split(".")[-1]
    name = name.split("."+fmt)[0]
    
    if geo == "":
        print("No file exist!!!")
    else:
        geoNode = None
        try:
            geoNode = hou.node("/obj/").createNode("geo",name)
        except:
            geoNode = hou.node("/obj/").createNode("geo")
            
        file = geoNode.createNode("file")
        file.parm("file").set(geo)
        
        xform = file.createOutputNode("xform")
        stash = None
        try:
            stash = xform.createOutputNode("stash",name)
        except:
            stash = xform.createOutputNode("stash")
            
        if soft == "Blender":
            xform.parm("scale").set(0.005)
        if soft == "Cinema 4D":
            xform.parm("scale").set(0.005)
        if soft == "Substance":
            xform.parm("scale").set(1)
            
        stash.setDisplayFlag(1)
        stash.setRenderFlag(1)    
        stash.parm("stashinput").pressButton()
        if soft == "Substance":
            go = stash.createOutputNode("an_Go_substance_painter")
            go.parm("Group_to_mat").set(0)
            go.setDisplayFlag(1)
            go.setRenderFlag(1)    

        remove(geo)

        if soft=="Substance":
            geo = geo[:-3] + "mtl"
            remove(geo)

        file.destroy()
        xform.destroy()
        
        ap = open(env,"w")
        ap.write("")
        ap.close()


def importTex(json_path = None):
    if json_path != None:
        HM.createMats(json_path)
    else:
        HM.createMats(getJsonPath())
    