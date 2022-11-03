"""## tkintertools
【运行最低要求: Python3.10.x】

这个模块是tkinter模块的扩展模块，将给用户提供以下功能：

1. 可透明的、可自定义的、美观的控件
2. 让控件大小、图像大小、图形大小均随窗口动态变化的功能
3. 缩放png图片的功能、播放gif图片的功能
4. 对控件基本的移动位置操作，形成简单的动画
5. 对颜色的一些处理，便捷地产生渐变色
6. 对文本的基础处理，控制长度及位置
7. 用Place实现复杂的布局，控件位置精准控制
8. 实现圆角化控件
9. ...

还有更多功能及用法，见模块使用教程（链接在下面）
### 模块基本信息
* 模块作者: 小康2022
* 模块版本: 2.4
* 上次更新: 2022/11/3
### 模块精华速览
* 容器类控件: `Tk`、`Toplevel`、`Canvas`
* 工具类: `PhotoImage`
* 虚拟画布类控件: `CanvasLabel`、`CanvasButton`、`CanvasEntry`、`CanvasText`
* 处理函数: `move_widget`、`correct_text`、`gradient_color`
### 更多详细内容
* 模块源码地址: https://gitcode.net/weixin_62651706/tkintertools
* 模块使用教程: http://t.csdn.cn/gFg9A
* 模块相关专栏: https://blog.csdn.net/weixin_62651706/category_11600888.html
"""

import tkinter
from sys import version_info
from typing import Generator, Literal

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
    'gradient_color',
)

__author__ = '小康2022'

__version__ = '2.4'

if version_info < (3, 10):
    print('\033[31m你的Python无法正常使用tkintertools模块！\033[0m')
    print('\a模块运行最低要求\033[32mPython3.10\033[0m')
    exit()


# 默认的文本前景颜色
COLOR_BLACK = '#000000', '#000000', '#000000'
# 默认文本背景颜色
COLOR_WHITE = '#FFFFFF', '#FFFFFF', '#FFFFFF'
# 默认的内部颜色
COLOR_FILL = '#E1E1E1', '#E5F1FB', '#CCE4F7'
# 默认按钮外框颜色
COLOR_BUTTON = '#C0C0C0', '#4A9EE0', '#4884B4'
# 默认文本外框颜色
COLOR_TEXT = '#C0C0C0', '#5C5C5C', '#4A9EE0'
# 透明颜色
COLOR_NONE = '', '', ''

# 默认控件外框宽度
BORDERWIDTH = 1
# 默认控件圆角半径
RADIUS = 0
# 默认控件显示文本
TEXT = ''
# 默认字体
FONT = '楷体', 15


# 容器控件


