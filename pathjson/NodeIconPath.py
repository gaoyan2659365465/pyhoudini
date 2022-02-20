#用于从json文件里面查找图标的路径
import json




class NodeIconPath():
    def __init__(self,SORT) -> None:
        self.paths = []
        with open(__file__[:-15]+SORT+".json", 'r',encoding='utf-8') as json_file:
            data = json_file.read()
            result = json.loads(data)
            for i in result:
                self.path = []
                self.path.append(i["标签_链接"].split('/')[-1][:-5])
                self.path.append(i["字段"][10:-22])
                self.paths.append(list(self.path))