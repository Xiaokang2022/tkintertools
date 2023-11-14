Release Notes - 版本说明
=======================

* Version - 最新版本 : `2.6.9`
* Release - 发布日期 : 2023/08/09

```
pip install tkintertools==2.6.9
```

Example - 样例演示
-----------------

* OS - 操作系统 : Windows11 22H2
* Interpreter - 解释器 : Python 3.11.4

New widget: Switch! This widget allows you to adjust the length, width, color, and size of rounded corners!  
新增控件：开关！这个控件可以调整长宽、颜色、以及圆角的大小！

![png](example.png)

<details><summary><b>Source Code - 源代码</b></summary>

```python
# Only the key parts of the code are shown here

tkt.Switch(canvas, 540, 420)
tkt.Switch(canvas, 610, 420, radius=4, default=True)
tkt.Switch(canvas, 680, 420, radius=0)
```

</details>

ChangeLog - 更新日志
-------------------

### Added - 新增

- [X] Added new widget switch (`Switch`)  
新增控件开关（`Switch`）

- [X] Added widget Tip (`ToolTip`) and all virtual widgets added the parameter `tooltip`  
新增控件提示框（`ToolTip`），且所有虚拟控件新增参数 `tooltip`

- [X] Added constants `DURATION`、`TOOLTIP_FG`、`TOOLTIP_BG`、`TOOLTIP_HIGNLIGHT_THICKNESS`、`TOOLTIP_HIGNLIGHT_BACKGROUND`、`COLOR_SWITCH_ON`、`COLOR_SWITCH_OFF`、`SWITCH_WIDTH`、`SWITCH_HEIGHT`、`SWITCH_RADIUS` and `SWITCH_ANIMATION_MS`  
新增常量 `DURATION`、`TOOLTIP_FG`、`TOOLTIP_BG`、`TOOLTIP_HIGNLIGHT_THICKNESS`、`TOOLTIP_HIGNLIGHT_BACKGROUND`、`COLOR_SWITCH_ON`、`COLOR_SWITCH_OFF`、`SWITCH_WIDTH`、`SWITCH_HEIGHT`、`SWITCH_RADIUS` 和 `SWITCH_ANIMATION_MS`

### Fixed - 修复

- [X] Fixed an issue where the text class widget called method `clear` was invalid  
修复了文本类控件调用方法 `clear` 无效的问题

- [X] Fixed an issue where the class `Animation` automatically determined the parent widget of the widget to be moved  
修复了类 `Animation` 自动确定待移动控件的父控件时出现错误的问题

### Changed - 变更

- [X] The positional parameter `length` of class `CheckButton` was renamed `height`  
类 `CheckButton` 的位置参数 `length` 更名为 `height`

### Optimized - 优化

- [X] Optimized the method `wm_geometry` of class `Tk` to accommodate some specially formatted parameters  
优化了类 `Tk` 的方法 `wm_geometry` 以适应某些特殊格式的参数

### Removed - 移除

- [X] Removed class `Singleton` and function `move`  
移除了类 `Singleton` 和函数 `move`

Todos - 待办事项
---------------

### Possible Features - 期望功能

- [ ] Perfect the scroll bar function of `Text` class  
完善 `Text` 类的滚动条功能

- [ ] Perfection and optimization of zoom function  
对缩放功能的完善和优化

- [ ] Try adding support for some MarkDown syntax  
尝试增加对部分 Markdown 语法的支持

- [ ] Try adding a new pattern of no progress to the `Progressbar` widget  
尝试为进度条控件增加无进度的新模式

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

- [ ] Fix the bug where the method `place` of class `anvas` did not work correctly  
解决类 `Canvas` 的方法 `place` 无法正常工作的 bug

- [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
3D 对象前后空间的位置关系在某些时候仍有问题

- [ ] When a widget is tapped, the widgets that follow it are also triggered  
点击控件时，其后面的控件也会被触发

---
[Last Version - 上个版本](../2.6.8/News.md) | [Next Version - 下个版本](../2.6.10/News.md)
