# Release Notes - 版本发布说明

-   Version - 最新版本 : `2.6.7`
-   Release - 发布日期 : 2023/07/06

```
pip install tkintertools==2.6.7
```

## Example - 样例演示

-   OS - 操作系统 : Windows11 22H2
-   Interpreter - 解释器 : Python 3.11.4

Hold down the left mouse button and drag to rotate these multiple geometry;  
按住鼠标左键拖动可以旋转这多个几何体；

Right-click and drag to move the position of these geometries in space;  
按住鼠标右键拖动可以移动这些几何体在空间中的位置；

Scroll the middle mouse button to zoom in and out of the picture;  
滚动鼠标中键可以放大和缩小画面；

These multiple geometries automatically rotate and float up and down;  
这多个几何体会自动地旋转以及上下浮动；

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


def spin():
    """ 自动旋转 """
    for geo in space.geos():
        geo.rotate(dz=0.01)


def floating(value):
    """ 上下浮动 """
    for geo in space.geos():
        geo.translate(dz=math.sin(value))


def animation(value=0):
    """ 形成动画 """
    spin()
    floating(value)
    space.space_sort()  # 给它们的空间位置排序以正确显示
    for geo in space.geos():
        geo.update()
    space.after(10, animation, value+math.pi/60)


def scale(event):
    """ 缩放事件 """
    k = 1.05 if event.keysym == 'equal' else 0.95 if event.keysym == 'minus' else 1  # 缩放比率
    for geo in space.geos():  # 遍历所有的几何体（不包括基本 3D 对象）
        geo.scale(k, k, k)  # 缩放
        geo.update()  # 更新改对象的实际画面
    space.space_sort()  # 空间前后位置排序


animation()
root.bind('<Key-equal>', scale)  # 绑定等号按键
root.bind('<Key-minus>', scale)  # 绑定减号按键
root.mainloop()  # 消息事件循环
```

</details>

## ChangeLog - 更新日志

### Added - 新增

-   [x] The function `rotate` of the 3D submodule adds the keyword `axis` to provide the function of rotating around the axis  
        3D 子模块的函数 `rotate` 新增关键字参数 `axis` 来提供绕轴旋转的功能

-   [x] Added constants `ROTATE_CENTER`, `ORIGIN_COORDINATE`, `ORIGIN_SIZE`, `ORIGIN_WIDTH`, `ORIGIN_FILL` and `ORIGIN_OUTLINE`  
        新增常量 `ROTATE_CENTER`、`ORIGIN_COORDINATE`、`ORIGIN_SIZE`、`ORIGIN_WIDTH`、`ORIGIN_FILL` 和 `ORIGIN_OUTLINE`

-   [x] Class `Tk` and `Toplevel` Added keyword arguments `alpha`, `toolwindow`, `topmost` and `transparentcolor`  
        类 `Tk` 和 `Toplevel` 新增关键字参数 `alpha`、`toolwindow`、`topmost` 和 `transparentcolor`

### Fixed - 修复

-   [x] Fixed a bug where the class `Text` would report an error when scrolling with the mouse wheel  
        修复了类 `Text` 在使用鼠标滚轮滚动时会报错的 bug

### Optimized - 优化

-   [x] Optimized some code and type hints  
        优化了部分代码和类型提示

-   [x] Optimized the internal implementation of the functions `translate` and `scale` to improve performance  
        优化函数 `translate`、`rotate` 和 `scale` 内部的实现，提高了性能

-   [x] A large number of incomplete docstrings have been modified and improved  
        修改和完善了大量的不完整的文档注释

### Changed - 变更

-   [x] Change some methods of some classes to protection methods  
        将部分类的部分方法更改为保护方法

### Removed - 移除

-   [x] Removed abstract classes and abstract methods  
        移除了抽象类和抽象方法

## Todos - 待办事项

### Possible Features - 期望功能

-   [ ] Perfect the scroll bar function of `Text` class  
        完善 `Text` 类的滚动条功能

-   [ ] Perfection and optimization of zoom function  
        对缩放功能的完善和优化

-   [ ] Try adding a new widget: `Switch`  
        尝试新增控件：开关 (`Switch`)

-   [ ] Try adding a new widget: `ToolTip`  
        尝试新增控件：提示框 (`ToolTip`)

-   [ ] Try adding support for some MarkDown syntax  
        尝试增加对部分 Markdown 语法的支持

-   [ ] Try adding a new pattern of no progress to the `Progressbar` widget  
        尝试为进度条控件增加无进度的新模式

-   [ ] Implement symmetry in 3D modules  
        实现 3D 模块中的对称功能

-   [ ] Enhanced projection functionality in 3D modules  
        增强 3D 模块中的投影功能

-   [ ] Add more 3D spatial geometry classes  
        增加更多 3D 空间几何体类

-   [ ] Add lights and achieve simple light and shadow renderings  
        添加光源，并实现简单的光影渲染的效果

### Known Bugs - 已知问题

-   [ ] Solve the bug that the vertical position of the text is wrong when the `Text` class is enlarged  
        解决 `Text` 类放大时，文本纵向位置错误的 bug

-   [ ] Solve the bug that text shrinks and overflows after zooming text controls  
        解决文本类控件缩放后文本产生缩水和溢出的 bug

-   [ ] Fix the bug of deletion misalignment when there is too much text in the `Text` class  
        解决 `Text` 类中文本过多时删减错位的 bug

-   [ ] Fix the bug where the method `place` of class `anvas` did not work correctly  
        解决类 `Canvas` 的方法 `place` 无法正常工作的 bug

-   [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
        3D 对象前后空间的位置关系在某些时候仍有问题
