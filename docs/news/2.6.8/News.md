Release Notes - 版本说明
=======================

* Version - 最新版本 : `2.6.8`
* Release - 发布日期 : 2023/08/03

```
pip install tkintertools==2.6.8
```

Example - 样例演示
-----------------

* OS - 操作系统 : Windows11 22H2
* Interpreter - 解释器 : Python 3.11.4

Same effect as previous `2.6.7` version, but with less code!  
效果与之前 `2.6.7` 版本相同，但是代码量更少！

![gif](example.gif)

<details><summary><b>Source Code - 源代码</b></summary>

```python
import math  # 数学支持

import tkintertools as tkt  # 引入基础模块
from tkintertools import tools_3d as t3d  # 引入 3d 子模块

root = tkt.Tk('3D', 1280, 720)  # 创建窗口
space = t3d.Space(root, 1280, 720, 0, 0)  # 创建空间

for a in -100, 0, 100:
    for b in -100, 0, 100:
        for c in -100, 0, 100:
            t3d.Cuboid(space, a-50, b-50, c-50, 100, 100, 100,  # 创建正方体
                       color_up='white', color_down='yellow', color_left='red',
                       color_right='orange', color_front='blue', color_back='green')


def animate(value=[0]):  # type: (list[int]) -> None
    """ 动画 """
    for geo in space.geos():
        geo.rotate(dz=0.01)
        geo.translate(dz=math.sin(value[0]))
        geo.update()
    value[0] += math.pi/60
    space.space_sort()


def scale(event):
    """ 缩放事件 """
    k = 1.05 if event.keysym == 'equal' else 0.95 if event.keysym == 'minus' else 1  # 缩放比率
    for geo in space.geos():  # 遍历所有的几何体（不包括基本 3D 对象）
        geo.scale(k, k, k)  # 缩放
        geo.update()  # 更新改对象的实际画面
    space.space_sort()  # 空间前后位置排序


tkt.Animation(space, 1000, callback=lambda _: animate(), loop=True).run()  # 调用类 Animation
root.bind('<Key-equal>', scale)  # 绑定等号按键
root.bind('<Key-minus>', scale)  # 绑定减号按键
root.mainloop()  # 消息事件循环
```

</details>

ChangeLog - 更新日志
-------------------

### Added - 新增

- [X] If the user's Python includes a PIL library, PIL is automatically invoked when autoscaling images to extend the functionality of the class `PhotoImage`  
若使用者的 Python 包含有 PIL 库，则在自动缩放图片时自动调用 PIL 来扩展类 `PhotoImage` 的功能

- [X] Added class `Animation` to achieve more efficient, convenient and functional animation effects  
新增类 `Animation` 来实现更加高效、更加方便和功能性更强的动画效果

- [X] Added constant `CONTROL`  
新增常量 `CONTROL`

### Fixed - 修复

- [X] Fixed the bug that widgets `Entry` and `Text` would report an error when pasting text  
修复控件 `Entry` 和 `Text` 粘贴文本时会报错的 bug

> Thanks to netizens [一梦千年](mailto:1076336488@qq.com) for discovering the above bug  
感谢网友 [一梦千年](mailto:1076336488@qq.com) 发现了上面的 bug

### Changed - 变更

- [X] Modified the name of the constant `FRAMES` to `FPS`  
修改常量 `FRAMES` 的名称为 `FPS`

- [X] The parameter `precision` of the method `zoom` of class `PhotoImage` was changed from positional argument to keyword argument  
类 `PhotoImage` 的方法 `zoom` 的参数 `precision` 由位置参数变更为关键字参数

### Deprecated - 弃用

- [X] The function `move` is about to be deprecated, please replace it with the new class `Animation`  
函数 `move` 即将被弃用，请用新类 `Animation` 来代替

- [X] The class `Singleton` is about to be deprecated and singleton mode classes will no longer be available in subsequent releases  
类 `Singleton` 即将被弃用，后续版本中将不再提供单例模式类

Todos - 待办事项
---------------

### Possible Features - 期望功能

- [ ] Perfect the scroll bar function of `Text` class  
完善 `Text` 类的滚动条功能

- [ ] Perfection and optimization of zoom function  
对缩放功能的完善和优化

- [ ] Try adding a new widget: `Switch`  
尝试新增控件：开关 (`Switch`)

- [ ] Try adding a new widget: `ToolTip`  
尝试新增控件：提示框 (`ToolTip`)

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

- [ ] Add lights and achieve simple light and shadow renderings  
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
[Last Version - 上个版本](../2.6.7/News.md) | [Next Version - 下个版本](../2.6.9/News.md)
