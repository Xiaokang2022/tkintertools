Release Notes - 版本说明
=======================

* Version - 最新版本 : `2.6.10`
* Release - 发布日期 : 2023/08/12

```
pip install tkintertools==2.6.10
```

Example - 样例演示
-----------------

* OS - 操作系统 : Windows11 22H2
* Interpreter - 解释器 : Python 3.11.4

The following progress bar widget are in variable mode  
下面的进度条控件为不定模式

![png](example.png)

<details><summary><b>Source Code - 源代码</b></summary>

```python
# Only the key parts of the code are shown here

pb = tkt.Progressbar(canvas, 320, 320, 640, 35, mode='indeterminate')  # indeterminate mode
pb.load(0.7) # load to 70%
```

</details>

ChangeLog - 更新日志
-------------------

### Added - 新增

- [X] Added file exceptions.py and exception classes `ScaleArgsValueError`, `ColorArgsValueError` and `WidgetStateModeError` to provide a description of some exceptions  
新增文件 exceptions.py 及异常类 `ScaleArgsValueError`、`ColorArgsValueError` 和 `WidgetStateModeError` 以提供部分异常的描述

- [X] The widget `Progressbar` adds a indeterminate mode  
控件 `Progressbar` 新增不定模式

### Changed - 变更

- [X] The value of the constant `SWITCH_WIDTH` is changed from 0 to 60  
常量 `SWITCH_WIDTH` 的值从 0 更改为 60

- [X] The parameter `width` of class `Switch` was changed from positional argument to keyword argument  
类 `Switch` 的参数 `width` 由位置参数更改为关键字参数

### Optimized - 优化

- [X] Change the way the output is formatted in all code from the "%" mode to the more efficient f-string mode  
将所有代码中格式化输出的方式由 “%” 方式更改为效率更高的 f-string 方式

- [X] Optimized type hints for some code  
优化了部分代码的类型提示

### Removed - 移除

- [X] Remove the function `text` and use f-string instead  
移除函数 `text`，可使用 f-string 来对其进行代替

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

- [ ] Solve the bug that the vertical position of the text is wrong when the `Text` class is enlarged  
解决 `Text` 类放大时，文本纵向位置错误的 bug

- [ ] Solve the bug that text shrinks and overflows after zooming text controls  
解决文本类控件缩放后文本产生缩水和溢出的 bug

- [ ] Fix the bug of deletion misalignment when there is too much text in the `Text` class  
解决 `Text` 类中文本过多时删减错位的 bug

- [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
3D 对象前后空间的位置关系在某些时候仍有问题

- [ ] When a widget is tapped, the widgets that follow it are also triggered  
点击控件时，其后面的控件也会被触发

---
[Last Version - 上个版本](../2.6.9/News.md) | [Next Version - 下个版本](../2.6.11/News.md)
