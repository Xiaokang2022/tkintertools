"""
tkintertools
============
The tkindertools module is an auxiliary module of the tkinder module.
Minimum Requirement: Python3.10.

Provides:
1. Transparent, rounded and customized widgets
2. Automatic control of picture size and widget size
3. Scalable png pictures and playable gif pictures
4. Regular mobile widgets and canvas interfaces
5. Gradient colors and contrast colors
6. Text with controllable length and alignment
7. Convenient, inheritable singleton pattern class

Base Information
----------------
* Author: XiaoKang2022<2951256653@qq.com>
* Version: 2.5.3
* Update: 2022/11/26

Contents
--------
* Container Widget: `Tk`, `Toplevel`, `Canvas`
* Virtual Canvas Widget: `CanvasLabel`, `CanvasButton`, `CanvasEntry`, `CanvasText`
* Tool Class: `PhotoImage`, `Singleton`
* Tool Function: `move_widget`, `correct_text`, `change_color`

More
----
* GitHub: https://github.com/392126563/tkintertools
* GitCode: https://gitcode.net/weixin_62651706/tkintertools
* Column: https://blog.csdn.net/weixin_62651706/category_11600888.html
* Tutorials: https://xiaokang2022.blog.csdn.net/article/details/127374661
"""

import tkinter
from sys import version_info
from typing import Generator, Literal, Self

__author__ = 'XiaoKang2022'
__version__ = '2.5.3'
__all__ = (
    'Tk',
    'Toplevel',
    'Canvas',
    'PhotoImage',
    'CanvasLabel',
    'CanvasButton',
    'CanvasEntry',
    'CanvasText',
    'move_widget',
    'correct_text',
    'change_color',
    'Singleton',
)

if version_info < (3, 10):
    raise RuntimeError('\033[36mPython version is too low!\033[0m\a')


COLOR_FILL_BUTTON = '#E1E1E1', '#E5F1FB', '#CCE4F7', '#F0F0F0'      # 默认的按钮内部颜色
COLOR_FILL_TEXT = '#FFFFFF', '#FFFFFF', '#FFFFFF', '#F0F0F0'        # 默认的文本内部颜色
COLOR_OUTLINE_BUTTON = '#C0C0C0', '#4A9EE0', '#4884B4', '#D5D5D5'   # 默认的按钮外框颜色
COLOR_OUTLINE_TEXT = '#C0C0C0', '#5C5C5C', '#4A9EE0', '#D5D5D5'     # 默认的文本外框颜色
COLOR_TEXT = '#000000', '#000000', '#000000', '#A3A9AC'             # 默认的文本颜色
COLOR_NONE = '', '', '', ''                                         # 透明颜色

BORDERWIDTH = 1     # 默认控件外框宽度
CURSOR = '│'        # 文本光标
FONT = '楷体', 15   # 默认字体
LIMIT = -1          # 默认文本长度
NULL = ''           # 空字符
RADIUS = 0          # 默认控件圆角半径


