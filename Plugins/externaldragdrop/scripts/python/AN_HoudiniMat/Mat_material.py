#coding:utf-8
from AN_HoudiniMat.Mat_base import *
import hou

nets = ["shop","shopnet","mat","matnet"]

#============redshift===============

class rsTexture(texMap):
    def __init__(self,parent,name = None,path = None,space = None):
        super(rsTexture,self).__init__(parent,name,path,space)
        self.type = "redshift::TextureSampler"
        self.create()

    def create(self):
        self.createNode()
        if self.path != None:
            self.node.parm("tex0").set(self.path)

        self.node.parm("tex0_gammaoverride").set(1)

        if self.colorSpace != "linear":
            self.node.parm("tex0_srgb").set(1)

        return self.node   

class rsMaterial(material):
    def __init__(self,name = None):
        super(rsMaterial,self).__init__()

        self.name = "redshift_vopnet"
        if name != None:
            self.name = name
        self.path = "/shop/"

    def create(self):
        parentNode = hou.node(self.path)
        tpName = parentNode.type().name()
        if  not tpName in nets:
            print("Create path Error!!!")
            return
        matVop = parentNode.createNode("redshift_vopnet",self.name)
        matVop.moveToGoodPosition()
        root = matVop.children()[0]
        mat = matVop.createNode("Material")
        connect(mat,root,0)
        mat.parm("refl_brdf").set("1") #GGX
        self.mainMat = mat

        if self.diffuseMap != None:
            self.diffuseNode = rsTexture(matVop,"difuseMap",self.diffuseMap,"srgb")
            self.diffuseNode.connectTo(mat,0)

        if self.specularMap != None:
            self.specularNode = rsTexture(matVop,"specularMap",self.specularMap,"linear")
            self.specularNode.connectTo(mat,6)
        
        if self.glossMap != None:
            self.glossNode = rsTexture(matVop,"glossMap",self.glossMap,"linear")
            self.glossNode.connectTo(mat,7)
            mat.parm("refl_isGlossiness").set(1)

        if self.roughnessMap != None:
            self.roughnessNode = rsTexture(matVop,"roughnessMap",self.roughnessMap,"linear")
            self.roughnessNode.connectTo(mat,7)
            mat.parm("refl_isGlossiness").set(0)

        if self.metalMap != None:
            self.metalNode = rsTexture(matVop,"metalMap",self.metalMap,"linear")
            self.metalNode.connectTo(mat,14)
            mat.parm("refl_fresnel_mode").set("2")

        if "metal" in self.name.lower():
            mat.parm("refl_fresnel_mode").set("2")
            mat.parm("refl_metalness").set(1)

        if "ice" in self.name.lower() or "glass" in self.name.lower():
            mat.parm("refr_weight").set(1)
            if self.diffuseMap != None:
                self.diffuseNode.connectTo(mat,16)

        if self.bumpMap != None:
            self.bumpNode = rsTexture(matVop,"bumpMap",self.bumpMap,"linear")
            self.bump = matVop.createNode("BumpMap","BumpMap")
            self.bump.setParms({"scale":self.bumpScale})
            self.bumpNode.connectTo(self.bump,0)
            connect(self.bump,mat,49)
            
        if self.normalMap != None:
            self.normalNode = matVop.createNode("NormalMap","normalMap")
            self.normalNode.setParms({"tex0":self.normalMap,"scale":self.bumpScale})
            connect(self.normalNode,mat,49)

        if self.normalNode != None and self.bumpNode != None:
            blend = matVop.createNode("redshift::BumpBlender")
            blend.setParms({"additive":1,"bumpWeight0":1})
            connect(self.normalNode,blend,0)
            connect(self.bump,blend,1)
            connect(blend,mat,49)

        if self.aoMap != None:
            self.aoNode = rsTexture(matVop,"aoMap",self.aoMap,"linear")
            if self.diffuseNode != None:
                self.aoNode.connectTo(self.diffuseNode.node,3)
            else:
                self.aoNode.connectTo(mat,1)
                
        if self.emissionMap != None:
            self.emissionNode = rsTexture(matVop,"emissionMap",self.emissionMap,"srgb")
            self.emissionNode.connectTo(mat,48)

        if self.opacityMap != None:
            sprite = matVop.createNode("redshift::Sprite")
            sprite.setParms({"tex0":self.opacityMap})
            root.setInput(0,sprite)
            sprite.setInput(0,mat)
        
        if self.displacementMap != None:
            self.displacementNode = rsTexture(matVop,"displacementMap",self.displacementMap,"linear")
            disp = matVop.createNode("redshift::Displacement")
            disp.parm("scale").set(self.displacementAmount)
            self.displacementNode.connectTo(disp,0)
            connect(disp,root,1)
           
        if self.anisotropyMap != None:
            self.anisotropyNode = rsTexture(matVop,"anisotropyMap",self.anisotropyMap,"linear")
            self.anisotropyNode.connectTo(mat,8)

        if self.anisotropy_rotMap != None:
            self.anisotropy_rotNode = rsTexture(matVop,"anisotropy_rotMap",self.anisotropy_rotMap,"linear")
            self.anisotropy_rotNode.connectTo(mat,9)

        if self.sssStrengthMap != None:
            self.sssStrengthNode = rsTexture(matVop,"sssStrengthMap",self.sssStrengthMap,"linear")
            self.sssStrengthNode.connectTo(mat,26)

        if self.sssColorMap != None:
            self.sssColorNode = rsTexture(matVop,"sssColorMap",self.sssColorMap,"srgb")
            self.sssColorNode.connectTo(mat,25)

        matVop.layoutChildren()
        



