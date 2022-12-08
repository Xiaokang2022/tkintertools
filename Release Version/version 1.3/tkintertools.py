"""tkintertools 模块是 tkinter 模块的扩展模块

这个模块将给用户提供透明化的控件，以及一些特殊的功能函数

作者：小康2022

版本：1.3

更新时间：2022/9/20
"""


import random
import tkinter
import typing


### 允许特定导入的类和函数 ###


__all__ = ['SpecialTk',
           'SpecialCanvas',
           'CanvasLabel',
           'CanvasButton',
           'CanvasEntry',
           'CanvasText',
           'move_widget',
           'correct_text',
           'process_color']


### 特殊容器控件 ###


class SpecialCanvas(tkinter.Canvas):
    """特殊画布类

    启动画布虚拟子控件的功能，需解开界面功能锁（将 `canvas_lock` 设为 `True` ）
    """

    def __init__(self, master: tkinter.Tk, width: float, height: float, *args, **kwargs) -> None:
        # 调用父类初始化方法
        tkinter.Canvas.__init__(self, master=master,
                                width=width, height=height, *args, **kwargs)
        # 添加到SpecialTk的画布列表中
        self.master: SpecialTk
        self.master.canvas_list.append(self)
        # 子控件列表（与绑定有关）
        self.widget_list: list[CanvasButton |
                               CanvasEntry | CanvasLabel | CanvasText] = []
        # 画布界面锁（切换界面用，用不到时要改为True）
        self.canvas_lock = False
        # 初始大小
        self.init_width = width
        self.init_height = height
        # 放缩比率
        self.rate_x = 1
        self.rate_y = 1


class SpecialTk(tkinter.Tk):
    """特殊Tk类

    用于集中处理 `SpecialCanvas` 绑定的关联事件
    """

    def __init__(self, *args, **kwargs) -> None:
        # 调用父类初始化方法
        tkinter.Tk.__init__(self, *args, **kwargs)
        # 子画布列表（与缩放绑定有关）
        self.canvas_list: list[SpecialCanvas] = []

    @staticmethod
    def __bind_move(event: tkinter.Event, canvas: SpecialCanvas) -> None:
        """ 鼠标光标移动事件 """
        for widget in canvas.widget_list:
            widget.move(event)

    @staticmethod
    def __bind_press(event: tkinter.Event, canvas: SpecialCanvas) -> None:
        """ 鼠标左键按下事件 """
        for widget in canvas.widget_list:
            if isinstance(widget, CanvasButton | CanvasEntry | CanvasText):
                widget.press(event)

    @staticmethod
    def __bind_release(event: tkinter.Event, canvas: SpecialCanvas) -> None:
        """ 鼠标左键松开事件 """
        for widget in canvas.widget_list:
            if isinstance(widget, CanvasButton):
                # 执行对应的关联函数
                widget.execute(event)
                # 外观恢复默认设置
                widget.default_setting()

    @staticmethod
    def __bind_mousewheel(event: tkinter.Event, canvas: SpecialCanvas) -> None:
        """ 鼠标滚轮滚动事件 """
        for widget in canvas.widget_list:
            if isinstance(widget, CanvasText):
                widget.scroll(event)

    def __bind_input(self, event: tkinter.Event) -> None:
        """ 键盘输入字符事件 """
        for canvas in self.canvas_list:
            for widget in canvas.widget_list:
                if isinstance(widget, CanvasEntry | CanvasText):
                    widget.input(event)

    def launch_bind(self) -> None:
        """ 启动关联事件的绑定 """

        # 绑定键盘输入
        self.bind('<Any-Key>', self.__bind_input)
        # 遍历所有画布
        for canvas in self.canvas_list:
            # 绑定鼠标光标移动
            canvas.bind('<Motion>', lambda event,
                        _canvas=canvas: self.__bind_move(event, _canvas))
            # 绑定鼠标左键按下
            canvas.bind('<Button-1>', lambda event,
                        _canvas=canvas: self.__bind_press(event, _canvas))
            # 绑定鼠标左键松开
            canvas.bind('<ButtonRelease-1>', lambda event,
                        _canvas=canvas: self.__bind_release(event, _canvas))
            # 绑定鼠标左键按下移动
            canvas.bind('<B1-Motion>', lambda event,
                        _canvas=canvas: self.__bind_press(event, _canvas))
            # 绑定鼠标滚轮滚动
            canvas.bind('<MouseWheel>', lambda event,
                        _canvas=canvas: self.__bind_mousewheel(event, _canvas))

    def launch_zoom(self, init_width: int, init_height: int) -> None:
        """ 启动子画布控件缩放检测 """

        # 检测当前窗口的大小
        window_width, window_height = self.winfo_width(), self.winfo_height()
        # 计算横向缩放倍率
        rate_x = window_width / init_width
        # 计算纵向缩放倍率
        rate_y = window_height / init_height
        # 判断窗口大小是否变化
        if window_width != init_width or window_height != init_height:
            # 更新子画布控件的大小
            for canvas in self.canvas_list:
                # 更新画布的横纵缩放比率
                canvas.rate_x = window_width / canvas.init_width
                canvas.rate_y = window_height / canvas.init_height
                # 更新子画布控件的子虚拟画布控件的位置
                for item in canvas.find_all():
                    canvas.coords(item, [coord * rate_y if ind % 2 else coord * rate_x for ind, coord in
                                         enumerate(canvas.coords(item))])
                    size: str = canvas.itemcget(item, 'tags')
                    if size.isdigit():
                        # 字体大小修改
                        font: str = canvas.itemcget(item, 'font')
                        font = font.split()
                        font[1] = round(
                            int(size) * min(canvas.rate_x, canvas.rate_y))
                        canvas.itemconfigure(item, font=font)

                # 更新子画布控件的子虚拟画布控件位置数据
                for widget in canvas.widget_list:
                    widget.x1 *= rate_x
                    widget.x2 *= rate_x
                    widget.y1 *= rate_y
                    widget.y2 *= rate_y
        # 更新当前窗口大小的参数
        self.after(10, self.launch_zoom, window_width, window_height)