class Tk(tkinter.Tk):
    """
    ### Tk类
    用于集中处理 `Canvas` 绑定的关联事件以及缩放操作
    """

    def __init__(
        self,
        title: str | None = None,
        geometry: str | None = None,
        minisize: tuple[int, int] | None = None,
        alpha: float | None = None,
        proportion_lock: bool = False,
        shutdown=None,  # type: function | None
        **kw
    ) -> None:
        """
        ### 参数说明
        `title`: 窗口标题
        `geometry`: 窗口大小及位置（格式：'宽度x高度+左上角横坐标+左上角纵坐标' 或者 '宽度x高度'）
        `minisize`: 窗口的最小缩放大小（默认为参数 geometry 的宽度与高度）
        `alpha`: 窗口透明度，范围为0~1，0为完全透明
        `proportion_lock`: 窗口缩放是否保持原比例
        `shutdown`: 关闭窗口之前执行的函数（会覆盖原关闭操作）
        `**kw`: 与原 tkinter 模块中的 Tk 类的参数相同
        """

        self.proportion_lock = proportion_lock

        # 宽高比例
        self._proportion = None
        # 宽高值
        self._width = 1
        self._height = 1
        # 初始宽高值
        self.width = 100
        self.height = 100

        # 子窗口列表（与Toplevel有关）
        self.toplevel_list: list[Toplevel] = []
        # 子画布列表（与缩放绑定有关）
        self.canvas_list: list[Canvas] = []

        tkinter.Tk.__init__(self, **kw)

        if geometry:
            self.geometry(geometry)
            if not minisize:
                self.minsize(*map(int, geometry.split('+')[0].split('x')))
        if title:
            self.title(title)
        if alpha != None:
            self.attributes('-alpha', alpha)
        if minisize:
            self.minsize(*minisize)
        if shutdown:
            self.protocol('WM_DELETE_WINDOW', shutdown)

        # 开启窗口缩放检测
        self.bind('<Configure>', self.zoom)

    def zoom(self, event: tkinter.Event) -> None:
        """ 内部方法：缩放检测 """
        if not self._proportion:
            # 记住初始化窗口宽高比例
            self._proportion = event.width / event.height
            # 记住初始化的窗口大小
            self._width = event.width
            self._height = event.height
            return

        if event.width != self._width or event.height != self._height:
            # 窗口大小改变
            if self.proportion_lock:  # NOTE: 比例同步有待优化
                # 使高度和宽度成比例同步变化
                delta = event.width / self._proportion-event.height
                if event.width not in (self._width, self.winfo_screenwidth()):  # 宽度改变
                    event.height += round(delta)
                elif event.height not in (self._height, self.winfo_screenheight()):  # 高度改变
                    event.width -= round(delta * self._proportion)
                self.geometry('%sx%s' % (event.width, event.height))

            # 更新子画布控件的大小
            for canvas in self.canvas_list:
                if canvas.expand:
                    # 更新画布的横纵缩放比率
                    canvas.rate_x = event.width / canvas.width
                    canvas.rate_y = event.height / canvas.height

                    # 相对缩放对所有Canvas生效
                    self.zoom_relative(
                        canvas, event.width / self._width, event.height / self._height)
                    if canvas.lock:
                        # 绝对缩放仅对当前Canvas生效
                        self.zoom_absolute(canvas)

            # 更新默认参数
            self._width = event.width
            self._height = event.height

    @staticmethod
    def zoom_relative(
        canvas,  # type: Canvas
        rate_x: float,
        rate_y: float
    ) -> None:
        """ 内部方法：相对缩放 """
        # 更新画布位置
        if canvas.lock:
            info = canvas.place_info()
            tkinter.Canvas.place(
                canvas,
                x=round(float(info['x'])*rate_x),
                y=round(float(info['y'])*rate_y))

        # 更新子画布控件的子虚拟画布控件位置数据
        for widget in canvas.widget_list:
            widget.x1 *= rate_x
            widget.x2 *= rate_x
            widget.y1 *= rate_y
            widget.y2 *= rate_y

        # 更新子画布控件的子虚拟画布控件的位置
        for item in canvas.item_dict:
            coords = [c * rate_y if i % 2 else c * rate_x for i,
                      c in enumerate(canvas.coords(item))]
            canvas.coords(item, coords)

    @staticmethod
    def zoom_absolute(
        canvas  # type: Canvas
    ) -> None:
        """ 内部方法：绝对缩放 """
        # 缩放画布
        tkinter.Canvas.place(
            canvas,
            width=canvas.width*canvas.rate_x,
            height=canvas.height*canvas.rate_y)

        # 缩放控件
        for item, key in canvas.item_dict.items():
            if key[0] == 'font':  # BUG: 字体缩小时有 bug
                # 字体大小修改
                font: str = canvas.itemcget(item, 'font')
                if font:
                    font = font.split()
                    font[1] = int(key[1] * min(canvas.rate_x, canvas.rate_y))
                    canvas.itemconfigure(item, font=font)
            elif key[0] == 'width':
                # 宽度大小修改
                rate = min(canvas.rate_x, canvas.rate_y)
                canvas.itemconfigure(item, width=float(key[1])*rate)
            elif key[0] == 'image':
                # 图像大小缩放
                if key[1] and key[1].file.split('.')[-1] == 'png':
                    key[2] = key[1].zoom(canvas.rate_x, canvas.rate_y, 1.1)
                    canvas.itemconfigure(item, image=key[2])

    @staticmethod
    def __touch(
        event: tkinter.Event,
        canvas  # type: Canvas
    ) -> None:
        """ 绑定鼠标触碰控件事件 """
        if canvas.lock:
            for widget in canvas.widget_list[::-1]:
                if widget.live:
                    if widget.touch(event):
                        if isinstance(widget, CanvasButton):
                            canvas.configure(cursor='hand2')
                        elif isinstance(widget, _TextWidget):
                            canvas.configure(cursor='xterm')
                        else:
                            canvas.configure(cursor='arrow')
                        return
            else:
                canvas.configure(cursor='arrow')

    @staticmethod
    def __press(
        event: tkinter.Event,
        canvas  # type: Canvas
    ) -> None:
        """ 绑定鼠标左键按下事件 """
        if canvas.lock:
            for widget in canvas.widget_list:
                if isinstance(widget, CanvasButton | CanvasEntry | CanvasText):
                    if widget.live:
                        # press 无需加速，其有额外作用
                        widget.press(event)

    @staticmethod
    def __release(
        event: tkinter.Event,
        canvas  # type: Canvas
    ) -> None:
        """ 绑定鼠标左键松开事件 """
        if canvas.lock:
            for widget in canvas.widget_list[::-1]:
                if isinstance(widget, CanvasButton):
                    if widget.live:
                        widget.touch(event)
                        if widget.execute(event):
                            return

    @staticmethod
    def __mousewheel(
        event: tkinter.Event,
        canvas  # type: Canvas
    ) -> None:
        """ 绑定鼠标滚轮滚动事件 """
        if canvas.lock:
            for widget in canvas.widget_list[::-1]:
                if isinstance(widget, CanvasText):
                    if widget.live:
                        if widget.scroll(event):
                            return

    def __input(self, event: tkinter.Event) -> None:
        """ 绑定键盘输入字符事件 """
        for canvas in self.canvas_list:
            if canvas.lock:
                for widget in canvas.widget_list[::-1]:
                    if isinstance(widget, CanvasEntry | CanvasText):
                        if widget.live:
                            if widget.input(event):
                                return

    def __paste(self) -> None:
        """ 快捷键粘贴 """
        for canvas in self.canvas_list:
            if canvas.lock:
                for widget in canvas.widget_list[::-1]:
                    if isinstance(widget, CanvasEntry | CanvasText):
                        if widget.live:
                            if widget.paste():
                                return

    def bind_event(self) -> None:
        """ 内部方法：关联事件的绑定 """
        # 绑定键盘输入字符
        self.bind('<Any-Key>', self.__input)
        # 绑定粘贴快捷键
        self.bind('<Control-KeyPress-v>', lambda _: self.__paste())

        for canvas in self.canvas_list:
            # 绑定鼠标触碰控件
            canvas.bind('<Motion>', lambda event,
                        _=canvas: self.__touch(event, _))
            # 绑定鼠标左键按下
            canvas.bind('<Button-1>', lambda event,
                        _=canvas: self.__press(event, _))
            # 绑定鼠标左键松开
            canvas.bind('<ButtonRelease-1>', lambda event,
                        _=canvas: self.__release(event, _))
            # 绑定鼠标左键按下移动
            canvas.bind('<B1-Motion>', lambda event,
                        _=canvas: self.__press(event, _))
            # 绑定鼠标滚轮滚动
            canvas.bind('<MouseWheel>', lambda event,
                        _=canvas: self.__mousewheel(event, _))

    def geometry(self, newGeometry: str | None = None) -> str | None:
        # 重写：添加修改初始宽高值的功能
        if newGeometry:
            self.width, self.height = map(
                int, newGeometry.split('+')[0].split('x'))
        return tkinter.Tk.geometry(self, newGeometry)

    def mainloop(self) -> None:
        # 重写：开启基本事件绑定
        self.bind_event()
        for toplevel in self.toplevel_list:
            toplevel.bind_event()
        tkinter.Tk.mainloop(self)

    def all_canvas(self) -> tuple:
        """ 返回窗口所有画布的元组 """
        return tuple(self.canvas_list)