#============arnold===============

class arTexture(texMap):
    def __init__(self,parent,name = None,path = None,space = None):
        super(arTexture,self).__init__(parent,name,path,space)
        self.type = "arnold::image"
        self.create()

    def create(self):
        self.createNode()
        if self.path != None:
            self.node.parm("filename").set(self.path)

        self.node.parm("color_space").set("linear")
        self.node.parm("ignore_missing_textures").set(1)

        if self.colorSpace != "linear":
            self.node.parm("color_space").set("sRGB")

        return self.node   

class arMaterial(material):
    def __init__(self,name = None):
        super(arMaterial,self).__init__()

        self.name = "arnold_vopnet"
        if name != None:
            self.name = name
        self.path = "/shop/"

    def create(self):
        parentNode = hou.node(self.path)
        tpName = parentNode.type().name()

        if  not tpName in nets:
            print("Create path Error!!!")
            return

        if "shop" in tpName:
            matVop = parentNode.createNode("arnold_vopnet",self.name)
            root = matVop.children()[0]
        else:
            matVop = parentNode
            root = parentNode.createNode("arnold_material",self.name)

        matVop.moveToGoodPosition()
        mat = matVop.createNode("arnold::standard_surface")
        connect(mat,root,0)
        self.mainMat = mat

        if self.diffuseMap != None:
            self.diffuseNode = arTexture(matVop,"difuseMap",self.diffuseMap,"srgb")
            self.diffuseNode.connectTo(mat,1)

        if self.specularMap != None:
            self.specularNode = arTexture(matVop,"specularMap",self.specularMap,"linear")
            self.specularNode.connectTo(mat,4)
        
        if self.glossMap != None:
            self.glossNode = arTexture(matVop,"glossMap",self.glossMap,"linear")
            substract = matVop.createNode("arnold::subtract")
            substract.parmTuple("input1").set((1,1,1))
            self.glossNode.connectTo(substract,1)
            connect(substract,mat,6)

        if self.roughnessMap != None:
            self.roughnessNode = arTexture(matVop,"roughnessMap",self.roughnessMap,"linear")
            self.roughnessNode.connectTo(mat,6)


        if self.metalMap != None:
            self.metalNode = arTexture(matVop,"metalMap",self.metalMap,"linear")
            self.metalNode.connectTo(mat,3)
        
        if "metal" in self.name.lower():
            mat.parm("metalness").set(1)

        if "ice" in self.name.lower() or "glass" in self.name.lower():
            mat.parm("transmission").set(1)
            if self.diffuseMap != None:
                self.diffuseNode.connectTo(mat,12)

        if self.bumpMap != None:
            self.bumpNode = arTexture(matVop,"bumpMap",self.bumpMap,"linear")
            self.bump = matVop.createNode("arnold::bump2d")
            self.bump.setParms({"bump_height":self.bumpScale})
            self.bumpNode.connectTo(self.bump,0)
            connect(self.bump,mat,39)
            
        if self.normalMap != None:
            self.normalNode = arTexture(matVop,"normalMap",self.normalMap,"linear")
            self.normal = matVop.createNode("arnold::normal_map")
            self.normal.setParms({"strength":self.bumpScale})
            self.normalNode.connectTo(self.normal,0)
            connect(self.normal,mat,39)

        if self.aoMap != None:
            self.aoNode = arTexture(matVop,"aoMap",self.aoMap,"linear")
            if self.diffuseNode != None:
                self.aoNode.connectTo(self.diffuseNode.node,1)
        
        if self.emissionMap != None:
            self.emissionNode = arTexture(matVop,"emissionMap",self.emissionMap,"srgb")
            self.emissionNode.connectTo(mat,36)

        if self.opacityMap != None:
            self.opacityNode = arTexture(matVop,"opacityMap",self.opacityMap,"linear")
            self.opacityNode.connectTo(mat,38)
        
        if self.displacementMap != None:
            self.displacementNode = arTexture(matVop,"displacementMap",self.displacementMap,"linear")
            disp = matVop.createNode("arnold::vector_map")
            disp.parm("scale").set(self.displacementAmount)
            self.displacementNode.connectTo(disp,0)
            connect(disp,root,1)
           
        if self.anisotropyMap != None:
            self.anisotropyNode = arTexture(matVop,"anisotropyMap",self.anisotropyMap,"linear")
            self.anisotropyNode.connectTo(mat,8)

        if self.anisotropy_rotMap != None:
            self.anisotropy_rotNode = arTexture(matVop,"anisotropy_rotMap",self.anisotropy_rotMap,"linear")
            self.anisotropy_rotNode.connectTo(mat,9)

        if self.sssStrengthMap != None:
            self.sssStrengthNode = arTexture(matVop,"sssStrengthMap",self.sssStrengthMap,"linear")
            self.sssStrengthNode.connectTo(mat,17)

        if self.sssColorMap != None:
            self.sssColorNode = arTexture(matVop,"sssColorMap",self.sssColorMap,"srgb")
            self.sssColorNode.connectTo(mat,18)

        matVop.layoutChildren()



