"""
tkintertools
============
The tkindertools module is an auxiliary module of the tkinder module.

Provides
--------
* Transparent, rounded and customized widgets
* Automatic control of picture size and widget size
* Scalable png pictures and playable gif pictures
* Regular mobile widgets and canvas interfaces
* Gradient colors and contrast colors
* Text with controllable length and alignment
* Convenient, inheritable singleton pattern class
* Display clear window and its contents

Contents
--------
* Container Widget: `Tk`, `Toplevel`, `Canvas`
* Virtual Widget: `Label`, `Button`, `Entry`, `Text`, `Progressbar`
* Tool Class: `PhotoImage`, `Singleton`
* Tool Function: `move`, `text`, `color`, `SetProcessDpiAwareness`

More
----
* GitCode: https://gitcode.net/weixin_62651706/tkintertools
* GitHub(Mirror): https://github.com/XiaoKang2022-CSDN/tkintertools
* Tutorials: https://xiaokang2022.blog.csdn.net/article/details/127374661
"""

import sys  # 检测 Python 版本

if sys.version_info < (3, 10):
    # 版本检测，低版本缺失部分语法
    error_info = '\n\033[31mOperation Requirements: \033[32m\nPython version shall not be less than\033[33m 3.10.0!\033[0m'
    raise RuntimeError(error_info)

import math  # 数学函数
import tkinter  # 基础模块
from ctypes import OleDLL  # DPI兼容
from fractions import Fraction  # 图片缩放
from typing import Generator, Iterable, Literal  # 类型提示

__author__ = 'Xiaokang2022<2951256653@qq.com>'
__version__ = '2.5.11.3'
__all__ = [
    'Tk', 'Toplevel', 'Canvas',
    'Label', 'Button', 'Entry', 'Text', 'Progressbar',
    'PhotoImage', 'Singleton',
    'move', 'text', 'color', 'SetProcessDpiAwareness'
]

PROCESS_SYSTEM_DPI_AWARE = 1  # DPI级别
SCALE = OleDLL('shcore').GetScaleFactorForDevice(0)/100  # 屏幕缩放因子

COLOR_BUTTON_FILL = '#E1E1E1', '#E5F1FB', '#CCE4F7', '#E0E0E0'      # 默认的按钮内部颜色
COLOR_BUTTON_OUTLINE = '#C0C0C0', '#288CDB', '#4884B4', '#D0D0D0'   # 默认的按钮外框颜色
COLOR_TEXT_FILL = '#FFFFFF', '#FFFFFF', '#FFFFFF', '#E0E0E0'        # 默认的文本内部颜色
COLOR_TEXT_OUTLINE = '#C0C0C0', '#414141', '#288CDB', '#D0D0D0'     # 默认的文本外框颜色
COLOR_TEXT = '#000000', '#000000', '#000000', '#A3A3A3'             # 默认的文本颜色
COLOR_NONE = '', '', '', ''                                         # 透明颜色
COLOR_BAR = '#E1E1E1', '#06b025'                                    # 默认的进度条颜色

BORDERWIDTH = 1             # 默认控件外框宽度
CURSOR = '│'                # 文本光标
FONT = 'KaiTi'              # 默认字体
SIZE = 20                   # 默认字体大小
LIMIT = -1                  # 默认文本长度
RADIUS = 0                  # 默认控件圆角半径
FRAMES = 60                 # 默认帧数


class Tk(tkinter.Tk):
    """ 创建窗口，并处理缩放操作 """

    def __init__(
        self,
        title: str | None = None,
        width: int | None = None,
        height: int | None = None,
        x: int | None = None,
        y: int | None = None,
        shutdown=None,  # type: function | None
        **kw
    ) -> None:
        """
        `title`: 窗口标题
        `width`: 窗口宽度（单位:像素）
        `height`: 窗口高度
        `x`: 窗口左上角横坐标（单位:像素）
        `y`: 窗口左上角纵坐标
        `shutdown`: 关闭窗口之前执行的函数（会覆盖原关闭操作）
        `**kw`: 与 tkinter.Tk 类的参数相同
        """
        if type(self) == Tk:  # NOTE:方便后面的 Toplevel 类继承
            tkinter.Tk.__init__(self, **kw)

        self.width: list[int] = [100, 1]  # [初始宽度, 当前宽度]
        self.height: list[int] = [100, 1]  # [初始高度, 当前高度]
        self._canvas: list[Canvas] = []  # 子画布列表

        if width and height:
            if x != None and y != None:
                self.geometry('%dx%d+%d+%d' % (width, height, x, y))
            else:
                self.geometry('%dx%d' % (width, height))

        self.title(title if title else None)
        self.protocol('WM_DELETE_WINDOW', shutdown if shutdown else None)

        self.bind('<Configure>', lambda _: self.__zoom())  # 开启窗口缩放检测

    def canvas(self) -> tuple:
        """ `Tk`类的`Canvas`元组 """
        return tuple(self._canvas)

    def __zoom(self) -> None:
        """ 缩放检测 """
        width, height = map(int, self.geometry().split('+')[0].split('x'))
        # NOTE: 此处必须用 geometry 方法，直接用 Event 或者 winfo 会有画面异常的 bug

        if width == self.width[1] and height == self.height[1]:  # 没有大小的改变
            return

        for canvas in self._canvas:
            if canvas.expand and canvas._lock:
                canvas.zoom(width/self.width[1], height/self.height[1])

        self.width[1], self.height[1] = width, height  # 更新窗口当前的宽高值

    def wm_geometry(self, newGeometry: str | None = None) -> str | None:
        # 重写: 添加修改初始宽高值的功能并兼容不同的DPI缩放
        if newGeometry:
            width, height, _width, _height, * \
                _ = map(int, (newGeometry+'+0+0').replace('+', 'x').split('x'))
            self.width, self.height = [width]*2, [height]*2
            geometry = '%dx%d+%d+%d' % (width, height, _width, _height)
            if not _:
                geometry = geometry.split('+')[0]
            return tkinter.Tk.wm_geometry(self, geometry)
        geometry = tkinter.Tk.wm_geometry(self, newGeometry)
        width, height, _width, _height, * \
            _ = map(int, (geometry+'+0+0').replace('+', 'x').split('x'))
        return '%dx%d+%d+%d' % (width, height, _width, _height)

    geometry = wm_geometry


