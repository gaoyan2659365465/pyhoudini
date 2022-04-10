#coding:utf-8
import os
import json
from AN_HoudiniMat.Mat_material import *

def load_json(file_path):
    file = open(file_path, mode='r')
    data = json.load(file)
    file.close()
    return data

def create(mat,data,name):
    objName = data["objName"]
    path = data["path"]
    fmt = data["format"]
    p = path + "/" + objName + "_" + name + "_"
    diffuse =  p + "BaseColor." + fmt
    rough = p + "Roughness." + fmt
    metal = p + "Metallic." + fmt
    normal = p + "Normal." + fmt

    if os.path.exists(diffuse):
        mat.diffuseMap = diffuse
    if os.path.exists(rough):
        mat.roughnessMap = rough
    if os.path.exists(metal):
        mat.metalMap = metal
    if os.path.exists(normal):
        mat.normalMap = normal

    if data["useAo"]:
        ao = p + "Ao." + fmt
        if os.path.exists(ao):
            mat.aoMap = ao
    if data["useHeight"]:
        height = p + "Height." + fmt
        if os.path.exists(height):
            mat.displacementMap = height
    if data["useOpacity"]:
        opacity = p + "Opacity." + fmt
        if os.path.exists(opacity):
            mat.opacityMap = opacity
    if data["useEmissive"]:
        emissive = p + "Emissive." + fmt
        if os.path.exists(emissive):
            mat.emissionMap = emissive
    if data["useSSS"]:
        sss = p + "SSS." + fmt
        if os.path.exists(sss):
            mat.sssStrengthMap = sss
    if data["useAnisotropy"]:
        al = p + "Anisotropy_Level." + fmt
        aa = p + "Anisotropy_Angle." + fmt
        if os.path.exists(al):
            mat.anisotropyMap = al
        if os.path.exists(aa):
            mat.anisotropy_rotMap = aa
            
    if data["update"]:      
        mat.update()
    else:
        mat.removeSameNode()
        mat.create()

def createMats(json_file,path = "/shop/"):
    data = load_json(json_file)
    renderer = data["renderer"]
    names = data["names"]

    for name in names:
        mat = None
        if renderer == "Redshift":
            mat = rsMaterial(name)
        elif renderer == "Arnold":
            mat = arMaterial(name)
        elif renderer == "Octane":
            mat = orMaterial(name)
        elif renderer == "RenderMan":
            mat = rmMaterial(name)
        elif renderer == "Mantra":
            mat = mrMaterial(name)
        else:
            print("Find unsupported renderer!!")
            return
        mat.path = path
        create(mat,data,name)

    
