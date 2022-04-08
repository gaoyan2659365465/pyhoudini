import json

#序列化
JSONPATH = __file__[:-24] + "build\\test.json"

class BP_Json():
    def __init__(self):
        """序列化类"""
        pass
    def dump(self):
        """保存"""
        return
    def load(self,obj):
        """加载"""
        return
    def dumpFile(self,data):
        """保存到文件"""
        json.dump(data, open(JSONPATH,'w'),ensure_ascii=False,indent=4)
    def loadFile(self):
        """加载文件"""
        with open(JSONPATH, 'r') as json_file:
            data = json_file.read()
            try:
                result = json.loads(data)
            except:
                print("出错")
                data.encode(encoding='gbk').decode(encoding='utf-8')
                result = json.loads(data)
            
        return result