class Toplevel(tkinter.Toplevel, Tk):
    """
    ### Toplevel 类
    用法类似于原 tkinter 模块里的 Toplevel，
    同时增加了 Tk 的功能
    """

    def __init__(
        self,
        master: Tk,
        title: str | None = None,
        geometry: str | None = None,
        minisize: tuple[int, int] | None = None,
        alpha: float | None = None,
        proportion_lock: bool = False,
        shutdown=None,  # type: function | None
        **kw
    ) -> None:
        """
        ### 参数说明
        `master`: 父窗口
        `title`: 窗口标题
        `geometry`: 窗口大小及位置（格式：'宽度x高度+左上角横坐标+左上角纵坐标' 或者 '宽度x高度'）
        `minisize`: 窗口的最小缩放大小（默认为参数 geometry 的宽度与高度）
        `alpha`: 窗口透明度，范围为0~1，0为完全透明
        `proportion_lock`: 窗口缩放是否保持原比例
        `shutdown`: 关闭窗口之前执行的函数（会覆盖关闭操作）
        `**kw`: 与原 tkinter 模块中的 Toplevel 类的参数相同
        """

        self.master = master
        self.proportion_lock = proportion_lock

        # 宽高比例
        self._proportion = None
        # 宽高值
        self._width = 1
        self._height = 1
        # 初始宽高值
        self.width = 100
        self.height = 100

        # 子窗口列表（与Toplevel有关）
        self.toplevel_list: list[Toplevel] = []
        # 子画布列表（与缩放绑定有关）
        self.canvas_list: list[Canvas] = []

        tkinter.Toplevel.__init__(self, master=master, **kw)

        if geometry:
            self.geometry(geometry)
            if not minisize:
                self.minsize(*map(int, geometry.split('+')[0].split('x')))
        if title:
            self.title(title)
        if alpha != None:
            self.attributes('-alpha', alpha)
        if minisize:
            self.minsize(*minisize)
        if shutdown:
            self.protocol('WM_DELETE_WINDOW', shutdown)

        # 开启窗口缩放检测
        self.bind('<Configure>', self.zoom)

        # 将实例添加到父控件的子窗口列表中
        master.toplevel_list.append(self)


class Canvas(tkinter.Canvas):
    """
    ### 画布类
    用于承载虚拟的画布控件
    """

    def __init__(
        self,
        master: Tk,
        width: int,
        height: int,
        lock: bool = True,
        expand: bool = True,
        **kw
    ) -> None:
        """
        ### 参数说明
        `master`: 父控件
        `width`: 画布宽度
        `height`: 画布高度
        `lock`: 画布内控件的功能锁（False 时没有功能）
        `expand`: 画布内控件是否能缩放
        `**kw`: 与原 tkinter 模块内 Canvas 类的参数相同
        """

        self.width = width
        self.height = height
        self.lock = lock
        self.expand = expand

        # 放缩比率
        self.rate_x = 1
        self.rate_y = 1

        # 子控件列表（与事件绑定有关）
        self.widget_list: list[_BaseWidget] = []
        # 子item字典（与大小缩放有关）
        self.item_dict = {}  # type: dict[tkinter._CanvasItemId, tuple | list]

        tkinter.Canvas.__init__(self, master, width=width,
                                height=height, highlightthickness=0, **kw)

        # 将实例添加到 Tk 的画布列表中
        master.canvas_list.append(self)

    def setlock(self, boolean: bool) -> None:
        """ 设置画布锁 """
        self.lock = boolean
        self.master: Tk
        if self.lock and self.expand:
            self.master.zoom_absolute(self)

    def all_widget(self) -> tuple:
        """ 返回画布所有控件元组 """
        return tuple(self.widget_list)

    def create_text(self, *args, **kw):
        # 重写：添加对 text 类型的 _CanvasItemId 的字体大小的控制
        if not (_ := kw.get('font')):
            kw['font'] = ('楷体', 10)  # 默认字体
        elif type(_) == str:
            kw['font'] = (_, 10)
        item = tkinter.Canvas.create_text(self, *args, **kw)
        self.item_dict[item] = 'font', kw['font'][1]
        return item

    def create_image(self, *args, **kw):
        # 重写：添加对 image 类型的 _CanvasItemId 的图像大小的控制
        item = tkinter.Canvas.create_image(self, *args, **kw)
        self.item_dict[item] = ['image', kw.get('image'), None]
        return item

    def create_rectangle(self, *args, **kw):
        # 重写：添加对 rectangle 类型的 _CanvasItemId 的线条宽度的控制
        item = tkinter.Canvas.create_rectangle(self, *args, **kw)
        self.item_dict[item] = 'width', self.itemcget(item, 'width')
        return item

    def create_line(self, *args, **kw):
        # 重写：添加对 line 类型的 _CanvasItemId 的线条宽度的控制
        item = tkinter.Canvas.create_line(self, *args, **kw)
        self.item_dict[item] = 'width', self.itemcget(item, 'width')
        return item

    def create_oval(self, *args, **kw):
        # 重写：添加对 oval 类型的 _CanvasItemId 的线条宽度的控制
        item = tkinter.Canvas.create_oval(self, *args, **kw)
        self.item_dict[item] = 'width', self.itemcget(item, 'width')
        return item

    def create_arc(self, *args, **kw):
        # 重写：添加对 arc 类型的 _CanvasItemId 的线条宽度的控制
        item = tkinter.Canvas.create_arc(self, *args, **kw)
        self.item_dict[item] = 'width', self.itemcget(item, 'width')
        return item

    def create_polygon(self, *args, **kw):
        # 重写：添加对 polygon 类型的 _CanvasItemId 的线条宽度的控制
        item = tkinter.Canvas.create_polygon(self, *args, **kw)
        self.item_dict[item] = 'width', self.itemcget(item, 'width')
        return item

    def create_bitmap(self, *args, **kw):  # NOTE: 有待进一步研究
        # 重写：目前仅有防报错作用
        item = tkinter.Canvas.create_bitmap(self, *args, **kw)
        self.item_dict[item] = None, None
        return item

    def create_window(self, *args, **kw):  # NOTE: 有待进一步研究
        # 重写：目前仅有防报错作用
        item = tkinter.Canvas.create_window(self, *args, **kw)
        self.item_dict[item] = None, None
        return item

    def itemconfigure(
        self,
        tagOrId,  # type: str | tkinter._CanvasItemId
        **kw
    ) -> dict[str, tuple[str, str, str, str, str]] | None:
        # 重写：创建空image的_CanvasItemId时漏去对图像大小的控制
        if type(kw.get('image')) == PhotoImage and not self.itemcget(tagOrId, 'image'):
            self.item_dict[tagOrId] = ['image', kw.get('image'), None]
        return tkinter.Canvas.itemconfigure(self, tagOrId, **kw)

    def place(self, *args, **kw) -> None:
        # 重写：增加一些特定功能
        self.width = kw.get('wdith', self.width)
        self.height = kw.get('height', self.height)
        return tkinter.Canvas.place(self, *args, **kw)

    def destroy(self) -> None:
        # 重写：兼容
        for widget in self.widget_list[:]:
            widget.destroy()
        self.master.canvas_list.remove(self)
        return tkinter.Canvas.destroy(self)


