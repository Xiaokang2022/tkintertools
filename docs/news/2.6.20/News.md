Release Notes - 版本发布说明
===========================

* Version - 最新版本 : `2.6.20`
* Release - 发布日期 : 2023/12/26

```
pip install tkintertools==2.6.20
```

ChangeLog - 更新日志
-------------------

### Optimized - 优化

- [X] The pause and resume functionality of the image class `PhotoImage` is encapsulated in the methods `pause` and `play`  
图片类 `PhotoImage` 的暂停和继续播放功能被封装为方法 `pause` 和 `play`

- [X] Optimized the way the `PhotoImage` class gets the total number of frames of a gif image, and now you can get the total number of frames by method `get_total_frames`  
优化类 `PhotoImage` 获取 gif 图片总帧数的方式，现在可以通过方法 `get_total_frames` 得到总帧数

- [X] The `color` function no longer manually obtains a gradient with a specified regularity, but instead specifies a control function through the parameter `controller`  
函数 `color` 不再通过手动方式得到指定规律的渐变色，而是通过参数 `controller` 指定一个控制函数

### Changed - 变更

- [X] The original method of `play` used for `PhotoImage` to start playback has been renamed to `start` to avoid conflicts with the method of `play` to continue playback  
图片类 `PhotoImage` 原来用于开始播放的方法 `play` 更名为 `start` 避免与继续播放的方法 `play` 起冲突

- [X] The constant `CONTROL` was renamed `CONTROLLER`  
常量 `CONTROL` 更名为 `CONTROLLER`

### Fixed - 修复

- [X] Fixed some incorrect type hints  
修复了一些错误的类型提示

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
