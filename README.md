**tkintertools**
================

Update/最近更新
-------------------
> Version: 2.5.4-pre  
> Date: 2022/12/8

1. A new widget has been added: progress bar(ProcessBar)  
增加了一个新的控件：进度条（ProcessBar）

2. Some colors are beautified  
美化了部分颜色

3. Delete some redundant codes in the function move_widget and solve the bug that tkinter._CanvasItemId cannot be moved  
删除函数 move_widget 中的部分冗余代码并解决了无法移动 tkinter._CanvasItemId 的 bug

4. Fixed the bug that the screen size would be abnormal when creating Canvas of different sizes  
修复了新建不同大小的 Canvas 时，画面大小会异常的 bug

5. The binding mechanism of associated events has been modified so that Canvas classes can be created at any time  
修改了关联事件的绑定机制，使得 Canvas 类可以被随时创建

Todos/下一步
----------

1. Solve the bug that the text box class set and append methods will not be updated immediately after use  
解决文本框类 set、append 方法使用后不会立即更新的bug

2. Solve the bug that the vertical position of the text is wrong when the text box is enlarged  
解决文本框放大时，文本纵向位置错误的bug

3. Solve the bug that the cursor will flash faster and faster after pasting text for text control  
解决文本类控件在粘贴文本后光标会越闪越快的bug

4. Solve the bug that there is no change in reducing the font size under certain conditions  
解决字体大小进行缩放时，在某种条件下缩小没有变化的bug

5. Solve the bug that text shrinks and overflows after zooming text controls  
解决文本类控件缩放后文本产生缩水和溢出的bug

Description/模块描述
-------------------

The tkindertools module is an auxiliary module of the tkinder module  
tkindertools 模块是tkinder模块的辅助模块

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
`CanvasLabel`, `CanvasButton`, `CanvasEntry`, `CanvasText`
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

* GitHub:  
https://github.com/392126563/tkintertools
* GitCode:  
https://gitcode.net/weixin_62651706/tkintertools
* Column/专栏:  
https://blog.csdn.net/weixin_62651706/category_11600888.html
* Tutorials/教程:  
https://xiaokang2022.blog.csdn.net/article/details/127374661
* Author/作者:  
https://xiaokang2022.blog.csdn.net
* Contact/联系我:  
2951256653@qq.com
