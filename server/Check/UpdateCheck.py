import requests
import os
import zipfile
from pathlib import Path
from os import startfile

c_version = '1.5.2'
def get_new_app(version_new):
    url = 'http://192.168.31.70/new/app'
    try:
        resp = requests.get(url)
        resp.encoding = 'UTF-8'
        if resp.status_code == 200:
            with open(__file__[:-14]+'pyhoudini{}.zip'.format(version_new), "wb") as file: 
                file.write(resp.content)
            return True
        else:
            print('【版本更新】服务器连接失败')
            return False
    except Exception as e:
        print('【版本更新】网络错误'+str(e))
        return False
    
# 检查客户端版本
def check_update():
    try:
        url = 'http://192.168.31.70/version'
        resp = requests.get(url)
        resp.encoding = 'UTF-8'
        if resp.status_code != 200:
            print('【版本检测】服务器连接失败')
            return False
        if resp.text == c_version:
            print('【版本检测】客户端版本正常')
            return True
        
        print('【版本检测】客户端版本过低，正在自动下载最新版:{}'.format(resp.text))
        if get_new_app(resp.text):
            print('【版本检测】最新版下载成功，文件名为程序名V{}，请使用最新版本！'.format(resp.text))   
             #删除旧版本 
            if os.path.isfile('pyhoudini{}.zip'.format(c_version)):
                os.remove('pyhoudini{}.zip'.format(c_version))
            
            unzipFile(oriPath=__file__[:-14]+'pyhoudini{}.zip'.format(resp.text),goalPath=__file__[:-14])
            
            if os.path.isfile(__file__[:-14]+'pyhoudini{}.zip'.format(resp.text)):
                os.remove(__file__[:-14]+'pyhoudini{}.zip'.format(resp.text))
            print(__file__[:-14]+resp.text+'/')
            startfile(__file__[:-14]+resp.text+'/')
        return True
    except Exception as e:
        print('【版本检测】网络错误')
        return False
 
# 开始运行
def run():
    # 检查客户端版本
    if not check_update():
        #input()
        return
    print('程序运行结束')
    #input()




def my_own_makedirs(filePath):
    '''
    递归创建文件夹，filePath从根目录开始判断，如果有那一层路径不存在就创建
    例如filePath为D:/报告/123.zip，那么程序会首先判断D:/是否存在，如果不存在则会创建；
    接下来会判断 D:/报告 是否存在，如果不存在则会创建；
    这个函数只会创建文件夹，而不会创建文件。
    :param filePath: 文件的路径，注意不是文件夹的路径，例如：D:/123.zip，字符串格式
    :return: None
    '''
    # print(filePath)
    filePath=filePath.replace("/","\\")
    folderList=filePath.split("\\")[0:-1]
    # print(folderList)
    currenPath=folderList[0]+"\\"
    for i in range(0,len(folderList)):
        currenPath = os.path.join(currenPath, folderList[i])
        # print(currenPath)
        if os.path.isdir(currenPath):
            # print("存在")
            pass
        else:
            print(currenPath+"不存在,开始创建")
            os.mkdir(currenPath)


def unzipFile(oriPath,goalPath):
    '''
    解决解压zip包时的中文乱码问题
    :param oriPath: 压缩文件的地址
    :param goalPath: 解压后存放的的目标位置
    :return: None
    '''

    with zipfile.ZipFile(file=oriPath, mode='r') as zf:
        # 解压到指定目录,首先创建一个解压目录
        unzip_dir_path = goalPath
        if not os.path.exists(unzip_dir_path):
            os.mkdir(unzip_dir_path)

        for old_name in zf.namelist():
            # print(zf.namelist())
            # print("old_name:",old_name)
            # 获取文件大小，目的是区分文件夹还是文件，如果是空文件应该不好用。
            file_size = zf.getinfo(old_name).file_size
            print(file_size)
            # 由于源码遇到中文是cp437方式，所以解码成gbk，windows即可正常
            new_name = old_name.encode('cp437').decode('gbk')
            # # 拼接文件的保存路径
            new_path = os.path.join(unzip_dir_path, new_name)
            print(new_path)
            my_own_makedirs(new_path)
            # 判断文件是文件夹还是文件
            if file_size > 0:
                # 是文件，通过open创建文件，写入数据

                with open(file=new_path, mode='wb') as f:
                    # zf.read 是读取压缩包里的文件内容
                    f.write(zf.read(old_name))
            # else:
            #     # 是文件夹，就创建
            #     os.mkdir(new_path)
