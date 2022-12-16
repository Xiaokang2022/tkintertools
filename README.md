**tkintertools**
================

Update/最近更新
--------------
> Version: 2.5.7-pre  
> Date: 2022/12/12

### Features/新增

- [X] The `move` function adds the parameter `frames`, which can change the number of frames of the animation when moving  
`move`函数新增参数`frames`，可改变移动时的动画的帧数

### Changed/变更

- [X] Change the function names of functions `move_widget`, `correct_text` and `change_color` to `move`, `text` and `color` respectively  
分别将函数`move_widget`、`correct_text`和`change_color`的函数名变更为`move`、`text`和`color`

### Refactored/优化

- [X] Optimized the code structure of the `color` function and the `move` function to make it more concise  
优化了`color`函数和`move`函数的代码结构，使其更加简洁

> 更多信息见更新日志: [CHANGELOG](./CHANGELOG.md)

Todos/待办
---------

- [ ] Solve the bug that the `CanvasText` class `set` and `append` methods will not be updated immediately after use  
解决`CanvasText`类`set`、`append`方法使用后不会立即更新的bug

- [ ] Solve the bug that the vertical position of the text is wrong when the `CanvasText` class is enlarged  
解决`CanvasText`类放大时，文本纵向位置错误的bug

- [ ] Solve the bug that the cursor will flash faster and faster after pasting text for text control  
解决文本类控件在粘贴文本后光标会越闪越快的bug

- [ ] Solve the bug that text shrinks and overflows after zooming text controls  
解决文本类控件缩放后文本产生缩水和溢出的bug

- [ ] Perfect the scroll bar function of `CanvasText` class  
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
`PhotoImage`, `Singleton`
* Tool Function/工具函数:  
`move`, `text`, `color`

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
