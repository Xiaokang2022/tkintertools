Release Notes - 版本发布说明
===========================

* Version - 最新版本 : `2.6.14`
* Release - 发布日期 : 2023/11/17

```
pip install tkintertools==2.6.14
```

Example - 样例演示
-----------------

* OS - 操作系统 : Windows11 23H2
* Interpreter - 解释器 : Python 3.12.0

Here's what you can expect after improving the settings of each parameter of the widget and fixing many bugs:  
下面是完善控件各个参数设定，修复了众多 bug 后所能呈现的效果：

![png](example_1.png)

The background is switched by the `Switch` action on the penultimate row.  
背景的切换通过倒数第二行的控件 `Switch` 操作得到。

![png](example_2.png)

<details><summary><b>Source Code - 源代码</b></summary>

```python
import webbrowser

import tkintertools as tkt


def colorful(canvas: tkt.Canvas, x: int, y: int, width: int, height: int, colortup: tuple[str, str], flag: bool = True) -> None:
    if flag:
        for i in range(width):
            fill = tkt.color(colortup, i / width)
            canvas.create_line(x + i, y, x + i, y + height, width=1, fill=fill)
    else:
        for i in range(height):
            fill = tkt.color(colortup, i / height)
            canvas.create_line(x, y + i, x + width, y + i, width=1, fill=fill)


root = tkt.Tk('tkintertools', 1280, 720)
canvas = tkt.Canvas(root, 1280, 720, 0, 0)
background = tkt.PhotoImage('background.png')
bg_item = canvas.create_image(640, 360, image=background)

colorful(canvas, 10, 360, 150, 40, ('#FF0000', '#00FF00'))
colorful(canvas, 170, 360, 250, 40, ('#00FF00', '#0000FF'))
colorful(canvas, 430, 360 + 5, 60, 30, ('#0000FF', '#FF0000'))
colorful(canvas, 500, 360, 200, 40, ('#00FFFF', '#FF00FF'))
colorful(canvas, 720, 360 + 5, 30, 30, ('#FF00FF', '#FFFF00'))
colorful(canvas, 935, 360 + 5, 335, 30, ('#FFFF00', '#00FFFF'))

colorful(canvas, 10, 410, 150, 40, ('#FF0000', '#00FF00'), False)
colorful(canvas, 170, 410, 250, 40, ('#00FF00', '#0000FF'), False)
colorful(canvas, 430, 410 + 5, 60, 30, ('#0000FF', '#FF0000'), False)
colorful(canvas, 500, 410, 200, 40, ('#00FFFF', '#FF00FF'), False)
colorful(canvas, 720, 410 + 5, 30, 30, ('#FF00FF', '#FFFF00'), False)
colorful(canvas, 935, 410 + 5, 335, 30, ('#FFFF00', '#00FFFF'), False)

tkt.Button(canvas, 10, 10, 150, 40, text='Button', radius=0)
tkt.Button(canvas, 10, 60, 150, 40, text='Button')
tkt.Button(canvas, 10, 110, 150, 40, text='Button', radius=20)
tkt.Button(canvas, 10, 160, 150, 40, text='Button').set_live(False)
tkt.Button(canvas, 10, 210, 150, 40, text='Button', radius=0, borderwidth=3)
tkt.Button(canvas, 10, 260, 150, 40, text='Button', color_fill=('lightgreen', 'springgreen', 'green'), color_outline=('grey', 'black', 'black'))
tkt.Button(canvas, 10, 310, 150, 40, text='Button', color_text=('orange', 'red', 'red'))
tkt.Button(canvas, 10, 360, 150, 40, text='Button', radius=0, color_fill=tkt.COLOR_NONE)
tkt.Button(canvas, 10, 410, 150, 40, text='Button', radius=0, color_fill=tkt.COLOR_NONE)
tkt.Button(canvas, 10, 460, 150, 40, text='Button', radius=0, color_fill=tkt.COLOR_NONE)
tkt.Button(canvas, 10, 510, 150, 40, text='Button', justify='left')
tkt.Button(canvas, 10, 560, 150, 40, text='Button', color_outline=('red', 'red', 'red'))
tkt.Button(canvas, 10, 610, 150, 40, text='Button', font=('华文行楷', tkt.SIZE))

tooltip = tkt.ToolTip("Click this to give me a star!\nThanks! (●'◡'●)")
tkt.Button(canvas, 10, 660, 150, 40, text='👉Like👈', tooltip=tooltip, command=lambda: webbrowser.open('https://github.com/Xiaokang2022/tkintertools'))

tkt.Entry(canvas, 170, 10, 250, 40, text=('Entry', 'Input'), radius=0)
tkt.Entry(canvas, 170, 60, 250, 40, text=('Entry', 'Input'))
tkt.Entry(canvas, 170, 110, 250, 40, text=('Entry', 'Input'), radius=20)
tkt.Entry(canvas, 170, 160, 250, 40, text=('Entry', 'Input')).set_live(False)
tkt.Entry(canvas, 170, 210, 250, 40, text=('Entry', 'Input'), radius=0, borderwidth=3)
tkt.Entry(canvas, 170, 260, 250, 40, text=('Entry', 'Input'), color_fill=('skyblue', 'cyan', 'cyan'), color_outline=('grey', 'black', 'black'))
tkt.Entry(canvas, 170, 310, 250, 40, text=('Entry', 'Input'), color_text=('lightgreen', 'springgreen', 'springgreen'))
tkt.Entry(canvas, 170, 360, 250, 40, text=('Entry', 'Input'), radius=0, color_fill=tkt.COLOR_NONE)
tkt.Entry(canvas, 170, 410, 250, 40, text=('Entry', 'Input'), radius=0, color_fill=tkt.COLOR_NONE)
tkt.Entry(canvas, 170, 460, 250, 40, text=('Entry', 'Input'), radius=0, color_fill=tkt.COLOR_NONE)
tkt.Entry(canvas, 170, 510, 250, 40, text=('Entry', 'Input'), justify='center')
tkt.Entry(canvas, 170, 560, 250, 40, text=('Entry', 'Input'), color_outline=('red', 'red', 'red'))
tkt.Entry(canvas, 170, 610, 250, 40, text=('Entry', 'Input'), font=('华文行楷', tkt.SIZE))
tkt.Entry(canvas, 170, 660, 250, 40, text=('Entry', 'Input'), show='●').set('Entry')

tkt.Switch(canvas, 430, 10 + 5, 30, radius=0)
tkt.Switch(canvas, 430, 60 + 5, 30, radius=4)
tkt.Switch(canvas, 430, 110 + 5, 30)
tkt.Switch(canvas, 430, 160 + 5, 30, radius=4).set_live(False)
tkt.Switch(canvas, 430, 210 + 5, 30, radius=0, borderwidth=3)
tkt.Switch(canvas, 430, 260 + 5, 30, default=True, color_fill_on=('orange', 'yellow', 'yellow'), color_outline_on=('grey', 'black', 'black'))
tkt.Switch(canvas, 430, 310 + 5, 30, color_fill_slider=('red', 'yellow', 'yellow'))
tkt.Switch(canvas, 430, 360 + 5, 30, radius=0, color_fill_on=tkt.COLOR_NONE, color_fill_off=tkt.COLOR_NONE)
tkt.Switch(canvas, 430, 410 + 5, 30, radius=0, color_fill_on=tkt.COLOR_NONE, color_fill_off=tkt.COLOR_NONE)
tkt.Switch(canvas, 430, 460 + 5, 30, radius=0, color_fill_on=tkt.COLOR_NONE, color_fill_off=tkt.COLOR_NONE)
tkt.Switch(canvas, 430, 510 + 10, 20, width=60, default=True)
tkt.Switch(canvas, 430, 560 + 5, 30, color_outline_on=('red', 'red', 'red'), color_outline_off=('red', 'red', 'red'))
tkt.Switch(canvas, 430, 610 + 5, 30, on=lambda: canvas.itemconfigure(bg_item, image=background), off=lambda: canvas.itemconfigure(bg_item, image=''), default=True)

tkt.Label(canvas, 500, 10, 200, 40, text='Label', radius=0)
tkt.Label(canvas, 500, 60, 200, 40, text='Label')
tkt.Label(canvas, 500, 110, 200, 40, text='Label', radius=20)
tkt.Label(canvas, 500, 160, 200, 40, text='Label').set_live(False)
tkt.Label(canvas, 500, 210, 200, 40, text='Label', radius=0, borderwidth=3)
tkt.Label(canvas, 500, 260, 200, 40, text='Label', color_fill=('lightpink', 'deeppink'), color_outline=('grey', 'black'))
tkt.Label(canvas, 500, 310, 200, 40, text='Label', color_text=('skyblue', 'cyan'))
tkt.Label(canvas, 500, 360, 200, 40, text='Label', radius=0, color_fill=tkt.COLOR_NONE)
tkt.Label(canvas, 500, 410, 200, 40, text='Label', radius=0, color_fill=tkt.COLOR_NONE)
tkt.Label(canvas, 500, 460, 200, 40, text='Label', radius=0, color_fill=tkt.COLOR_NONE, color_text=('grey', 'white', 'white'))
tkt.Label(canvas, 500, 510, 200, 40, text='Label', justify='right')
tkt.Label(canvas, 500, 560, 200, 40, text='Label', color_outline=('red', 'red', 'red'))
tkt.Label(canvas, 500, 610, 200, 40, text='Label', font=('华文行楷', tkt.SIZE))

tkt.CheckButton(canvas, 720, 10 + 5, 30, text='CheckButton', radius=0)
tkt.CheckButton(canvas, 720, 60 + 5, 30, text='CheckButton')
tkt.CheckButton(canvas, 720, 110 + 5, 30, text='CheckButton', radius=15)
tkt.CheckButton(canvas, 720, 160 + 5, 30, text='CheckButton').set_live(False)
tkt.CheckButton(canvas, 720, 210 + 5, 30, text='CheckButton', radius=0, borderwidth=3)
tkt.CheckButton(canvas, 720, 260 + 5, 30, text='CheckButton', color_fill=('skyblue', 'cyan', 'cyan'), color_outline=('grey', 'black', 'black'))
tkt.CheckButton(canvas, 720, 310 + 5, 30, text='CheckButton', color_text=('pink', 'orange', 'orange'))
tkt.CheckButton(canvas, 720, 360 + 5, 30, text='CheckButton', radius=0, color_fill=tkt.COLOR_NONE, color_text=('grey', 'white', 'white'))
tkt.CheckButton(canvas, 720, 410 + 5, 30, text='CheckButton', radius=0, color_fill=tkt.COLOR_NONE, color_text=('grey', 'white', 'white'))
tkt.CheckButton(canvas, 720, 460 + 5, 30, text='CheckButton', radius=0, color_fill=tkt.COLOR_NONE, color_text=('grey', 'white', 'white'))
tkt.CheckButton(canvas, 895, 510 + 5, 30, text='CheckButton', justify='left', color_text=('grey', 'white', 'white'))
tkt.CheckButton(canvas, 720, 560 + 5, 30, text='CheckButton', color_outline=('red', 'red', 'red'), color_text=('grey', 'white', 'white'))
tkt.CheckButton(canvas, 720, 610 + 5, 30, text='CheckButton', font=('华文行楷', tkt.SIZE), color_text=('grey', 'white', 'white'))
tkt.CheckButton(canvas, 720, 660 + 5, 30, text='CheckButton', tick='✕', value=True, color_text=('grey', 'white', 'white'))

tkt.ProgressBar(canvas, 935, 10 + 5, 335, 30)
tkt.ProgressBar(canvas, 935, 60 + 5, 335, 30).load(0.5)
tkt.ProgressBar(canvas, 935, 110 + 5, 335, 30).load(1)
tkt.ProgressBar(canvas, 935, 160 + 5, 335, 30).set_live(False)
tkt.ProgressBar(canvas, 935, 210 + 5, 335, 30, borderwidth=3)
tkt.ProgressBar(canvas, 935, 260 + 5, 335, 30, color_fill=('lightpink', 'deeppink'), color_outline=('grey', 'black')).load(2 / 3)
tkt.ProgressBar(canvas, 935, 310 + 5, 335, 30, color_text=('brown', 'red', 'red')).load(1 / 3)
tkt.ProgressBar(canvas, 935, 360 + 5, 335, 30, color_fill=('', 'pink')).load(1 / 6)
tkt.ProgressBar(canvas, 935, 410 + 5, 335, 30, color_fill=('', 'deeppink')).load(1 / 7)
tkt.ProgressBar(canvas, 935, 460 + 5, 335, 30, color_fill=('', 'skyblue'), color_text=('grey', 'white', 'white')).load(1 / 9)
tkt.ProgressBar(canvas, 935, 510 + 5, 335, 30, justify='left').load(5 / 7)
tkt.ProgressBar(canvas, 935, 560 + 5, 335, 30, color_outline=('red', 'red', 'red'))
tkt.ProgressBar(canvas, 935, 610 + 5, 335, 30, font=('华文行楷', tkt.SIZE))
tkt.ProgressBar(canvas, 935, 660 + 5, 335, 30, mode='indeterminate').load(0.3)

canvas.create_text(565 + 1, 680 + 1, text='Created by 小康2022', fill='grey')
canvas.create_text(565, 680, text='Created by 小康2022', fill='gold')

root.mainloop()
```

