ChangeLog/更新日志
=================

[2.6.5] - 2023-06-17
--------------------

### Features/新增

- [X] The new class `Space` added to the submodule `tools_3d` can provide the ability to translate, rotate and scale 3D objects  
子模块 `tools_3d` 新增类 `Space` 可以提供对 3D 对象进行平移、旋转和缩放等操作的功能

### Fixed/修复

- [X] Fixed a bug where class `Cuboid` and class `Tetrahedron` did not add instances to parent class `Canvas_3D`  
修复了类 `Cuboid` 和类 `Tetrahedron` 没有将实例添加到父类 `Canvas_3D` 的 bug

- [X] Fixed a bug where an error was displayed when a 3D object appeared behind the camera position  
修复了当 3D 对象出现在相机位置后面时会显示错误的 bug

- [X] Fixed some incorrect type hints  
修复了部分错误的类型提示

### Removed/移除

- [X] Removed the constant `BACKGROUND` and no longer qualified the default background color of class `Canvas`    
移除常量 `BACKGROUND` 并且不再对类 `Canvas` 的默认背景颜色做限定

[2.6.4] - 2023-06-12
--------------------

### Features/新增

- [X] The class `tool_3d` submodule `Canvas_3D` has added the function `space_sort` to calculate and sort the actual position of space to support the correct display of geometry colors  
`tool_3d` 子模块的类 `Canvas_3D` 新增对空间实际位置进行计算和排序的函数 `space_sort`，以支持几何体颜色的正确显示

### Fixed/修复

- [X] Fixed a bug where movement and rotation between points, lines, and sides in the 3D module are out of sync  
修复了 3D 模块中的点、线与面之间移动和旋转不同步的 bug

- [X] Fixed a bug where class `Canvas_3D` in the 3D module would be invalid when passing arguments to class `Canvas` in the original `tkinter` module  
修复了 3D 模块中的类 `Canvas_3D` 在传递原 `tkinter` 模块中的类 `Canvas` 的参数时会无效的 bug

### Changed/变更

- [X] The parameter `cfg_3d` of class `Canvas_3D` is changed to 3 specific parameters, namely camera distance `camera_distance`, picture abscissa deviation `dx` and screen ordinate deviation `dy`  
类 `Canvas_3D` 的参数 `cfg_3d` 被更改为 3 个具体的参数，分别为相机距离 `camera_distance`、画面横坐标偏差 `dx` 和画面纵坐标偏差 `dy`

- [X] In the 3D submodule, the value of the camera distance constant is changed to 1000  
3D 子模块中相机距离常量的值更改为 1000

- [X] Compatibility changes, because Python 3.7 is about to enter the end-of-life stage, and in order to improve program performance, Python3.7 is not compatible, but Python3.8 is compatible  
兼容性更改，由于 Python3.7 即将步入 end-of-life 阶段，且为了提高程序性能，现无法兼容 Python3.7，但能够兼容 Python3.8

[2.6.3] - 2023-06-07
--------------------

### Optimized/优化

- [X] The 3D object implementation varies with the size of the canvas  
3D 对象实现随画布大小变化而变化

- [X] Make the default value of the corner radius more intelligent, 4 when the system is `Windows11`, `Linux`, `Mac`, and 0 for the rest  
使圆角半径的默认值更加智能，当系统为 `Windows11`、`Linux`、`Mac` 时为 4，其余情况为 0

- [X] Added more type hints, especially for overloads  
添加了更多类型提示，尤其是对重载的提示

### Fixed/修复

- [X] Fixed a bug where the parameter `keep` would affect the position of class `Canvas`  
修复参数 `keep` 会对类 `Canvas` 的位置产生影响的 bug

### Changed/变更

- [X] Set the default value of the parameter `keep` of the class `Canvas_3D` in the 3D module to `True`, i.e. keep the canvas width and height scaled proportionally by default  
将3d模块中的类 `Canvas_3D` 的参数 `keep` 的默认值设为 `True`，即默认保持画布宽高缩放成比例

[2.6.2] - 2023-05-30
--------------------

