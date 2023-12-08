Release Notes - 版本发布说明
===========================

* Version - 最新版本 : `2.6.17`
* Release - 发布日期 : 2023/12/07

```
pip install tkintertools==2.6.17
```

!!! danger "Note - 注意"
    After that, there will be no new features in the Series 2 version, but there will still be optimizations and bug fixes, and by the end of the year, the Series 2 version will be completely retired!  
    该版本之后，系列 2 版本将不会再新增任何功能，但仍会优化和修复 bug，到今年年底时，系列 2 版本将彻底停更！

    `tkintertools` for Series 3 is already in development, so stay tuned!  
    系列 3 的 `tkintertools` 已经在开发中了，敬请期待吧！

</details>

ChangeLog - 更新日志
-------------------

### Optimized - 优化

- [X] Corrected some incorrect English words  
修改了部分错误的英文单词

### Changed - 变更

- [X] The font unit changes from points to pixels  
字体单位由磅更改为像素

- [X] Reduced the display position offset of tooltip widgets  
减小了提示框控件的显示位置偏移

### Fixed - 修复

- [X] Fixed a bug where tooltip widgets could appear in very wrong places  
修复了提示框控件有可能显示在非常错误的位置的问题

- [X] Fixed a bug where the widget class `Entry` was in a non-centered state and the canvas was shrunk, entering an endless loop when entering text, causing the window to not respond  
修复了控件类 `Entry` 在非居中状态，且画布缩小之后，输入文本时进入死循环，导致窗口未响应的问题

- [X] Fixed a bug where widget color properties were sometimes unchangeable  
修复了控件颜色属性某些时候不可更改的问题

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