class Toplevel(tkinter.Toplevel, Tk):
    """ 类似于`tkinter.Toplevel`，同时增加了`Tk`的功能 """

    def __init__(
        self,
        master: Tk,
        title: str | None = None,
        width: int | None = None,
        height: int | None = None,
        x: int | None = None,
        y: int | None = None,
        shutdown=None,  # type: function | None
        **kw
    ) -> None:
        """
        `master`: 父窗口
        `title`: 窗口标题
        `width`: 窗口宽度（单位:像素）
        `height`: 窗口高度
        `x`: 窗口左上角横坐标（单位:像素）
        `y`: 窗口左上角纵坐标
        `shutdown`: 关闭窗口之前执行的函数（会覆盖关闭操作）
        `**kw`: 与 tkinter.Toplevel 类的参数相同
        """
        tkinter.Toplevel.__init__(self, master, **kw)
        Tk.__init__(self, title, width, height, x, y, shutdown, **kw)
        self.focus_set()


class Canvas(tkinter.Canvas):
    """ 用于承载虚拟的画布控件，并处理部分绑定事件 """

    def __init__(
        self,
        master: Tk,
        width: int,
        height: int,
        lock: bool = True,
        expand: bool = True,
        keep: bool = False,
        **kw
    ) -> None:
        """
        `master`: 父控件
        `width`: 画布宽度
        `height`: 画布高度
        `lock`: 画布内控件的功能锁（False时功能暂时失效）
        `expand`: 画布内控件是否能缩放
        `keep`: 保持画布比例不变
        `**kw`: 与 tkinter.Canvas 类的参数相同
        """
        self.width = [width]*2  # [初始宽度, 当前宽度]
        self.height = [height]*2  # [初始高度, 当前高度]
        self._lock = lock
        self.expand = expand
        self.keep = keep

        self.rx = 1.  # 横向放缩比率
        self.ry = 1.  # 纵向放缩比率
        self._widget: list[_BaseWidget] = []  # 子控件列表（与事件绑定有关）
        self._font = {}  # type: dict[tkinter._CanvasItemId, float]
        self._image = {}  # type: dict[tkinter._CanvasItemId, list]

        tkinter.Canvas.__init__(
            self, master, width=width, height=height, highlightthickness=0, **kw)

        master._canvas.append(self)  # 将实例添加到 Tk 的画布列表中

        self.bind('<Motion>', self.__touch)  # 绑定鼠标触碰控件
        self.bind('<Any-Key>', self.__input)  # 绑定键盘输入字符（和Ctrl+v的代码顺序不可错）
        self.bind('<Button-1>', self.__click)  # 绑定鼠标左键按下
        self.bind('<B1-Motion>', self.__click)  # 绑定鼠标左键按下移动
        self.bind('<MouseWheel>', self.__mousewheel)  # 绑定鼠标滚轮滚动
        self.bind('<ButtonRelease-1>', self.__release)  # 绑定鼠标左键松开
        self.bind('<Control-v>', lambda _: self.__paste())  # 绑定粘贴快捷键

    def widget(self) -> tuple:
        """ `Canvas`类的子控件元组 """
        return tuple(self._widget)

    def lock(self, value: bool | None = None) -> bool | None:
        """
        设置画布锁
        `value`: 布尔值，True则可操作，False反之，None则返回当前值
        """
        if value == None:
            return self._lock
        self._lock = value
        if value and self.expand:
            self.zoom()

    def zoom(self, rate_x: float | None = None, rate_y: float | None = None) -> None:
        """
        缩放画布及其内部的所有元素
        `rate_x`: 横向缩放比率，默认值表示自动更新缩放（根据窗口缩放程度）
        `rate_y`: 纵向缩放比率，默认值同上
        """
        if not rate_x:
            rate_x = self.master.width[1]/self.master.width[0]/self.rx
        if not rate_y:
            rate_y = self.master.height[1]/self.master.height[0]/self.ry

        if self.keep:  # 维持比例
            rx = rate_x*self.master.width[1]/self.master.width[0]/self.rx
            ry = rate_y*self.master.height[1]/self.master.height[0]/self.ry
            rate_x = rate_y = min(rx, ry)

        # 更新画布的位置及大小的数据
        self.width[1] *= rate_x
        self.height[1] *= rate_y
        temp_x, self.rx = self.rx, self.width[1]/self.width[0]
        temp_y, self.ry = self.ry, self.height[1]/self.height[0]

        place_info = self.place_info()
        tkinter.Canvas.place(  # 更新画布的位置及大小
            self,
            width=self.width[1],
            height=self.height[1],
            x=float(place_info['x'])*rate_x,
            y=float(place_info['y'])*rate_y)

        for widget in self._widget:  # 更新子画布控件的子虚拟画布控件位置数据
            widget.x1 *= rate_x
            widget.x2 *= rate_x
            widget.y1 *= rate_y
            widget.y2 *= rate_y

        for item in self.find_all():  # item 位置缩放
            self.coords(
                item, *[c*(rate_x, rate_y)[i & 1] for i, c in enumerate(self.coords(item))])

        for item in self._font:  # 字体大小缩放
            self._font[item][1] *= math.sqrt(rate_x*rate_y)
            font = self._font[item][:]
            font[1] = int(font[1])
            self.itemconfigure(item, font=font)

        for item in self._image:  # 图像大小缩放（采用相对的绝对缩放）
            if self._image[item][0] and self._image[item][0].extension != 'gif':
                self._image[item][1] = self._image[item][0].zoom(
                    temp_x*rate_x, temp_y*rate_y, 1.2)
                self.itemconfigure(item, image=self._image[item][1])

    def __touch(self, event: tkinter.Event, flag: bool = True) -> None:
        """ 鼠标触碰控件事件 """
        if self._lock:
            for widget in self._widget[::-1]:
                if widget.live and widget.touch(event) and flag:
                    if isinstance(widget, _TextWidget):
                        self.configure(cursor='xterm')
                    elif isinstance(widget, Button):
                        self.configure(cursor='hand2')
                    else:
                        self.configure(cursor='arrow')
                    flag = False
            if flag:
                self.configure(cursor='arrow')

    def __click(self, event: tkinter.Event) -> None:
        """ 鼠标左键按下事件 """
        if self._lock:
            for widget in self._widget[::-1]:
                if widget.live and isinstance(widget, Button | _TextWidget):
                    widget.click(event)  # NOTE: 无需 return，按下空白区域也有作用
                    self.focus_set()

    def __release(self, event: tkinter.Event) -> None:
        """ 鼠标左键松开事件 """
        if self._lock:
            for widget in self._widget[::-1]:
                if widget.live and isinstance(widget, Button):
                    if widget.touch(event):
                        return widget.execute(event)

    def __mousewheel(self, event: tkinter.Event) -> None:
        """ 鼠标滚轮滚动事件 """
        if self._lock:
            for widget in self._widget[::-1]:
                if widget.live and isinstance(widget, Text):
                    if widget.scroll(event):
                        return

    def __input(self, event: tkinter.Event) -> None:
        """ 键盘输入字符事件 """
        if self._lock:
            for widget in self._widget[::-1]:
                if widget.live and isinstance(widget, _TextWidget):
                    if widget.input(event):
                        return

    def __paste(self) -> None:
        """ 快捷键粘贴事件 """
        if self._lock:
            for widget in self._widget[::-1]:
                if widget.live and isinstance(widget, _TextWidget):
                    if widget.paste():
                        return

    def create_text(self, *args, **kw):
        # 重写：添加对 text 类型的 _CanvasItemId 的字体大小的控制
        font = kw.get('font')
        if not font:
            kw['font'] = FONT, SIZE
        elif isinstance(font, str):
            kw['font'] = font, SIZE
        item = tkinter.Canvas.create_text(self, *args, **kw)
        self._font[item] = list(kw['font'])
        return item

    def create_image(self, *args, **kw):
        # 重写：添加对 image 类型的 _CanvasItemId 的图像大小的控制
        item = tkinter.Canvas.create_image(self, *args, **kw)
        self._image[item] = [kw.get('image'), None]
        return item

    def itemconfigure(
        self,
        tagOrId,  # type: str | tkinter._CanvasItemId
        **kw
    ) -> dict[str, tuple[str, str, str, str, str]] | None:
        # 重写：创建空image的_CanvasItemId时漏去对图像大小的控制
        if type(kw.get('image')) == PhotoImage:
            self._image[tagOrId] = [kw.get('image'), None]
        return tkinter.Canvas.itemconfigure(self, tagOrId, **kw)

    def place(self, *args, **kw) -> None:
        # 重写：增加一些特定功能
        self.width[0] = kw.get('wdith', self.width[0])
        self.height[0] = kw.get('height', self.height[0])
        return tkinter.Canvas.place(self, *args, **kw)

    def destroy(self) -> None:
        # 重写：兼容
        self.master._canvas.remove(self)
        for widget in self.widget():
            widget.destroy()
        return tkinter.Canvas.destroy(self)


