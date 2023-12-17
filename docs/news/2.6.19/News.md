Release Notes - 版本发布说明
===========================

* Version - 最新版本 : `2.6.19`
* Release - 发布日期 : 2023/12/17

```
pip install tkintertools==2.6.19
```

Example - 样例演示
-----------------

* OS - 操作系统 : Windows11 23H2
* Interpreter - 解释器 : Python 3.12.0

The following action demonstrates the new use of the `PhotoImage` class:  
下面的操作演示了类 `PhotoImage` 的新用法：

!!! note "Example Code"

    ```python
    import tkintertools as tkt

    root = tkt.Tk('PhotoImage Test', 1600, 900, 0, 0)
    canvas = tkt.Canvas(root, 1600, 900, 0, 0)

    gif = tkt.PhotoImage('example.gif')
    image = canvas.create_image(800, 450)

    for _ in gif.parse():  # Pre-parsing, you can not do it (if you don't do it, it is runtime parsing)
        pass

    gif.play(canvas, image, 30)

    root.after(1000, canvas.lock, False)  # Paused after 1000ms
    root.after(2000, canvas.lock, True)  # Play after 2000ms
    root.after(10000, gif.stop, image)  # Terminated after 10000ms

    root.mainloop()
    ```

ChangeLog - 更新日志
-------------------

[`2.6.19`] - 2023-12-17
-----------------------

### Fixed - 修复

- [X] Fixed a bug where GIFs could not be played  
修复了 gif 动图无法播放的问题

### Optimized - 优化

- [X] `PhotoImage` has optimized the mechanism of playing GIFs, and if there is no pre-parsing before playback, it will be automatically parsed during playback  
图片类 `PhotoImage` 关于播放 gif 动图的机制得到优化，若播放前没有预解析，则会自动进行播放时解析

- [X] Some codes have been optimized  
优化了部分代码

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

- [ ] Change the underlying calculation of the 3D submodule from "Euler angle" to "quaternion" to improve performance  
改变 3D 子模块底层计算方式从“欧拉角”到“四元数”以提升性能

### Known Bugs - 已知问题

- [ ] Solve the bug that text shrinks and overflows after zooming the `Text` class  
解决 `Text` 类缩放后文本产生缩水和溢出的 bug

- [ ] Fix the bug of deletion misalignment when there is too much text in the `Text` class  
解决 `Text` 类中文本过多时删减错位的 bug

- [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
3D 对象前后空间的位置关系在某些时候仍有问题
