---
comments: true
---

# Release Notes - 版本发布说明

## Framework - 框架

-   Version - 最新版本 : `3.0.0.alpha7`
-   Last Update - 上次更新 : 2024/05/05

### Change Things - 更新内容

- [X] Introducing a pure Python-based third-party module, `darkdetect`, to implement theme dynamic following system and multi-OS dark theme support   
引入纯 Python 实现的第三方模块 `darkdetect`，以实现主题动态跟随系统以及多操作系统暗黑主题的支持 

- [X] Added text class widget  
新增文本类小部件

- [X] Fixed a few bugs and added a lot of content to the framework  
修复些许 bug，框架内增加大量内容

- [X] Some basic dialogs have been added  
增加了部分基本对话框

### Base Test - 基础测试

- **Light Mode**

![png](./light.png)

- **Dark Mode**

![png](./dark.png)

??? note "Test Code - 测试代码"

    ```python
    """Test"""

    import math
    import typing

    import tkintertools as tkt
    import tkintertools.animate.animations as animations
    import tkintertools.animate.controllers as controllers
    import tkintertools.constants as constants
    import tkintertools.standard.features as features
    import tkintertools.standard.shapes as shapes
    import tkintertools.standard.texts as texts
    import tkintertools.style as style

    root = tkt.Tk(title=f"tkintertools {tkt.__version__}")
    root.center()

    canvas = tkt.Canvas(root, free_anchor=True, keep_ratio="full", zoom_item=True)
    canvas.place(width=1280, height=720, x=640, y=360, anchor="center")

    constants.IS_WIN10 = False

    tkt.Information(canvas, (100, 100), (200, 50), text="Information")
    tkt.Label(canvas, (350, 100), (100, 50), text='Label')
    tkt.Button(canvas,  (500, 100), (100, 50), text='Button')
    tkt.UnderlineButton(canvas, (650, 100), (200, 50), text='UnderlineButton')
    tkt.HighlightButton(canvas, (900, 100), (200, 50), text='HighlightButton')

    tkt.Entry(canvas, (100, 200), (200, 40))
    tkt.Switch(canvas, (350, 200), 60, default=True)
    tkt.CheckButton(canvas, (500, 200), 30, default=True)
    tkt.RadioButton(canvas, (550, 200), 24)
    pb1 = tkt.ProgressBar(canvas, (650, 200), (450, 8))
    pb2 = tkt.ProgressBar(canvas, (650, 200+30), (450, 20))

    animations.Animation(2000, controllers.smooth, callback=pb1.set,
                        fps=60, repeat=math.inf).start(delay=0)
    animations.Animation(2000, controllers.smooth, callback=pb2.set,
                        fps=60, repeat=math.inf).start(delay=500)

    constants.IS_WIN10 = True

    tkt.Information(canvas, (100, 300), (200, 50), text="Information")
    tkt.Label(canvas, (350, 300), (100, 50), text='Label')
    tkt.Button(canvas,  (500, 300), (100, 50), text='Button')
    tkt.UnderlineButton(canvas, (650, 300), (200, 50), text='UnderlineButton')
    tkt.HighlightButton(canvas, (900, 300), (200, 50), text='HighlightButton')

    tkt.Entry(canvas, (100, 400), (200, 40))
    tkt.Switch(canvas, (350, 400), 60)
    tkt.CheckButton(canvas, (500, 400), 30)
    tkt.RadioButton(canvas, (550, 400), 24).set(False)
    pb3 = tkt.ProgressBar(canvas, (650, 400), (450, 8))
    pb4 = tkt.ProgressBar(canvas, (650, 400+30), (450, 20))


    animations.Animation(2000, controllers.smooth, callback=pb3.set,
                        fps=60, repeat=math.inf).start(delay=1000)
    animations.Animation(2000, controllers.smooth, callback=pb4.set,
                        fps=60, repeat=math.inf).start(delay=1500)


    constants.IS_WIN10 = False


    class MyCustomButton(tkt.Widget):

        def __init__(
            self,
            id: int,
            master: tkt.Canvas,
            position: tuple[int, int],
            size: tuple[int, int],
            *,
            text: str = "",
            family: str = constants.FONT,
            fontsize: int = constants.SIZE,
            weight: typing.Literal['normal', 'bold'] = "normal",
            slant: typing.Literal['roman', 'italic'] = "roman",
            underline: bool = False,
            overstrike: bool = False,
            command: typing.Callable | None = None,
        ) -> None:
            if id == 2:
                position[1] -= 25
                size = 100, 100
            tkt.Widget.__init__(self, master, position, size)
            s1 = style.get(tkt.Button, shapes.Rectangle)
            s2 = style.get(tkt.Button, shapes.RoundedRectangle)
            match id:
                case 0: shapes.Rectangle(self)
                case 1: shapes.Oval(self, styles=s1)
                case 2: shapes.RegularPolygon(self, side=5)
                case 3: shapes.RoundedRectangle(self, styles=s2)
                case 4: shapes.SemicircularRectangle(self, styles=s2)
                case 5: shapes.SharpRectangle(self, styles=s1)
                case 6: shapes.Parallelogram(self, styles=s1)
            texts.Information(self, text=text, family=family, size=fontsize, weight=weight,
                            slant=slant, underline=underline, overstrike=overstrike,
                            styles=style.get(tkt.Button, texts.Information))
            features.Button(self, command=command)


    for i in range(7):
        x = 100 + i*150
        MyCustomButton(i, canvas, [x, 550], (100, 50), text="MCB")


    root.mainloop()
    ```