class _BaseWidget:
    """ 虚拟画布控件基类 """

    def __init__(
        self,
        canvas: Canvas,
        x: float,
        y: float,
        width: float,
        height: float,
        radius: float,
        text: str,
        justify: str,
        borderwidth: float,
        font: tuple[str, int, str],
        image,  # type: PhotoImage | None
        color_text: tuple[str, str, str],
        color_fill: tuple[str, str, str],
        color_outline: tuple[str, str, str]
    ) -> None:
        """
        ### 标准参数
        `canvas`: 父画布容器控件
        `x`: 控件左上角的横坐标
        `y`: 控件左上角的纵坐标
        `width`: 控件的宽度
        `height`: 控件的高度
        `radius`: 控件圆角化半径
        `text`: 控件显示的文本，对于文本控件而言，可以为一个元组：(默认文本, 鼠标触碰文本)
        `justify`: 文本的对齐方式
        `borderwidth`: 外框的宽度
        `font`: 控件的字体设定 (字体, 大小, 样式)
        `image`: 控件的背景（支持 png 类型，大小必须小于控件，否则会溢出）
        `color_text`: 控件文本的颜色
        `color_fill`: 控件内部的颜色
        `color_outline`: 控件外框的颜色
        ### 特定参数
        `command`: 按钮控件的关联函数
        `show`: 文本控件的显示文本
        `limit`: 文本控件的输入字数限制，为负数时表示没有字数限制
        `read`: 文本控件的只读模式
        `cursor`: 输入提示符的字符，默认为一竖线
        ### 详细说明
        字体的值为一个包含两个或三个值的元组，共两种形式
        形式一: `(字体名称, 字体大小)`
        形式二: `(字体名称, 字体大小, 字体样式)`

        颜色为一个包含三个或四个 RGB 颜色字符串的元组，共两种形式
        不使用禁用功能时: `(正常颜色, 触碰颜色, 交互颜色)`
        需使用禁用功能时: `(正常颜色, 触碰颜色, 交互颜色, 禁用颜色)`
        """
        self.master = canvas
        self.value = text
        self.justify = justify
        self.font = font
        self.photoimage = image
        self.color_text = list(color_text)
        self.color_fill = list(color_fill)
        self.color_outline = list(color_outline)

        x *= canvas.rx
        y *= canvas.ry
        width *= canvas.rx
        height *= canvas.ry

        self.x1, self.y1 = x, y  # 控件左上角坐标
        self.x2, self.y2 = x+width, y+height  # 控件左下角坐标
        self.width, self.height = width, height  # 控件的宽高值
        self.radius = radius  # 边角圆弧半径
        self.live = True  # 控件活跃标志
        self._state = 'normal'  # 控件的状态
        self.pre_state = None  # 记录之前的状态
        self.command_ex = {
            'normal': None, 'touch': None,
            'click': None, 'disabled': None
        }  # type: dict[str, function | None]

        canvas._widget.append(self)  # 将实例添加到父画布控件

        if radius:
            if 2 * radius > width:
                radius = width // 2
                self.radius = radius
            if 2 * radius > height:
                radius = height // 2
                self.radius = radius

            d = 2*radius  # 圆角直径
            _x, _y = x+radius*canvas.rx, y+radius*canvas.ry
            _w, _h = width-d*canvas.rx, height-d*canvas.ry

            kw = {'outline': '', 'fill': color_fill[0]}
            self.inside = [  # 虚拟控件内部填充颜色
                canvas.create_rectangle(
                    x, _y, x+width, y+height-radius*canvas.ry, **kw),
                canvas.create_rectangle(
                    _x, y, x+width-radius*canvas.rx, y+height, **kw),
                canvas.create_arc(
                    x, y, x+d*canvas.rx, y+d*canvas.ry, start=90, **kw),
                canvas.create_arc(
                    x+_w, y, x+width, y+d*canvas.ry, start=0, **kw),
                canvas.create_arc(
                    x, y+_h, x+d*canvas.rx, y+height, start=180, **kw),
                canvas.create_arc(
                    x+_w, y+_h, x+width, y+height, start=270, **kw)]

            kw = {'extent': 100, 'style': 'arc', 'outline': color_outline[0]}
            self.outside = [  # 虚拟控件外框
                canvas.create_line(
                    _x, y, x+width-radius*canvas.rx, y, fill=color_outline[0], width=borderwidth),
                canvas.create_line(
                    _x, y+height, x+width-radius*canvas.rx, y+height, fill=color_outline[0], width=borderwidth),
                canvas.create_line(
                    x, _y, x, y+height-radius*canvas.ry, fill=color_outline[0], width=borderwidth),
                canvas.create_line(
                    x+width, _y, x+width, y+height-radius*canvas.ry, fill=color_outline[0], width=borderwidth),
                canvas.create_arc(
                    x, y, x+d*canvas.rx, y+d*canvas.ry, start=90, width=borderwidth, **kw),
                canvas.create_arc(
                    x+_w, y, x+width, y+d*canvas.ry, start=0, width=borderwidth, **kw),
                canvas.create_arc(
                    x, y+_h, x+d*canvas.rx, y+height, start=180, width=borderwidth, **kw),
                canvas.create_arc(
                    x+_w, y+_h, x+width, y+height, start=270, width=borderwidth, **kw)]
        else:
            self.rect = canvas.create_rectangle(  # 虚拟控件的外框
                x, y, x+width, y+height,
                width=borderwidth,
                outline=color_outline[0],
                fill=color_fill[0])

        self.image = canvas.create_image(
            x+width/2, y+height/2, image=image)  # 背景图片

        self.text = canvas.create_text(  # 虚拟控件显示的文字
            x + (radius+2 if justify == 'left' else width-radius-3
                 if justify == 'right' else width / 2),
            y + height / 2,
            text=text,
            font=font,
            justify=justify,
            anchor='w' if justify == 'left' else 'e' if justify == 'right' else 'center',
            fill=color_text[0])

        if type(font) != str:
            font = list(font)
            font[1] = int(font[1]*math.sqrt(canvas.rx*canvas.ry))
            canvas._font[self.text][1] = font[1]
            canvas.itemconfigure(self.text, font=font)

    def state(self, mode: Literal['normal', 'touch', 'click', 'disabled'] | None = None) -> None:
        """
        mode 参数为 None 时仅更新控件，否则改变虚拟控件的外观
        `normal`: 正常状态
        `touch`: 鼠标触碰时的状态
        `click`: 鼠标按下时的状态
        `disabled`: 禁用状态
        """
        if mode:
            self._state, self.pre_state = mode, self._state
            if self._state == self.pre_state:  # 保持状态时直接跳过
                return

        if self._state == 'normal':
            mode = 0
        elif self._state == 'touch':
            mode = 1
        elif self._state == 'click':
            mode = 2
        else:
            mode = 3

        self.master.itemconfigure(self.text, fill=self.color_text[mode])
        if isinstance(self, Text):
            self.master.itemconfigure(self._text, fill=self.color_text[mode])

        if self.radius:
            for item in self.inside:  # 修改色块
                self.master.itemconfigure(item, fill=self.color_fill[mode])

            # 修改线条
            for item in self.outside[:4]:
                self.master.itemconfigure(item, fill=self.color_outline[mode])
            for item in self.outside[4:]:
                self.master.itemconfigure(
                    item, outline=self.color_outline[mode])
        else:
            self.master.itemconfigure(
                self.rect, outline=self.color_outline[mode])
            if isinstance(self, Progressbar):
                self.master.itemconfigure(self.bottom, fill=self.color_fill[0])
                self.master.itemconfigure(self.bar, fill=self.color_fill[1])
            else:
                self.master.itemconfigure(
                    self.rect, fill=self.color_fill[mode])

        if self.command_ex[self._state]:
            self.command_ex[self._state]()

    def move(self, dx: float, dy: float) -> None:
        """
        移动控件的位置
        `dx`: 横向移动长度（单位：像素）
        `dy`: 纵向移动长度
        """
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy

        if self.radius:
            for item in self.inside+self.outside:
                self.master.move(item, dx, dy)
        else:
            self.master.move(self.rect, dx, dy)

        self.master.move(self.image, dx, dy)
        self.master.move(self.text, dx, dy)

        if isinstance(self, _TextWidget):
            self.master.move(self._cursor, dx, dy)
        if isinstance(self, Text):
            self.master.move(self._text, dx, dy)
        if isinstance(self, Progressbar):
            self.master.move(self.bar, dx, dy)

    def moveto(self, x: float, y: float) -> None:
        """
        改变控件的位置
        `x`: 改变到的横坐标（单位：像素）
        `y`: 改变到的纵坐标
        """
        self.x1, self.x2 = x, x+self.width
        self.y1, self.y2 = y, y+self.height

        if self.radius:
            for item in self.inside+self.outside:
                self.master.moveto(item, x, y)
        else:
            self.master.moveto(self.rect, x, y)

        self.master.moveto(self.image, x, y)
        self.master.moveto(self.text, x, y)

        if isinstance(self, _TextWidget):
            self.master.moveto(self._cursor, x, y)
        if isinstance(self, Text):
            self.master.moveto(self._text, x, y)
        if isinstance(self, Progressbar):
            self.master.moveto(self.bar, x, y)

    def configure(self, *args, **kw) -> str | tuple | None:
        """
        修改或查询原有参数的值，可供修改或查询的参数有
        1. 所有控件: `color_text`、`color_fill`、`color_outline`
        2. 非文本控件: `text`
        """
        if args:
            if args[0] == 'text':
                return self.value
            else:
                return getattr(self, args[0])

        value = kw.get('text', None)
        text = kw.get('color_text', None)
        fill = kw.get('color_fill', None)
        outline = kw.get('color_outline', None)

        if value != None:
            self.value = value
        if text:
            self.color_text = text
        if fill:
            self.color_fill = fill
        if outline:
            self.color_outline = outline

        if isinstance(self, Label | Button | Progressbar) and value != None:
            self.master.itemconfigure(self.text, text=value)

    def destroy(self) -> None:
        """ 摧毁控件释放内存 """
        self.live = False
        self.master._widget.remove(self)

        if self.radius:
            for item in self.inside+self.outside:
                self.master.delete(item)
        else:
            self.master.delete(self.rect)

        if isinstance(self, _TextWidget):
            self.master.delete(self._cursor)
        if isinstance(self, Text):
            self.master.delete(self._text)
        if isinstance(self, Progressbar):
            self.master.delete(self.bar)

        self.master.delete(self.image)
        self.master.delete(self.text)

    def set_live(self, boolean: bool | None = None) -> bool | None:
        """ 设定或查询live值 """
        if boolean == None:
            return self.live
        else:
            self.live = boolean
            if boolean:
                self.state('normal')
            else:
                self.state('disabled')


