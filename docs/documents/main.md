tkintertools.main
===

描述: Main File  
外部引用: `Image`, `ImageTk`, `fractions`, `math`, `tkinter`, `typing`  
源代码位置: site-packages\tkintertools\main.py

Functions - 函数
---

### 01. askfont

!!! note "askfont `Function`"

    ```python
    askfont(
        bind=None,
        initfont=''
    )
    ```

    字体选择对话框，弹出选择字体的默认对话框窗口

    * `bind`: 关联的回调函数，有且仅有一个参数 `font`
    * `initfont`: 初始字体，格式为 `font` 参数默认格式

    注意: 由于 `tkinter` 模块无法直接打开该窗口，所以此处添加了这个函数
    
### 02. color

!!! note "color `Function`"

    ```python
    color(
        __color,
        /,
        proportion=1.0,
        *,
        seqlength=1,
        num=2
    )
    ```

    按一定比例给出已有 RGB 颜色字符串的渐变 RGB 颜色字符串，或者给出已有 RGB 颜色字符串的对比色

    * `color`: 颜色元组或列表 (初始颜色, 目标颜色)，或者一个颜色字符串（此时返回其对比色）
    * `proportion`: 改变比例（浮点数，范围为 0 ~ 1），默认值为 1
    * `seqlength`: 如果值为 1，则直接返回结果，其余情况返回长度为 `seqlength` 的渐变颜色列表，默认为 1
    * `num`: 每一通道的 16 进制位数，默认为 2 位，可选值为 1 ~ 4
    
Classes - 类
---

### 01. Animation

