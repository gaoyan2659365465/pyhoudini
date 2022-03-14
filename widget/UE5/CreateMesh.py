import unreal
import random
import json
import os

def spawnActor(path,location):
    actor_class = unreal.EditorAssetLibrary.load_asset(path)
    actor_location = unreal.Vector(location[0]*100,location[2]*100,location[1]*100)
    actor_rotation = unreal.Rotator(0,0,0)#0-360
    actor = unreal.EditorLevelLibrary.spawn_actor_from_object(actor_class,actor_location,actor_rotation)
    return actor


def readJson():
    path = __file__[:-13] + "HoudiniNodeData.json"
    if os.path.exists(path) == False:
        return
    try:
        with open(path, 'r',encoding='utf-8') as json_file:
            data = json_file.read()
            result = json.loads(data)
            return result
    except:
        with open(path, 'r',encoding='gbk') as json_file:
            data = json_file.read()
            result = json.loads(data)
            return result

def executeSlowTask():
    data = readJson()#读取json文件
    P = data['P']#获取位置
    quantity_steps_in_slow_task = len(P)#根据有多少个点，循环多少次
    listactor = []
    with unreal.ScopedSlowTask(quantity_steps_in_slow_task,"My Slow Task Text ...") as slow_task:
        slow_task.make_dialog(True)
        for x in range(quantity_steps_in_slow_task):
            if slow_task.should_cancel():
                break
            slow_task.enter_progress_frame(1,"My Slow Task Text ..."+str(x)+'/'+str(quantity_steps_in_slow_task))
            actor = spawnActor(data['meshPath'][x],P[x])
            listactor.append(actor)
    return listactor

#executeSlowTask()


# import sys
# from importlib import reload
# PATH = "C:/Users/26593/Desktop/pyhoudini/widget/UE5/"
# sys.path.append(PATH) 
# import CreateMesh
# reload(CreateMesh)