### 控件基类 ###


class BaseWidget:
    """虚拟画布控件基类

    内部类，供模块内部调用和继承
    """

    def __init__(self,
                 canvas: SpecialCanvas,
                 x1: float,
                 y1: float,
                 x2: float,
                 y2: float,
                 text: str = '',
                 font_size: int = 15,
                 color_text_normal: str = 'grey',
                 color_rectangle_outline_normal: str = 'grey',
                 color_rectangle_inline_normal: str = '',
                 color_text_press: str = 'white',
                 color_rectangle_outline_press: str = 'white',
                 color_rectangle_inline_press: str = 'grey',
                 color_text_move: str = 'white',
                 color_rectangle_outline_move: str = 'white',
                 color_rectangle_inline_move: str = '') -> None:
        # 添加自身到父画布控件
        canvas.widget_list.append(self)

        # 父画布控件
        self.canvas = canvas
        # 显示文本
        self.value = text
        # 是否处于活跃状态
        self.live = True

        # 左上角与右下角坐标
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        # 显示文字正常颜色
        self.CTN = color_text_normal
        # 外框轮廓正常颜色
        self.CRON = color_rectangle_outline_normal
        # 外框内部正常颜色
        self.CRIN = color_rectangle_inline_normal

        # 显示文字按下颜色
        self.CTP = color_text_press
        # 外框轮廓按下颜色
        self.CROP = color_rectangle_outline_press
        # 外框内部按下颜色
        self.CRIP = color_rectangle_inline_press

        # 显示文字移动颜色
        self.CTM = color_text_move
        # 外框轮廓移动颜色
        self.CROM = color_rectangle_outline_move
        # 外框内部移动颜色
        self.CRIM = color_rectangle_inline_move

        # 虚拟按钮的外框
        self.rectangle = self.canvas.create_rectangle(x1, y1, x2, y2,
                                                      width=2,
                                                      outline=self.CRON,
                                                      fill=self.CRIN)
        # 虚拟按钮显示的文字
        self.text = self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2,
                                            text=text,
                                            font=('楷体', round(
                                                font_size * min(canvas.rate_x, canvas.rate_y))),
                                            justify='center',
                                            fill=self.CTN,
                                            tags=str(font_size))

    def default_setting(self) -> None:
        """ 恢复默认外观设置 """

        self.canvas.itemconfigure(self.rectangle, outline=self.CRON)
        self.canvas.itemconfigure(self.rectangle, fill=self.CRIN)
        self.canvas.itemconfigure(self.text, fill=self.CTN)

    def change_position(self, dx: float, dy: float) -> None:
        """ 改变控件的位置 """

        # 改变坐标值
        self.x1 += dx
        self.x2 += dx
        self.y1 += dy
        self.y2 += dy

        # 更新按钮外框的位置
        self.canvas.coords(self.rectangle, self.x1, self.y1, self.x2, self.y2)
        # 更新显示文字的位置
        self.canvas.coords(self.text, (self.x1 + self.x2) /
                           2, (self.y1 + self.y2) / 2)

    def destroy(self) -> None:
        """ 摧毁控件释放内存 """

        # 取消执行关联函数的功能
        self.live = False
        self.canvas.delete(self.rectangle)
        self.canvas.delete(self.text)


