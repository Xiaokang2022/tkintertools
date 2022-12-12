**tkintertools**
================

Update/最近更新
--------------
> Version: 2.5.6  
> Date: 2022/12/12

### Fixed/修复

* Fixed the bug that the singleton mode class (`Singleton`) could not pass parameters during initialization  
修复了单例模式类（`Singleton`）在初始化时无法传递参数的bug

* Fixed the bug that sometimes the font parameters of `_CanvasItemId` could not be found when scaling fonts in `Canvas` class  
修复了`Canvas`类在缩放字体时，有时会找不到`_CanvasItemId`的字体参数的bug

### Changed/变更

* The zoom method of the picture is changed from absolute zoom to relative absolute zoom  
图片的缩放方式由绝对缩放变更为相对的绝对缩放方式

### Refactored/优化

* Optimized the structure of the `PhotoImage` class  
优化了`PhotoImage`类的结构

* All useless codes (TODO marked) are deleted  
删除了所有无用的代码（TODO标记的）

* The `fractions` module is introduced to improve the precision of image scaling and reduce the operation time  
引入了fractions模块并提高了图片缩放时的精度且减少了运算时间

### Removed/删除

* `Canvas` class deletes two redundant and overridden instance methods: `create_ bitmap` and `create_ window`  
`Canvas`类删除了两个冗余的、重写的实例方法：`create_bitmap`和`create_window`

Todos/待办
---------

* Solve the bug that the `CanvasText` class `set` and `append` methods will not be updated immediately after use  
解决`CanvasText`类`set`、`append`方法使用后不会立即更新的bug

* Solve the bug that the vertical position of the text is wrong when the `CanvasText` class is enlarged  
解决`CanvasText`类放大时，文本纵向位置错误的bug

* Solve the bug that the cursor will flash faster and faster after pasting text for text control  
解决文本类控件在粘贴文本后光标会越闪越快的bug

* Solve the bug that text shrinks and overflows after zooming text controls  
解决文本类控件缩放后文本产生缩水和溢出的bug

* Perfect the scroll bar function of `CanvasText` class  
完善`CanvasText`类的滚动条功能

Description/模块描述
-------------------

The `tkintertools` module is an auxiliary module of the `tkinter` module  
`tkintertools`模块是`tkinter`模块的辅助模块

Minimum Requirement: Python3.10  
最低要求：Python3.10

Provides/提供:
1. Transparent, rounded and customized widgets  
透明、圆角化和可自定义的控件

2. Automatic control of picture size and widget size  
自动控制图片大小和控件大小

3. Scalable png pictures and playable gif pictures  
可缩放的png图片和可播放的gif图片

4. Regular mobile widgets and canvas interfaces  
按一定规律移动控件和画布界面

5. Gradient colors and contrast colors  
渐变色和对比色

6. Text with controllable length and alignment  
长度和对齐方式可控的文本

7. Convenient, inheritable singleton pattern class  
便捷的、可供继承的单例模式类

Contents/模块内容
----------------

* Container Widget/容器控件:  
`Tk`, `Toplevel`, `Canvas`
* Virtual Canvas Widget/虚拟画布控件:  
`CanvasLabel`, `CanvasButton`, `CanvasEntry`, `CanvasText`, `ProcessBar`
* Tool Class/工具类:  
`PhotoImage`, `singleton`
* Tool Function/工具函数:  
`move_widget`, `correct_text`, `change_color`

Attentions/特别注意
------------------

* `tkinertools.py` is the latest version, and its version number is not necessarily the same as the tutorial (generally newer than the tutorial)  
`tkintertools.py` 是目前的最新版本，其版本号不一定与教程一致（一般比教程的要新）

* In the `Release Version` folder is the source code of the `tkinertools` module with a large version number in the past  
`Release Version` 文件夹里面的是过去的大版本号的 `tkintertools` 模块的源代码

More/更多
--------

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