### Features/新增

- [X] Added `tkintertools` sub-module `tools_3d` to support drawing 3D graphics  
新增 `tkintertools` 子模块 `tools_3d` 以支持绘制 3D 图形

[2.6.1] - 2023-05-21
--------------------

### Optimized/优化

- [X] Enhance the cross platform functionality of the module, which can run on the Windows and Linux platform  
提升模块的跨平台性，可在 Windows 和 Linux 平台上运行

- [X] Optimized reference documentation for classes and functions  
优化了类和函数的参考文档

- [X] Improved module compatibility to Python 3.7  
提升模块兼容性，向下兼容至 Python3.7

- [X] Optimized test files, compatible with different operating systems, and fixed a small number of bugs  
优化了测试文件，兼容不同操作系统，修复少量 bug

- [X] Optimize the methods of the widget checkbox `CheckButton`  
优化控件复选框 `CheckButton` 的各项功能

- [X] The class `Canvas` adds parameters `x` and `y` to reduce redundant code  
类 `Canvas` 新增参数 `x` 和 `y` 以减少多余代码

### Fixed/修复

- [X] Fixed a bug where widgets would misalign after calling the method `moveto`  
修复了控件在调用了方法 `moveto` 后会发生错位的 bug

### Removed/移除

- [X] Remove Unused Constants `SCALE`  
删除无用常量 `SCALE`

[2.6.0] - 2023-03-28
--------------------

### Features/新增

- [X] New virtual canvas widget check box: `CheckButton`  
新增虚拟画布控件复选框：`CheckButton`

### Fixed/修复

- [X] Solve the bug that the `Text` class `set` and `append` methods will not be updated immediately after use  
解决 `Text`类`set`、`append` 方法使用后不会立即更新的 bug

### Optimized/优化

- [X] Optimize the parameters of some classes and functions  
优化部分类和函数的参数

[2.5.12] - 2023-03-20
---------------------

### Features/新增

- [X] Add a `image` parameter to all widgets to add a background image  
所有控件新增参数 `image` 来添加背景图片

### Fixed/修复

- [X] Fixed a bug where the `move` function cannot move a window  
修复了 `move` 函数无法移动窗口的 bug

### Optimized/优化

- [X] Move the binding code of the associated keyboard from class `Tk` to class `Canvas`  
将关联键盘的绑定代码全部由类 `Tk` 移到类 `Canvas` 中

- [X] Optimized some of the code to prevent bugs that shouldn't occur  
优化了部分代码，防止出现一些不应该出现的 bug

### Removed/移除

- [X] Deleted function `font`  
删除了函数 `font`


[2.5.11] - 2023-03-13
---------------------

### Features/新增

- [X] Class `Canvas` adds parameter `keep` to extend function  
类 `Canvas` 新增参数 `keep` 以扩展功能

- [X] Add the tool function `SetProcessDpiAwareness` to enhance the function  
新增工具函数 `SetProcessDpiAwareness` 以增强功能

- [X] New tool function `font` is added to solve the problem of font size matching DPI level  
新增工具函数 `font` 以解决字体大小适配 DPI 级别的问题

### Fixed/修复

- [X] Fixed the problem of inaccurate Python version requirements. The minimum module operation requirement should be Python 3.11  
修复了 Python 版本要求不准确的问题，模块最低运行要求应为 Python3.11

- [X] Fixed the problem that the `configure` method of `_BaseWidget` cannot get the normal effect when modifying the parameter `text` to an empty string  
修复了控件基类 `_BaseWidget` 的方法 `configure` 在将参数 `text` 修改为空字符串时无法得到正常效果的问题

### Optimized/优化

- [X] Optimize the solution to the adaptive DPI problem  
优化解决适配 DPI 问题的方案

- [X] Optimized the way font size fits DPI  
优化了字体大小适配 DPI 的方式

- [X] The canvas widget will be scaled according to the scale of the canvas when it is placed, rather than after it is placed  
画布控件在放置时就会根据画布的缩放而缩放，而不是在放置后才进行缩放

