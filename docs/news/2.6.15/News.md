Release Notes - 版本发布说明
===========================

* Version - 最新版本 : `2.6.15`
* Release - 发布日期 : 2023/11/26

```
pip install tkintertools==2.6.15
```

</details>

ChangeLog - 更新日志
-------------------

### Added - 新增

- [X] A new method for the `Animation` class is called `shutdown` to terminate the current animation  
类 `Animation` 新增方法 `shutdown` 来终止当前动画

- [X] The geometry class `Cuboid` and the geometry class `Tetrahedron` of submodule `tools_3d` have been initialized to increase the degree of freedom in style configuration  
子模块 `tools_3d` 的类 `Cuboid` 和类 `Tetrahedron` 新增一些初始化参数来提高样式配置的自由度

- [X] The constants `TCL`, `PROPORTION`, `SEQLENGTH`, and `NUM` are added  
新增常量 `TCL`、`PROPORTION`、`SEQLENGTH` 和 `NUM`

- [X] The `color` function adds the parameters `seqlength` and `num` to enhance the functionality  
函数 `color` 新增参数 `seqlength` 和 `num` 来增强功能

### Optimized - 优化

- [X] The parameter support for the function `color` has been expanded to support color names such as red, skyblue, and cyan2  
函数 `color` 的参数支持的范围扩大，可以支持诸如 red、skyblue 和 cyan2 等颜色名称

- [X] Some functions can be called without the need for a parent widget  
部分函数无需父控件即可调用

### Fixed - 修复

- [X] Fixed a bug where the function `color` would get an incorrect result in rare cases  
修复了函数 `color` 在罕见情况下会得到错误结果的问题

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

- [ ] Solve the bug that text shrinks and overflows after zooming text controls  
解决文本类控件缩放后文本产生缩水和溢出的 bug

- [ ] Fix the bug of deletion misalignment when there is too much text in the `Text` class  
解决 `Text` 类中文本过多时删减错位的 bug

- [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
3D 对象前后空间的位置关系在某些时候仍有问题

---
[Last Version - 上个版本](../2.6.14/News.md) | [Version Content - 版本目录](../README.md) | [Next Version - 下个版本](../3.0.0/News.md)