class _BaseWidget:
    """ 内部类 """

    def __init__(
        self,
        canvas: Canvas,
        x: float,
        y: float,
        width: float,
        height: float,
        radius: int,
        text: str,
        justify: str,
        borderwidth: float,
        font: tuple[str, int, str],
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
        `color_text`: 控件文本的颜色
        `color_fill`: 控件内部的颜色
        `color_outline`: 控件外框的颜色
        ---
        ### 特定参数
        `command`: 按钮控件的关联函数
        `show`: 文本控件的显示文本
        `limit`: 文本控件的输入字数限制，为负数时表示没有字数限制
        `space`: 文本控件能否输入空格的标识
        `read`: 文本控件的只读模式
        `cursor`: 输入提示符的字符，默认为一竖线
        ---
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
        self.color_text = list(color_text)
        self.color_fill = list(color_fill)
        self.color_outline = list(color_outline)

        # 控件左上角坐标
        self.x1, self.y1 = x, y
        # 控件左下角坐标
        self.x2, self.y2 = x+width, y+height
        # 控件的宽高值
        self.width, self.height = width, height
        # 边角圆弧半径
        self.radius = radius
        # 控件活跃标志
        self.live = True
        # 控件的状态
        self._state = 'normal'

        # 将实例添加到父画布控件
        canvas.widget_list.append(self)

        if radius:
            if 2 * radius > width:
                radius = width // 2
                self.radius = radius
            if 2 * radius > height:
                radius = height // 2
                self.radius = radius

            d = 2*radius  # 圆角直径
            _x, _y, _w, _h = x+radius, y+radius, width-d, height-d

            # 虚拟控件内部填充颜色
            kw = {'outline': NULL, 'fill': color_fill[0]}
            self.inside = [
                canvas.create_rectangle(
                    x, _y, x+width, y+height-radius, **kw),
                canvas.create_rectangle(
                    _x, y, x+width-radius, y+height, **kw),
                canvas.create_arc(
                    x, y, x+d, y+d, start=90, extent=100, **kw),
                canvas.create_arc(
                    x+_w, y, x+width, y+d, start=0, extent=100, **kw),
                canvas.create_arc(
                    x, y+_h, x+d, y+height, start=180, extent=100, **kw),
                canvas.create_arc(
                    x+_w, y+_h, x+width, y+height, start=270, extent=100, **kw)]

            # 虚拟控件外框
            kw = {'extent': 100, 'style': 'arc', 'outline': color_outline[0]}
            self.outside = [
                canvas.create_line(
                    _x, y, x+width-radius, y, fill=color_outline[0]),
                canvas.create_line(
                    _x, y+height, x+width-radius, y+height, fill=color_outline[0]),
                canvas.create_line(
                    x, _y, x, y+height-radius, fill=color_outline[0]),
                canvas.create_line(
                    x+width, _y, x+width, y+height-radius+1, fill=color_outline[0]),
                canvas.create_arc(
                    x, y, x+d, y+d, start=90, **kw),
                canvas.create_arc(
                    x+_w, y, x+width, y+d, start=0, **kw),
                canvas.create_arc(
                    x, y+_h, x+d, y+height, start=180, **kw),
                canvas.create_arc(
                    x+_w, y+_h, x+width, y+height, start=270, **kw)]
        else:
            # 虚拟控件的外框
            self.rect = canvas.create_rectangle(
                x, y, x+width, y+height,
                width=borderwidth,
                outline=color_outline[0],
                fill=color_fill[0])

        # 虚拟控件显示的文字
        self.text = canvas.create_text(
            x + (radius+2 if justify == 'left' else width-radius-3
                 if justify == 'right' else width / 2),
            y + height / 2,
            text=text,
            font=font,
            justify=justify,
            anchor='w' if justify == 'left' else 'e' if justify == 'right' else 'center',
            fill=color_text[0])

    def state(self, mode: Literal['normal', 'touch', 'press', 'disabled'] | None = None) -> None:
        """
        mode 参数为 None 时仅更新控件，否则改变虚拟控件的外观
        `normal`: 正常状态
        `touch`: 鼠标触碰时的状态
        `press`: 鼠标按下时的状态
        `disabled`: 禁用状态
        """
        if mode:
            self._state = mode

        if self._state == 'normal':
            mode = 0
        elif self._state == 'touch':
            mode = 1
        elif self._state == 'press':
            mode = 2
        else:
            mode = 3

        self.master.itemconfigure(self.text, fill=self.color_text[mode])
        if isinstance(self, CanvasText):
            self.master.itemconfigure(self._text, fill=self.color_text[mode])

        if self.radius:
            # 修改色块
            for item in self.inside:
                self.master.itemconfigure(item, fill=self.color_fill[mode])

            # 修改线条
            for item in self.outside[:4]:
                self.master.itemconfigure(item, fill=self.color_outline[mode])
            for item in self.outside[4:]:
                self.master.itemconfigure(
                    item, outline=self.color_outline[mode])
        else:
            self.master.itemconfigure(self.rect, fill=self.color_fill[mode])
            self.master.itemconfigure(
                self.rect, outline=self.color_outline[mode])

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

        self.master.move(self.text, dx, dy)
        if isinstance(self, CanvasText):
            self.master.move(self._text, dx, dy)

        if hasattr(self, 'cursor'):
            self.cursor: tkinter._CanvasItemId
            self.master.move(self.cursor, dx, dy)

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

        if value := kw.get('text', None):
            self.value = value
        if text := kw.get('color_text', None):
            self.color_text = text
        if fill := kw.get('color_fill', None):
            self.color_fill = fill
        if outline := kw.get('color_outline', None):
            self.color_outline = outline

        if isinstance(self, CanvasLabel | CanvasButton) and value:
            self.master.itemconfigure(self.text, text=value)

    def destroy(self) -> None:
        """ 摧毁控件释放内存 """
        self.live = False
        self.master.widget_list.remove(self)

        if self.radius:
            for item in self.inside+self.outside:
                self.master.delete(item)
        else:
            self.master.delete(self.rect)
        if isinstance(self, _TextWidget):
            self.master.delete(self.cursor)
        if isinstance(self, CanvasText):
            self.master.delete(self._text)
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
                # TODO
                # if isinstance(self, CanvasText):
                #     self.scrollbar.configure(
                #         color_fill=COLOR_NONE,
                #         color_outline=COLOR_NONE)


class CanvasLabel(_BaseWidget):
    """
    ### 虚拟画布标签控件
    创建一个虚拟的标签控件，用于显示少量文本
    """

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        radius: int = RADIUS,
        text: str = NULL,
        borderwidth: int = BORDERWIDTH,
        justify: str = tkinter.CENTER,
        font: tuple[str, int, str] = FONT,
        color_text: tuple[str, str, str] = COLOR_TEXT,
        color_fill: tuple[str, str, str] = COLOR_FILL_BUTTON,
        color_outline: tuple[str, str, str] = COLOR_OUTLINE_BUTTON
    ) -> None:
        _BaseWidget.__init__(self, canvas, x, y, width, height, radius, text, justify,
                             borderwidth, font, color_text, color_fill, color_outline)

    def touch(self, event: tkinter.Event) -> bool:
        """ 触碰状态检测 """
        condition = self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2
        self.state('touch' if condition else 'normal')
        return condition


