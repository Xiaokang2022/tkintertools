**tkintertools**
================

> 许可证: [LICENSE](./LICENSE)

Update/最近更新
--------------
> Version: 2.5.9  
> Date: 2023/01/13

### Features/新增

- [X] Class `PhotoImage` new method `stop` is used to stop the playback of moving pictures  
类`PhotoImage`新增方法`stop`用于停止动图的播放

### Fixed/修复

- [X] Fixed an incomplete parameter bug in the `moveto` method of the `Canvas` class  
修复了`Canvas`类的方法`moveto`在参数上不完备的bug

- [X] Fixed a bug that sometimes causes multiple controls to touch at the same time  
修复了有时候会产生多个控件同时触碰的bug

- [X] Fixed parameter error of class `PhotoImage`  
修复了类`PhotoImage`的参数错误

### Refactored/优化

- [X] Optimize codes, simplify some codes and delete redundant parts  
优化代码，简化部分代码，删去冗余部分

### Removed/删除

- [X] The redundant parameters `minsize` and `alpha` of the `Tk` and `Toplevel` classes have been deleted  
删除了`Tk`类和`Toplevel`类的冗余参数`minsize`和`alpha`

> 更多信息见更新日志: [CHANGELOG](./CHANGELOG.md)

Description/模块描述
-------------------

The `tkintertools` module is an auxiliary module of the `tkinter` module  
`tkintertools`模块是`tkinter`模块的辅助模块

### Provides/提供功能

* Transparent, rounded and customized widgets  
透明、圆角化和可自定义的控件

* Automatic control of picture size and widget size  
自动控制图片大小和控件大小

* Scalable png pictures and playable gif pictures  
可缩放的png图片和可播放的gif图片

* Regular mobile widgets and canvas interfaces  
按一定规律移动控件和画布界面

* Gradient colors and contrast colors  
渐变色和对比色

* Text with controllable length and alignment  
长度和对齐方式可控的文本

* Convenient, inheritable singleton pattern class  
便捷的、可供继承的单例模式类

* Display clear window and its contents  
显示清晰的窗口及其内容

### Contents/模块内容

* Container Widget/容器控件:  
`Tk`, `Toplevel`, `Canvas`
* Virtual Canvas Widget/虚拟画布控件:  
`CanvasLabel`, `CanvasButton`, `CanvasEntry`, `CanvasText`, `ProcessBar`
* Tool Class/工具类:  
`PhotoImage`, `Singleton`
* Tool Function/工具函数:  
`move`, `text`, `color`

### Attentions/特别注意

* `tkinertools.py` is the latest version, and its version number is not necessarily the same as the tutorial (generally newer than the tutorial)  
`tkintertools.py` 是目前的最新版本，其版本号不一定与教程一致（一般比教程的要新）

* In the `Release Version` folder is the source code of the `tkinertools` module with a large version number in the past  
`Release Version` 文件夹里面的是过去的大版本号的 `tkintertools` 模块的源代码

* `Compatible Version` folder contains the latest compatible version, which is compatible with python 3.7  
`Compatible Version`文件夹里面是当前最新版本的兼容版本，可兼容python3.7版本

> 兼容版本: [Compatible Version](./Compatible%20Version/)  
过去版本: [Release Version](./Release%20Version/)

### More/更多

* GitCode:  
https://gitcode.net/weixin_62651706/tkintertools
* GitHub(Mirror/镜像):  
https://github.com/Xiaokang2022/tkintertools
* Gitee(Mirror/镜像):  
https://gitee.com/xiaokang-2022/tkintertools
* Column/专栏:  
https://blog.csdn.net/weixin_62651706/category_11600888.html
* Tutorials/教程:  
https://xiaokang2022.blog.csdn.net/article/details/127374661
* Author/作者:  
https://xiaokang2022.blog.csdn.net
* Contact/联系我:  
<2951256653@qq.com>
