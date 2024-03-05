# Release Notes - 版本发布说明

-   Version - 最新版本 : `2.6.18`
-   Release - 发布日期 : 2023/12/10

```
pip install tkintertools==2.6.18
```

## ChangeLog - 更新日志

### Fixed - 修复

-   [x] Fixed a bug where the actual font size of 3D text with the same font size setting was inconsistent in different locations  
         修复在不同位置的但字体大小设定相同的 3D 文本的实际字体大小不一致的 bug

### Changed - 变更

-   [x] Class `Canvas_3D` was renamed `Canvas3D`, and Class `_3D_Object` was renamed to `_Object3D`  
         类 `Canvas_3D` 更名为 `Canvas3D`，类 `_3D_Object` 更名为 `_Object3D`

### Optimized - 优化

-   [x] Some codes have been optimized  
         优化了部分代码

## Todos - 待办事项

### Possible Features - 期望功能

-   [ ] Perfect the scroll bar function of `Text` class  
         完善 `Text` 类的滚动条功能

-   [ ] Perfection and optimization of zoom function  
         对缩放功能的完善和优化

-   [ ] Try adding support for some MarkDown syntax  
         尝试增加对部分 Markdown 语法的支持

-   [ ] Implement symmetry in 3D modules  
         实现 3D 模块中的对称功能

-   [ ] Enhanced projection functionality in 3D modules  
         增强 3D 模块中的投影功能

-   [ ] Add more 3D spatial geometry classes  
         增加更多 3D 空间几何体类

-   [ ] Add lights and achieve simple light and shadow renderings  
         添加光源，并实现简单的光影渲染的效果

-   [ ] Change the underlying calculation of the 3D submodule from "Euler angle" to "quaternion" to improve performance  
         改变 3D 子模块底层计算方式从“欧拉角”到“四元数”以提升性能

### Known Bugs - 已知问题

-   [ ] Solve the bug that text shrinks and overflows after zooming the `Text` class  
         解决 `Text` 类缩放后文本产生缩水和溢出的 bug

-   [ ] Fix the bug of deletion misalignment when there is too much text in the `Text` class  
         解决 `Text` 类中文本过多时删减错位的 bug

-   [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
         3D 对象前后空间的位置关系在某些时候仍有问题