class CanvasButton(_BaseWidget):
    """
    ### 虚拟画布按钮控件
    创建一个虚拟的按钮，并执行关联函数
    """

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        radius: int = RADIUS,
        text: str = NULL,
        borderwidth: int = BORDERWIDTH,
        justify: str = tkinter.CENTER,
        font: tuple[str, int, str] = FONT,
        command=None,  # type: function | None
        color_text: tuple[str, str, str] = COLOR_TEXT,
        color_fill: tuple[str, str, str] = COLOR_FILL_BUTTON,
        color_outline: tuple[str, str, str] = COLOR_OUTLINE_BUTTON
    ) -> None:
        _BaseWidget.__init__(self, canvas, x, y, width, height, radius, text, justify,
                             borderwidth, font, color_text, color_fill, color_outline)
        self.command = command

    def execute(self, event: tkinter.Event) -> bool:
        """ 执行关联函数 """
        condition = self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2
        if condition and self.command:
            self.command()
        return condition

    def press(self, event: tkinter.Event) -> None:
        """ 交互状态检测 """
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            self.state('press')
        else:
            self.state('normal')

    def touch(self, event: tkinter.Event) -> bool:
        """ 触碰状态检测 """
        condition = self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2
        self.state('touch' if condition else 'normal')
        return condition


class _TextWidget(_BaseWidget):
    """ 内部类 """

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        radius: int,
        text: tuple[str] | str,
        limit: int,
        space: bool,
        justify: str,
        icursor: str,
        borderwidth: int,
        font: tuple[str, int, str],
        color_text: tuple[str, str, str],
        color_fill: tuple[str, str, str],
        color_outline: tuple[str, str, str]
    ) -> None:

        self.limit = limit
        self.space = space
        self.icursor = icursor

        # 表面显示值
        self.value_surface = NULL
        # 光标闪烁间隔
        self._cursor_time = 300
        # 光标闪烁标志
        self._cursor = False

        if type(text) == str:
            self.value_normal, self.value_touch = text, NULL
        else:
            self.value_normal, self.value_touch = text

        _BaseWidget.__init__(self, canvas, x, y, width, height, radius, NULL, justify,
                             borderwidth, font, color_text, color_fill, color_outline)

        # 鼠标光标（位置顺序不可乱动）
        self.cursor = canvas.create_text(0, 0, font=font, fill=color_text[2])

    def touch_on(self) -> None:
        """ 鼠标悬停状态 """
        if self._state != 'press':
            self.state('touch')

            # 判断显示的值是否为第一默认值
            if self.master.itemcget(self.text, 'text') == self.value_normal:
                # 更新为第二默认值
                self.master.itemconfigure(self.text, text=self.value_touch)

    def touch_off(self) -> None:
        """ 鼠标离开状态 """
        if self._state != 'press':
            self.state('normal')

            # 判断显示的值是否为第二默认值
            if self.master.itemcget(self.text, 'text') == self.value_touch:
                # 更新为第一默认值
                self.master.itemconfigure(self.text, text=self.value_normal)

    def press(self, event: tkinter.Event) -> None:
        """ 交互状态检测 """
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            if self._state != 'press':
                self.press_on()
        else:
            self.press_off()

    def touch(
        self,  # type: CanvasEntry | CanvasText
        event: tkinter.Event
    ) -> bool:
        """ 触碰状态检测 """
        condition = self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2
        self.touch_on() if condition else self.touch_off()
        return condition

    def cursor_flash(self) -> None:
        """ 鼠标光标闪烁 """
        if self._cursor_time >= 300:
            self._cursor_time, self._cursor = 0, not self._cursor
            if self._cursor:
                self.master.itemconfigure(self.cursor, text=self.icursor)
            else:
                self.master.itemconfigure(self.cursor, text=NULL)

        if self._state == 'press':
            self._cursor_time += 10
            self.master.after(10, self.cursor_flash)
        else:
            self._cursor_time, self._cursor = 300, False  # 恢复默认值
            self.master.itemconfigure(self.cursor, text=NULL)

    def cursor_update(self, text: str = ' ') -> None:
        """ 鼠标光标更新 """
        self._cursor_time, self._cursor = 300, False  # 恢复默认值
        if isinstance(self, CanvasEntry):
            self.master.coords(self.cursor, self.master.bbox(
                self.text)[2], self.y1+self.height * self.master.rate_y / 2)
        elif isinstance(self, CanvasText):
            _pos = self.master.bbox(self._text)
            self.master.coords(self.cursor, _pos[2], _pos[1])
        self.master.itemconfigure(
            self.cursor, text=NULL if not text else self.icursor)

    def paste(self) -> bool:
        """ 快捷键粘贴 """
        condition = self._state == 'press' and not getattr(self, 'show', None)
        if condition:
            self.append(self.master.clipboard_get())
        return condition

    def get(self) -> str:
        """ 获取输入框的值 """
        return self.value

    def set(self, value: str) -> None:
        """ 设置输入框的值 """
        self.value = self.value_surface = ''
        self.append(value)

    def append(self, value: str) -> None:
        """ 添加输入框的值 """
        temp, self._state = self._state, 'press'
        (event := tkinter.Event()).keysym = None
        for char in value:
            event.char = char
            self.input(event)
        self._state = temp
        self.cursor_flash()