class TextWidget(BaseWidget):
    """虚拟画布文本控件基类

    内部类，供继承和调用
    """

    # 表面显示值
    value_surface = ''
    # 鼠标左键是否在输入框内按下
    PRESS = False

    def cursor(self, _cursor: bool = True, delay: int = 300) -> None:
        """ 鼠标光标闪烁显示 """
        if delay == 300:
            # 更新显示
            if self.canvas.itemcget(self.text, 'justify') == 'center':
                self.canvas.itemconfigure(
                    self.text, text='  ' + self.value_surface + ('▏' if _cursor else '  '))
            else:
                self.canvas.itemconfigure(
                    self.text, text=self.value_surface + ('▏' if _cursor else '  '))
            _cursor = not _cursor
            delay = 0

        if self.PRESS:
            # 更新函数
            self.canvas.after(10, self.cursor, _cursor, delay + 10)


### 虚拟画布控件 ###


class CanvasLabel(BaseWidget):
    """虚拟画布标签

    创建一个可透明的虚拟标签，用于显示少量文本

    该虚拟控件没有鼠标点击事件
    """

    def __move(self) -> None:
        """ 鼠标悬停状态 """

        self.canvas.itemconfigure(self.text, fill=self.CTM)
        self.canvas.itemconfigure(self.rectangle, outline=self.CROM)
        self.canvas.itemconfigure(self.rectangle, fill=self.CRIM)

    def move(self, event: tkinter.Event) -> None:
        """ 鼠标悬停状态检测 """

        if self.canvas.canvas_lock:
            if self.x1 < event.x < self.x2 and self.y1 < event.y < self.y2:
                # 鼠标悬停
                self.__move()
            else:
                # 恢复外观为默认值
                self.default_setting()


class CanvasButton(BaseWidget):
    """虚拟画布按钮类

    创建一个透明且含边框的虚拟按钮

    确保管理其的虚拟画布的功能界面锁已开启，
    且启动了 `special_bind` 方法
    """

    # 绑定的执行函数
    command = None

    def execute(self, event: tkinter.Event) -> None:
        """ 执行关联函数 """

        if self.live and self.canvas.canvas_lock:
            if self.x1 < event.x < self.x2 and self.y1 < event.y < self.y2 and self.command:
                # 执行关联函数
                self.command()

    def __press(self) -> None:
        """ 虚拟按钮按下状态 """

        self.canvas.itemconfigure(self.text, fill=self.CTP)
        self.canvas.itemconfigure(self.rectangle, outline=self.CROP)
        self.canvas.itemconfigure(self.rectangle, fill=self.CRIP)

    def __move(self) -> None:
        """ 鼠标悬停状态 """

        self.canvas.itemconfigure(self.text, fill=self.CTM)
        self.canvas.itemconfigure(self.rectangle, outline=self.CROM)
        self.canvas.itemconfigure(self.rectangle, fill=self.CRIM)

    def press(self, event: tkinter.Event) -> None:
        """ 按钮按下状态检测 """

        if self.canvas.canvas_lock:
            if self.x1 < event.x < self.x2 and self.y1 < event.y < self.y2:
                # 鼠标左键按下
                self.__press()
            else:
                # 恢复外观为默认值
                self.default_setting()

    def move(self, event: tkinter.Event) -> None:
        """ 鼠标悬停状态检测 """

        if self.canvas.canvas_lock:
            if self.x1 < event.x < self.x2 and self.y1 < event.y < self.y2:
                # 鼠标悬停
                self.__move()
            else:
                # 恢复外观为默认值
                self.default_setting()

    def change_text(self, value: str) -> None:
        """ 重新设定显示文字 """

        # 改变显示值
        self.value = value
        # 更新显示值
        self.canvas.itemconfigure(self.text, text=value)


