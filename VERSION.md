version 2.5.3
-------------

1. Added singleton pattern class for inheritance  
增加了单例模式类供继承

2. Canvas class overrides destroy method to be compatible with the original destroy method  
Canvas 类重写 destroy 方法以兼容原 destroy 方法

3. Solved the bug that the destroy method of the control can only delete half of the controls when traversing  
解决了控件的 destroy 方法在遍历使用时只能删除一半控件的bug

4. Add some methods (attributes) of Tk, Toplevel and Canvas to access some attributes that should not be directly accessed  
增加 Tk、Toplevel、Canvas 的一些方法(属性)来访问一些不应该被直接访问的属性

5. Some codes of Tk and Toplevel are optimized, and the code amount of Toplevel controls is greatly reduced  
优化了 Tk、Toplevel 的部分代码，Toplevel 控件的代码量大大缩减

6. The proportion_lock parameter and its function of Tk and Toplevel are deleted  
删除了 Tk、Toplevel 的 proportion_lock 参数及其功能

7. Toplevel class overrides destroy method to be compatible with the original destroy method  
Toplevel 类重写 destroy 方法以兼容原 destroy 方法

version 2.5.2
-------------

1. Change the mouse position detection order to further improve the running speed  
改变鼠标位置检测顺序，进一步提升运行速度

2. Solved the bug that the set and append methods of text virtual controls may fail in some cases  
解决了文本类虚拟控件set、append方法某些时候会失效的bug

3. Solved the bug that the mouse style flickers when the mouse cursor moves over the button  
解决了鼠标光标移动到按钮上时的鼠标样式会闪烁的bug

4. Added mouse style for text type virtual control  
添加了对文本类虚拟控件的鼠标样式

5. Fixed the bug that the read parameter of the text box control failed  
修复了文本框控件read参数失效的bug

version 2.5.1
-------------

1. Solved the bug that the input prompt position was not aligned after the input box was enlarged  
解决了输入框放大后输入提示符位置没对齐的bug

2. Some redundant codes are deleted to improve the overall running speed  
删除了部分冗余代码，提升总体运行速度

3. Optimized the mouse position determination mechanism, improved the running speed, and added changes in the mouse style (for buttons)  
优化了鼠标位置判定机制，提升运行速度，并加入了鼠标样式的变化（对于按钮）

4. Solved the bug that text virtual controls will lose focus after being pasted once  
解决了文本类虚拟控件粘贴一次后会失去焦点的bug

5. Fix a few errors in the module documentation  
修复模块文档中的少许错误

version 2.5
-----------

* Big update  
大更新