class CanvasEntry(_TextWidget):
    """
    ### 虚拟画布输入框控件
    创建一个虚拟的输入框控件，可输入单行少量字符，并获取这些字符
    """

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        radius: int = RADIUS,
        text: tuple[str] | str = NULL,
        show: str | None = None,
        limit: int = LIMIT,
        space: bool = False,
        cursor: str = CURSOR,
        borderwidth: int = BORDERWIDTH,
        justify: str = tkinter.LEFT,
        font: tuple[str, int, str] = FONT,
        color_text: tuple[str, str, str] = COLOR_TEXT,
        color_fill: tuple[str, str, str] = COLOR_FILL_TEXT,
        color_outline: tuple[str, str, str] = COLOR_OUTLINE_TEXT
    ) -> None:
        _TextWidget.__init__(self, canvas, x, y, width, height, radius, text, limit, space, justify,
                             cursor, borderwidth, font, color_text, color_fill, color_outline)
        self.master.itemconfigure(self.text, text=self.value_normal)
        self.show = show

    def press_on(self) -> None:
        """ 控件获得焦点 """
        self.state('press')
        self.master.itemconfigure(self.text, text=self.value_surface)
        self.cursor_update(NULL)
        self.cursor_flash()

    def press_off(self) -> None:
        """ 控件失去焦点 """
        self.state('normal')

        if self.value == NULL:
            self.master.itemconfigure(self.text, text=self.value_normal)
        else:
            self.master.itemconfigure(self.text, text=self.value_surface)

    def input(self, event: tkinter.Event) -> None:
        """ 文本输入 """
        if self._state == 'press':
            if event.keysym == 'BackSpace':
                # 按下退格键
                self.value = self.value[:-1]
            elif len(self.value) == self.limit:
                # 达到字数限制
                return True
            elif len(event.char):
                if not event.char.isprintable() or (event.char == ' ' and not self.space):
                    return True
                else:
                    # 按下普通按键
                    self.value += event.char
            else:
                return True

            # 更新表面显示值
            self.value_surface = len(
                self.value) * self.show if self.show else self.value

            # 更新显示
            self.master.itemconfigure(self.text, text=self.value_surface)
            self.update_text()
            self.cursor_update()
            return True

    def update_text(self):
        """ 更新控件 """
        while True:
            pos = self.master.bbox(self.text)
            if pos[2] > self.x2-self.radius-2 or pos[0] < self.x1+self.radius+1:
                self.value_surface = self.value_surface[1:]
                self.master.itemconfigure(self.text, text=self.value_surface)
            else:
                break

        # BUG: 当窗口扩大再缩小时，可能出现过短情况


class CanvasText(_TextWidget):
    """
    ### 虚拟画布文本框类
    创建一个透明的虚拟文本框，
    用于输入多行文本和显示多行文本（只读模式）
    """

    def __init__(
        self,
        canvas: Canvas,
        x: int,
        y: int,
        width: int,
        height: int,
        radius: int = RADIUS,
        text: tuple[str] | str = NULL,
        limit: int = LIMIT,
        space: bool = True,
        read: bool = False,
        cursor: bool = CURSOR,
        borderwidth: int = BORDERWIDTH,
        justify: str = tkinter.LEFT,
        font: tuple[str, int, str] = FONT,
        color_text: tuple[str, str, str] = COLOR_TEXT,
        color_fill: tuple[str, str, str] = COLOR_FILL_TEXT,
        color_outline: tuple[str, str, str] = COLOR_OUTLINE_TEXT
    ) -> None:
        _TextWidget.__init__(self, canvas, x, y, width, height, radius, text, limit, space, justify,
                             cursor, borderwidth, font, color_text, color_fill, color_outline)

        _x = x + (width-radius-3 if justify == 'right' else width /
                  2 if justify == 'center' else radius+2)
        _anchor = 'n' if justify == 'center' else 'ne' if justify == 'right' else 'nw'

        # 位置确定文本(位置不要乱动)
        self._text = canvas.create_text(_x, y+radius+2,
                                        justify=justify,
                                        anchor=_anchor,
                                        font=font,
                                        fill=color_text[0])

        # TODO: 待写
        # # 滚动条
        # if radius:
        #     self.scrollbar = CanvasButton(
        #         canvas, x+width-7, y+radius, 5, height-2*radius, 2.5, NULL)
        # else:
        #     self.scrollbar = CanvasButton(
        #         canvas, x+width-7, y+2, 5, height-4, 0, NULL)

        # 只读模式
        self.read = read
        # # 修改多行文本靠左显示
        self.master.coords(self.text, _x, y+radius+2)
        self.master.itemconfigure(
            self.text, text=self.value_normal, anchor=_anchor)
        self.master.itemconfigure(self.cursor, anchor='n')

        # 行位置数
        self.position = [0, 0]

    def press_on(self) -> None:
        """ 控件获得焦点 """
        if not self.read:
            self.state('press')
            *__, _ = [''] + self.value_surface.rsplit('\n', 1)
            self.master.itemconfigure(self.text, text=''.join(__))
            self.master.itemconfigure(self._text, text=_)
            self.cursor_update(NULL)
            self.cursor_flash()

    def press_off(self) -> None:
        """ 控件失去焦点 """
        self.state('normal')

        if self.value == NULL:
            self.master.itemconfigure(self.text, text=self.value_normal)
        else:
            *__, _ = [''] + self.value_surface.rsplit('\n', 1)
            self.master.itemconfigure(self.text, text=''.join(__))
            self.master.itemconfigure(self._text, text=_)

    def input(self, event: tkinter.Event) -> bool:
        """ 文本输入 """
        if self._state == 'press':
            if event.keysym == 'BackSpace':
                # 按下退格键
                self.input_backspace()
            elif len(self.value) == self.limit:
                # 达到字数限制
                return True
            elif event.keysym == 'Tab':
                # 按下Tab键
                self.append(' '*4)
            elif event.keysym == 'Return' or event.char == '\n':
                # 按下回车键
                self.input_return()
            elif event.char.isprintable() and event.char:
                # 按下其他普通的键
                _text = self.master.itemcget(self._text, 'text')
                self.master.itemconfigure(self._text, text=_text+event.char)
                _pos = self.master.bbox(self._text)

                if _pos[2] > self.x2-self.radius-2 or _pos[0] < self.x1+self.radius+1:
                    # 文本溢出啦
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
            self.value_surface = text+'\n'+_text

            return True

    def input_return(self) -> None:
        """ 回车键功能 """
        self.value += '\n'

        # 相关数据获取
        text = self.master.itemcget(self.text, 'text')
        _text = self.master.itemcget(self._text, 'text')
        _pos = self.master.bbox(self._text)

        self.master.itemconfigure(self._text, text='')

        if _pos[3]+_pos[3]-_pos[1] < self.y2-self.radius-2:
            # 还没填满文本框
            self.master.move(self._text, 0, _pos[3] - _pos[1])
            self.master.itemconfigure(
                self.text, text=text+bool(text)*'\n'+_text)
        else:
            # 文本框已经被填满了
            text = text.split('\n', 1)[-1]
            self.master.itemconfigure(self.text, text=text+'\n'+_text)

            self.position[0] += 1
            self.position[1] += 1

    def input_backspace(self) -> None:
        """ 退格键功能 """
        if not self.value:
            # 没有内容，删个毛啊
            return

        _text = self.master.itemcget(self._text, 'text')
        self.value = self.value[:-1]

        if _text:
            # 正常地删除字符
            self.master.itemconfigure(self._text, text=_text[:-1])
        else:
            # 遇到换行符
            _ = self.value.rsplit('\n', 1)[-1]
            self.master.itemconfigure(self._text, text=_)

            if self.value == self.master.itemcget(self.text, 'text'):
                # 内容未超出框的大小
                _pos = self.master.bbox(self._text)
                self.master.move(self._text, 0, _pos[1] - _pos[3])
                __ = self.value.removesuffix(_)[:-('\n' in self.value)]
            else:
                # 内容已经超出框框的大小啦
                text = self.master.itemcget(self.text, 'text')
                __ = self.value.removesuffix(
                    text)[:-1].rsplit('\n', 1)[-1]+'\n'+text.removesuffix(_)[:-1]

                self.position[0] -= 1
                self.position[1] -= 1

            self.master.itemconfigure(self.text, text=__)

    def scroll(self, event: tkinter.Event) -> None:
        """ 文本滚动 """
        # TODO: 待写
        # if self.value != self.value_surface:
        #     if event.delta > 0:
        #         # 滚轮向上滑动，文本下移
        #         text = self.master.itemcget(self.text, 'text')
        #         _ = text.rsplit('\n', 1)[-1]
        #         self.master.itemconfigure(self._text, text=_)
        #     else:
        #         pass

        #     # 更新表面显示值
        #     text = self.master.itemcget(self.text, 'text')
        #     _text = self.master.itemcget(self._text, 'text')
        #     self.value_surface = text+'\n'+_text

        #     return True


