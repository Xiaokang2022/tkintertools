Release Notes - 版本发布说明
===========================

* Version - 最新版本 : `2.6.12`
* Release - 发布日期 : 2023/11/15

```
pip install tkintertools==2.6.12
```

Example - 样例演示
-----------------

* OS - 操作系统 : Windows11 23H2
* Interpreter - 解释器 : Python 3.12.0

The following are the docstrings displayed in tkintertools on Visual Studio Code and PyCharm, respectively.  
以下分别是 Visual Studio Code 和 PyCharm 上 tkintertools 显示的 docstring。

**Visual Studio Code:**

![VisualStudioCode.png](VisualStudioCode.png)

**PyCharm:**

![PyCharm.png](PyCharm.png)

ChangeLog - 更新日志
-------------------

### Added - 新增

- [X] Widget class `CheckButton` adds parameter `tick` to change its markup symbol  
控件类 `CheckButton` 新增参数 `tick` 来改变其标记符号

- [X] The `Switch` widget class adds parameters `color_fill_slider` and `color_outline_slider` to change the appearance of its internal sliders  
控件类 `Switch` 新增参数 `color_fill_slider` 和 `color_outline_slider` 来更改其内部滑块的外观

### Optimized - 优化

- [X] Drastically changed the format of the docstring to solve the problem that the docstring was displayed out of order on PyCharm  
大幅度修改 docstring 的格式，以解决 docstring 在 PyCharm 上格式显示错乱的问题

- [X] Remove redundant code  
移除冗余代码

- [X] Optimized `tools_3d` submodule code to improve performance by 13.26%  
优化了 `tools_3d` 子模块代码，提高了 13.26% 的性能

### Fixed - 修复

- [X] Fixed an bug where when clicking on a widget, the widget behind it would also be triggered  
修复了点击控件时，其后面的控件也会被触发的问题

- [X] Missing symbol '#' for function `color` return value  
函数 `color` 返回值缺少符号 “#”

- [X] Fixed an bug where the canvas of the `tools_3d` submodule could not use widgets such as buttons  
修复了 `tools_3d` 子模块的画布无法使用按钮等控件的问题

- [X] Fixed an bug where the `Switch` of the Widget class could not control the `Switch` by clicking on the inner slider  
修复了控件类 `Switch` 点击内部滑块无法操控 `Switch` 的问题

Todos - 待办事项
---------------

### Possible Features - 期望功能

- [ ] Perfect the scroll bar function of `Text` class  
完善 `Text` 类的滚动条功能

- [ ] Perfection and optimization of zoom function  
对缩放功能的完善和优化

- [ ] Try adding support for some MarkDown syntax  
尝试增加对部分 Markdown 语法的支持

- [ ] Implement symmetry in 3D modules  
实现 3D 模块中的对称功能

- [ ] Enhanced projection functionality in 3D modules  
增强 3D 模块中的投影功能

- [ ] Add more 3D spatial geometry classes  
增加更多 3D 空间几何体类

-  [ ] Add lights and achieve simple light and shadow renderings  
添加光源，并实现简单的光影渲染的效果

### Known Bugs - 已知问题

- [ ] Solve the bug that text shrinks and overflows after zooming text widgets  
解决文本类控件缩放后文本产生缩水和溢出的 bug

- [ ] Fix the bug of deletion misalignment when there is too much text in the `Text` class  
解决 `Text` 类中文本过多时删减错位的 bug

- [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
3D 对象前后空间的位置关系在某些时候仍有问题