#============octane===============

class orTexture(texMap):
    def __init__(self,parent,name = None,path = None,space = None):
        super(orTexture,self).__init__(parent,name,path,space)
        if self.colorSpace == "srgb":
            self.type = "octane::NT_TEX_IMAGE"
        elif self.colorSpace == "linear":
            self.type = "octane::NT_TEX_FLOATIMAGE"
        elif self.colorSpace == "linear":
            self.type = "octane::NT_TEX_FLOATIMAGE"

        self.create()

    def create(self):
        self.createNode()
        if self.path != None:
            self.node.parm("A_FILENAME").set(self.path)

        self.node.parm("A_RELOAD").set(1)

        if self.colorSpace == "linear":
            self.node.parm("gamma").set(1)

        return self.node   

class orMaterial(material):
    def __init__(self,name = None):
        super(orMaterial,self).__init__()

        self.name = "octane_vopnet"
        if name != None:
            self.name = name
        self.path = "/shop/"

    def create(self):
        parentNode = hou.node(self.path)
        tpName = parentNode.type().name()
        if  not tpName in nets:
            print("Create path Error!!!")
            return
        matVop = parentNode.createNode("octane_vopnet",self.name)
        matVop.moveToGoodPosition()
        root = matVop.children()[0]
        mat = matVop.createNode("octane::NT_MAT_UNIVERSAL")
        connect(mat,root,0)
        self.mainMat = mat
    
        if self.diffuseMap != None:
            self.diffuseNode = orTexture(matVop,"difuseMap",self.diffuseMap,"srgb")
            self.diffuseNode.connectTo(mat,1)

        if self.specularMap != None:
            self.specularNode = orTexture(matVop,"specularMap",self.specularMap,"linear")
            self.specularNode.connectTo(mat,4)
        
        if self.glossMap != None:
            self.glossNode = orTexture(matVop,"glossMap",self.glossMap,"linear")
            invert = matVop.createNode("octane::NT_TEX_INVERT")
            self.glossNode.connectTo(invert,0)
            connect(invert,mat,5)

        if self.roughnessMap != None:
            self.roughnessNode = orTexture(matVop,"roughnessMap",self.roughnessMap,"linear")
            self.roughnessNode.connectTo(mat,5)



        if self.metalMap != None:
            self.metalNode = orTexture(matVop,"metalMap",self.metalMap,"linear")
            self.metalNode.connectTo(mat,2)

        if "metal" in self.name.lower():
            mat.parm("metallic").set(1)

        if self.bumpMap != None:
            self.bumpNode = orTexture(matVop,"bumpMap",self.bumpMap,"linear")
            self.bumpNode.connectTo(mat,30)
            self.bumpNode.node.parm("power").set(self.bumpScale)

        if self.normalMap != None:
            self.normalNode = orTexture(matVop,"normalMap",self.normalMap,"srgb")
            self.normalNode.connectTo(mat,31)
            self.normalNode.node.parm("gamma").set(1)
            self.normalNode.node.parm("power").set(self.bumpScale)

        if self.aoMap != None:
            self.aoNode = orTexture(matVop,"aoMap",self.aoMap,"linear")
            if self.diffuseNode != None:
                self.aoNode.connectTo(self.diffuseNode.node,0)
        
        if self.emissionMap != None:
            self.emissionNode = orTexture(matVop,"emissionMap",self.emissionMap,"srgb")
            self.emissionNode.connectTo(mat,35)

        if self.opacityMap != None:
            self.opacityNode = orTexture(matVop,"opacityMap",self.opacityMap,"linear")
            self.opacityNode.connectTo(mat,27)
        
        if self.displacementMap != None:
            self.displacementNode = orTexture(matVop,"displacementMap",self.displacementMap,"linear")
            disp = matVop.createNode("octane::NT_DISPLACEMENT")
            disp.parm("amount").set(self.displacementAmount)
            self.displacementNode.connectTo(disp,0)
            connect(disp,mat,32)
           
        if self.anisotropyMap != None:
            self.anisotropyNode = orTexture(matVop,"anisotropyMap",self.anisotropyMap,"linear")
            self.anisotropyNode.connectTo(mat,6)

        if self.anisotropy_rotMap != None:
            self.anisotropy_rotNode = orTexture(matVop,"anisotropy_rotMap",self.anisotropy_rotMap,"linear")
            self.anisotropy_rotNode.connectTo(mat,7)

        medium = None
        if self.sssStrengthMap != None:
            # medium = matVop.createNode("octane::NT_MED_SCATTERING")
            # connect(medium,mat,26)
            self.sssStrengthNode = orTexture(matVop,"sssStrengthMap",self.sssStrengthMap,"linear")
            #self.sssStrengthNode.connectTo(medium,0)

        if self.sssColorMap != None:
            # if medium == None:
            #     medium = matVop.createNode("octane::NT_MED_SCATTERING")
            #     connect(medium,mat,26)
            self.sssColorNode = orTexture(matVop,"sssColorMap",self.sssColorMap,"srgb")
            #self.sssColorNode.connectTo(medium,4)
            self.sssColorNode.connectTo(mat,0)
            if self.sssStrengthNode != None:
                self.sssStrengthNode.connectTo(self.sssColorNode.node,0)

        matVop.layoutChildren()



