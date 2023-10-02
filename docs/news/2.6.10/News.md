News/最新功能👇
--------------

### Release Notes/版本说明

**最新版本: `tkintertools-v2.6.10`**

> **Note**   
> tkintertools 的介绍、使用教程和开发文档均在 [Wiki](https://github.com/Xiaokang2022/tkintertools/wiki) 中，大家可前往查阅  
> **后面的时间里，将对 tkintertools 进行重构，以修复和完善前期版本无法解决的问题，故短期内不再更新，敬请期待！**

下面是本次开发版本（`v2.6.9` -> `v2.6.10`）的更新内容条目：

- [X] Added file exceptions.py and exception classes `ScaleArgsValueError`, `ColorArgsValueError` and `WidgetStateModeError` to provide a description of some exceptions  
新增文件 exceptions.py 及异常类 `ScaleArgsValueError`、`ColorArgsValueError` 和 `WidgetStateModeError` 以提供部分异常的描述
- [X] The widget `Progressbar` adds a indeterminate mode  
控件 `Progressbar` 新增不定模式
- [X] The value of the constant `SWITCH_WIDTH` is changed from 0 to 60  
常量 `SWITCH_WIDTH` 的值从 0 更改为 60
- [X] The parameter `width` of class `Switch` was changed from positional argument to keyword argument  
类 `Switch` 的参数 `width` 由位置参数更改为关键字参数
- [X] Change the way the output is formatted in all code from the "%" mode to the more efficient f-string mode  
将所有代码中格式化输出的方式由 “%” 方式更改为效率更高的 f-string 方式
- [X] Optimized type hints for some code  
优化了部分代码的类型提示
- [X] Remove the function `text` and use f-string instead  
移除函数 `text`，可使用 f-string 来对其进行代替

### Template Demo/模板演示

下面是一个主要新功能的示例程序：进度条控件为不定模式

下面是示例程序的效果图（运行环境为 **Windows11 家庭中文版 23H2 - Python3.11.4**）：

![news](news.png)

<details><summary><b>src/源代码</b></summary>

```python
# 此处只展示核心代码

pb = tkt.Progressbar(canvas, 320, 320, 640, 35, mode='indeterminate')  # 不定模式
pb.load(0.7)  # 加载到 70% 的状态
```

</details>