class _TextWidget(_BaseWidget):
    """ 文本类控件基类 """

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        radius: float,
        text: tuple[str] | str,
        limit: int,
        justify: str,
        icursor: str,
        borderwidth: int,
        font: tuple[str, int, str],
        image,  # type: PhotoImage | None
        color_text: tuple[str, str, str],
        color_fill: tuple[str, str, str],
        color_outline: tuple[str, str, str]
    ) -> None:

        self.canvas = canvas
        self.limit = limit
        self.icursor = icursor

        self.interval = 300  # 光标闪烁间
        self.flag = False  # 光标闪烁标志
        # 隐式值
        self._value = ['', text, ''] if type(text) == str else ['', *text]

        _BaseWidget.__init__(self, canvas, x, y, width, height, radius, '', justify,
                             borderwidth, font, image, color_text, color_fill, color_outline)

        # 提示光标 NOTE:位置顺序不可乱动，font不可乱改
        self._cursor = canvas.create_text(0, 0, fill=color_text[2], font=font)
        canvas._font[self._cursor][1] = canvas._font[self.text][1]
        font = canvas.itemcget(self.text, 'font')
        canvas.itemconfigure(self._cursor, font=font)

    def touch_on(self) -> None:
        """ 鼠标悬停状态 """
        if self._state != 'click':
            self.state('touch')

            if self.master.itemcget(self.text, 'text') == self._value[1]:
                self.master.itemconfigure(self.text, text=self._value[2])

    def touch_off(self) -> None:
        """ 鼠标离开状态 """
        if self._state != 'click':
            self.state('normal')

            if self.master.itemcget(self.text, 'text') == self._value[2]:
                self.master.itemconfigure(self.text, text=self._value[1])

    def click(self, event: tkinter.Event) -> None:
        """ 交互状态检测 """
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            if self._state != 'click':
                self.click_on()
        else:
            self.click_off()

    def touch(
        self,  # type: Entry | Text
        event: tkinter.Event
    ) -> bool:
        """ 触碰状态检测 """
        condition = self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2
        self.touch_on() if condition else self.touch_off()
        return condition

    def cursor_flash(self) -> None:
        """ 鼠标光标闪烁 """
        if self.interval >= 300:
            self.interval, self.flag = 0, not self.flag
            if self.flag:
                self.master.itemconfigure(self._cursor, text=self.icursor)
            else:
                self.master.itemconfigure(self._cursor, text='')

        if self._state == 'click':
            self.interval += 10
            self.master.after(10, self.cursor_flash)
        else:
            self.interval, self.flag = 300, False  # 恢复默认值
            self.master.itemconfigure(self._cursor, text='')

    def cursor_update(self, text: str = ' ') -> None:
        """ 鼠标光标更新 """
        self.interval, self.flag = 300, False  # 恢复默认值
        if isinstance(self, Entry):
            self.master.coords(self._cursor, self.master.bbox(
                self.text)[2], self.y1+self.height * self.master.ry / 2)  # BUG
        elif isinstance(self, Text):
            _pos = self.master.bbox(self._text)
            self.master.coords(self._cursor, _pos[2], _pos[1])
        self.master.itemconfigure(
            self._cursor, text='' if not text else self.icursor)

    def update(self) -> None:
        """ 更新文本显示 """
        self.master.itemconfigure(self.text, text=self._value[0])

    def paste(self) -> bool:
        """ 快捷键粘贴 """
        condition = self._state == 'click' and not getattr(self, 'show', None)
        if condition:
            self.append(self.master.clipboard_get())
        return condition

    def get(self) -> str:
        """ 获取输入框的值 """
        return self.value

    def set(self, value: str) -> None:
        """ 设置输入框的值 """
        self.value = self._value[0] = ''
        self.append(value)

    def append(self, value: str) -> None:
        """ 添加输入框的值 """
        temp, self._state = self._state, 'click'
        event = tkinter.Event()
        event.keysym = None
        for char in value:
            event.char = char
            self.input(event)
        self._state = temp