!!! note "Animation `Class`"

    动画

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            widget,
            ms,
            *,
            control=None,
            translation=None,
            color=None,
            fps=60,
            start=None,
            step=None,
            stop=None,
            callback=None,
            canvas=None,
            loop=False
        )
        ```


        * `widget`: 进行动画的控件
        * `ms`: 动画总时长（单位：毫秒）
        * `control`: 控制函数，为元组 (函数, 起始值, 终止值) 的形式
        * `translation`: 平移运动，x 方向位移，y 方向位移
        * `color`: 颜色变换
        * `fps`: 每秒帧数
        * `start`: 动画开始前执行的函数
        * `step`: 动画每一帧结束后执行的函数（包括开始和结束）
        * `stop`: 动画结束后执行的函数
        * `callback`: 回调函数，每一帧调用一次，传入参数为单帧占比
        * `canvas`: 当 `widget` 是画布中的绘制对象时，应指定 `canvas`
        * `loop`: 是否循环播放动画，默认不循环，循环时参数 `stop` 失效



    !!! example "\_parts `Method` `Internal`"

        ```python
        _parts(
            self,
            control,
            up,
            down
        )
        ```

        部分比率


    !!! example "\_run `Method` `Internal`"

        ```python
        _run(
            self,
            _ind=0
        )
        ```

        执行动画


    !!! example "\_translate `Method` `Internal`"

        ```python
        _translate(
            self,
            dx,
            dy
        )
        ```

        平移


    !!! note "run `Method`"

        ```python
        run(
            self
        )
        ```

        运行动画


    !!! note "shutdown `Method`"

        ```python
        shutdown(
            self
        )
        ```

        终止动画

### 02. BaseWidget

!!! note "BaseWidget `Class`"

    虚拟画布控件基类

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            x,
            y,
            width,
            height,
            radius,
            text,
            justify,
            borderwidth,
            font,
            image,
            tooltip,
            color_text,
            color_fill,
            color_outline
        )
        ```


        标准参数：标准参数是所有控件都有的 

        * `canvas`: 父画布容器控件
        * `x`: 控件左上角的横坐标
        * `y`: 控件左上角的纵坐标
        * `width`: 控件的宽度
        * `height`: 控件的高度
        * `radius`: 控件圆角化半径
        * `text`: 控件显示的文本，对于文本控件而言，可以为一个元组：(默认文本, 鼠标触碰文本)
        * `justify`: 文本的对齐方式
        * `borderwidth`: 外框的宽度
        * `font`: 控件的字体设定 (字体, 大小, 样式)
        * `image`: 控件的背景（支持 png 类型，大小必须小于控件，否则会溢出控件边框）
        * `tooltip`: 提示框
        * `color_text`: 控件文本的颜色
        * `color_fill`: 控件内部的颜色
        * `color_outline`: 控件外框的颜色

        特定参数：特定参数只有某些控件类才有 

        * `command`: 按钮控件的关联函数
        * `show`: 文本控件的显示文本
        * `limit`: 文本控件的输入字数限制，为负数时表示没有字数限制
        * `read`: 文本控件的只读模式
        * `cursor`: 文本控件输入提示符的字符，默认为一竖线
        * `mode`: 进度条控件的模式，`determinate` 为确定模式，`indeterminate` 为不定模式，默认为前者
        * `tick`: 复选框控件的标记符号，默认为一个“对号”

        详细说明

        1. 字体的值为一个包含两个或三个值的元组或者单个的字符串，共三种形式:
             * 形式一: `字体名称`
             * 形式二: `(字体名称, 字体大小)`
             * 形式三: `(字体名称, 字体大小, 字体样式)`
        2. 颜色为一个包含三个或四个 RGB 颜色字符串的元组，共两种形式:
             * 不使用禁用功能时: `(正常颜色, 触碰颜色, 交互颜色)`
             * 需使用禁用功能时: `(正常颜色, 触碰颜色, 交互颜色, 禁用颜色)`
             * 特别地，进度条控件的参数 `color_bar` 为: `(底色, 进度条颜色)`



    !!! note "configure `Method`"

        ```python
        configure(
            self,
            *args,
            **kw
        )
        ```

        修改或查询参数的值

        可供修改或查询的参数有: 
        1. 所有控件: `color_text`、`color_fill`、`color_outline`
        2. 非文本控件: `text`

        注意：颜色修改不会立即生效，可通过鼠标经过生效，或者调用 `state` 方法立即刷新状态！



    !!! note "destroy `Method`"

        ```python
        destroy(
            self
        )
        ```

        摧毁控件释放内存


    !!! note "move `Method`"

        ```python
        move(
            self,
            dx,
            dy
        )
        ```

        移动控件的位置

        * `dx`: 横向移动长度
        * `dy`: 纵向移动长度



    !!! note "moveto `Method`"

        ```python
        moveto(
            self,
            x,
            y
        )
        ```

        改变控件的位置（以控件左上角为基准）

        * `x`: 改变到的横坐标
        * `y`: 改变到的纵坐标



    !!! note "set\_live `Method`"

        ```python
        set_live(
            self,
            value=None
        )
        ```

        设置或查询控件的活跃状态

        * `value`: 可以为 `bool` 类型（设置当前值）或者 `None`（返回当前值）



    !!! note "state `Method`"

        ```python
        state(
            self,
            mode=None
        )
        ```

        设置或查询控件的状态，参数 `mode` 为 `None` 或者无参数时仅更新控件，否则改变虚拟控件的外观 

        * `mode`: 可以为下列值之一 `normal`（正常状态）、`touch`（鼠标触碰时的状态）、`click`（鼠标按下时的状态）、`disabled`（禁用状态） 和 `None`（查询控件状态）


### 03. Button

