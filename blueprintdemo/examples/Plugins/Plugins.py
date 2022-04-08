#加载各种第三方库

import os
import configparser
config = configparser.ConfigParser() # 类实例化

def gci(filepath):
    #遍历filepath下所有文件，包括子目录  
    list01 = []
    files = os.listdir(filepath)  
    for fi in files:    
        fi_d = os.path.join(filepath,fi)    
        if os.path.isdir(fi_d):
            #print(os.path.join(filepath, fi_d))
            list02 = gci(fi_d)
            list01 = list01 + list02
        else:      
            #print(os.path.join(filepath,fi_d))#递归遍历/root目录下所有文件
            path01 = os.path.join(filepath,fi_d)
            if path01.find(".ini") != -1:
                list01.append(os.path.join(filepath,fi_d))
    return list01
            

plugins_path = os.getcwd() + "\examples\Plugins"
#list01 = gci(plugins_path)
#list01 = gci("C:/Users/26593/Desktop/blueprintdemo/examples/Plugins")
list01 = gci(__file__[:-11])

config.read(list01[0],encoding='utf-8')
list_section = config.sections()

def get_ini(name):
    value = config.items(name)
    return value