class PhotoImage(tkinter.PhotoImage):
    """
    ### 图片类
    生成图片并进行相应的一些处理（支持png和gif格式）
    """

    def __init__(
        self,
        file: str | bytes,
        **kw
    ) -> None:
        """
        ### 参数说明
        `file`: 图片文件的路径
        `**kw`: 其他参数
        """
        self.file = file

        if file.split('.')[-1] == 'gif':
            self.frames: list[tkinter.PhotoImage] = []
        else:
            tkinter.PhotoImage.__init__(self, file=file, **kw)

    def parse(self) -> Generator[int, None, None]:
        """
        解析动图，返回一个生成器
        """
        ind = 0

        try:
            while True:
                self.frames.append(tkinter.PhotoImage(
                    file=self.file, format='gif -index %d' % ind))
                ind += 1
                yield ind
        except:
            pass

    def play(
        self,
        canvas: Canvas,
        id,  # type: tkinter._CanvasItemId
        interval: int,
        _ind: int = 0
    ) -> None:
        """
        播放动图，canvas.lock为False会暂停
        `canvas`: 播放动画的画布
        `id`: 播放动画的 _CanvasItemId（就是 create_text 的返回值）
        `interval`: 每帧动画的间隔时间
        """
        if _ind == len(self.frames):
            _ind = 0
        canvas.itemconfigure(id, image=self.frames[_ind])
        args = canvas, id, interval, _ind+canvas.lock
        canvas.after(interval, self.play, *args)

    def zoom(self, rate_x: float, rate_y: float, precision: float = 1) -> tkinter.PhotoImage:
        """
        缩放图片
        `rate_x`: 横向缩放倍率
        `rate_y`: 纵向缩放倍率
        `precision`: 精度到小数点后的位数，越大运算就越慢
        """

        key = round(10**precision)  # NOTE: 需要算法以提高精度和速度（浮点数->小的近似分数）

        image = tkinter.PhotoImage.zoom(self, key, key)
        image = image.subsample(round(key / rate_x), round(key / rate_y))

        return image


class Singleton(object):
    """ 单例模式类 """

    _instance = None

    def __new__(cls: type[Self]) -> Self:
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance


def move_widget(
    master: Tk | Canvas | tkinter.Misc | tkinter.BaseWidget,
    widget: Canvas | _BaseWidget | tkinter.BaseWidget,
    dx: int,
    dy: int,
    times: float,
    mode,  # type: Literal['smooth','rebound','flat'] | tuple
    _x: int = 0,
    _y: int = 0,
    _ind: int = 0
) -> None:
    """
    ### 控件移动函数
    以特定方式移动由 Place 布局的某个控件或某些控件的集合或图像
    #### 参数说明
    `master`: 控件所在的父控件
    `widget`: 要移动位置的控件
    `dx`: 横向移动的距离（单位：像素）
    `dy`: 纵向移动的距离
    `times`: 移动总时长（单位：秒）
    `mode`: 移动速度模式，为以下三种，
    或者为 (函数, 起始值, 终止值) 的形式，
    或者为一个长度等于20的，总和为100的元组
    1. `smooth`: 速度先慢后快再慢 (Sin, 0, π)
    2. `rebound`: 和 smooth 一样，但是最后会回弹一下 (Cos, 0, 0.6π)
    3. `flat`: 匀速平移
    """

    # 速度变化模式
    if type(mode) == tuple and len(mode) >= 20:
        # 记忆值
        v = mode
    elif mode == 'smooth':
        # 流畅模式
        v = 0, 1, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 7, 6, 5, 4, 3, 1, 0
    elif mode == 'rebound':
        # 抖动模式
        v = 11, 11, 10, 10, 10, 9, 9, 8, 7, 6, 6, 5, 4, 3, 1, 0, -1, -2, -3, -4
    elif mode == 'flat':
        # 平滑模式
        v = (5,) * 20
    else:
        # 函数模式
        f, start, end = mode
        end = (end-start) / 19
        v = tuple(f(start+end*_) for _ in range(20))
        key = 100 / sum(v)
        v = tuple(key*_ for _ in v)

    # 总计实际应该移动的百分比
    proportion = sum(v[:_ind+1]) / 100

    # 计算本次移动量
    x = round(proportion * dx - _x)
    y = round(proportion * dy - _y)

    if isinstance(master, tkinter.Misc) and isinstance(widget, tkinter.BaseWidget):
        # 父控件：tkinter控件
        # 子控件：tkinter控件
        origin_x = int(widget.place_info()['x'])
        origin_y = int(widget.place_info()['y'])
        widget.place(x=origin_x+x, y=origin_y+y)
    elif isinstance(master, Canvas) and isinstance(widget, _BaseWidget):
        # 父控件：Canvas
        # 子控件：_BaseWidget
        widget.move(x, y)
    else:
        # 父控件：Canvas | tkinter.Canvas
        # 子控件：tkinter._CanvasItemId
        master.move(widget, x, y)

    if _ind != 19:
        # 迭代函数
        args = master, widget, dx, dy, times, v, _x+x, _y+y, _ind+1
        widget.master.after(round(times*50), move_widget, *args)


def correct_text(
    length: int,
    string: str,
    position: Literal['left', 'center', 'right'] = 'center'
) -> str:
    """
    ### 文本控制函数
    可将目标字符串改为目标长度并居中对齐，ASCII码字符算1个长度，中文及其他字符算2个
    #### 参数说明
    `length`: 目标长度
    `string`: 要修改的字符串
    `position`: 文本处于该长度范围的位置，可选三个值
    1. `left`: 文本靠左
    2. `center`: 文本居中
    3. `right`: 文本靠右
    """

    # 计算空格总个数
    length -= sum([1 + (ord(i) > 256) for i in string])
    if position == 'left':
        # 靠左
        return ' '*length+string
    elif position == 'right':
        # 靠右
        return string+length*' '
    else:
        # 居中
        length, key = divmod(length, 2)
        return ' '*length+string+(length+key)*' '