!!! note "Button(BaseWidget) `Class`"

    按钮控件

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            x,
            y,
            width,
            height,
            *,
            radius=5,
            text='',
            borderwidth: int = 1,
            justify='center',
            font=('Microsoft YaHei', -24),
            command=None,
            image=None,
            tooltip=None,
            color_text=('#000000', '#000000', '#000000', '#A3A3A3'),
            color_fill=('#E1E1E1', '#E5F1FB', '#CCE4F7', '#E0E0E0'),
            color_outline=('#C0C0C0', '#288CDB', '#4884B4', '#D0D0D0')
        )
        ```



    !!! example "\_click `Method` `Internal`"

        ```python
        _click(
            self,
            event
        )
        ```

        交互状态检测


    !!! example "\_execute `Method` `Internal`"

        ```python
        _execute(
            self,
            event
        )
        ```

        执行关联函数


    !!! example "\_touch `Method` `Internal`"

        ```python
        _touch(
            self,
            event
        )
        ```

        触碰状态检测

### 04. Canvas

!!! note "Canvas(Canvas) `Class`"

    画布容器控件

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            master,
            width,
            height,
            x=None,
            y=None,
            *,
            lock=True,
            expand=True,
            keep=False,
            **kw
        )
        ```


        * `master`: 父控件
        * `width`: 画布宽度
        * `height`: 画布高度
        * `x`: 画布左上角的横坐标
        * `y`: 画布左上角的纵坐标
        * `lock`: 画布内控件的功能锁，为 `False` 时功能暂时失效
        * `expand`: 画布内控件是否能缩放
        * `keep`: 画布比例是否保持不变
        * `**kw`: 与 `tkinter.Canvas` 类的参数相同



    !!! example "\_click `Method` `Internal`"

        ```python
        _click(
            self,
            event
        )
        ```

        鼠标左键按下事件


    !!! example "\_input `Method` `Internal`"

        ```python
        _input(
            self,
            event
        )
        ```

        键盘输入字符事件


    !!! example "\_paste `Method` `Internal`"

        ```python
        _paste(
            self
        )
        ```

        快捷键粘贴事件


    !!! example "\_release `Method` `Internal`"

        ```python
        _release(
            self,
            event
        )
        ```

        鼠标左键松开事件


    !!! example "\_touch `Method` `Internal`"

        ```python
        _touch(
            self,
            event,
            flag=True
        )
        ```

        鼠标触碰控件事件


    !!! example "\_zoom `Method` `Internal`"

        ```python
        _zoom(
            self,
            rate_x=None,
            rate_y=None
        )
        ```

        缩放画布及其内部的所有元素

        * `rate_x`: 横向缩放比率，默认值表示自动更新缩放（根据窗口缩放程度）
        * `rate_y`: 纵向缩放比率，默认值同上



    !!! note "lock `Method`"

        ```python
        lock(
            self,
            value=None
        )
        ```

        设置或查询画布锁的状态

        * `value`: 为 `True` 则可操作，为 `False` 则反之，无参数或参数为 `None` 则返回当前值



    !!! note "widget `Method`"

        ```python
        widget(
            self
        )
        ```

        返回 `Canvas` 类全部的 `BaseWidget` 对象

### 05. CheckButton

!!! note "CheckButton(Button) `Class`"

    复选框控件

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            x,
            y,
            height,
            *,
            radius=5,
            text='',
            value=False,
            tick='✓',
            borderwidth=1,
            justify='right',
            font=('Microsoft YaHei', -24),
            image=None,
            tooltip=None,
            color_text=('#000000', '#000000', '#000000', '#A3A3A3'),
            color_fill=('#E1E1E1', '#E5F1FB', '#CCE4F7', '#E0E0E0'),
            color_outline=('#C0C0C0', '#288CDB', '#4884B4', '#D0D0D0')
        )
        ```



    !!! note "get `Method`"

        ```python
        get(
            self
        )
        ```

        获取复选框状态


    !!! note "set `Method`"

        ```python
        set(
            self,
            value
        )
        ```

        设置复选框状态

### 06. Entry

!!! note "Entry(TextWidget) `Class`"

    输入框控件

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            x,
            y,
            width,
            height,
            *,
            radius=5,
            text='',
            show=None,
            limit=-1,
            cursor='│',
            borderwidth=1,
            justify='left',
            font=('Microsoft YaHei', -24),
            image=None,
            tooltip=None,
            color_text=('#000000', '#000000', '#000000', '#A3A3A3'),
            color_fill=('#FFFFFF', '#FFFFFF', '#FFFFFF', '#E0E0E0'),
            color_outline=('#C0C0C0', '#414141', '#288CDB', '#D0D0D0')
        )
        ```



    !!! example "\_click\_off `Method` `Internal`"

        ```python
        _click_off(
            self
        )
        ```

        控件失去焦点


    !!! example "\_click\_on `Method` `Internal`"

        ```python
        _click_on(
            self
        )
        ```

        控件获得焦点


    !!! example "\_input `Method` `Internal`"

        ```python
        _input(
            self,
            event,
            flag=False
        )
        ```

        文本输入


    !!! example "\_update\_text `Method` `Internal`"

        ```python
        _update_text(
            self
        )
        ```

        更新控件