class Tk(tkinter.Tk):
    """
    Tk类

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
        *args, **kw
    ) -> None:
        """
        ### 参数说明
        `title`: 窗口标题
        `geometry`: 窗口大小及位置（格式：'宽度x高度+左上角横坐标+左上角纵坐标' 或者 '宽度x高度'）
        `minisize`: 窗口的最小缩放大小（默认为参数 geometry 的宽度与高度）
        `alpha`: 窗口透明度，范围为0~1，0为完全透明
        `proportion_lock`: 窗口缩放是否保持原比例
        `shutdown`: 关闭窗口之前执行的函数（会覆盖关闭操作）
        `*args`, `**kw`: 与原 tkinter 模块中的 Tk 类的参数相同
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

        tkinter.Tk.__init__(self, *args, **kw)

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
                delta = event.width / self._proportion - event.height
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
                    # 绝对缩放仅对当前Canvas生效
                    if canvas.lock:
                        self.zoom_absolute(canvas)

            # 更新默认参数
            self._width = event.width
            self._height = event.height

    @staticmethod
    def zoom_relative(canvas,  # type: Canvas
                      rate_x: float,
                      rate_y: float):
        """ 内部方法：相对缩放 """
        # 更新子画布控件的子虚拟画布控件位置数据
        for widget in canvas.widget_list:
            widget.x1 *= rate_x
            widget.x2 *= rate_x
            widget.y1 *= rate_y
            widget.y2 *= rate_y

        # 更新子画布控件的子虚拟画布控件的位置
        for item in canvas.item_dict.keys():
            coords = [c * rate_y if i % 2 else c * rate_x for i,
                      c in enumerate(canvas.coords(item))]
            canvas.coords(item, coords)

    @staticmethod
    def zoom_absolute(canvas  # type: Canvas
                      ):
        """ 内部方法：绝对缩放 """
        for item, key in canvas.item_dict.items():
            if key[0] == 'font':  # NOTE: 字体缩小时有 BUG
                # 字体大小修改
                font: str = canvas.itemcget(item, 'font')
                font = font.split()
                if font:  # NOTE: 不加if判断会有 BUG
                    font[1] = int(key[1] * min(canvas.rate_x, canvas.rate_y))
                    canvas.itemconfigure(item, font=font)
            elif key[0] == 'width':
                # 宽度大小修改
                rate = min(canvas.rate_x, canvas.rate_y)
                canvas.itemconfigure(item, width=float(key[1])*rate)
            elif key[0] == 'image':
                # 图像大小缩放
                if key[1] and key[1].file.split('.')[-1] == 'png':
                    key[2] = key[1].zoom(canvas.rate_x, canvas.rate_y)
                    canvas.itemconfigure(item, image=key[2])

    @staticmethod
    def __touch(event: tkinter.Event,
                canvas  # type: Canvas
                ) -> None:
        """ 绑定鼠标触碰控件事件 """
        if canvas.lock:
            for widget in canvas.widget_list:
                widget: CanvasLabel
                widget.touch(event)

    @staticmethod
    def __press(event: tkinter.Event,
                canvas  # type: Canvas
                ) -> None:
        """ 绑定鼠标左键按下事件 """
        if canvas.lock:
            for widget in canvas.widget_list:
                if isinstance(widget, CanvasButton | CanvasEntry | CanvasText):
                    widget.press(event)

    @staticmethod
    def __release(event: tkinter.Event,
                  canvas  # type: Canvas
                  ) -> None:
        """ 绑定鼠标左键松开事件 """
        if canvas.lock:
            for widget in canvas.widget_list:
                if isinstance(widget, CanvasButton):
                    widget.execute(event)
                    widget.touch(event)

    @staticmethod
    def __mousewheel(event: tkinter.Event,
                     canvas  # type: Canvas
                     ) -> None:
        """ 绑定鼠标滚轮滚动事件 """
        if canvas.lock:
            for widget in canvas.widget_list:
                if isinstance(widget, CanvasText):
                    widget.scroll(event)

    def __input(self, event: tkinter.Event) -> None:
        """ 绑定键盘输入字符事件 """
        for canvas in self.canvas_list:
            if canvas.lock:
                for widget in canvas.widget_list:
                    if isinstance(widget, CanvasEntry | CanvasText):
                        widget.input(event)
                break

    def bind_event(self) -> None:
        """ 内部方法：关联事件的绑定 """
        # 绑定键盘输入字符
        self.bind('<Any-Key>', self.__input)

        for canvas in self.canvas_list:
            # 绑定鼠标触碰控件
            canvas.bind('<Motion>', lambda event,
                        _canvas=canvas: self.__touch(event, _canvas))
            # 绑定鼠标左键按下
            canvas.bind('<Button-1>', lambda event,
                        _canvas=canvas: self.__press(event, _canvas))
            # 绑定鼠标左键松开
            canvas.bind('<ButtonRelease-1>', lambda event,
                        _canvas=canvas: self.__release(event, _canvas))
            # 绑定鼠标左键按下移动
            canvas.bind('<B1-Motion>', lambda event,
                        _canvas=canvas: self.__press(event, _canvas))
            # 绑定鼠标滚轮滚动
            canvas.bind('<MouseWheel>', lambda event,
                        _canvas=canvas: self.__mousewheel(event, _canvas))

    def geometry(self, newGeometry: str | None = None):
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


