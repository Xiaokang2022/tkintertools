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
        <img src="https://img.shields.io/badge/ChangeLog-2023/03/13-orange" alt="CHANGELOG" />
    </a>
    <a href="./TODO.md">
    <img src="https://img.shields.io/badge/ToDo-6-yellow" alt="TODO" />
    </a>
    <br>
    <img src="https://img.shields.io/badge/Mail-2951256653@qq.com-purple" alt="Contact" />
    <a href="https://xiaokang2022.blog.csdn.net">
        <img src="https://img.shields.io/badge/Blog-https://xiaokang2022.blog.csdn.net-red" alt="Blog" />
    </a>
</div>

🚀Description/模块说明
----------------------
`tkintertools` 是一个完全没有使用任何第三方模块和库的Python界面开发模块，同时，它也没有任何依赖包，它的功能完全由内置模块和函数实现。

`tkintertools` 是一款基于 `tkinter` 模块的二次开发的界面编程模块，它和 `tkinter` 最大的不同在于，它的控件并非真实的控件，而是在 `tkinter` 模块中 `Canvas` 对象中绘制而成的，这就赋予了 `tkintertools` 控件一些特性，列举如下：

1. 控件背景可以是透明的👍
2. 控件的样式可以是自定义的👍
3. 控件的创建速度是远大于 `tkinter` 的控件的👍

开发 `tkintertools` 模块选用的 Python 版本为 3.10，在这个及以上版本的 Python 拥有很好的类型提示语法，能为用户提供最好的语法提示。这里没有选择用 .pyi 存根文件的方式来实现类型提示的功能，主要原因是 .pyi 文件不方便和模块真正的文件进行同步修改，而且既然这个类型提示的功能在 Python3.6（Python3.10 的类型提示语法得到进一步强化） 以上在源代码中实现，那何必再用存根文件呢？

使用 Python3.10 强化了的类型提示语法也意味着用户使用的 Python 版本也必须至少为 3.10，为了弥补兼容性，后续会推出兼容版的 tkintertools。目前需要兼容的用户，可以在源代码中自行修改，需要修改的语法如下：

3.9 及更低版本 : 类型提示语法中的 “|”，isinstance 函数中的 “|”  
3.7 及更低版本 : 赋值运算符的海象运算符 “:=”  
3.6 及更低版本 : `fractions` 模块 `Fraction` 类的 `limit_denominator` 方法（建议升级Python版本）  
3.5 及更低版本 : 全部的类型提示语法（建议升级Python版本）

🚀Provides/模块功能
-------------------
Here, only the more distinctive features will be listed  
这里只会列举出比较具有特色的功能

### ⭐Customizable widgets/可自定义的控件

### ⭐Automatically control size/自动控制大小

### ⭐Easily move widgets/轻松移动控件

### ⭐Gradient colors/渐变色

### ⭐Automatically adapt to DPI/自动适应DPI

### ⭐Scalable Picture/可缩放图片

🚀Contents/模块内容
-------------------
Each non internal class and function in the module will be described in detail here  
这里会详细说明模块中的每个非内部类和函数

### ⭐Container Widget/容器控件

1. `Tk` : 窗口类

    继承于 `tkinter.Tk`，在继承了 `tkinter` 模块内 `Tk` 的基础上，又加入了对 `tkintertools` 模块中的 `Canvas` 对象的支持，并加入了检测窗口大小是否缩放的机制，以使得其子 `Canvas` 均能正确地进行缩放

2. `Toplevel` : 顶级窗口类

    继承于 `tkinter.Toplevel` 和 `Tk`，加入了对 `tkintertools` 模块中的 `Canvas` 对象的支持，其余均与 `Tk` 一样

3. `Canvas` : 画布类

    继承于 `tkinter.Canvas`，加入了对画布虚拟控件的支持，同时是各类响应事件、缩放控制的管理者，也对 `tkinter.Canvas` 的实例方法有一定的兼容性

### ⭐Virtual Canvas Widget/虚拟画布控件

1. `Label` : 标签控件

    标签控件的功能和 `tkinter.Label` 的功能类似，但更加的多元化  
    下面是 `Label` 控件的外观：  
    <img width="720px" src="https://gitcode.net/weixin_62651706/tkintertools/-/raw/master/docs/images/LabelTest.png" alt="LabelTest.png" />
    > SourceCode/源代码 : [test_label.py](./test_label.py)

2. `Button` : 按钮控件

    按钮控件相较于 `tkinter.Button` ，其自由度更高，`tkinter.Button` 只有在按下的时候才能触发绑定的关联事件，而 `Button` 却可以在鼠标移至按钮上方时、鼠标按下时、鼠标松开时都可以绑定关联事件  
    下面是 `Button` 控件的外观：  
    <img width="360px" src="https://gitcode.net/weixin_62651706/tkintertools/-/raw/master/docs/images/ButtonTest.png" alt="ButtonTest.png" />
    > SourceCode/源代码 : [test_button.py](./test_button.py)