class Label(_BaseWidget):
    """ 创建一个虚拟的标签控件，用于显示少量文本 """

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        radius: float = RADIUS,
        text: str = '',
        borderwidth: int = BORDERWIDTH,
        justify: str = tkinter.CENTER,
        font: tuple[str, int, str] = (FONT, SIZE),
        image=None,  # type: PhotoImage | None
        color_text: tuple[str, str, str] = COLOR_TEXT,
        color_fill: tuple[str, str, str] = COLOR_BUTTON_FILL,
        color_outline: tuple[str, str, str] = COLOR_BUTTON_OUTLINE
    ) -> None:
        _BaseWidget.__init__(self, canvas, x, y, width, height, radius, text, justify,
                             borderwidth, font, image, color_text, color_fill, color_outline)

    def touch(self, event: tkinter.Event) -> bool:
        """ 触碰状态检测 """
        condition = self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2
        self.state('touch' if condition else 'normal')
        return condition


class Button(_BaseWidget):
    """ 创建一个虚拟的按钮，并执行关联函数 """

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        radius: float = RADIUS,
        text: str = '',
        borderwidth: int = BORDERWIDTH,
        justify: str = tkinter.CENTER,
        font: tuple[str, int, str] = (FONT, SIZE),
        command=None,  # type: function | None
        image=None,  # type: PhotoImage | None
        color_text: tuple[str, str, str] = COLOR_TEXT,
        color_fill: tuple[str, str, str] = COLOR_BUTTON_FILL,
        color_outline: tuple[str, str, str] = COLOR_BUTTON_OUTLINE
    ) -> None:
        _BaseWidget.__init__(self, canvas, x, y, width, height, radius, text, justify,
                             borderwidth, font, image, color_text, color_fill, color_outline)
        self.command = command

    def execute(self, event: tkinter.Event) -> None:
        """ 执行关联函数 """
        condition = self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2
        if condition and self.command:
            self.command()

    def click(self, event: tkinter.Event) -> None:
        """ 交互状态检测 """
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            self.state('click')
        else:
            self.state('normal')

    def touch(self, event: tkinter.Event) -> bool:
        """ 触碰状态检测 """
        condition = self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2
        self.state('touch' if condition else 'normal')
        return condition