[2.5.10] - 2023-02-04
---------------------

### Features/新增

- [X] Canvas virtual widget base class `_BaseWidget` Add instance attribute `command_ex` to extend functions  
画布虚拟控件基类 `_BaseWidget` 新增实例属性 `command_ex` 以扩展功能

- [X] Function `move` adds parameter `end` to enhance function  
函数 `move` 新增参数 `end` 以增强功能

- [X] New method of canvas virtual widget base class `moveto`  
画布虚拟控件基类新增方法 `moveto`

### Fixed/修复

- [X] Fixed the bug that the class `Tk` cannot make the distance between the window and the screen 0  
修复了类 `Tk` 无法使窗口与屏幕距离为 0 的 bug

- [X] Fixed the bug that the parameter `borderwidth` of the control is invalid when it has rounded corners  
修复了控件在有圆角状态下参数 `borderwidth` 失效的 bug

### Changed/变更

- [X] The initialization parameters of `Tk` class and `Toplevel` class have become more concise  
`Tk` 类和 `Toplevel` 类的初始化参数变得更加简洁了

### Optimized/优化

- [X] The state change of the canvas virtual widget adds a previous state detection, greatly improving performance  
画布虚拟控件的状态改变加了个先前状态检测，大幅提高性能

- [X] The performance of function `move` has been optimized  
函数 `move` 的性能得到了优化

[2.5.9] - 2023-01-13
--------------------

### Features/新增

- [X] Class `PhotoImage` new method `stop` is used to stop the playback of moving pictures  
类 `PhotoImage` 新增方法 `stop` 用于停止动图的播放

### Fixed/修复

- [X] Fixed an incomplete parameter bug in the `moveto` method of the `Canvas` class  
修复了 `Canvas` 类的方法 `moveto` 在参数上不完备的 bug

- [X] Fixed a bug that sometimes causes multiple controls to touch at the same time  
修复了有时候会产生多个控件同时触碰的 bug

- [X] Fixed parameter error of class `PhotoImage`  
修复了类 `PhotoImage` 的参数错误

### Optimized/优化

- [X] Optimize codes, simplify some codes and delete redundant parts  
优化代码，简化部分代码，删去冗余部分

### Removed/移除

- [X] The redundant parameters `minsize` and `alpha` of the `Tk` and `Toplevel` classes have been deleted  
删除了 `Tk` 类和 `Toplevel` 类的冗余参数 `minsize` 和 `alpha`

[2.5.8] - 2023-01-12
--------------------

### Fixed/修复

- [X] Fixed a bug that the function `move` cannot perform the default move mode `flat`  
修复了函数 `move` 无法进行默认的移动模式 `flat` 的 bug

- [X] Solve the bug that the cursor will flash faster and faster after pasting text for text control  
解决文本类控件在粘贴文本后光标会越闪越快的 bug

### Optimized/优化

- [X] `move` function has been optimized to improve applicability, accuracy and speed  
优化了 `move` 函数，提升了适用性、精度以及速度

- [X] `Canvas` class adds compatibility methods `coords`, `move`, `moveto` and `bbox` to improve the DPI adaptation problem  
`Canvas` 类新增兼容方法 `coords`、`move`、`moveto` 和 `bbox`，完善了 DPI 的适配问题

- [X] `Tk` Class Add Method `wm_minszie`, `wm_maxsize` to be compatible with DPI adaptation problems  
`Tk` 类新增方法 `wm_minszie`、`wm_maxsize` 以兼容 DPI 适配问题

- [X] Optimize the `PhotoImage` class so that it can be used without globalization  
优化 `PhotoImage` 类，使之无需全局化，即可使用

- [X] Overall optimization of code and reduction of code volume  
总体优化了代码，减少了代码量

[2.5.7] - 2023-01-10
--------------------

### Features/新增

- [X] The `move` function adds the parameter `frames`, which can change the number of frames of the animation when moving  
`move` 函数新增参数 `frames`，可改变移动时的动画的帧数

