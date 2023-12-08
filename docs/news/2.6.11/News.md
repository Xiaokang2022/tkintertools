Release Notes - 版本发布说明
===========================

* Version - 最新版本 : `2.6.11`
* Release - 发布日期 : 2023/10/17

```
pip install tkintertools==2.6.11
```

Example - 样例演示
-----------------

* OS - 操作系统 : Windows11 22H2
* Interpreter - 解释器 : Python 3.12.0

The following code has different results between the two versions, the result of `2.6.11` is significantly better than `2.6.10`, and the improvement can be calculated by comparing the frame rate.  
下面的代码在两个版本间的结果不同，`2.6.11` 的结果要优于 `2.6.10`，通过比较帧率可以计算得到提升效果。

!!! info "说明"
    My computer configuration is low, the frame rate is for reference only, the instantaneous frame rate is not very stable, and my computer screenshots and other background operations are related, the specific results please refer to the average value.  
    我的电脑配置较低，帧率仅供参考，瞬时帧率不是非常稳定，与我电脑截屏和其他后台操作有关，具体结果请以平均值为准。

tkintertools `2.6.10` (FPS: 21.75, Avg: 23.42): 

![png](example1.png)

tkintertools `2.6.11` (FPS: 21.30, Avg: 26.15): 

![png](example2.png) 

<details><summary><b>Source Code - 源代码</b></summary>

```python
import random
import time
import tkintertools as tkt
from tkintertools import tools_3d as t3d


class TestSpace(t3d.Space):
    """Test Space class"""

    def __init__(self, master, width, height, x, y):
        super().__init__(master, width, height, x, y)
        self.info = self.create_text(-640+10, -360+10, anchor='nw')

    def space_sort(self, t=[0, 0, 1]) -> None:
        # override: caculate FPS, t: [time of now, total FPS, count]
        now = time.time()
        fps = 1 - (now - t[0])
        super().space_sort()
        self.itemconfigure(
            self.info, text='FPS: %.2f\nAvg: %.2f' % (fps, t[1] - t[2]))
        t[0] = now
        t[1] += fps
        t[2] += 1


root = tkt.Tk('3D', 1280, 720)
space = TestSpace(root, 1280, 720, 0, 0)
cuboid_lst = []

for _ in range(64):  # 64 cubes are randomly generated
    x = random.randint(-100, 100)
    y = random.randint(-100, 100)
    z = random.randint(-100, 100)
    length = random.randint(-100, 100)
    width = random.randint(-100, 100)
    height = random.randint(-100, 100)
    cuboid_lst.append(t3d.Cuboid(
        space, x, y, z, length, width, height,
        color_up='white', color_down='yellow', color_left='red',
        color_right='orange', color_front='blue', color_back='green'))


def spin():
    for cuboid in cuboid_lst:
        cuboid.rotate(dy=0.1, dz=0.2)
        cuboid.update()
    space.space_sort()
    space.after(1, spin)


spin()  # Rotate 3D objects!
root.mainloop()
```

</details>

ChangeLog - 更新日志
-------------------

### Optimized/优化

- [X] Optimized the code of submodule `tools_3d`, introduced built-in module `array` instead of the underlying list to improve the calculation speed, and improved the overall performance by **11.66%** !  
优化了子模块 `tools_3d` 的代码，引入内置模块 `array` 代替底层列表来提高计算速度，综合性能提升 **11.66%** ！

### Removed/移除

- [X] Removed classes `_Point`, `_Line` and `_Side` from submodule `tools_3d`  
移除了子模块 `tools_3d` 中的类 `_Point`、`_Line` 和 `_Side`

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

- [ ] Solve the bug that text shrinks and overflows after zooming text widgets  
解决文本类控件缩放后文本产生缩水和溢出的 bug

- [ ] Fix the bug of deletion misalignment when there is too much text in the `Text` class  
解决 `Text` 类中文本过多时删减错位的 bug

- [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
3D 对象前后空间的位置关系在某些时候仍有问题

- [ ] When a widget is tapped, the widgets that follow it are also triggered  
点击控件时，其后面的控件也会被触发