### 07. Label

!!! note "Label(BaseWidget) `Class`"

    标签控件

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            x,
            y,
            width,
            height,
            *,
            radius=5,
            text='',
            borderwidth=1,
            justify='center',
            font=('Microsoft YaHei', -24),
            image=None,
            tooltip=None,
            color_text=('#000000', '#000000', '#000000', '#A3A3A3'),
            color_fill=('#E1E1E1', '#E5F1FB', '#CCE4F7', '#E0E0E0'),
            color_outline=('#C0C0C0', '#288CDB', '#4884B4', '#D0D0D0')
        )
        ```



    !!! example "\_touch `Method` `Internal`"

        ```python
        _touch(
            self,
            event
        )
        ```

        触碰状态检测

### 08. PhotoImage

!!! note "PhotoImage(PhotoImage) `Class`"

    图片类

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            file,
            **kw
        )
        ```


        * `file`: 图片文件的路径
        * `**kw`: 与 `tkinter.PhotoImage` 的参数相同



    !!! note "parse `Method`"

        ```python
        parse(
            self,
            start=0
        )
        ```

        解析动图，并得到动图的每一帧动画，该方法返回一个生成器 

        * `start`: 动图解析的起始索引（帧数-1）



    !!! note "play `Method`"

        ```python
        play(
            self,
            canvas,
            item,
            interval,
            **kw
        )
        ```

        播放动图，设置 `canvas.lock` 为 `False` 会暂停 

        * `canvas`: 播放动画的画布
        * `item`: 播放动画的 `_CanvasItemId`（`create_text` 方法的返回值）
        * `interval`: 每帧动画的间隔时间



    !!! note "stop `Method`"

        ```python
        stop(
            self,
            item,
            clear=False
        )
        ```

        终止对应动图的播放，且无法重新播放 

        * `item`: 播放动画的 `_CanvasItemId`（`create_text` 方法的返回值）
        * `clear`: 清除图片的标识，为 `True` 就清除图片


### 09. ProgressBar

!!! note "ProgressBar(BaseWidget) `Class`"

    进度条控件

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            x,
            y,
            width,
            height,
            *,
            borderwidth=1,
            justify='center',
            font=('Microsoft YaHei', -24),
            image=None,
            tooltip=None,
            color_text=('#000000', '#000000', '#000000', '#A3A3A3'),
            color_outline=('#C0C0C0', '#414141', '#288CDB', '#D0D0D0'),
            color_fill=('#E1E1E1', '#06b025'),
            mode='determinate'
        )
        ```



    !!! example "\_touch `Method` `Internal`"

        ```python
        _touch(
            self,
            event
        )
        ```

        触碰状态检测


    !!! note "load `Method`"

        ```python
        load(
            self,
            percentage
        )
        ```

        加载进度条的值（调整值）

        * `percentage`: 进度条的值，范围 0~1，大于 1 的值将被视为 1


### 10. Switch

!!! note "Switch(Button) `Class`"

    开关控件

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            x,
            y,
            height=30,
            *,
            width=60,
            radius=inf,
            borderwidth=1,
            tooltip=None,
            color_fill_on=('#288CDB', '#3E98DF', '#4884B4', '#E0E0E0'),
            color_fill_off=('#E1E1E1', '#E5F1FB', '#CCE4F7', '#E0E0E0'),
            color_outline_on=('#288CDB', '#3E98DF', '#4884B4', '#E0E0E0'),
            color_outline_off=('#C0C0C0', '#288CDB', '#4884B4', '#D0D0D0'),
            color_fill_slider=('#000000', '#000000', '#000000', '#333333'),
            color_outline_slider=('#333333', '#333333', '#333333', '#666666'),
            default=False,
            on=None,
            off=None
        )
        ```


        * `canvas`: 父画布控件
        * `x`: 横坐标
        * `y`: 纵坐标
        * `height`: 高度，默认为 30 像素
        * `width`: 宽度，默认为高度的两倍
        * `radius`: 圆角半径，默认为完全圆弧
        * `borderwidth`: 边框宽度
        * `tooltip`: 提示框
        * `color_fill_on`: 内部颜色（状态：开）
        * `color_fill_off`: 内部颜色（状态：关）
        * `color_outline_on`: 边框颜色（状态：开）
        * `color_outline_off`: 边框颜色（状态：关）
        * `color_fill_slider`: 滑块内部颜色
        * `color_outline_slider`: 滑块边框颜色
        * `default`: 默认值，默认为 `False`
        * `on`: 转换到开时触发的回调函数
        * `off`: 转换到关时触发的回调函数



    !!! example "\_animate `Method` `Internal`"

        ```python
        _animate(
            self,
            ms=250
        )
        ```

        移动动画


    !!! note "get `Method`"

        ```python
        get(
            self
        )
        ```

        返回状态


    !!! note "set `Method`"

        ```python
        set(
            self,
            value
        )
        ```

        设定状态

