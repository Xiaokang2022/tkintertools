ChangeLog/更新日志
==================

[2.5.7] - 2023-01-10
--------------------

### Features/新增

* The `move` function adds the parameter `frames`, which can change the number of frames of the animation when moving  
`move`函数新增参数`frames`，可改变移动时的动画的帧数

* `Tk` class adds the adaptation function to screen DPI, which can make the window clearer  
`Tk` 类新增对屏幕DPI的适配功能，可使窗口更加清晰

* New compatible version and compatible version conversion file  
新增兼容版本以及兼容版本转换文件

### Changed/变更

* Change the function names of functions `move_widget`, `correct_text` and `change_color` to `move`, `text` and `color` respectively  
分别将函数`move_widget`、`correct_text`和`change_color`的函数名变更为`move`、`text`和`color`

* Corrected some parameters  
修正了些许参数

* Increase the default frame rate parameter of the move function to 30  
提高了移动函数的默认帧率参数至30

### Refactored/优化

* Optimized the code structure of the `color` function and the `move` function to make it more concise  
优化了`color`函数和`move`函数的代码结构，使其更加简洁

[2.5.6] - 2022-12-12
--------------------

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

[2.5.5] - 2022-12-11
--------------------

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

[2.5.4] - 2022-12-08
--------------------

### Features/新增

* A new widget has been added: progress bar(`ProcessBar`)  
增加了一个新的控件：进度条（`ProcessBar`）

### Fixed/修复

* Fixed the bug that the screen size would be abnormal when creating `Canvas` of different sizes  
修复了新建不同大小的`Canvas`时，画面大小会异常的 bug

* Solved the bug that there is no change when the font size is scaled under certain conditions  
解决了字体大小进行缩放时，在某种条件下缩小没有变化的 bug

* Solved the bug that function `move_widget` cannot move `tkinter._CanvasItemId`  
解决了函数`move_widget`无法移动`tkinter._CanvasItemId`的 bug

### Changed/变更

* The binding mechanism of associated events has been modified so that `Canvas` classes can be created at any time  
修改了关联事件的绑定机制，使得`Canvas`类可以被随时创建

### Refactored/优化

* Some colors are beautified  
美化了部分颜色

* Optimized some codes in function `move_widget`  
优化了函数`move_widget`中的部分代码

[2.5.3] - 2022-11-27
--------------------

### Features/新增

* Added singleton pattern(`Singleton`) class for inheritance  
增加了单例模式类（`Singleton`）供继承

* Add some methods (attributes) of `Tk`, `Toplevel` and `Canva`s to access some attributes that should not be directly accessed  
增加`Tk`、`Toplevel`、`Canvas`的一些方法(属性)来访问一些不应该被直接访问的属性

### Fixed/修复

* Solved the bug that the `destroy` method of the control can only delete half of the controls when traversing  
解决了控件的`destroy`方法在遍历使用时只能删除一半控件的 bug

    > Thanks/特别感谢  
    Thanks to [-ShuiGuang-](https://blog.csdn.net/atlantis618) for finding the above bug  
    感谢 [-ShuiGuang-](https://blog.csdn.net/atlantis618) 发现了上面的 bug

### Refactored/优化

* `Canvas` class overrides `destroy` method to be compatible with the original `destroy` method  
`Canvas`类重写`destroy`方法以兼容原`destroy`方法

* `Toplevel` class overrides `destroy` method to be compatible with the original `destroy` method  
`Toplevel`类重写`destroy`方法以兼容原`destroy`方法

* Some codes of `Tk` and `Toplevel` are optimized, and the code amount of `Toplevel` controls is greatly reduced  
优化了`Tk`、`Toplevel`的部分代码，`Toplevel`控件的代码量大大缩减

### Removed/删除

* The `proportion_lock` parameter and its function of `Tk` and `Toplevel` are deleted  
删除了`Tk`、`Toplevel`的`proportion_lock`参数及其功能

[2.5.2] - 2022-11-25
--------------------

### Features/新增

* Added mouse style for text type virtual control  
添加了对文本类虚拟控件的鼠标样式

### Fixed/修复

* Solved the bug that the `set` and `append` methods of text virtual controls may fail in some cases  
解决了文本类虚拟控件`set`、`append`方法某些时候会失效的 bug

* Solved the bug that the mouse style flickers when the mouse cursor moves over the button  
解决了鼠标光标移动到按钮上时的鼠标样式会闪烁的 bug

* Fixed the bug that the `read` parameter of the text box control failed  
修复了文本框控件`read`参数失效的 bug

### Refactored/优化

* Change the mouse position detection order to further improve the running speed  
改变鼠标位置检测顺序，进一步提升运行速度

[2.5.1] - 2022-11-23
--------------------

### Features/新增

* Added mouse style for button virtual controls  
添加了对按钮虚拟控件的鼠标样式

### Fixed/修复

* Solved the bug that the input prompt position was not aligned after the input box was enlarged  
解决了输入框放大后输入提示符位置没对齐的 bug

* Solved the bug that text virtual controls will lose focus after being pasted once  
解决了文本类虚拟控件粘贴一次后会失去焦点的 bug

* Fix a few errors in the module documentation  
修复模块文档中的少许错误

### Changed/变更

* Modified the mouse position determination mechanism and improved the running speed  
修改了鼠标位置判定机制，同时提升运行速度

### Refactored/优化

* Some redundant codes are deleted to improve the overall running speed  
删除了部分冗余代码，提升总体运行速度

[2.5.0] - 2022-11-21
--------------------

No more logging