class CanvasEntry(TextWidget):
    """虚拟画布输入框类

    创建一个透明的虚拟输入框

    设置 `show` 属性来更改文本的显示样式

    设置 `limit` 属性来更改输入文本的限制长度
    """

    # 真实值
    value_real = ''
    # 显示模式
    show = ''
    # 限定文本输入的长度
    limit = 15

    def __init__(self,
                 canvas: SpecialCanvas,
                 x1: float,
                 y1: float,
                 x2: float,
                 y2: float,
                 text_normal: str = '',
                 text_move: str = '',
                 *args, **kwargs) -> None:
        # 调用父类
        BaseWidget.__init__(self, canvas, x1, y1, x2, y2,
                            text_normal, *args, **kwargs)

        # 鼠标悬停显示文本
        self.text_move = text_move

    def __press_on(self) -> None:
        """ 鼠标左键按下状态 """

        self.PRESS = True
        self.canvas.itemconfigure(self.rectangle, outline=self.CROP)
        # 触发鼠标光标闪烁
        self.cursor()

    def __press_off(self) -> None:
        """ 鼠标左键松开状态 """

        self.PRESS = False
        self.canvas.itemconfigure(self.rectangle, outline=self.CRON)

        # 判断是否已经输入了文本
        if self.value_real == '':
            # 设为默认显示值
            self.canvas.itemconfigure(self.text, text=self.value)
        else:
            # 设为显示值
            self.canvas.itemconfigure(self.text, text=self.value_surface)

    def __move_on(self) -> None:
        """ 鼠标悬停状态 """

        if not self.PRESS:
            self.canvas.itemconfigure(self.rectangle, outline=self.CROM)

            # 判断显示的值是否为第一默认值
            if self.canvas.itemcget(self.text, 'text') == self.value:
                # 更新为第二默认值
                self.canvas.itemconfigure(self.text, text=self.text_move)

    def __move_off(self) -> None:
        """ 鼠标离开状态 """

        if not self.PRESS:
            self.canvas.itemconfigure(self.rectangle, outline=self.CRON)

            # 判断显示的值是否为第二默认值
            if self.canvas.itemcget(self.text, 'text') == self.text_move:
                # 更新为第一默认值
                self.canvas.itemconfigure(self.text, text=self.value)

    def press(self, event: tkinter.Event) -> None:
        """ 鼠标左键按下状态检测 """

        if self.canvas.canvas_lock:
            if self.x1 < event.x < self.x2 and self.y1 < event.y < self.y2:
                if not self.PRESS:
                    # 鼠标左键按下
                    self.__press_on()
            else:
                # 鼠标左键松开
                self.__press_off()

    def move(self, event: tkinter.Event) -> None:
        """ 鼠标悬停状态检测 """

        if self.canvas.canvas_lock:
            if self.x1 < event.x < self.x2 and self.y1 < event.y < self.y2:
                # 鼠标悬停
                self.__move_on()
            else:
                # 鼠标离开
                self.__move_off()

    def change_text(self, value: str) -> None:
        """ 重新设定显示文字 """

        # 改变真实值
        self.value_real = value
        # 改变显示值
        self.value_surface = len(value) * self.show if self.show else value
        # 更新显示值
        self.canvas.itemconfigure(self.text, text=self.value_surface)

    def input(self, event: tkinter.Event) -> None:
        """ 文本输入 """

        if self.canvas.canvas_lock:
            if self.PRESS and self.live:
                if event.keysym == 'BackSpace':
                    # 按下退格键
                    self.value_real = self.value_real[:-1]
                if len(event.char) and len(self.value_real) < self.limit:
                    if 32 < ord(event.char) < 127 or ord(event.char) > 255:
                        # 按下普通按键
                        self.value_real += event.char

                # 更新表面显示值
                self.value_surface = len(
                    self.value_real) * self.show if self.show else self.value_real
                # 更新显示
                self.canvas.itemconfigure(
                    self.text, text='  ' + self.value_surface + '▏')


