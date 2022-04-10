#coding:utf-8
import os
import collections


def createMaps():
    maps = collections.OrderedDict()
    maps["diff"] = "diffuseMap"
    maps["_col"] = "diffuseMap"
    maps["basecolor"] = "diffuseMap"
    maps["roughness"] = "roughnessMap"
    maps["spec"] = "specularMap"
    maps["_refl"] = "specularMap"
    maps["gloss"] = "glossMap"
    maps["metallic"] = "metalMap"
    maps["normal"] = "normalMap"
    maps["_nrm"] = "normalMap"
    maps["bump"] = "bumpMap"
    maps["disp"] = "displacementMap"
    maps["emission"] = "emissionMap"
    maps["opacity"] = "opacityMap"
    maps["alpha"] = "opacityMap"
    maps["mask"] = "opacityMap"
    maps["rough"] = "roughnessMap"
    maps["nor"] = "normalMap"
    maps["height"] = "displacementMap"
    maps["depth"] = "displacementMap"
    maps["ao"] = "aoMap"
    maps["_overlay"] = "aoMap"
    maps["occlusion"] = "aoMap"
    maps["anisotropy_l"] = "anisotropyMap" 
    maps["anisotropy_a"] = "anisotropy_rotMap" 
    maps["anisotropy_r"] = "anisotropy_rotMap" 
    maps["sss"] = "sssStrengthMap" 
    maps["metal"] = "metalMap"
    maps["emit"] = "emissionMap"
    return maps

def setTex(mat,name,tex):
    if name == "diffuseMap":
        mat.diffuseMap = tex
    elif name == "roughnessMap":
        mat.roughnessMap = tex
    elif name == "specularMap":
        mat.specularMap = tex
    elif name == "glossMap":
        mat.glossMap = tex
    elif name == "metalMap":
        mat.metalMap = tex
    elif name == "normalMap":
        mat.normalMap = tex
    elif name == "bumpMap":
        mat.bumpMap = tex
    elif name == "displacementMap":
        mat.displacementMap = tex
    elif name == "emissionMap":
        mat.emissionMap = tex
    elif name == "opacityMap":
        mat.opacityMap = tex
    elif name == "aoMap":
        mat.aoMap = tex
    elif name == "anisotropyMap":
        mat.anisotropyMap = tex
    elif name == "anisotropy_rotMap":
        mat.anisotropy_rotMap = tex
    elif name == "sssStrengthMap":
        mat.sssStrengthMap = tex


def createFromFolder(mat,folderPath):
    path = folderPath.replace("\\","/")
    if not path.endswith("/"):
        path += "/"

    if not os.path.exists(folderPath):
        print("Folder dose not exist!!!")
        return

    files = os.listdir(path)
    
    count = 0
    for k,v in createMaps().items():
        for file in files:
            if k in file.lower():
                tex = path + file
                setTex(mat,v,tex)
                count += 1
                if count >= len(files):
                    return
                break
