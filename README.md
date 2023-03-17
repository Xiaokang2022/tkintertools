**tkintertools**
================

> 许可证: [LICENSE](./LICENSE)

Update/最近更新
--------------
> Version: 2.5.11.3  
> Date: 2023/03/17

### Features/新增

- [X] Add a `image` parameter to all widgets to add a background image  
所有控件新增参数`image`来添加背景图片

### Refactored/优化

- [X] Move the binding code of the associated keyboard from class `Tk` to class `Canvas`  
将关联键盘的绑定代码全部由类`Tk`移到类`Canvas`中

### Removed/删除

- [X] Deleted function `font`  
删除了函数`font`

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
`Label`, `Button`, `Entry`, `Text`, `Progressbar`
* Tool Class/工具类:  
`PhotoImage`, `Singleton`
* Tool Function/工具函数:  
`move`, `text`, `color`, `SetProcessDpiAwareness`

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
