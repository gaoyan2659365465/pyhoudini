# pyHoudini

#### 介绍
使用PySide2制作的Houdini小插件，用于整理节点笔记本，可以按每个节点来分开做笔记的一个小软件


#### 安装教程
请查看插件里面的使用说明解决安装的问题


如果你是houdini18版本很遗憾无法使用本插件
因为houdini18与19差别巨大，我也做出了努力但无济于事，所以推荐使用houdini19来安装此插件。

点击保存以后，数据会存储到插件目录的data文件夹内，可以进行手动迁移到其他电脑或安装同步软件


![image text](https://gitee.com/seerhugan/py-houdini/raw/master/%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E/1%E5%8F%B3%E9%94%AE%E6%B7%BB%E5%8A%A0%E6%96%B0%E5%B7%A5%E5%85%B7.png)

![image text](https://gitee.com/seerhugan/py-houdini/raw/master/%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E/2%E7%B2%98%E8%B4%B4%E4%BB%A3%E7%A0%81%E4%BF%AE%E6%94%B9%E4%BD%A0%E8%87%AA%E5%B7%B1%E7%9A%84%E8%B7%AF%E5%BE%84.jpg)


常见问题：
1、插件不显示图标
C:/Program Files/Side Effects Software/Houdini 19.0.383/houdini/config/Icons/icons.zip
可能是图标zip路径给错了，需要照着默认的改一下
有些人可能19版本也没有图片zip文件，我发到群里了，如果找不到的可以从群里下载然后自行解压到插件目录(正常情况是有的)
qq群271878722
解决步骤：
先看看插件目录pyhoudini\Plugins\NodeBook里面有没有icons文件夹，如果有的话删掉
然后使用压缩包直接手动解压到插件目录
（注意：我提供的压缩包是需要手动解压的，不要填进插件里，插件会自动解压
这样文件夹层级就不对了，会出现icons里面套着一个icons文件夹）
因为我提供的压缩包里面已经有icons文件夹了
如果出现这种情况，需要把里面的icons文件夹拷贝出来，不要出现层级嵌套！否则插件依然识别不到图标
然后重新打开houdini

极少见情况19版本也没法显示图标，并且内容浏览器的笔记也无法显示，这个问题我也没能解决
目前只遇到一例