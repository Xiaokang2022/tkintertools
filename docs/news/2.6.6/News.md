Release Notes - 版本发布说明
===========================

* Version - 最新版本 : `2.6.6`
* Release - 发布日期 : 2023/07/01

```
pip install tkintertools==2.6.6
```

ChangeLog - 更新日志
-------------------

### Added - 新增

- [X] The classes `_Point`, `_Line`, `_Side`, and `Geometry` of the 3D submodule all have a new method `center` that returns the geometric center of the 3D object  
3D 子模块的类 `_Point`、`_Line`、`_Side` 和 `Geometry` 都新增一个方法 `center` 返回该 3D 对象的几何中心

- [X] Added abstract class `_3D_Object` as the metabase class for classes `_Point`, `_Line`, and `_Side`  
新增抽象类 `_3D_Object` 来作为类 `_Point`、`_Line` 和 `_Side` 的元基类

### Optimized - 优化

- [X] Optimized parameter passing in 3D submodules, users do not need to ensure the transitivity of `list` at all times, and parameters that used to only use the `list` type are now `Iterable` type  
优化了 3D 子模块中的参数传递，使用者不需要时刻保证 `list` 的传递性，且原来只能使用 `list` 类型的参数现在为 `Iterable` 类型

- [X] The way 3D objects are centered in the 3D submodule has changed, which has improved performance and reduced the amount of code  
3D 子模块中 3D 对象居中方式改变，相比原来性能提升了不少，代码量也减少了

- [X] Corrected some incorrect type hints and improved some missing method comments  
改正了部分错误的类型提示，完善了部分缺少的方法注释

- [X] In the 3D submodule, the distance between two points was originally calculated with the function `hypot`, and now the function `dist` is used directly to calculate the Euclidean distance between two points to improve performance  
3D 子模块中原来用函数 `hypot` 计算两点间距离，现在直接用函数 `dist` 计算两点间欧几里得距离，提高性能

- [X] The position display of widgets of class `Point` has been optimized in the 3D submodule so that it is always at the forefront  
3D 子模块中优化了类 `Point` 的控件位置显示，让其始终保持在最前

- [X] The calculation formula for the camera distance in the 3D submodule has been optimized to improve the performance by a bit  
3D 子模块中相机距离的计算公式优化，提高了一点性能

### Changed - 变更

- [X] The parameters `point1` and `point2` of class `Point` of the 3D submodule and its parent class `_Point` were renamed to `point_start` and `point_end` respectively  
3D 子模块的类 `Point` 及其父类 `_Point` 的参数 `point1` 和 `point2` 分别被重命名为 `point_start` 和 `point_end`

- [X] The parameter `origin_color` of the class `Space` of the 3D submodule has been changed to four new parameters, namely `origin_size`, `origin_width`, `origin_fill` and `origin_outline`  
3D 子模块的类 `Space` 的参数 `origin_color` 被更改为四个新的参数，分别是 `origin_size`、`origin_width`、`origin_fill` 和 `origin_outline`

### Removed - 移除

- [X] The classes `Canvas_3D` and `Space` of the 3D submodule remove the parameters `dx` and `dy`, and the default field of view of the canvas remains centered, i.e. their center is now the original upper-left vertex  
3D 子模块的类 `Canvas_3D` 和 `Space` 移除参数 `dx` 和 `dy`，画布默认视野保持居中，也就是说，现在它们的中心位置才是原来的左上角顶点

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
实现3d模块中的对称功能

- [ ] Enhanced projection functionality in 3D modules  
增强 3D 模块中的投影功能

- [ ] Add more 3D spatial geometry classes  
增加更多 3D 空间几何体类

- [ ] Add lights and achieve simple light and shadow renderings  
添加光源，并实现简单的光影渲染的效果

### Known Bugs - 已知问题

- [ ] Solve the bug that the vertical position of the text is wrong when the `Text` class is enlarged  
解决 `Text` 类放大时，文本纵向位置错误的 bug

- [ ] Solve the bug that text shrinks and overflows after zooming text widgets  
解决文本类控件缩放后文本产生缩水和溢出的 bug

- [ ] Fix the bug of deletion misalignment when there is too much text in the `Text` class  
解决 `Text` 类中文本过多时删减错位的 bug

- [ ] Fix the bug where the method `place` of class `anvas` did not work correctly  
解决类 `Canvas` 的方法 `place` 无法正常工作的 bug

- [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
3D 对象前后空间的位置关系在某些时候仍有问题

- [ ] When creating a 3D object of concave geometry, calling its `scale` method displays an error  
创建凹面几何体的 3D 对象时，调用其 `scale` 方法会显示错误