class Entry(_TextWidget):
    """ 创建一个虚拟的输入框控件，可输入单行少量字符，并获取这些字符 """

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        radius: float = RADIUS,
        text: tuple[str] | str = '',
        show: str | None = None,
        limit: int = LIMIT,
        cursor: str = CURSOR,
        borderwidth: int = BORDERWIDTH,
        justify: str = tkinter.LEFT,
        font: tuple[str, int, str] = (FONT, SIZE),
        image=None,  # type: PhotoImage | None
        color_text: tuple[str, str, str] = COLOR_TEXT,
        color_fill: tuple[str, str, str] = COLOR_TEXT_FILL,
        color_outline: tuple[str, str, str] = COLOR_TEXT_OUTLINE
    ) -> None:
        _TextWidget.__init__(self, canvas, x, y, width, height, radius, text, limit, justify,
                             cursor, borderwidth, font, image, color_text, color_fill, color_outline)
        self.master.itemconfigure(self.text, text=self._value[1])
        self.show = show

    def click_on(self) -> None:
        """ 控件获得焦点 """
        self.state('click')
        self.master.itemconfigure(self.text, text=self._value[0])
        self.cursor_update('')
        self.cursor_flash()

    def click_off(self) -> None:
        """ 控件失去焦点 """
        self.state('normal')

        if self.value == '':
            self.master.itemconfigure(self.text, text=self._value[1])
        else:
            self.master.itemconfigure(self.text, text=self._value[0])

    def input(self, event: tkinter.Event) -> None:
        """ 文本输入 """
        if self._state == 'click':
            if event.keysym == 'BackSpace':  # 按下退格键
                self.value = self.value[:-1]
            elif len(self.value) == self.limit:  # 达到字数限制
                return True
            elif len(event.char):
                if not event.char.isprintable() or (event.char == ' '):
                    return True
                else:  # 按下普通按键
                    self.value += event.char
            else:
                return True

            self._value[0] = len(  # 更新表面显示值
                self.value) * self.show if self.show else self.value

            # 更新显示
            self.master.itemconfigure(self.text, text=self._value[0])
            self.update_text()
            self.cursor_update()
            return True

    def update_text(self) -> None:
        """ 更新控件 """
        while True:
            pos = self.master.bbox(self.text)
            if pos[2] > self.x2-self.radius-2 or pos[0] < self.x1+self.radius+1:
                self._value[0] = self._value[0][1:]
                self.master.itemconfigure(self.text, text=self._value[0])
            else:
                break


class Text(_TextWidget):
    """ 创建一个透明的虚拟文本框，用于输入多行文本和显示多行文本（只读模式）"""

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        radius: float = RADIUS,
        text: tuple[str] | str = '',
        limit: int = LIMIT,
        read: bool = False,
        cursor: bool = CURSOR,
        borderwidth: int = BORDERWIDTH,
        justify: str = tkinter.LEFT,
        font: tuple[str, int, str] = (FONT, SIZE),
        image=None,  # type: PhotoImage | None
        color_text: tuple[str, str, str] = COLOR_TEXT,
        color_fill: tuple[str, str, str] = COLOR_TEXT_FILL,
        color_outline: tuple[str, str, str] = COLOR_TEXT_OUTLINE
    ) -> None:
        _TextWidget.__init__(self, canvas, x, y, width, height, radius, text, limit, justify,
                             cursor, borderwidth, font, image, color_text, color_fill, color_outline)

        _x = x + (width-radius-3 if justify == 'right' else width /
                  2 if justify == 'center' else radius+2)
        _anchor = 'n' if justify == 'center' else 'ne' if justify == 'right' else 'nw'

        self._text = canvas.create_text(  # 位置确定文本 NOTE:位置不要乱动
            _x, y+radius+2,
            justify=justify,
            anchor=_anchor,
            font=font,
            fill=color_text[0])

        self.read = read  # 只读模式

        # 修改多行文本靠左显示
        self.master.coords(self.text, _x, y+radius+2)
        self.master.itemconfigure(
            self.text, text=self._value[1], anchor=_anchor)
        self.master.itemconfigure(self._cursor, anchor='n')

        self.position = [0, 0]  # 行位置数

    def click_on(self) -> None:
        """ 控件获得焦点 """
        if not self.read:
            self.state('click')
            *__, _ = [''] + self._value[0].rsplit('\n', 1)
            self.master.itemconfigure(self.text, text=''.join(__))
            self.master.itemconfigure(self._text, text=_)
            self.cursor_update('')
            self.cursor_flash()

    def click_off(self) -> None:
        """ 控件失去焦点 """
        self.state('normal')

        if self.value == '':
            self.master.itemconfigure(self.text, text=self._value[1])
        else:
            *__, _ = [''] + self._value[0].rsplit('\n', 1)
            self.master.itemconfigure(self.text, text=''.join(__))
            self.master.itemconfigure(self._text, text=_)

    def input(self, event: tkinter.Event) -> bool:
        """ 文本输入 """
        if self._state == 'click':
            if event.keysym == 'BackSpace':  # 按下退格键
                self.input_backspace()
            elif len(self.value) == self.limit:  # 达到字数限制
                return True
            elif event.keysym == 'Tab':  # 按下Tab键
                self.append(' '*4)
            elif event.keysym == 'Return' or event.char == '\n':  # 按下回车键
                self.input_return()
            elif event.char.isprintable() and event.char:  # 按下其他普通的键
                _text = self.master.itemcget(self._text, 'text')
                self.master.itemconfigure(self._text, text=_text+event.char)
                _pos = self.master.bbox(self._text)

                if _pos[2] > self.x2-self.radius-2 or _pos[0] < self.x1+self.radius+1:  # 文本溢出啦
                    self.master.itemconfigure(self._text, text=_text)
                    self.input_return()
                    self.master.itemconfigure(self._text, text=event.char)

                self.value += event.char
            else:
                return True

            self.cursor_update()

            # 更新表面显示值
            text = self.master.itemcget(self.text, 'text')
            _text = self.master.itemcget(self._text, 'text')
            self._value[0] = text+'\n'+_text

            return True

    def input_return(self) -> None:
        """ 回车键功能 """
        self.value += '\n'

        # 相关数据获取
        text = self.master.itemcget(self.text, 'text')
        _text = self.master.itemcget(self._text, 'text')
        _pos = self.master.bbox(self._text)

        self.master.itemconfigure(self._text, text='')

        if _pos[3]+_pos[3]-_pos[1] < self.y2-self.radius-2:  # 还没填满文本框
            self.master.move(self._text, 0, _pos[3] - _pos[1])
            self.master.itemconfigure(
                self.text, text=text+bool(text)*'\n'+_text)
        else:  # 文本框已经被填满了
            text = text.split('\n', 1)[-1]
            self.master.itemconfigure(self.text, text=text+'\n'+_text)

            self.position[0] += 1
            self.position[1] += 1

    def input_backspace(self) -> None:
        """ 退格键功能 """
        if not self.value:  # 没有内容，删个毛啊
            return

        _text = self.master.itemcget(self._text, 'text')
        self.value = self.value[:-1]

        if _text:  # 正常地删除字符
            self.master.itemconfigure(self._text, text=_text[:-1])
        else:  # 遇到换行符
            _ = self.value.rsplit('\n', 1)[-1]
            self.master.itemconfigure(self._text, text=_)

            # 内容未超出框的大小
            if self.value == self.master.itemcget(self.text, 'text'):
                _pos = self.master.bbox(self._text)
                self.master.move(self._text, 0, _pos[1] - _pos[3])
                __ = self.value.removesuffix(_)[:-('\n' in self.value)]
            else:  # 内容已经超出框框的大小啦
                text = self.master.itemcget(self.text, 'text')
                __ = self.value.removesuffix(
                    text)[:-1].rsplit('\n', 1)[-1]+'\n'+text.removesuffix(_)[:-1]

                self.position[0] -= 1
                self.position[1] -= 1

            self.master.itemconfigure(self.text, text=__)

    def scroll(self, event: tkinter.Event) -> None:
        """ 文本滚动 """