3. `Entry` : 输入框控件

    输入框控件可以轻松地设置输入的文本位置（靠左、居中和靠右），同时，它可以在鼠标移至输入框上方、鼠标未在输入框上方两种状态显示不同的默认文本  
    下面是 `Entry` 控件的外观：  
    <img width="360px" src="https://gitcode.net/weixin_62651706/tkintertools/-/raw/master/docs/images/EntryTest.png" alt="EntryTest.png" />
    > SourceCode/源代码 : [test_entry.py](./test_entry.py)

4. `Text` : 文本框控件

    文本框类似于输入框，这里就不再赘述  
    下面是 `Text` 控件的外观：  
    <img width="720px" src="https://gitcode.net/weixin_62651706/tkintertools/-/raw/master/docs/images/TextTest.png" alt="TextTest.png" />
    > SourceCode/源代码 : [test_text.py](./test_text.py)

5. `Progressbar` : 进度条控件

    进度条控件相比 `tkinter.ttk.Progressbar`，外观上的自由度较大  
    下面是 `Progressbar` 控件的外观：  
    <img width="360px" src="https://gitcode.net/weixin_62651706/tkintertools/-/raw/master/docs/images/ProgressbarTest.png" alt="ProgressbarTest.png" />
    > SourceCode/源代码 : [test_progressbar.py](./test_progressbar.py)

### ⭐Tool Class/工具类

1. `PhotoImage` : 图片类，继承于 `tkinter.PhotoImage`
2. `Singleton` : 单例模式类

    单例模式，不用介绍了吧？通过继承它来使用

### ⭐Tool Function/工具函数

1. `move` : 移动函数

    移动函数可以轻松地按一定的规律、移动速度、移动时间去移动 `tkintertools` 模块内的所有对象，同时兼容了 `tkinter` 内的对象，即 `tkinter` 中的对象也可以很方便地移动，甚至它还可以移动窗口的位置！  
    <img width="720px" src="https://gitcode.net/weixin_62651706/tkintertools/-/raw/master/docs/images/MoveTest.gif" alt="MoveTest.gif" />
    > SourceCode/源代码 : [test_move.py](./test_move.py)

2. `text` : 文本函数

    可以快速并方便地得到一个参数长度的字符串，且字符串的内容可以指定位置  
    如：得到一个20长度的字符串“tkintertools”  
    `left`   : "tkintertools        "  
    `center` : "    tkintertools    "  
    `right`  : "        tkintertools"  

3. `color` : 颜色函数

    颜色函数可以轻松求出一个颜色到另外一个颜色的过渡颜色，因此可以轻松得到渐变色的效果，同时，改变传入的参数还可以得到传入颜色的对比色  
    第二张图是 test.py 在图像测试中绘制的图案  
    <img width="360px" src="https://gitcode.net/weixin_62651706/tkintertools/-/raw/master/docs/images/ColorTest.png" alt="ColorTest.png" />
    <img width="360px" src="https://gitcode.net/weixin_62651706/tkintertools/-/raw/master/docs/images/Test_Draw.png" alt="Test_Draw.png" />
    > SourceCode/源代码 : [test_color.py](./test_color.py)

4. `SetProcessDpiAwareness` : DPI 级别设置函数

    这个函数实际上只是对函数 `ctypes.OleDLL('shcore').SetProcessDpiAwareness` 的一个简单包装，其值可为 0、1 和 2，分别代表程序 DPI 的不同级别，那么缩放效果也就不同，`tkintertools` 选择的值是 1，但程序默认值实际为 0  
    下面是执行了这个函数的效果  
    <img width="720px" src="https://gitcode.net/weixin_62651706/tkintertools/-/raw/master/docs/images/SetProcessDpiAwareness_0.png" alt="SetProcessDpiAwareness_0.png" />  
    下面是未执行这个函数的效果  
    <img width="720px" src="https://gitcode.net/weixin_62651706/tkintertools/-/raw/master/docs/images/SetProcessDpiAwareness_1.png" alt="SetProcessDpiAwareness_1.png" />  
    从上面的两张图中可以很明显的看出第一张很模糊，第二张很清晰，这就是 DPI 级别不同的原因，不过这一点在平面缩放比不是 100% 的时候才会出现  
    大家对上面的图肯定很熟悉，这不就是 IDLE 吗！？对，这个的问题的解决办法也是来自于 IDLE 的源代码 [pyshell.py line 18~20]  
    注意：该函数在程序的不同位置执行的效果不一样！一般用在 `mainloop` 前面

🚀More/更多
-----------
> GitCode:  
> https://gitcode.net/weixin_62651706/tkintertools

> GitHub(Mirror/镜像):  
> https://github.com/XiaoKang2022-CSDN/tkintertools

> Column/专栏:  
> https://blog.csdn.net/weixin_62651706/category_11600888.html

> Tutorials/教程:  
> https://xiaokang2022.blog.csdn.net/article/details/127374661