def change_color(
    color:  tuple[str, str] | list[str] | str,
    proportion: float = 1
) -> str:
    """
    ### 颜色处理函数
    按一定比例给出已有RGB颜色字符串的渐变RGB颜色字符串，或颜色的对比色
    #### 参数说明
    `color`: 颜色元组或列表 (初始颜色, 目标颜色)，或者一个颜色字符串
    `proportion`: 渐变比例（浮点数，范围为0~1）
    """

    if type(color) == str:
        color = color, None

    # 判断颜色字符串格式（#FFF或者#FFFFFF格式）
    key = 256 if len(color[0]) == 7 else 16

    # 解析初始颜色的RGB
    _ = int(color[0][1:], 16)
    _, B = divmod(_, key)
    R, G = divmod(_, key)

    # 解析目标颜色的RGB
    if color[1]:
        _ = int(color[1][1:], 16)
        _, _B = divmod(_, key)
        _R, _G = divmod(_, key)
    else:
        _R, _G, _B = 255 - R, 255 - G, 255 - B

    # 根据比率计算返回值
    RGB = R + round((_R - R) * proportion)
    RGB *= key
    RGB += G + round((_G - G) * proportion)
    RGB *= key
    RGB += B + round((_B - B) * proportion)

    # 以对应格式返回结果
    return '#%0*X' % (6 if key == 256 else 3, RGB)


def test() -> None:
    """ 测试函数 """
    from tkinter.messagebox import askyesno
    from random import randint

    def shutdown():
        """ 关闭窗口 """
        if askyesno('提示', '是否退出测试程序?'):
            root.destroy()

    def change_bg(ind=0, color=[None, '#F1F1F1']):
        """ 颜色变幻 """
        if not ind:
            color[0], color[1] = color[1], '#%06X' % randint(0, 1 << 24)
        color = change_color(color, ind)
        _color = change_color(color)
        canvas_doc.configure(bg=color)
        canvas_doc.itemconfigure(doc, fill=_color)
        for widget in canvas_main.widget_list:
            widget.color_fill[0], widget.color_text[0] = color, _color
            widget.state()
        root.after(20, change_bg, 0 if ind >= 1 else ind+0.01)

    def draw(ind=0):
        """ 绘制球体 """
        canvas_graph.create_oval(
            (300-ind/3)*canvas_graph.rate_x, (100-ind/3)*canvas_graph.rate_y,
            (400+ind)*canvas_graph.rate_x, (200+ind)*canvas_graph.rate_y,
            outline=change_color(('#FFFFFF', '#000000'), ind/100),
            width=2.5, fill=NULL if ind else '#FFF')
        if ind < 100:
            root.after(30, draw, ind+1)

    root = Tk('Test', '960x540', alpha=0.9, shutdown=shutdown)
    (canvas_main := Canvas(root, 960, 540)).place(x=0, y=0)
    (canvas_doc := Canvas(root, 960, 540)).place(x=-960, y=0)
    (canvas_graph := Canvas(root, 960, 540)).place(x=960, y=0)

    CanvasButton(
        canvas_main, 10, 500, 120, 30, 0, '模块文档',
        command=lambda: (move_widget(root, canvas_main, 960*canvas_main.rate_x, 0, 0.3, 'rebound'),
                         move_widget(root, canvas_doc, 960*canvas_doc.rate_x, 0, 0.3, 'rebound')))
    CanvasButton(
        canvas_main, 830, 500, 120, 30, 0, '图像测试',
        command=lambda: (move_widget(root, canvas_main, -960*canvas_main.rate_x, 0, 0.3, 'rebound'),
                         move_widget(root, canvas_graph, -960*canvas_graph.rate_x, 0, 0.3, 'rebound')))
    CanvasButton(
        canvas_doc, 830, 500, 120, 30, 0, '返回主页',
        command=lambda: (move_widget(root, canvas_main, -960*canvas_main.rate_x, 0, 0.3, 'rebound'),
                         move_widget(root, canvas_doc, -960*canvas_doc.rate_x, 0, 0.3, 'rebound')))
    CanvasButton(
        canvas_graph, 10, 500, 120, 30, 0, '返回主页',
        command=lambda: (move_widget(root, canvas_main, 960*canvas_main.rate_x, 0, 0.3, 'rebound'),
                         move_widget(root, canvas_graph, 960*canvas_graph.rate_x, 0, 0.3, 'rebound')))

    try:
        image = PhotoImage('tkinter.png')
        canvas_graph.create_image(830, 130, image=image)
    except:
        print('\033[31m啊哦！你没有示例图片喏……\033[0m')

    CanvasText(canvas_main, 10, 10, 465, 200, 10,
               ('居中圆角文本框', '竖线光标'), justify='center')
    CanvasText(canvas_main, 485, 10, 465, 200, 0,
               ('靠右方角文本框', '下划线光标'), cursor=' _')
    CanvasEntry(canvas_main, 10, 220, 200, 25, 5,
                ('居中圆角输入框', '点击输入'), justify='center')
    CanvasEntry(canvas_main, 750, 220, 200, 25, 0,
                ('靠右方角输入框', '点击输入'), '•')
    CanvasButton(
        canvas_main, 10, 250, 120, 25, 5, '圆角按钮',
        command=lambda: move_widget(canvas_main, label_1, 0, -120 * canvas_main.rate_y, 0.25, 'rebound'))
    CanvasButton(
        canvas_main, 830, 250, 120, 25, 0, '方角按钮',
        command=lambda: move_widget(canvas_main, label_2, 0, -120 * canvas_main.rate_y, 0.25, 'smooth'))

    doc = canvas_doc.create_text(360, 270, text=__doc__, font=('楷体', 12))

    label_1 = CanvasLabel(canvas_main, 225, 550, 250,
                          100, 10, '圆角标签\n移动模式:rebound')
    label_2 = CanvasLabel(canvas_main, 485, 550, 250,
                          100, 0, '方角标签\n移动模式:smooth')
    button_1 = CanvasButton(canvas_doc, 830, 10, 120, 30, 0, '颜色变幻',
                            command=lambda: (button_1.set_live(False), change_bg()))
    button_2 = CanvasButton(canvas_graph, 10, 10, 120, 30, 0, '绘制图形',
                            command=lambda: (button_2.set_live(False), draw()))

    root.mainloop()


if __name__ == '__main__':
    test()