class Progressbar(_BaseWidget):
    """ 虚拟的进度条，可以直观的方式显示任务进度 """

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        borderwidth: int = BORDERWIDTH,
        justify: str = tkinter.CENTER,
        font: tuple[str, int, str] = (FONT, SIZE),
        image=None,  # type: PhotoImage | None
        color_text: tuple[str, str, str] = COLOR_TEXT,
        color_outline: tuple[str, str, str] = COLOR_TEXT_OUTLINE,
        color_bar: tuple[str, str] = COLOR_BAR
    ) -> None:
        self.bottom = canvas.create_rectangle(
            x, y, x+width, y+height, width=borderwidth, fill=color_bar[0])
        self.bar = canvas.create_rectangle(
            x, y, x, y+height, width=borderwidth, outline='', fill=color_bar[1])

        _BaseWidget.__init__(self, canvas, x, y, width, height, 0, '0.00%', justify,
                             borderwidth, font, image, color_text, COLOR_NONE, color_outline)

        self.color_fill = list(color_bar)

    def touch(self, event: tkinter.Event) -> bool:
        """ 触碰状态检测 """
        condition = self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2
        self.state('touch' if condition else 'normal')
        return condition

    def load(self, percentage: float) -> None:
        """
        进度条加载，并更新外观
        `percentage`: 进度条的值，范围 0~1
        """
        percentage = 0 if percentage < 0 else 1 if percentage > 1 else percentage
        x2 = self.x1 + self.width * percentage * self.master.rx
        self.master.coords(self.bar, self.x1, self.y1, x2, self.y2)
        self.configure(text='%.2f%%' % (percentage * 100))


class PhotoImage(tkinter.PhotoImage):
    """ 生成图片并进行相应的一些处理 """

    def __init__(
        self,
        file: str | bytes,
        **kw
    ) -> None:
        """
        `file`: 图片文件的路径
        `**kw`: 与 tkinter.PhotoImage 的参数相同
        """
        self.file = file  # 图片文件的路径
        self.extension = file.rsplit('.', 1)[-1]  # 文件扩展名
        self._item = {}  # type: dict[tkinter._CanvasItemId, Canvas | None]

        if self.extension == 'gif':  # 动态图片
            self.image: list[tkinter.PhotoImage] = []
        else:  # 静态图片
            self.image = tkinter.PhotoImage.__init__(self, file=file, **kw)

    def parse(self, start: int = 0) -> Generator[int, None, None]:
        """
        解析动图，返回一个生成器
        `start`: 动图解析的起始索引（帧数-1）
        """
        try:
            while True:
                self.image.append(tkinter.PhotoImage(
                    file=self.file, format='gif -index %d' % start))
                value = yield start  # 抛出索引
                start += value if value else 1
        except tkinter.TclError:
            return

    def play(
        self,
        canvas: Canvas,
        item,  # type: tkinter._CanvasItemId
        interval: int,
        **kw
    ) -> None:
        """
        播放动图，canvas.lock为False会暂停
        `canvas`: 播放动画的画布
        `item`: 播放动画的 _CanvasItemId（create_text 的返回值）
        `interval`: 每帧动画的间隔时间
        """
        if kw.get('_ind', None) == None:  # 初始化的判定
            self._item[item], kw['ind'] = canvas, -1
        if not self._item[item]:  # 终止播放的判定
            return
        if canvas._lock:  # 暂停播放的判定
            canvas.itemconfigure(item, image=self.image[kw['_ind']])
        canvas.after(interval, lambda: self.play(  # 迭代执行函数
            canvas, item, interval, _ind=0 if (_ind := kw['_ind']+1) == len(self.image) else _ind))

    def stop(
        self,
        item,  # type: tkinter._CanvasItemId
        clear: bool = False
    ) -> None:
        """
        终止动图的播放
        `item`: 播放动画的 _CanvasItemId（create_text 的返回值）
        `clear`: 清除图片的标识
        """
        self._item[item] = None
        if clear:  # 清除背景
            self._item[item].itemconfigure(item, image=None)

    def zoom(self, rate_x: float, rate_y: float, precision: float | None = None) -> tkinter.PhotoImage:
        """
        缩放图片
        `rate_x`: 横向缩放倍率
        `rate_y`: 纵向缩放倍率
        `precision`: 精度到小数点后的位数（推荐 1.2），越大运算就越慢（默认值代表绝对精确）
        """
        if precision != None:
            limit = round(10**precision)
            rate_x = Fraction(str(rate_x)).limit_denominator(limit)
            rate_y = Fraction(str(rate_y)).limit_denominator(limit)
            image = tkinter.PhotoImage.zoom(
                self, rate_x.numerator, rate_y.numerator)
            image = image.subsample(rate_x.denominator, rate_y.denominator)
        else:
            width, height = int(self.width()*rate_x), int(self.height()*rate_y)
            image = tkinter.PhotoImage(width=width, height=height)
            for x in range(width):
                for y in range(height):
                    image.put('#%02X%02X%02X' % self.get(
                        int(x/rate_x), int(y/rate_y)), (x, y))

        return image