class CanvasText(TextWidget):
    """虚拟画布文本框类

    创建一个透明的虚拟文本框，
    用于输入多行文本和显示多行文本（只读模式）

    设置 `read` 属性为 `True` 来开启只读模式

    设置 `limit` 属性的值来限制输入的文本长度
    """

    # 总文本默认最大输入长度
    limit = 100
    # 只读模式
    read = False

    def __init__(self, *args, **kwargs) -> None:

        # 调用父类
        BaseWidget.__init__(self, *args, **kwargs)
        # 修改多行文本靠左显示
        self.canvas.coords(self.text, self.x1 + 10, self.y1 + 10)
        self.canvas.itemconfigure(self.text, anchor='nw', justify='left')
        # 计算单行文本容纳量
        self.width = (self.x2 - self.x1) // 10 - 2
        # 计算文本容纳行数
        self.height = (self.y2 - self.y1) // 20
        # 文本位置
        self.position = self.height

    def __press_on(self) -> None:
        """ 鼠标左键按下状态 """

        if not self.read:
            self.PRESS = True
            self.canvas.itemconfigure(self.rectangle, outline=self.CROP)
            self.canvas.itemconfigure(self.text, fill=self.CTP)
            # 触发鼠标光标闪烁
            self.cursor()

    def __press_off(self) -> None:
        """ 鼠标左键松开状态 """

        if not self.read:
            self.PRESS = False
            self.canvas.itemconfigure(self.rectangle, outline=self.CRON)
            self.canvas.itemconfigure(self.text, fill=self.CTN)
            self.canvas.itemconfigure(self.text, text=self.value)

    def __move_on(self) -> None:
        """ 鼠标悬停状态 """

        if not self.PRESS:
            self.canvas.itemconfigure(self.rectangle, outline=self.CROM)
            self.canvas.itemconfigure(self.text, fill=self.CTM)

    def __move_off(self) -> None:
        """ 鼠标离开状态 """

        if not self.PRESS:
            self.canvas.itemconfigure(self.rectangle, outline=self.CRON)
            self.canvas.itemconfigure(self.text, fill=self.CTN)

    def press(self, event: tkinter.Event) -> None:
        """ 鼠标左键按下状态检测 """

        if self.canvas.canvas_lock:
            if self.x1 < event.x < self.x2 and self.y1 < event.y < self.y2:
                if not self.PRESS:
                    # 鼠标左键按下
                    self.__press_on()
            else:
                # 鼠标左键松开
                self.__press_off()

    def move(self, event: tkinter.Event) -> None:
        """ 鼠标悬停状态检测 """

        if self.canvas.canvas_lock:
            if self.x1 < event.x < self.x2 and self.y1 < event.y < self.y2:
                # 鼠标悬停
                self.__move_on()
            else:
                # 鼠标离开
                self.__move_off()

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
        if key <= self.height:
            # 更新显示值
            self.canvas.itemconfigure(self.text, text=self.value)
        else:
            # 同步更新文本上下位置数据
            self.position += value.count('\n')
            # 计算显示文本的部分
            ind = key - self.height
            self.value_surface = '\n'.join(
                self.value.split('\n')[ind:ind + self.height])
            self.canvas.itemconfigure(self.text, text=self.value_surface)

    def scroll(self, event: tkinter.Event) -> None:
        """ 文本滚动 """

        if self.canvas.canvas_lock:
            if self.x1 < event.x < self.x2 and self.y1 < event.y < self.y2:
                if event.delta > 0 and self.position > self.height:
                    # 鼠标向上滚动，显示文本部分向下滚动
                    self.position -= 1
                elif event.delta < 0 and self.position < self.value.count('\n'):
                    # 鼠标向下滚动，显示文本部分向上滚动
                    self.position += 1
                # 计算显示文本的部分
                ind = self.position - self.height
                self.value_surface = '\n'.join(
                    self.value.split('\n')[ind:ind + self.height])
                self.canvas.itemconfigure(self.text, text=self.value_surface)

    def input(self, event: tkinter.Event) -> None:
        """ 文本输入 """

        if self.canvas.canvas_lock:
            if self.PRESS and self.live and not self.read:
                if event.keysym == 'BackSpace':
                    # 按下退格键
                    if len(self.value) > 1 and self.value[-2] == '\n':
                        self.value = self.value[:-2]
                    elif len(self.value):
                        self.value = self.value[:-1]
                elif len(event.char) and len(self.value) < self.limit:
                    # 按下普通按键
                    if 32 < ord(event.char) < 127 or ord(event.char) > 255:
                        line = sum(
                            [1 if 32 < ord(i) < 127 else 2 for i in self.value.split('\n')[-1]])
                        line += 1 if 32 < ord(event.char) < 127 else 2
                        if line > self.width:
                            self.value += '\n' + event.char
                        else:
                            self.value += event.char

                # 更新显示
                self.value_surface = self.value
                self.canvas.itemconfigure(self.text, text=self.value + '▏')