#============mantra===============

class mrMaterial(material):
    def __init__(self,name = None):
        super(mrMaterial,self).__init__()

        self.name = "principledshader"
        if name != None:
            self.name = name
        self.path = "/shop/"

    def create(self):
        parentNode = hou.node(self.path)
        tpName = parentNode.type().name()
        if  not tpName in nets:
            print("Create path Error!!!")
            return

        if "shop" in tpName:
            mat = parentNode.createNode("principledshader",self.name)
            idx = 0
        else:
            mat = parentNode.createNode("principledshader::2.0",self.name)
            idx = 1

        mat.moveToGoodPosition()
        self.mainMat = mat

        if self.diffuseMap != None:
            mat.setParms({"basecolor_useTexture":1,"basecolor_texture":self.diffuseMap})

        if self.specularMap != None:
            mat.setParms({"reflect_useTexture":1,"reflect_texture":self.specularMap})
        
        if self.glossMap != None:
            mat.setParms({"rough_useTexture":1,"rough_texture":self.glossMap})

        if self.roughnessMap != None:
            mat.setParms({"rough_useTexture":1,"rough_texture":self.roughnessMap})

        if self.metalMap != None:
            mat.setParms({"metallic_useTexture":1,"metallic_texture":self.metalMap})

        if "metal" in self.name.lower():
            mat.parm("metallic").set(1)

        if self.bumpMap != None:
            if idx == 0:
                mat.setParms({"enableBumpOrNormalTexture":1,"normalTexture":self.bumpMap,
                "normalTexScale":self.bumpScale,"normalTexType":"bump"})
            else:
                mat.setParms({"baseBumpAndNormal_enable":1,"baseBump_bumpTexture":self.normalMap,
                "baseBump_bumpScale":self.bumpScale,"baseBumpAndNormal_type":"bump"})
            
        if self.normalMap != None:
            if idx == 0:
                 mat.setParms({"enableBumpOrNormalTexture":1,"normalTexture":self.normalMap,
                "normalTexScale":self.bumpScale,"normalTexType":"normal"})
            else:
                mat.setParms({"baseBumpAndNormal_enable":1,"baseNormal_texture":self.normalMap,
                "baseNormal_scale":self.bumpScale,"baseBumpAndNormal_type":"normal"})
               

        if self.aoMap != None:
            pass
        
        if self.emissionMap != None:
            mat.setParms({"emitcolor_useTexture":1,"emitcolor_texture":self.emissionMap})

        if self.opacityMap != None:
            if idx == 0:
                mat.setParms({"ogl_opacitymap":self.opacityMap})
            else:
                mat.setParms({"opaccolor_useTexture":1,"opaccolor_texture":self.opacityMap})
        
        if self.displacementMap != None:
            if idx == 0:
                mat.setParms({"enableDispTexture":1,"dispTexTexture":self.displacementMap,
                "dispTexScale":self.displacementAmount})
            else:
                mat.setParms({"dispTex_enable":1,"dispTex_texture":self.displacementMap,
                "dispTex_scale":self.displacementAmount})
           
        if self.anisotropyMap != None:
            mat.setParms({"aniso_useTexture":1,"aniso_texture":self.anisotropyMap})

        if self.anisotropy_rotMap != None:
            mat.setParms({"anisodir_useTexture":1,"anisodir_texture":self.anisotropy_rotMap})

        if self.sssStrengthMap != None:
            if idx == 0:
                mat.setParms({"subsurface_useTexture":1,"subsurface_texture":self.sssStrengthMap})
            else:
                mat.setParms({"sss_useTexture":1,"sss_texture":self.sssStrengthMap})

        if self.sssColorMap != None:
            if idx == 0:
                pass
            else:
                mat.setParms({"ssscolor_useTexture":1,"ssscolor_texture":self.sssColorMap})