</details>

ChangeLog - 更新日志
-------------------

### Added - 新增

- [X] The `CheckButton` widget class adds a `font` parameter to modify its font  
控件类 `CheckButton` 新增参数 `font` 来修改其字体

### Changed - 变更

- [X] Modify the name of some color constants and the parameters related to some colors  
修改部分颜色常量的名称和部分颜色相关的参数

- [X] The widget class `Progressbar` is renamed to `ProgressBar`  
控件类 `Progressbar` 更名为 `ProgressBar`

### Fixed - 修复

- [X] Fixed the bug that the color of the `Switch` of the widget class was displayed incorrectly  
修复控件类 `Switch` 颜色显示错误的问题

- [X] Fixed an bug where the initial color of the `CheckButton` of the widget class would not be displayed immediately  
修复控件类 `CheckButton` 初始颜色不会立刻显示的问题

- [X] Fixed the bug that the text style of the widget class `Entry` was not updated after calling the method `set`  
修复控件类 `Entry` 在调用方法 `set` 之后文本样式没有更新的问题

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

### Known Bugs - 已知问题

- [ ] Solve the bug that text shrinks and overflows after zooming text controls  
解决文本类控件缩放后文本产生缩水和溢出的 bug

- [ ] Fix the bug of deletion misalignment when there is too much text in the `Text` class  
解决 `Text` 类中文本过多时删减错位的 bug

- [ ] The position relationship between the space before and after the 3D object is still problematic at some point  
3D 对象前后空间的位置关系在某些时候仍有问题
