Release Notes - 版本发布说明
===========================

* Version - 最新版本 : `2.6.13`
* Release - 发布日期 : 2023/11/17

```
pip install tkintertools==2.6.13
```

Example - 样例演示
-----------------

* OS - 操作系统 : Windows11 23H2
* Interpreter - 解释器 : Python 3.12.0

以下样例展示了新功能标记文本和 3D 文本：

> ℹ️**Note - 注意**  
> 标记文本只是伴随着 Point，其文本大小并不会随着 Point 位置的变化而变化，但是 3D 文本不同，它的大小会随着空间位置变化而变化，但是它始终朝向我们

![png](example.png)

<details><summary><b>Source Code - 源代码</b></summary>

```python
import tkintertools as tkt
from tkintertools import tools_3d as t3d

root = tkt.Tk('3D', 1600, 900)
space = t3d.Space(root, 1600, 900, 0, 0, bg='black')
t3d.Line(space, [0, 0, 0], [200, 0, 0], width=2, fill='#FF0000')  # X
t3d.Line(space, [0, 0, 0], [0, 200, 0], width=2, fill='#00FF00')  # Y
t3d.Line(space, [0, 0, 0], [0, 0, 200], width=2, fill='#0000FF')  # Z
t3d.Point(space, [200, 0, 0], size=0, markuptext='X', markupfill='#FF0000', markupdelta=(0, 30))  # Markup Text X
t3d.Point(space, [0, 200, 0], size=0, markuptext='Y', markupfill='#00FF00', markupdelta=(0, 30))  # Markup Text Y
t3d.Point(space, [0, 0, 200], size=0, markuptext='Z', markupfill='#0000FF', markupdelta=(0, 30))  # Markup Text Z
t3d.Point(space, [0, 200, 200], fill='yellow', size=5, markuptext='Markup\nPoint', markupfill='white', markupdelta=(0, 30), markupfont=(tkt.FONT, 12))  # Markup Point
t3d.Text(space, [200, 200, 0], '3D Text', fill='orange')  # 3D Text
root.mainloop()
```

</details>

ChangeLog - 更新日志
-------------------

### Added - 新增

- [X] The submodule `tools_3d` adds markup text-related functions and corresponding parameters to the class `Point`: `markuptext`, `markupdelta`, `markupfont`, `markupfill`, and `markupjustify`  
子模块 `tools_3d` 的类 `Point` 新增标记文本相关功能以及对应参数：`markuptext`、`markupdelta`、`markupfont`、`markupfill` 和 `markupjustify`

- [X] Submodule `tools_3d` adds a new class `Text` to implement 3D text that is always facing us (unlike markup text, which has a zoom function)  
子模块 `tools_3d` 新增类 `Text` 来实现始终朝向我们的 3D 文本（与标记文本不同，其有缩放功能）

### Changed - 变更

- [X] The class `Switch` has been partially refactored from a stand-alone class to a subclass that inherits from the base class `BaseWidget`, and a number of methods have been added that are compatible with `BaseWidget`  
类 `Switch` 部分重构，由独立类变更为继承基类 `BaseWidget` 的子类，添加了许多和 `BaseWidget` 兼容的方法

- [X] Change the main code file name to main.py to avoid occupying the special file name \_\_main\_\_.py  
修改主代码文件名称为 main.py，避免占用特殊文件名 \_\_main\_\_.py

### Fixed - 修复

- [X] Fixed an bug where submodule `tools_3d` was reversed on Z coordinates, i.e., changing the spatial coordinate system from a left-handed coordinate system to a right-handed coordinate system  
修复子模块 `tools_3d` 在 Z 坐标上正负颠倒的问题，即，将空间坐标系由左手坐标系改为右手坐标系

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

- [ ] Solve the bug that text shrinks and overflows after zooming text controls  
解决文本类控件缩放后文本产生缩水和溢出的 bug

- [ ] Fix the bug of deletion misalignment when there is too much text in the `Text` class  
解决 `Text` 类中文本过多时删减错位的 bug

- [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
3D 对象前后空间的位置关系在某些时候仍有问题

---
[Last Version - 上个版本](../2.6.12/News.md) | [Version Content - 版本目录](../README.md) | [Next Version - 下个版本](../2.6.14/News.md)