- [X] `Tk` class adds the adaptation function to screen DPI, which can make the window clearer  
`Tk` 类新增对屏幕 DPI 的适配功能，可使窗口更加清晰

- [X] New compatible version and compatible version conversion file  
新增兼容版本以及兼容版本转换文件

### Changed/变更

- [X] Change the function names of functions `move_widget`, `correct_text` and `change_color` to `move`, `text` and `color` respectively  
分别将函数 `move_widget`、`correct_text` 和 `change_color` 的函数名变更为 `move`、`text` 和 `color`

- [X] Corrected some parameters  
修正了些许参数

- [X] Increase the default frame rate parameter of the move function to 30  
提高了移动函数的默认帧率参数至 30

### Optimized/优化

- [X] Optimized the code structure of the `color` function and the `move` function to make it more concise  
优化了 `color` 函数和 `move` 函数的代码结构，使其更加简洁

[2.5.6] - 2022-12-12
--------------------

### Fixed/修复

- [X] Fixed the bug that the singleton mode class (`Singleton`) could not pass parameters during initialization  
修复了单例模式类（`Singleton`）在初始化时无法传递参数的 bug

- [X] Fixed the bug that sometimes the font parameters of `_CanvasItemId` could not be found when scaling fonts in `Canvas` class  
修复了 `Canvas` 类在缩放字体时，有时会找不到 `_CanvasItemId` 的字体参数的 bug

### Changed/变更

- [X] The zoom method of the picture is changed from absolute zoom to relative absolute zoom  
图片的缩放方式由绝对缩放变更为相对的绝对缩放方式

### Optimized/优化

- [X] Optimized the structure of the `PhotoImage` class  
优化了 `PhotoImage` 类的结构

- [X] All useless codes (TODO marked) are deleted  
删除了所有无用的代码（TODO 标记的）

- [X] The `fractions` module is introduced to improve the precision of image scaling and reduce the operation time  
引入了 fractions 模块并提高了图片缩放时的精度且减少了运算时间

### Removed/移除

- [X] `Canvas` class deletes two redundant and overridden instance methods: `create_ bitmap` and `create_ window`  
`Canvas` 类删除了两个冗余的、重写的实例方法：`create_bitmap` 和 `create_window`

[2.5.5] - 2022-12-11
--------------------

### Features/新增

- [X] Added type prompt `Self` for the `self` parameter of instance methods of all classes  
为所有类的实例方法的 `self` 参数添加了类型提示 `Self`

### Fixed/修复

- [X] Fixed the bug that the width and height will not change in some cases when scaling `Canvas` classes  
修复了 `Canvas` 类缩放时，宽高在某些情况下不会改变的 bug

### Changed/变更

- [X] Modified the access method of `Tk` class, `Toplevel` class and `Canvas` class protection attributes  
修改了 `Tk` 类、`Toplevel` 类、`Canvas` 类的保护属性的获取方式

- [X] Greatly modified the canvas scaling mechanism, fully adapted to all situations, and accelerated the scaling speed  
大幅度地修改了画布缩放的机制，完全适应所有情况，并加快了缩放速度

### Optimized/优化

- [X] Optimize the structure of all multiple loops and judgment statements, making the code more beautiful  
优化了所有多重循环加判断语句的结构，使代码更为美观

[2.5.4] - 2022-12-08
--------------------

### Features/新增

- [X] A new widget has been added: progress bar(`Progressbar`)  
增加了一个新的控件：进度条（`Progressbar`）

### Fixed/修复

- [X] Fixed the bug that the screen size would be abnormal when creating `Canvas` of different sizes  
修复了新建不同大小的 `Canvas` 时，画面大小会异常的 bug

- [X] Solved the bug that there is no change when the font size is scaled under certain conditions  
解决了字体大小进行缩放时，在某种条件下缩小没有变化的 bug

- [X] Solved the bug that function `move_widget` cannot move `tkinter._CanvasItemId`  
解决了函数 `move_widget` 无法移动 `tkinter._CanvasItemId` 的 bug

### Changed/变更