class Singleton(object):
    """ 单例模式类，用于继承 """

    _instance = None

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance


def move(
    master: Tk | Canvas | tkinter.Misc | tkinter.BaseWidget,
    widget: Canvas | _BaseWidget | tkinter.BaseWidget,
    dx: int,
    dy: int,
    times: int,
    mode: Iterable | Literal['smooth', 'rebound', 'flat'],
    frames: int = FRAMES,
    end=None,  # type: function | None
    _ind: int = 0
) -> None:
    """
    ### 移动函数
    以特定方式移动由 Place 布局的某个控件或某些控件的集合或图像\n
    `master`: 控件所在的父控件
    `widget`: 要移动位置的控件
    `dx`: 横向移动的距离（单位：像素）
    `dy`: 纵向移动的距离（单位：像素）
    `times`: 移动总时长（单位：毫秒）
    `mode`: 移动速度模式，为 smooth（顺滑）、rebound（回弹）和 flat（平移）这三种，或者为元组 (函数, 起始值, 终止值) 的形式
    `frames`: 帧数，越大移动就越流畅，但计算越慢（范围为 1~100）
    `end`: 移动结束时执行的函数
    """
    if _ind:  # 记忆值
        dis = mode
    elif mode == 'flat':  # 平滑模式
        return move(master, widget, dx, dy, times, (lambda _: 1, 0, 1), frames, end)
    elif mode == 'smooth':  # 流畅模式
        return move(master, widget, dx, dy, times, (math.sin, 0, math.pi), frames, end)
    elif mode == 'rebound':  # 回弹模式
        return move(master, widget, dx, dy, times, (math.cos, 0, 0.6*math.pi), frames, end)
    else:  # 函数模式
        func, start, stop, count = *mode, round(times*frames/1000)
        interval = (stop-start) / count
        dis = tuple(func(start+interval*i) for i in range(1, count+1))
        key = 1 / sum(dis)
        dis = tuple((key*i*dx, key*i*dy) for i in dis)

    if isinstance(widget, tkinter.Tk | tkinter.Toplevel):  # 窗口
        geometry, ox, oy = widget.geometry().split('+')
        widget.geometry(
            '%s+%d+%d' % (geometry, int(ox)+dis[_ind][0], int(oy)+dis[_ind][1]))
    elif isinstance(master, tkinter.Misc) and isinstance(widget, tkinter.BaseWidget):  # tkinter 的控件
        place_info = widget.place_info()
        origin_x, origin_y = float(place_info['x']), float(place_info['y'])
        widget.place(x=origin_x+dis[_ind][0], y=origin_y+dis[_ind][1])
    elif isinstance(master, Canvas) and isinstance(widget, _BaseWidget):  # 虚拟画布控件
        widget.move(dis[_ind][0], dis[_ind][1])
    elif isinstance(widget, int):  # tkinter._CanvasItemId
        master.move(widget, dis[_ind][0], dis[_ind][1])
    else:  # 其他自定义情况
        widget.move(dis[_ind][0], dis[_ind][1])

    if _ind+1 == round(times*frames/1000):  # 停止条件
        return end() if end else None

    master.after(
        round(times/frames), move, master, widget, dx, dy, times, dis, frames, end, _ind+1)  # 间隔一定时间执行函数


def text(
    length: int,
    string: str,
    position: Literal['left', 'center', 'right'] = 'center'
) -> str:
    """
    ### 文本函数
    可将目标字符串改为目标长度并居中对齐，ASCII 码字符算 1 个长度，中文及其他字符算 2 个\n
    `length`: 目标长度
    `string`: 要修改的字符串
    `position`: 文本处于该长度范围的位置，可选 left（靠左）、center（居中）和 right（靠右）这三个值
    """
    length -= sum(1 + (ord(i) >= 256) for i in string)  # 计算空格总个数
    if position == 'left':  # 靠左
        return ' '*length+string
    elif position == 'right':  # 靠右
        return string+length*' '
    else:  # 居中
        length, key = divmod(length, 2)
        return ' '*length+string+(length+key)*' '


def color(
    color: Iterable[str] | str,
    proportion: float = 1.
) -> str:
    """
    ### 颜色函数
    按一定比例给出已有 RGB 颜色字符串的渐变 RGB 颜色字符串，或颜色的对比色\n
    `color`: 颜色元组或列表 (初始颜色, 目标颜色)，或者一个颜色字符串（此时返回对比色）
    `proportion`: 改变比例（浮点数，范围为 0~1）
    """
    rgb, _rgb = [[None]*3, [None]*3], 0

    if isinstance(color, str):  # 对比色的情况处理
        color = color, '#%06X' % (16777216-int(color[1:], 16))

    for i, c in enumerate(color):  # 解析颜色的 RGB
        _ = int(c[1:], 16)
        _, rgb[i][2] = divmod(_, 256)
        rgb[i][:2] = divmod(_, 256)

    for c, _c in zip(*rgb):  # 根据比率计算返回值
        _rgb <<= 8
        _rgb += c + round((_c - c) * proportion)

    return '#%06X' % _rgb


def SetProcessDpiAwareness(awareness: Literal[0, 1, 2] = PROCESS_SYSTEM_DPI_AWARE) -> None:
    """
    ### 设定程序DPI级别
    设定窗口程序的DPI级别，让系统知道该对程序如何缩放\n
    `awareness`: DPI级别，值可以为0、1和2，程序默认为0，默认值为1
    """
    OleDLL('shcore').SetProcessDpiAwareness(awareness)
