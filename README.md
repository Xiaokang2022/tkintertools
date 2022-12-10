**tkintertools**
================

Update/最近更新
--------------
> Version: 2.5.5  
> Date: 2022/12/11

### Features/新增

* Added type prompt `Self` for the `self` parameter of instance methods of all classes  
为所有类的实例方法的`self`参数添加了类型提示`Self`

### Fixed/修复

* Fixed the bug that the width and height will not change in some cases when scaling `Canvas` classes  
修复了`Canvas`类缩放时，宽高在某些情况下不会改变的 bug

### Changed/变更

* Modified the access method of `Tk` class, `Toplevel` class and `Canvas` class protection attributes  
修改了`Tk`类、`Toplevel`类、`Canvas`类的保护属性的获取方式

* Greatly modified the canvas scaling mechanism, fully adapted to all situations, and accelerated the scaling speed  
大幅度地修改了画布缩放的机制，完全适应所有情况，并加快了缩放速度

### Refactored/优化

* Optimize the structure of all multiple loops and judgment statements, making the code more beautiful  
优化了所有多重循环加判断语句的结构，使代码更为美观

Todos/待办
---------

* Solve the bug that the text box class `set` and `append` methods will not be updated immediately after use  
解决文本框类`set`、`append`方法使用后不会立即更新的bug

* Solve the bug that the vertical position of the text is wrong when the text box is enlarged  
解决文本框放大时，文本纵向位置错误的bug

* Solve the bug that the cursor will flash faster and faster after pasting text for text control  
解决文本类控件在粘贴文本后光标会越闪越快的bug

* Solve the bug that text shrinks and overflows after zooming text controls  
解决文本类控件缩放后文本产生缩水和溢出的bug

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