class Toplevel(tkinter.Toplevel, Tk):
    """
    Toplevel 类

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
        *args, **kw
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
        `*args`, `**kw`: 与原 tkinter 模块中的 Toplevel 类的参数相同
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

        # 子画布列表（与缩放绑定有关）
        self.canvas_list: list[Canvas] = []

        tkinter.Toplevel.__init__(self, master=master, *args, **kw)

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
    画布类

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
        # 子item列表（与大小缩放有关）
        self.item_dict = {}  # type: dict[tkinter._CanvasItemId, tuple | list]

        tkinter.Canvas.__init__(
            self,
            master,
            width=width,
            height=height,
            highlightthickness=0,
            **kw)

        # 将实例添加到 Tk 的画布列表中
        master.canvas_list.append(self)

    def setlock(self, boolean: bool):
        """ 设置画布锁 """
        self.lock = boolean
        self.master: Tk
        if self.lock and self.expand:
            self.master.zoom_absolute(self)

    def create_text(self, *args, **kw):
        # 重写：添加对 text 类型的 _CanvasItemId 的字体大小的控制
        item = tkinter.Canvas.create_text(self, *args, **kw)
        self.item_dict[item] = 'font', kw.get('font')[1]
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


# 控件基类


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
        `text`: 控件显示的文本
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
        `limit`: 文本控件的输入字数限制
        `space`: 文本控件能否输入空格的标识
        `read`: 文本控件的只读模式
        ---
        ### 详细说明
        字体的值为一个三元组 
        例如: `('微软雅黑', 15, 'bold') `

        颜色为一个包含三个 RGB 颜色字符串的元组 
        详细: `(正常颜色, 触碰颜色, 交互颜色)`
        """

        self.master = canvas
        self.value = text
        self.font = font
        self.color_text = color_text
        self.color_fill = color_fill
        self.color_outline = color_outline

        # 控件左上角坐标
        self.x1, self.y1 = x, y
        # 控件左下角坐标
        self.x2, self.y2 = x + width, y + height
        # 边角圆弧半径
        self.radius = radius
        # 控件活跃标志
        self.live = True

        # 将实例添加到父画布控件
        canvas.widget_list.append(self)

        if radius:
            if 2 * radius > height:
                radius = height // 2
                self.radius = radius

            d = 2*radius  # 圆角直径
            _x, _y, _w, _h = x+radius, y+radius, width-d, height-d

            # 虚拟控件内部填充颜色
            kw = {'outline': '', 'fill': color_fill[0]}
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
                x, y, x + width, y + height,
                width=borderwidth,
                outline=color_outline[0],
                fill=color_fill[0])

        # 虚拟控件显示的文字
        self.text = canvas.create_text(
            x + width / 2, y + height / 2,
            text=text,
            font=font,
            justify=justify,
            fill=color_text[0])

    def state(self, mode: Literal['normal', 'touch', 'press']) -> None:
        """
        改变虚拟控件的状态
        `normal`: 正常状态
        `touch`: 鼠标触碰时的状态
        `press`: 鼠标按下时的状态
        """
        mode = 0 if mode == 'normal' else 1 if mode == 'touch' else 2
        self.master.itemconfigure(self.text, fill=self.color_text[mode])

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
            for item in self.inside + self.outside:
                self.master.move(item, dx, dy)
        else:
            self.master.move(self.rect, dx, dy)
        self.master.move(self.text, dx, dy)

        if hasattr(self, 'cursor'):
            self.cursor: tkinter._CanvasItemId
            self.master.move(self.cursor, dx, dy)

    def configure(self, **kw) -> None:
        """
        改变原有参数的值

        可供修改的参数有 `text`、`color_text`、`color_fill` 及 `color_outline`
        """
        if value := kw.get('text', self.value):
            self.value = value
        if text := kw.get('color_text', self.color_text):
            self.color_text = text
        if fill := kw.get('color_fill', self.color_fill):
            self.color_fill = fill
        if outline := kw.get('color_outline', self.color_outline):
            self.color_outline = outline

        self.master.itemconfigure(self.text, text=value, fill=text[0])

        if self.radius:
            for item in self.inside:
                self.master.itemconfigure(item, fill=fill[0])
            for item in self.outside[:4]:
                self.master.itemconfigure(item, fill=outline[0])
            for item in self.outside[4:]:
                self.master.itemconfigure(item, outline=outline[0])
        else:
            self.master.itemconfigure(
                self.rect, fill=fill[0], outline=outline[0])

        if hasattr(self, 'cursor'):
            self.master.itemconfigure(self.cursor, fill=text[2])

    def destroy(self) -> None:
        """ 摧毁控件释放内存 """
        self.live = False
        if self.radius:
            for item in self.inside + self.outside:
                self.master.delete(item)
        else:
            self.master.delete(self.rect)
        self.master.delete(self.text)

        try:
            self.master.widget_list.remove(self)  # NOTE: 如果删掉try会有奇怪的 BUG
        except:
            pass


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
        borderwidth: int,
        font: tuple[str, int, str],
        color_text: tuple[str, str, str],
        color_fill: tuple[str, str, str],
        color_outline: tuple[str, str, str]
    ) -> None:

        self.limit = limit
        self.space = space

        # 表面显示值
        self.value_surface = ''
        # 光标闪烁间隔
        self.cursor_time = 300
        # 光标闪烁标志
        self._cursor = False
        # 鼠标左键按下标志
        self._press = False

        if type(text) == tuple:
            self.value_normal, self.value_touch = text
        else:
            self.value_normal = text

        _BaseWidget.__init__(self, canvas, x, y, width, height, radius, '', justify,
                             borderwidth, font, color_text, color_fill, color_outline)

        # 鼠标光标（位置顺序不可乱动）
        self.cursor = canvas.create_text(x+width/2, y+height/2,
                                         font=font, fill=color_text[2])

    def press_on(self) -> None:
        """ 控件获得焦点 """
        if not getattr(self, 'read', None):
            self._press = True
            self.state('press')
            self.master.itemconfigure(self.text, text=self.value_surface)
            self.cursor_flash()

    def press_off(self) -> None:
        """ 控件失去焦点 """
        if not getattr(self, 'read', None):
            self._press = False
            self.state('normal')
            self.master.itemconfigure(self.text, text=self.value_surface)

    def press(self, event: tkinter.Event) -> None:
        """ 交互状态检测 """
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            if not self._press:
                self.press_on()
        else:
            self.press_off()

    def touch(self,  # type: CanvasEntry | CanvasText
              event: tkinter.Event) -> None:
        """ 触碰状态检测 """
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            self.touch_on()
        else:
            self.touch_off()

    def cursor_flash(self) -> None:
        """ 鼠标光标闪烁 """
        if self.cursor_time >= 300:
            self.cursor_time, self._cursor = 0, not self._cursor
            if self._cursor:
                if self.master.itemcget(self.text, 'justify') == tkinter.CENTER:
                    # 居中的文本
                    self.master.itemconfigure(
                        self.cursor, text=self.__text(self.value_surface) + '│')
                elif self.master.itemcget(self.text, 'justify') == tkinter.LEFT:
                    # 靠左的文本
                    self.master.itemconfigure(
                        self.cursor, text=self.__text(self.value_surface) + '│')
            else:
                self.master.itemconfigure(self.cursor, text='')

        if self._press:
            self.cursor_time += 10
            self.master.after(10, self.cursor_flash)
        else:
            self.cursor_time, self._cursor = 300, False  # 恢复默认值
            self.master.itemconfigure(self.cursor, text='')

    def cursor_update(self) -> None:
        """ 鼠标光标更新 """
        self.cursor_time, self._cursor = 300, False  # 恢复默认值
        if self.master.itemcget(self.text, 'justify') == tkinter.CENTER:
            # 居中的文本
            self.master.itemconfigure(
                self.cursor, text=self.__text(self.value_surface) + '│')
        elif self.master.itemcget(self.text, 'justify') == tkinter.LEFT:
            # 靠左的文本
            self.master.itemconfigure(
                self.cursor, text=self.__text(self.value_surface) + '│')

    @staticmethod
    def __text(string: str) -> str:
        """ 内部函数 """
        out = ''
        for i in string:
            if i == '\n':
                out += i
            elif 0 <= ord(i) <= 256:
                out += ' '
            else:
                out += '  '
        return out