### 11. Text

!!! note "Text(TextWidget) `Class`"

    文本框控件

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            x,
            y,
            width,
            height,
            *,
            radius=5,
            text='',
            limit=-1,
            read=False,
            cursor='│',
            borderwidth=1,
            justify='left',
            font=('Microsoft YaHei', -24),
            image=None,
            tooltip=None,
            color_text=('#000000', '#000000', '#000000', '#A3A3A3'),
            color_fill=('#FFFFFF', '#FFFFFF', '#FFFFFF', '#E0E0E0'),
            color_outline=('#C0C0C0', '#414141', '#288CDB', '#D0D0D0')
        )
        ```



    !!! example "\_click\_off `Method` `Internal`"

        ```python
        _click_off(
            self
        )
        ```

        控件失去焦点


    !!! example "\_click\_on `Method` `Internal`"

        ```python
        _click_on(
            self
        )
        ```

        控件获得焦点


    !!! example "\_input `Method` `Internal`"

        ```python
        _input(
            self,
            event,
            flag=False
        )
        ```

        文本输入


    !!! example "\_input\_backspace `Method` `Internal`"

        ```python
        _input_backspace(
            self
        )
        ```

        退格键功能


    !!! example "\_input\_return `Method` `Internal`"

        ```python
        _input_return(
            self
        )
        ```

        回车键功能

### 12. TextWidget

!!! note "TextWidget(BaseWidget) `Class`"

    虚拟文本类控件基类 

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            x,
            y,
            width,
            height,
            radius,
            text,
            limit,
            justify,
            icursor,
            borderwidth,
            font,
            image,
            tooltip,
            color_text,
            color_fill,
            color_outline
        )
        ```



    !!! example "\_click `Method` `Internal`"

        ```python
        _click(
            self,
            event
        )
        ```

        交互状态检测


    !!! example "\_cursor\_flash `Method` `Internal`"

        ```python
        _cursor_flash(
            self
        )
        ```

        鼠标光标闪烁


    !!! example "\_cursor\_update `Method` `Internal`"

        ```python
        _cursor_update(
            self,
            text=' '
        )
        ```

        鼠标光标更新


    !!! example "\_paste `Method` `Internal`"

        ```python
        _paste(
            self
        )
        ```

        快捷键粘贴


    !!! example "\_touch `Method` `Internal`"

        ```python
        _touch(
            self,
            event
        )
        ```

        触碰状态检测


    !!! example "\_touch\_off `Method` `Internal`"

        ```python
        _touch_off(
            self
        )
        ```

        鼠标离开状态


    !!! example "\_touch\_on `Method` `Internal`"

        ```python
        _touch_on(
            self
        )
        ```

        鼠标悬停状态


    !!! note "append `Method`"

        ```python
        append(
            self,
            value
        )
        ```

        添加输入框的值


    !!! note "clear `Method`"

        ```python
        clear(
            self
        )
        ```

        清空文本类控件的内容


    !!! note "get `Method`"

        ```python
        get(
            self
        )
        ```

        获取输入框的值


    !!! note "set `Method`"

        ```python
        set(
            self,
            value
        )
        ```

        设置输入框的值