### 3D Test - 3D 测试

![3D](./3D.png)

??? note "Test Code - 测试代码"

    ```python
    import math

    import tkintertools as tkt
    import tkintertools.animate.controllers as controllers
    from tkintertools import animate, three

    root = tkt.Tk((1600, 900))
    root.theme(background="black")
    space = three.Space(root, keep_ratio="full", bg="black", free_anchor=True,
                        highlightbackground="white")
    space.place(width=1600, height=900, x=800, y=450, anchor="center")
    space.update_idletasks()

    r = 300

    O = three.Point(space, [0, 0, 0], fill='white', size=3)
    X = three.Line(space, [0, 0, 0], [1, 0, 0], fill='')
    Y = three.Line(space, [0, 0, 0], [0, 1, 0], fill='')
    Z = three.Line(space, [0, 0, 0], [0, 0, 1], fill='')

    ring: dict[str, list[three.Text3D]] = {'x': [], 'y': [], 'z': []}
    line: dict[str, list[three.Text3D]] = {'x': [], 'y': [], 'z': []}

    for i in range(26):
        t = chr(65+i)
        φ = i/26 * math.tau
        c1 = r * math.sin(φ)
        c2 = r * math.cos(φ)
        ring['x'].append(three.Text3D(space, [0, c1, c2], text=t, fill='#FF0000'))
        ring['y'].append(three.Text3D(space, [c1, 0, c2], text=t, fill='#00FF00'))
        ring['z'].append(three.Text3D(space, [c1, c2, 0], text=t, fill='#0000FF'))

    for i in range(10):
        t = str(i)
        c = (i+1) * 600/11 - r
        line['x'].append(three.Text3D(space, [c, 0, 0], text=t, fill='#00FFFF'))
        line['y'].append(three.Text3D(space, [0, c, 0], text=t, fill='#FF00FF'))
        line['z'].append(three.Text3D(space, [0, 0, c], text=t, fill='#FFFF00'))


    def animation():
        for obj3D in ring['x']:
            obj3D.rotate(0.05, axis=X.coordinates)
        for obj3D in ring['y']:
            obj3D.rotate(0.05, axis=Y.coordinates)
        for obj3D in ring['z']:
            obj3D.rotate(0.05, axis=Z.coordinates)
        for obj3D in line['x']:
            obj3D.rotate(-0.05, axis=Y.coordinates)
        for obj3D in line['y']:
            obj3D.rotate(-0.05, axis=Z.coordinates)
        for obj3D in line['z']:
            obj3D.rotate(-0.05, axis=X.coordinates)
        for obj3D in space.items_3d():
            obj3D.rotate(0, -0.01, 0.01, center=O.center())
            obj3D.update()


    animate.Animation(1000, controllers.flat, repeat=math.inf,
                    callback=lambda _: animation()).start()


    root.mainloop()
    ```

## Designer - 设计器

The designer is in development mode  
设计器已进入开发状态

!!! info "Important - 重要"

    When tkintertools 3 enters beta, Designer will be detached from the tkintertools project and become a separate project to reduce the size of the project when it is packaged by users in the future.  
    tkintertools 3 进入 beta 版本后，designer 将从 tkintertools 项目中分离，并成为一个单独的项目，以减小未来用户打包时项目的大小。

### Light Theme - 明亮主题

![png](./example_1.png)

### Dark Theme - 暗黑主题

![png](./example_2.png)

### Start Designer - 启动设计器

You can start using the command below  
你可以使用下面的命令启动

```sh linenums="0"
python -m tkintertools [options]
```

In addition to this, you can also run the following Python code to start  
除此之外，你还可以运行下面的 Python 代码启动

```python
from tkintertools import designer

designer.run()
```
