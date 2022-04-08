#从剪切板获取文本，转易语言dll代码

# -*- coding: UTF8 -*-
import win32clipboard as wc
import win32con

# 获取剪切板内容
def getCopy():
    wc.OpenClipboard()
    t = wc.GetClipboardData(win32con.CF_UNICODETEXT)
    wc.CloseClipboard()
    return t

# 写入剪切板内容
def setCopy(str):
    wc.OpenClipboard()
    wc.EmptyClipboard()
    wc.SetClipboardData(win32con.CF_UNICODETEXT, str)
    wc.CloseClipboard()

def getFunName(str01):
    #通过字符串获取函数名
    str02 = ""
    text_line = str01.split("\n")#取一行
    for i in text_line:
        if i.find("调用格式：") != -1:
            str02 = i
            break
    if str02 == "":return ""
    int01 = str02.find("〉 ")
    int02 = str02.find(" （")
    str03 = str02[int01+2:int02]
    return str03

def getFunReturn(str01):
    #通过字符串获取函数返回值
    str02 = ""
    text_line = str01.split("\n")#取一行
    for i in text_line:
        if i.find("调用格式：") != -1:
            str02 = i
            break
    if str02 == "":return ""
    int01 = str02.find("调用格式： 〈")
    int02 = str02.find("〉 ")
    str03 = str02[int01+7:int02]
    return str03

def getFunValue(str01):
    #通过字符串获取函数参数
    list01 = []
    list02 = []
    text_line = str01.split("\n")#取一行
    for i in text_line:
        if i.find(">的名称为“") != -1:
            int01 = i.find(">的名称为“")
            int02 = i.find("”，类型为“")
            int03 = i.find("型（")
            str03 = i[int01+6:int02]
            str04 = i[int02+6:int03+1]
            list01.append(str03)
            list01.append(str04)
            list02.append(list(list01))
            list01 = []
    return list02

def createE(name,str_return,value):
    #创作E代码
    corestr = ".版本 2\n.子程序 "
    corestr = corestr + "BP_" + name
    corestr = corestr + ", " + str_return + ", 公开\n"
    str01 = ""
    for i in value:
        corestr = corestr + ".参数 " + i[0] + ", " + i[1] + "\n"
        str01 = str01 + i[0] + ", "
    str01 = str01[0:-2]
    corestr = corestr + "返回( " + name + " ("+str01+")" + ")\n"
    return corestr
    

e_str = getCopy()
e_list = e_str.split("操作系统需求： Windows、Linux")
for i in e_list:
    str_name = getFunName(i)
    str_return = getFunReturn(i)
    str_value = getFunValue(i)
    str_core = createE(str_name,str_return,str_value)
    print(str_core)