# 虚拟画布控件


class CanvasLabel(_BaseWidget):
    """
    虚拟画布标签控件

    创建一个虚拟的标签控件，用于显示少量文本
    """

    def __init__(self,
                 canvas: Canvas,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 radius: int = RADIUS,
                 text: str = TEXT,
                 borderwidth: int = BORDERWIDTH,
                 justify: str = tkinter.CENTER,
                 font: tuple[str, int, str] = FONT,
                 color_text: tuple[str, str, str] = COLOR_BLACK,
                 color_fill: tuple[str, str, str] = COLOR_FILL,
                 color_outline: tuple[str, str, str] = COLOR_BUTTON) -> None:
        _BaseWidget.__init__(self, canvas, x, y, width, height, radius, text, justify,
                             borderwidth, font, color_text, color_fill, color_outline)

    def touch(self, event: tkinter.Event) -> None:
        """ 触碰状态检测 """
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            self.state('touch')
        else:
            self.state('normal')


class CanvasButton(_BaseWidget):
    """
    虚拟画布按钮控件

    创建一个虚拟的按钮，并执行关联函数
    """

    def __init__(self,
                 canvas: Canvas,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 radius: int = RADIUS,
                 text: str = TEXT,
                 borderwidth: int = BORDERWIDTH,
                 justify: str = tkinter.CENTER,
                 font: tuple[str, int, str] = FONT,
                 command=None,  # type: function | None
                 color_text: tuple[str, str, str] = COLOR_BLACK,
                 color_fill: tuple[str, str, str] = COLOR_FILL,
                 color_outline: tuple[str, str, str] = COLOR_BUTTON) -> None:
        _BaseWidget.__init__(self, canvas, x, y, width, height, radius, text, justify,
                             borderwidth, font, color_text, color_fill, color_outline)
        self.command = command

    def execute(self, event: tkinter.Event) -> None:
        """ 执行关联函数 """
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            if self.live and self.command:
                self.command()

    def press(self, event: tkinter.Event) -> None:
        """ 交互状态检测 """
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            self.state('press')
        else:
            self.state('normal')

    def touch(self, event: tkinter.Event) -> None:
        """ 触碰状态检测 """
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            self.state('touch')
        else:
            self.state('normal')


