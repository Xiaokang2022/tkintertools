<div align="center">
    <h1>🚀<b>tkintertools</b>🚀</h1>
    <img height="120px" alt="logo" src="https://gitcode.net/weixin_62651706/tkintertools/-/raw/master/tkintertools.png"/>
    <p>The <code>tkintertools</code> module is an auxiliary module of the <code>tkinter</code> module</p>
    <p><code>tkintertools</code> 模块是 <code>tkinter</code> 模块的辅助模块</p>
    <img src="https://img.shields.io/badge/Version-2.5.11.3-blue" alt="latest version" />
    <a href="./LICENSE">
        <img src="https://img.shields.io/badge/License-Mulan PSL v2-green" alt="License" />
    </a>
    <a href="./CHANGELOG.md">
        <img src="https://img.shields.io/badge/ChangeLog-2.5.11-orange" alt="CHANGELOG" />
    </a>
    <img src="https://img.shields.io/badge/Python-3.10.0-yellow" alt="environment" />
    <br>
    <img src="https://img.shields.io/badge/Mail-2951256653@qq.com-purple" alt="Contact" />
    <a href="https://xiaokang2022.blog.csdn.net">
        <img src="https://img.shields.io/badge/Blog-https://xiaokang2022.blog.csdn.net-red" alt="Blog" />
    </a>
</div>

⚡Description/模块说明⚡
-----------------------
tkintertools 是一个完全没有使用任何第三方模块和库的Python界面开发模块，同时，它也没有任何依赖包，它的功能完全由内置模块和函数实现。

tkintertools 是一款基于 tkinter 模块的二次开发的界面编程模块，它和 tkinter 最大的不同在于，tkintertools 的控件并非真实的控件，而是在 tkinter 模块中 Canvas 对象中绘制而成的，这就赋予了 tkintertools 控件一些特性，列举如下：

1. 控件背景可以是透明的👍
2. 控件的样式可以是自定义的👍
3. 控件的创建速度是远大于 tkinter 的控件的👍

开发 tkintertools 模块选用的 Python 版本为 3.10，在这个及以上版本的 Python 拥有很好的类型提示语法，能为用户提供最好的语法提示。这里没有选择用 .pyi 存根文件的方式来实现类型提示的功能，主要原因是 .pyi 文件不方便和模块真正的文件进行同步修改，而且既然这个类型提示的功能在 Python3.6（Python3.10 的类型提示语法得到进一步强化） 以上在源代码中实现，那何必再用存根文件呢？

使用 Python3.10 强化了的类型提示语法也意味着用户使用的 Python 版本也必须至少为 3.10，为了弥补兼容性，后续会推出兼容版的 tkintertools。目前需要兼容的用户，可以在源代码中自行修改，需要修改的语法如下：

3.9 及更低版本 : 类型提示语法中的 “|”，isinstance 函数中的 “|”  
3.7 及更低版本 : 赋值运算符的海象运算符 “:=”  
3.6 及更低版本 : fractions 模块 Fraction 类的 limit_denominator 方法（建议升级Python版本）  
3.5 及更低版本 : 全部的类型提示语法（建议升级Python版本）

⚡Provides/模块功能⚡
--------------------
Here, only the more distinctive features will be listed  
这里只会列举出比较具有特色的功能

### ⭐Customizable widgets/可自定义的控件

### ⭐Automatically control size/自动控制大小

### ⭐Easily move widgets/轻松移动控件

### ⭐Gradient colors/渐变色

### ⭐Automatically adapt to DPI/自动适应DPI

### ⭐Scalable Picture/可缩放图片

⚡Contents/模块内容⚡
--------------------
Each non internal class and function in the module will be described in detail here  
这里会详细说明模块中的每个非内部类和函数

### ⭐Container Widget/容器控件

1. `Tk` : 窗口类，继承于 `tkinter.Tk`
2. `Toplevel` : 顶级窗口类，继承于 `tkinter.Toplevel`
3. `Canvas` : 画布类，继承于 `tkinter.Canvas`

### ⭐Virtual Canvas Widget/虚拟画布控件

1. `Label` : 标签控件
2. `Button` : 按钮控件
3. `Entry` : 输入框控件
4. `Text` : 文本框控件
5. `Progressbar` : 进度条控件

### ⭐Tool Class/工具类

1. `PhotoImage` : 图片类，继承于 `tkinter.PhotoImage`
2. `Singleton` : 单例模式类，用于继承

### ⭐Tool Function/工具函数

1. `move` : 移动函数
2. `text` : 文本函数
3. `color` : 颜色函数
4. `SetProcessDpiAwareness` : DPI 级别设置函数

⚡More/更多⚡
------------
> GitCode:  
> https://gitcode.net/weixin_62651706/tkintertools

> GitHub(Mirror/镜像):  
> https://github.com/XiaoKang2022-CSDN/tkintertools

> Column/专栏:  
> https://blog.csdn.net/weixin_62651706/category_11600888.html

> Tutorials/教程:  
> https://xiaokang2022.blog.csdn.net/article/details/127374661
