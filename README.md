**tkintertools**
================

> 许可证: [LICENSE](./LICENSE)

Update/最近更新
--------------
> Version: 2.5.8  
> Date: 2023/01/12

### Fixed/修复

- [X] Fixed a bug that the function `move` cannot perform the default move mode `flat`  
修复了函数`move`无法进行默认的移动模式`flat`的bug

- [X] Solve the bug that the cursor will flash faster and faster after pasting text for text control  
解决文本类控件在粘贴文本后光标会越闪越快的bug

### Refactored/优化

- [X] `move` function has been optimized to improve applicability, accuracy and speed  
优化了`move`函数，提升了适用性、精度以及速度

- [X] `Canvas` class adds compatibility methods `coords`, `move`, `moveto` and `bbox` to improve the DPI adaptation problem  
`Canvas`类新增兼容方法`coords`、`move`、`moveto`和`bbox`，完善了DPI的适配问题

- [x] `Tk` Class Add Method `wm_minszie`, `wm_maxsize` to be compatible with DPI adaptation problems  
`Tk`类新增方法`wm_minszie`、`wm_maxsize`以兼容DPI适配问题

- [X] Optimize the `PhotoImage` class so that it can be used without globalization  
优化`PhotoImage`类，使之无需全局化，即可使用

- [X] Overall optimization of code and reduction of code volume  
总体优化了代码，减少了代码量

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