class CanvasEntry(_TextWidget):
    """
    虚拟画布输入框控件

    创建一个虚拟的输入框控件，可输入单行少量字符，并获取这些字符
    """

    def __init__(self,
                 canvas: Canvas,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 radius: int = RADIUS,
                 text: tuple[str] | str = TEXT,
                 show: str | None = None,
                 limit: int = 15,
                 space: bool = False,
                 borderwidth: int = BORDERWIDTH,
                 justify: str = tkinter.CENTER,
                 font: tuple[str, int, str] = FONT,
                 color_text: tuple[str, str, str] = COLOR_BLACK,
                 color_fill: tuple[str, str, str] = COLOR_WHITE,
                 color_outline: tuple[str, str, str] = COLOR_TEXT) -> None:
        if type(text) == str:
            text = (text, '')
        elif type(text) == None:
            text = ('', '')

        _TextWidget.__init__(self, canvas, x, y, width, height, radius, text, limit, space, justify,
                             borderwidth, font, color_text, color_fill, color_outline)
        self.master.itemconfigure(self.text, text=self.value_normal)
        self.show = show

    def press_off(self) -> None:
        # 重写父类方法
        _TextWidget.press_off(self)
        if self.value == '':
            self.master.itemconfigure(self.text, text=self.value_normal)

    def touch_on(self) -> None:
        """ 鼠标悬停状态 """
        if not self._press:
            self.state('touch')

            # 判断显示的值是否为第一默认值
            if self.master.itemcget(self.text, 'text') == self.value_normal:
                # 更新为第二默认值
                self.master.itemconfigure(self.text, text=self.value_touch)

    def touch_off(self) -> None:
        """ 鼠标离开状态 """
        if not self._press:
            self.state('normal')

            # 判断显示的值是否为第二默认值
            if self.master.itemcget(self.text, 'text') == self.value_touch:
                # 更新为第一默认值
                self.master.itemconfigure(self.text, text=self.value_normal)

    def change_text(self, value: str) -> None:
        """ 重新设定显示文字 """
        # 改变真实值
        self.value = value
        # 改变显示值
        self.value_surface = len(value) * self.show if self.show else value
        # 更新显示值
        self.master.itemconfigure(self.text, text=self.value_surface)

    def input(self, event: tkinter.Event) -> None:
        """ 文本输入 """
        if self._press and self.live:
            if event.keysym == 'BackSpace':
                # 按下退格键
                self.value = self.value[:-1]
            if len(event.char) and len(self.value) < self.limit:
                key = ord(event.char)
                if 32 < key < 127 or key > 255 or (key == 32 and self.space):
                    # 按下普通按键
                    self.value += event.char

            # 更新表面显示值
            self.value_surface = len(
                self.value) * self.show if self.show else self.value
            # 更新显示
            self.master.itemconfigure(self.text, text=self.value_surface)
            self.cursor_update()