- [X] The binding mechanism of associated events has been modified so that `Canvas` classes can be created at any time  
修改了关联事件的绑定机制，使得 `Canvas` 类可以被随时创建

### Optimized/优化

- [X] Some colors are beautified  
美化了部分颜色

- [X] Optimized some codes in function `move_widget`  
优化了函数 `move_widget` 中的部分代码

[2.5.3] - 2022-11-27
--------------------

### Features/新增

- [X] Added singleton pattern(`Singleton`) class for inheritance  
增加了单例模式类（`Singleton`）供继承

- [X] Add some methods (attributes) of `Tk`, `Toplevel` and `Canvas` to access some attributes that should not be directly accessed  
增加 `Tk`、`Toplevel`、`Canvas` 的一些方法(属性)来访问一些不应该被直接访问的属性

### Fixed/修复

- [X] Solved the bug that the `destroy` method of the control can only delete half of the controls when traversing  
解决了控件的 `destroy` 方法在遍历使用时只能删除一半控件的 bug
 
        Thanks to [-ShuiGuang-](https://blog.csdn.net/atlantis618) for finding the above bug  
        感谢 [-ShuiGuang-](https://blog.csdn.net/atlantis618) 发现了上面的 bug

### Optimized/优化

- [X] `Canvas` class overrides `destroy` method to be compatible with the original `destroy` method  
`Canvas` 类重写 `destroy` 方法以兼容原 `destroy` 方法

- [X] `Toplevel` class overrides `destroy` method to be compatible with the original `destroy` method  
`Toplevel` 类重写 `destroy` 方法以兼容原 `destroy` 方法

- [X] Some codes of `Tk` and `Toplevel` are optimized, and the code amount of `Toplevel` controls is greatly reduced  
优化了 `Tk`、`Toplevel` 的部分代码，`Toplevel` 控件的代码量大大缩减

### Removed/移除

- [X] The `proportion_lock` parameter and its function of `Tk` and `Toplevel` are deleted  
删除了 `Tk`、`Toplevel` 的 `proportion_lock` 参数及其功能

[2.5.2] - 2022-11-25
--------------------

### Features/新增

- [X] Added mouse style for text type virtual control  
添加了对文本类虚拟控件的鼠标样式

### Fixed/修复

- [X] Solved the bug that the `set` and `append` methods of text virtual controls may fail in some cases  
解决了文本类虚拟控件 `set`、`append` 方法某些时候会失效的 bug

- [X] Solved the bug that the mouse style flickers when the mouse cursor moves over the button  
解决了鼠标光标移动到按钮上时的鼠标样式会闪烁的 bug

- [X] Fixed the bug that the `read` parameter of the text box control failed  
修复了文本框控件 `read` 参数失效的 bug

### Optimized/优化

- [X] Change the mouse position detection order to further improve the running speed  
改变鼠标位置检测顺序，进一步提升运行速度

[2.5.1] - 2022-11-23
--------------------

### Features/新增

- [X] Added mouse style for button virtual controls  
添加了对按钮虚拟控件的鼠标样式

### Fixed/修复

- [X] Solved the bug that the input prompt position was not aligned after the input box was enlarged  
解决了输入框放大后输入提示符位置没对齐的 bug

- [X] Solved the bug that text virtual controls will lose focus after being pasted once  
解决了文本类虚拟控件粘贴一次后会失去焦点的 bug

- [X] Fix a few errors in the module documentation  
修复模块文档中的少许错误

### Changed/变更

- [X] Modified the mouse position determination mechanism and improved the running speed  
修改了鼠标位置判定机制，同时提升运行速度

### Optimized/优化

- [X] Some redundant codes are deleted to improve the overall running speed  
删除了部分冗余代码，提升总体运行速度

[2.5.0] - 2022-11-21
--------------------

- [X] No more logging  
没有更多日志了

--------------------

TIP: Since I didn't get into the habit of logging before, there are no more logs, but fortunately the version number is inherited ಥ_ಥ  
提示: 由于我以前没有养成记录日志的习惯，故没有更多的日志了，好在版本号继承了下来 ಥ_ಥ