### 功能函数 ###


def move_widget(root: tkinter.Tk | SpecialCanvas | tkinter.Canvas,
                widget: SpecialCanvas | BaseWidget,
                dx: int,
                dy: int,
                fps: int,
                mode: typing.Literal['smooth', 'shake', 'flat'],
                ind: int = 0) -> None:
    """平滑移动函数

    以 `smooth`、`shake`、`flat` 三种模式
    平滑地移动某些或某部分图像

    此函数为Place准备，暂不适用于Pack和Grid
    """

    # 三种模式的速度变化列表
    if mode == 'smooth':
        lib = [1, 2, 2, 3, 3, 5, 6, 7, 9, 12, 12, 9, 7, 6, 5, 3, 3, 2, 2, 1]
    elif mode == 'shake':
        lib = [10, 10, 9, 9, 8, 8, 7, 7, 6, 6,
               5, 5, 4, 4, 3, 3, 1, -1, - 2, -3]
    elif mode == 'flat':
        lib = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

    # x偏移量
    x = int(lib[ind] * dx / 100)
    # y偏移量
    y = int(lib[ind] * dy / 100)

    if isinstance(root, tkinter.Tk):
        # 原x坐标
        origin_x = int(widget.place_info()['x'])
        # 原y坐标
        origin_y = int(widget.place_info()['y'])
        widget.place(x=origin_x + x, y=origin_y + y)
    elif isinstance(widget, BaseWidget):
        widget.change_position(x, y)
    else:
        root.move(widget, x, y)

    if ind < 19:
        # 更新函数
        root.after(1000 // fps, move_widget, root, widget,
                   dx, dy, fps, mode, ind + 1)


def correct_text(length: int, string: str) -> str:
    """字符串长度修正函数

    针对“楷体”中英文长度不一致，无法对齐的问题

    可将目标字符串改为目标长度并居中对齐
    """

    # 修正长度
    n = length - sum([1 + (ord(i) > 256) for i in string])
    # 修正空格数
    space = (n // 2) * ' '
    # 居中对齐
    value = space + string + space
    # 奇偶处理
    return value if n % 2 == 0 else value + ' '


def process_color(color: str | None = None, key: float | str = '') -> str:
    """颜色字符串处理函数（RGB码）

    随机产生一个RGB颜色字符串

    以及给出已有RGB颜色字符串的渐变RGB颜色字符串
    """

    lib, rgb = '0123456789ABCDEF', ''
    if not color:
        # 随机RGB颜色字符串
        for _ in range(6):
            rgb += lib[random.randint(0, 15)]
    else:
        # 渐变RGB颜色字符串的生成
        *slice_seq, length = (1, 2, 3, 1) if len(color) == 4 else (1, 3, 5, 2)
        if type(key) == float:
            for ind in slice_seq:
                rgb += oct(round(int(color[ind: ind +
                           length], 16) * key) % 16)[2:]
        elif type(key) == str:
            for ind in slice_seq:
                rgb += oct(int(color[ind: ind + length],
                           16) + int(key, 16))[2:]
    return '#' + rgb