### 13. Tk

!!! note "Tk(Tk) `Class`"

    根窗口容器控件

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            title=None,
            width=None,
            height=None,
            x=None,
            y=None,
            *,
            shutdown=None,
            alpha=None,
            toolwindow=None,
            topmost=None,
            transparentcolor=None,
            **kw
        )
        ```


        * `title`: 窗口标题
        * `width`: 窗口宽度
        * `height`: 窗口高度
        * `x`: 窗口左上角横坐标
        * `y`: 窗口左上角纵坐标
        * `shutdown`: 关闭窗口之前执行的函数，但会覆盖原关闭操作
        * `alpha`: 窗口的透明度，取值在 0 ~ 1 之间，且 1 为不透明
        * `toolwindow`: 窗口是否为工具窗口
        * `topmost`: 窗口是否置顶，为布尔值
        * `transparentcolor`: 过滤掉该颜色
        * `**kw`: 与 `tkinter.Tk` 类的其他参数相同



    !!! example "\_zoom `Method` `Internal`"

        ```python
        _zoom(
            self
        )
        ```

        缩放检测


    !!! note "canvas `Method`"

        ```python
        canvas(
            self
        )
        ```

        返回 `Tk` 类全部的 `Canvas` 对象

### 14. ToolTip

!!! note "ToolTip `Class`"

    提示框容器控件

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            text,
            *,
            font=('Microsoft YaHei', ),
            fg='black',
            bg='white',
            justify='left',
            highlightthickness=1,
            highlightbackground='grey',
            delay=500,
            duration=5000
        )
        ```


        * `text`: 要显示的文本
        * `font`: 文本字体
        * `fg`: 前景色，默认为黑色
        * `bg`: 背景色，默认为淡黄色
        * `justify`: 文本对齐方式
        * `highlightthickness`: 边框厚度，默认为 1 像素
        * `highlightbackground`: 边框颜色，默认为黑色
        * `delay`: 延迟时间，超过这个时间后，提示框才会出现，默认为 500 毫秒（必须大于等于零）
        * `duration`: 持续时间，达到这个值后，提示框会消失，默认为 5000 毫秒（值为 `None` 表示不会自己消失，需要触发才会消失，但有时候会触发失败……）



    !!! example "\_cancel `Method` `Internal`"

        ```python
        _cancel(
            self,
            master
        )
        ```

        取消倒计时


    !!! example "\_countdown `Method` `Internal`"

        ```python
        _countdown(
            self,
            master
        )
        ```

        倒计时


    !!! example "\_destroy `Method` `Internal`"

        ```python
        _destroy(
            self
        )
        ```

        消失


    !!! example "\_place `Method` `Internal`"

        ```python
        _place(
            self
        )
        ```

        显示

### 15. Toplevel

!!! note "Toplevel(Toplevel, Tk) `Class`"

    子窗口容器控件

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            master=None,
            title=None,
            width=None,
            height=None,
            x=None,
            y=None,
            *,
            shutdown=None,
            alpha=None,
            toolwindow=None,
            topmost=None,
            transparentcolor=None,
            **kw
        )
        ```


        * `master`: 父窗口
        * `title`: 窗口标题
        * `width`: 窗口宽度
        * `height`: 窗口高度
        * `x`: 窗口左上角横坐标
        * `y`: 窗口左上角纵坐标
        * `shutdown`: 关闭窗口之前执行的函数，但会覆盖关闭操作
        * `alpha`: 窗口的透明度，取值在 0 ~ 1 之间，且 1 为不透明
        * `toolwindow`: 窗口是否为工具窗口
        * `topmost`: 窗口是否置顶，为布尔值
        * `transparentcolor`: 过滤掉该颜色
        * `**kw`: 与 `tkinter.Toplevel` 类的参数相同


