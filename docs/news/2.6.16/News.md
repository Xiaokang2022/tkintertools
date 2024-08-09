# Release Notes - 版本发布说明

-   Version - 最新版本 : `2.6.16`
-   Release - 发布日期 : 2023/12/01

```
pip install tkintertools==2.6.16
```

## ChangeLog - 更新日志

### Added - 新增

-   [x] The `ToolTip` class has added a `delay` parameter to enhance functionality  
        类 `ToolTip` 新增参数 `delay` 来增强功能

### Optimized - 优化

-   [x] The function `askfont` has been optimized so that the font selection dialog can now be opened without the need for a parent container widget  
        对函数 `askfont` 进行了优化，现在无需父容器控件也可以打开字体选择对话框

### Changed - 变更

-   [x] The values of some constants have been modified  
        部分常量的值进行了修改

### Removed - 移除

-   [x] Removed the function `SetProcessDpiAwareness` and the constant `PROCESS_SYSTEM_DPI_AWARE`  
        移除函数 `SetProcessDpiAwareness` 和常量 `PROCESS_SYSTEM_DPI_AWARE`

### Fixed - 修复

-   [x] Fixed the bug that the font size of the menu bar was abnormal  
        修复菜单栏字体大小异常的问题

-   [x] Fixed the bug that images could not be loaded  
        修复图片无法加载的问题

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

-   [ ] Solve the bug that text shrinks and overflows after zooming text widgets  
        解决文本类控件缩放后文本产生缩水和溢出的 bug

-   [ ] Fix the bug of deletion misalignment when there is too much text in the `Text` class  
        解决 `Text` 类中文本过多时删减错位的 bug

-   [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
        3D 对象前后空间的位置关系在某些时候仍有问题
