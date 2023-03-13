**tkintertools**
================

> 许可证: [LICENSE](./LICENSE)

Update/最近更新
--------------
> Version: 2.5.11  
> Date: 2023/03/13

### Features/新增

- [X] Class `Canvas` adds parameter `keep` to extend function  
类`Canvas`新增参数`keep`以扩展功能

- [X] Add the tool function `SetProcessDpiAwareness` to enhance the function  
新增工具函数`SetProcessDpiAwareness`以增强功能

- [x] New tool function `font` is added to solve the problem of font size matching DPI level  
新增工具函数`font`以解决字体大小适配DPI级别的问题

### Fixed/修复

- [X] Fixed the problem of inaccurate Python version requirements. The minimum module operation requirement should be Python 3.11  
修复了 Python 版本要求不准确的问题，模块最低运行要求应为 Python3.11

- [X] Fixed the problem that the `configure` method of `_BaseWidget` cannot get the normal effect when modifying the parameter `text` to an empty string  
修复了控件基类`_BaseWidget`的方法`configure`在将参数`text`修改为空字符串时无法得到正常效果的问题

### Refactored/优化

- [X] Optimize the solution to the adaptive DPI problem  
优化解决适配 DPI 问题的方案

- [X] Optimized the way font size fits DPI  
优化了字体大小适配 DPI 的方式

- [X] The canvas widget will be scaled according to the scale of the canvas when it is placed, rather than after it is placed  
画布控件在放置时就会根据画布的缩放而缩放，而不是在放置后才进行缩放

> 更多信息见更新日志: [CHANGELOG](./CHANGELOG.md)

Description/模块描述
-------------------

The `tkintertools` module is an auxiliary module of the `tkinter` module  
`tkintertools`模块是`tkinter`模块的辅助模块

### Provides/提供功能

* Transparent, rounded and customized widgets  
透明、圆角化和可自定义的控件

* Automatic widget of picture size and widget size  
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
`move`, `text`, `color`, `font`, `SetProcessDpiAwareness`

### Attentions/特别注意

* `tkinertools.py` is the latest version, and its version number is not necessarily the same as the tutorial (generally newer than the tutorial)  
`tkintertools.py` 是目前的最新版本，其版本号不一定与教程一致（一般比教程的要新）

### More/更多

* GitCode:  
https://gitcode.net/weixin_62651706/tkintertools
* GitHub(Mirror/镜像):  
https://github.com/XiaoKang2022-CSDN/tkintertools
* Column/专栏:  
https://blog.csdn.net/weixin_62651706/category_11600888.html
* Tutorials/教程:  
https://xiaokang2022.blog.csdn.net/article/details/127374661
* Author/作者:  
https://xiaokang2022.blog.csdn.net
* Contact/联系我:  
<2951256653@qq.com>
