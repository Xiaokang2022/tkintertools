# Release Notes - 版本发布说明

-   Version - 最新版本 : `2.6.21`
-   Release - 发布日期 : 2024/01/01

```
pip install tkintertools
```

!!! danger "Attention - 特别注意"

    This will be the last version of `tkintertools 2.*` and will not be updated in any future!
    这将是 `tkintertools 2.*` 的最后一个版本，后续将不再得到任何的更新！

    `tkintertools 3.0` will be available soon!
    `tkintertools 3.0` 将在不久后推出！

## ChangeLog - 更新日志

### Changed - 变更

-   [x] The class `Text` in submodule `tools_3d` was renamed `Text3D` to distinguish `Text` in `main`  
        子模块 `tools_3d` 中的类 `Text` 更名为 `Text3D` 以区分 `main` 中的 `Text`

### Optimized - 优化

-   [x] Improved Type Hints  
        完善了类型提示

### Fixed - 修复

-   [x] Fixed a bug where the parameter `proportion` of the function `color` was invalid  
        修复了函数 `color` 的参数 `proportion` 失效的问题

-   [x] Fixed a bug where the `configure` parameter of the `Switch` class was incorrect
        修复了类 `Switch` 的方法 `configure` 参数取值错误的问题

### Removed - 移除

-   [x] `Animation` has removed the `color` parameter (can be implemented with the `callback` parameter)  
        动画类 `Animation` 移除了参数 `color`（可用参数 `callback` 代替实现）

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