#============renderman===============

class rmTexture(texMap):
    def __init__(self,parent,name = None,path = None,space = None):
        super(rmTexture,self).__init__(parent,name,path,space)
        self.type = "pxrtexture"
        self.create()

    def connectTo(self,node,port):
        if self.colorSpace == "linear":
            node.setInput(port,self.node,1)
        else:
            connect(self.node,node,port)

    def create(self):
        self.createNode()
        if self.path != None:
            self.node.parm("filename").set(self.path)

        if self.colorSpace == "linear":
            self.node.parm("linearize").set(1)

        return self.node   

class rmMaterial(material):
    def __init__(self,name = None):
        super(rmMaterial,self).__init__()

        self.name = "risnet"
        if name != None:
            self.name = name
        self.path = "/shop/"

    def create(self):
        parentNode = hou.node(self.path)
        tpName = parentNode.type().name()

        if  not tpName in nets:
            print("Create path Error!!!")
            return

        if "shop" in tpName:
            matVop = parentNode.createNode("risnet",self.name)
            root = matVop.createNode("collect","output_collect")
        else:
            matVop = parentNode.createNode("pxrmaterialbuilder",self.name)
            root = matVop.children()[0]

        matVop.moveToGoodPosition()
        mat = matVop.createNode("pxrdisney")
        connect(mat,root,0)
        self.mainMat = mat

        if self.diffuseMap != None:
            self.diffuseNode = rmTexture(matVop,"difuseMap",self.diffuseMap,"srgb")
            self.diffuseNode.connectTo(mat,0)

        if self.specularMap != None:
            self.specularNode = rmTexture(matVop,"specularMap",self.specularMap,"linear")
            self.specularNode.connectTo(mat,5)

        if self.glossMap != None:
            self.glossNode = rmTexture(matVop,"glossMap",self.glossMap,"linear")
            invert = matVop.createNode("pxrinvert")
            self.glossNode.connectTo(invert,0)
            connect(invert,mat,7)
            
        if self.roughnessMap != None:
            self.roughnessNode = rmTexture(matVop,"roughnessMap",self.roughnessMap,"linear")
            self.roughnessNode.connectTo(mat,7)



        if self.metalMap != None:
            self.metalNode = rmTexture(matVop,"metalMap",self.metalMap,"linear")
            self.metalNode.connectTo(mat,4)

        if "metal" in self.name.lower():
            mat.parm("metallic").set(1)

        if self.bumpMap != None:
            self.bumpNode = matVop.createNode("pxrbump")
            self.bumpNode.setParms({"scale":self.bumpScale,"filename":self.bumpMap})
            connect(self.bumpNode,mat,13)
            
        if self.normalMap != None:
            self.normalNode = matVop.createNode("pxrnormalmap")
            self.normalNode.setParms({"bumpScale":self.bumpScale,"filename":self.normalMap})
            connect(self.normalNode,mat,13)

        if self.aoMap != None:
            self.aoNode = rmTexture(matVop,"aoMap",self.aoMap,"linear")
            if self.diffuseNode != None:
                self.aoNode.connectTo(self.diffuseNode.node,4)
        
        if self.emissionMap != None:
            self.emissionNode = rmTexture(matVop,"emissionMap",self.emissionMap,"srgb")
            self.emissionNode.connectTo(mat,1)

        if self.opacityMap != None:
            self.opacityNode = rmTexture(matVop,"opacityMap",self.opacityMap,"linear")
            self.opacityNode.connectTo(mat,14)
        
        if self.displacementMap != None:
            self.displacementNode = rmTexture(matVop,"displacementMap",self.displacementMap,"linear")
            disp = matVop.createNode("pxrdisplace")
            disp.parm("dispAmount").set(self.displacementAmount)
            self.displacementNode.connectTo(disp,1)
            connect(disp,root,1)
           
        if self.anisotropyMap != None:
            self.anisotropyNode = rmTexture(matVop,"anisotropyMap",self.anisotropyMap,"linear")
            self.anisotropyNode.connectTo(mat,8)

        # if self.anisotropy_rotMap != None:
        #     pass

        if self.sssStrengthMap != None:
            self.sssStrengthNode = rmTexture(matVop,"sssStrengthMap",self.sssStrengthMap,"linear")
            self.sssStrengthNode.connectTo(mat,2)

        if self.sssColorMap != None:
            self.sssColorNode = rmTexture(matVop,"sssColorMap",self.sssColorMap,"srgb")
            self.sssColorNode.connectTo(mat,3)

        matVop.layoutChildren()