class CanvasText(_TextWidget):
    """虚拟画布文本框类

    创建一个透明的虚拟文本框，
    用于输入多行文本和显示多行文本（只读模式）
    """

    def __init__(self,
                 canvas: Canvas,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 radius: int = RADIUS,
                 limit: int = 100,
                 space: bool = True,
                 read: bool = False,
                 borderwidth: int = BORDERWIDTH,
                 justify: str = tkinter.LEFT,
                 font: tuple[str, int, str] = FONT,
                 color_text: tuple[str, str, str] = COLOR_BLACK,
                 color_fill: tuple[str, str, str] = COLOR_WHITE,
                 color_outline: tuple[str, str, str] = COLOR_TEXT) -> None:
        _TextWidget.__init__(self, canvas, x, y, width, height, radius, TEXT, limit, space, justify,
                             borderwidth, font, color_text, color_fill, color_outline)
        # 只读模式
        self.read = read
        # 修改多行文本靠左显示
        self.master.coords(self.text, self.x1 + self.radius + 2,
                           self.y1 + self.radius + 2)
        self.master.coords(self.cursor, self.x1 + self.radius - 9,
                           self.y1 + self.radius + 2)  # NOTE: BUG
        self.master.itemconfigure(self.text, anchor='nw', justify=justify)
        self.master.itemconfigure(self.cursor, anchor='nw', justify=justify)
        # 计算单行文本容纳量
        self.row = round((self.x2 - self.x1 - self.radius) /
                         int(font[1] * 3/4)) + 1
        # 计算文本容纳行数
        self.line = round((self.y2 - self.y1 - self.radius) /
                          int(font[1] * 3/2)) + 1
        # 文本位置
        self._pos = self.line

    def touch_on(self) -> None:
        """ 鼠标悬停状态 """
        if not self._press:
            self.state('touch')

    def touch_off(self) -> None:
        """ 鼠标离开状态 """
        if not self._press:
            self.state('normal')

    def change_text(self, value: str) -> None:
        """ 重新设定显示文字 """
        # 改变文本
        self.value_surface = self.value = value
        # 更新显示值
        self.append('')

    def append(self, value: str) -> None:
        """ 添加文本 """
        # 改变文本
        self.value += value
        key = self.value.count('\n')
        if key <= self.line:
            # 更新显示值
            self.master.itemconfigure(self.text, text=self.value)
        else:
            # 同步更新文本上下位置数据
            self._pos += value.count('\n')
            # 计算显示文本的部分
            ind = key - self.line
            self.value_surface = '\n'.join(
                self.value.split('\n')[ind:ind + self.line])
            self.master.itemconfigure(self.text, text=self.value_surface)

    def scroll(self, event: tkinter.Event) -> None:
        """ 文本滚动 """
        if self.x1 <= event.x <= self.x2 and self.y1 <= event.y <= self.y2:
            if event.delta > 0 and self._pos > self.line:
                # 鼠标向上滚动，显示文本部分向下滚动
                self._pos -= 1
            elif event.delta < 0 and self._pos < self.value.count('\n'):
                # 鼠标向下滚动，显示文本部分向上滚动
                self._pos += 1
            # 计算显示文本的部分
            ind = self._pos - self.line
            self.value_surface = '\n'.join(
                self.value.split('\n')[ind:ind + self.line])
            self.master.itemconfigure(self.text, text=self.value_surface)

    def input(self, event: tkinter.Event) -> None:
        """ 文本输入 """
        if self._press and self.live and not self.read:
            if event.keysym == 'BackSpace':
                # 按下退格键
                if len(self.value) > 1 and self.value[-2] == '\n':
                    self.value = self.value[:-2]
                elif len(self.value):
                    self.value = self.value[:-1]
            elif len(event.char) and len(self.value) < self.limit:
                # 按下普通按键
                key = ord(event.char)
                if 32 < key < 127 or key > 255 or (key == 32 and self.space):
                    line = sum(
                        [1 if 32 <= ord(i) < 127 else 2 for i in self.value.split('\n')[-1]])
                    line += 1 if 32 <= key < 127 else 2
                    if line > self.row:
                        self.value += '\n' + event.char
                    else:
                        self.value += event.char

            # 更新显示
            self.value_surface = self.value
            self.master.itemconfigure(self.text, text=self.value)
            self.cursor_update()


# 工具类


class PhotoImage(tkinter.PhotoImage):
    """
    ### 图片类
    生成图片并进行相应的一些处理（支持png和gif格式）
    """

    def __init__(self, file: str | bytes, *args, **kw) -> None:
        """
        ### 参数说明
        `file`: 图片文件的路径
        `*args`、`**kw`: 其他参数
        """
        self.file = file

        if file.split('.')[-1] == 'gif':
            self.frames = []
        else:
            tkinter.PhotoImage.__init__(self, file=file, *args, **kw)

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

    def play(self,
             canvas: Canvas,
             id,  # type: tkinter._CanvasItemId
             interval: int,
             _ind: int = 0) -> None:
        """
        播放动图，canvas.lock为False会暂停
        `canvas`: 播放动画的画布
        `id`: 播放动画的 _CanvasItemId（就是 create_text 的返回值）
        `interval`: 每帧动画的间隔时间
        """
        if _ind == len(self.frames):
            _ind = 0
        canvas.itemconfigure(id, image=self.frames[_ind])
        args = canvas, id, interval, _ind + canvas.lock
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


# 功能函数


def move_widget(
    master: Tk | Canvas | tkinter.Misc | tkinter.BaseWidget,
    widget: Canvas | _BaseWidget | tkinter.Misc | tkinter.BaseWidget,
    dx: int,
    dy: int,
    times: float,
    mode,  # type: Literal['smooth','shake','flat'] | tuple
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
    1. `smooth`: 速度先慢后快再慢（Sin函数模式，0~π）
    2. `shake`: 和 smooth 一样，但是最后会回弹一下(Cos函数模式，0~0.6π)
    3. `flat`: 匀速平移
    """

    # 速度变化模式
    if type(mode) == tuple and len(mode) >= 20:
        # 记忆值
        v = mode
    elif mode == 'smooth':
        # 流畅模式
        v = 0, 1, 3, 4, 5, 6, 7, 8, 8, 8, 8, 8, 8, 7, 6, 5, 4, 3, 1, 0
    elif mode == 'shake':
        # 抖动模式
        v = 11, 11, 10, 10, 10, 9, 9, 8, 7, 6, 6, 5, 4, 3, 1, 0, -1, -2, -3, -4
    elif mode == 'flat':
        # 平滑模式
        v = (5,) * 20
    else:
        # 函数模式
        f, start, end = mode
        end = (end - start) / 19
        v = tuple(f(start + end * _) for _ in range(20))
        key = 100 / sum(v)
        v = tuple(key * _ for _ in v)

    # 总计实际应该移动的百分比
    proportion = sum(v[:_ind + 1]) / 100

    # 计算本次移动量
    x = round(proportion * dx - _x)
    y = round(proportion * dy - _y)

    if isinstance(master, tkinter.Misc) and isinstance(widget, tkinter.BaseWidget):
        # 父控件：tkinter控件
        # 子控件：tkinter控件
        origin_x = int(widget.place_info()['x'])
        origin_y = int(widget.place_info()['y'])
        widget.place(x=origin_x + x, y=origin_y + y)
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
        args = master, widget, dx, dy, times, v, _x + x, _y + y, _ind + 1
        widget.master.after(round(times * 50), move_widget, *args)


def correct_text(
    length: int,
    string: str,
    position: Literal['left', 'center', 'right'] = 'center'
) -> str:
    """
    ### 修正字符串长度
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
        return ' ' * length + string
    elif position == 'right':
        # 靠右
        return string + length * ' '
    else:
        # 居中
        length, key = divmod(length, 2)
        return ' ' * length + string + (length + key) * ' '


def gradient_color(
    color: tuple[str, str],
    proportion: float = 0
) -> str:
    """
    ### 渐变色函数
    按一定比例给出已有RGB颜色字符串的渐变RGB颜色字符串
    #### 参数说明
    `color`: 颜色元组 (初始颜色, 目标颜色)
    `proportion`: 渐变比例（浮点数，范围为0~1）
    """

    # 判断颜色字符串格式（#FFF或者#FFFFFF格式）
    key = 256 if len(color[0]) == 7 else 16

    # 解析初始颜色的RGB
    _ = int(color[0][1:], 16)
    _, B = divmod(_, key)
    R, G = divmod(_, key)

    # 解析目标颜色的RGB
    _ = int(color[1][1:], 16)
    _, _B = divmod(_, key)
    _R, _G = divmod(_, key)

    # 根据比率计算返回值
    RGB = R + round((_R - R) * proportion)
    RGB *= key
    RGB += G + round((_G - G) * proportion)
    RGB *= key
    RGB += B + round((_B - B) * proportion)

    # 以对应格式返回结果
    return '#%0*X' % (6 if key == 256 else 3, RGB)


def _test():
    """ 测试函数 """
    from tkinter.messagebox import askyesno
    from math import cos, pi

    def shutdown(): return root.destroy() if askyesno('提示', '是否退出?') else None
    root = Tk('测试程序', '960x540', alpha=0.9, shutdown=shutdown)
    canvas = Canvas(root, 960, 540)
    canvas.pack(expand=True, fill='both')

    for i in range(100):
        color = gradient_color(('#FFFFFF', '#000000'), i/100)
        canvas.create_oval(
            466 - i/3, 66 - i/3, 566 + i, 166 + i,
            outline=color, width=2.5, fill='' if i else '#FFF')

    try:
        image = PhotoImage('tkinter.png')
        canvas.create_image(830, 150, image=image)
    except:
        print('\033[31m啊哦！你没有示例图片喏……\033[0m')
        root.bell()

    label1 = CanvasLabel(canvas,
                         700 * canvas.rate_x, 550 * canvas.rate_y,
                         250 * canvas.rate_x, 100 * canvas.rate_y,
                         10, '圆角标签\n移动模式:shake',
                         font=('楷体', round(15 * canvas.rate_x)))
    label2 = CanvasLabel(canvas,
                         430 * canvas.rate_x, 550 * canvas.rate_y,
                         250 * canvas.rate_x, 100 * canvas.rate_y,
                         0, '方角标签\n移动模式:smooth',
                         font=('楷体', round(15 * canvas.rate_x)))

    CanvasButton(
        canvas, 50, 50, 120, 25, 5, '圆角按钮',
        command=lambda: move_widget(canvas, label1, 0, -120 * canvas.rate_y, 0.25, 'shake'))
    CanvasButton(
        canvas, 50, 100, 120, 25, 0, '方角按钮',
        command=lambda: move_widget(canvas, label2, 0, -120 * canvas.rate_y, 0.25, 'smooth'))
    CanvasEntry(canvas, 200, 50, 200, 25, 5, ('圆角输入框', '点击输入'), limit=9)
    CanvasEntry(canvas, 200, 100, 200, 25, 0, ('方角输入框', '点击输入'), '*', 16)
    CanvasText(canvas, 50, 150, 350, 150, 10, limit=400).change_text('圆角文本框')
    CanvasText(canvas, 50, 340, 350, 150, 0, limit=400).change_text('方角文本框')

    root.mainloop()


if __name__ == '__main__':
    """ 测试 """
    print(__doc__)
    _test()
