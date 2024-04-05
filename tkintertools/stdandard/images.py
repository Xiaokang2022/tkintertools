"""All standard Images"""

import fractions
import tkinter
import typing

from .. import core

try:
    from PIL import Image, ImageTk
    __PIL = True
except ImportError:
    __PIL = False


class NoImage(core.Image):
    """"""

    def display(self) -> None:
        pass


class StillImage(core.Image):
    """"""


class DynamicImage(core.Image):
    """"""

    def __init__(self, path: str, **kw) -> None:
        """
        * `path`: the path of image file
        * `**kw`: compatible with other parameters of class `tkinter.PhotoImage`
        """
        self.path = path
        self.extension = self._get_extension()
        self._item: dict[int, "core.Canvas" | None] = {}

        if self.extension == "gif":
            self.image: list[tkinter.PhotoImage] = []
            self.parse_done = False
            self.active = False
        elif self.extension == "png":
            tkinter.PhotoImage.__init__(self, file=path, **kw)
        else:  # BUG: ???
            ImageTk.PhotoImage.__init__(self, Image.open(path))

    def parse(self, start: int = 0) -> typing.Generator[int, None, None] | None:
        """解析动图，并得到动图的每一帧动画，该方法返回一个生成器 

        * `start`: 动图解析的起始索引（帧数减一）
        """
        try:
            if self.parse_done:
                return
            while True:
                self.image.append(tkinter.PhotoImage(
                    file=self.path, format=f"gif -index {start}"))
                value = yield start  # 抛出索引
                start += value if value else 1
        except tkinter.TclError:
            self.parse_done = True
            return

    def start(self, canvas: "core.Canvas", item: int, *, interval: int, callback: typing.Callable[[int], typing.Any] | None = None, **kw) -> None:
        """播放动图，`canvas.lock` 为 `False` 时会暂停 

        * `canvas`: 播放动画的画布
        * `item`: 播放动画的 `_CanvasItemId`（`create_image` 方法的返回值）
        * `interval`: 每帧动画的间隔时间
        * `callback`: 运行时解析的回调函数，传入当前已解析的帧数
        """
        if kw.get("_ind", None) is None:  # 初始化的判定
            self._item[item], kw["_ind"] = canvas, -1
            self.play()
        if not self._item[item]:  # 终止播放的判定
            return
        if self.active and canvas._lock:  # 暂停播放的判定
            if not self.parse_done:
                if getattr(self, "parser", None) is None:
                    self.parser = self.parse()
                next(self.parser, None)
                if callback is not None:
                    callback(kw["_ind"] + 1)
            canvas.itemconfigure(item, image=self.image[kw["_ind"]])
        _ind = kw["_ind"] + 1
        # 迭代执行函数
        canvas.after(interval if self.parse_done else 1, lambda: self.start(
            canvas, item, interval=interval, callback=callback, _ind=0 if _ind == len(self.image) else _ind))

    def play(self) -> None:
        """播放"""
        self.active = True

    def pause(self) -> None:
        """暂停"""
        self.active = False

    def stop(self, item: int, clear: bool = False) -> None:
        """终止对应动图的播放，且无法重新播放 

        * `item`: 播放动画的 `_CanvasItemId`（`create_text` 方法的返回值）
        * `clear`: 清除图片的标识，为 `True` 就清除图片
        """
        self._item[item] = None
        if clear:  # 清除背景
            self._item[item].itemconfigure(item, image=None)

    def get_total_frames(self, _index: int = 16, _base: int = 0) -> int:
        """获得 gif 图片的总帧数"""
        if __PIL:
            return self._get_total_frames_with_PIL(self.path)
        if _index == 0:
            return _base + 1
        try:
            tkinter.PhotoImage(
                file=self.path, format=f"gif -index {_index+_base}")
        except tkinter.TclError:
            return self.get_total_frames(_index >> 1, _base)
        return self.get_total_frames(_index << 1, _index+_base)

    def _get_total_frames_with_PIL(self, image: str, _frames: int = 0) -> int:
        """通过 PIL 库获取 gif 图片的总帧数"""
        image_object = Image.open(image)
        try:
            while True:
                _frames += 1
                image_object.seek(image_object.tell() + 1)
        except EOFError:
            return _frames

    def zoom(self, rate_x: float, rate_y: float, *, precision: float | None = None) -> tkinter.PhotoImage:
        """缩放图片，但不会缩放该图片对象本身，只是返回一个缩放后的图片对象 

        * `rate_x`: 横向缩放倍率
        * `rate_y`: 纵向缩放倍率
        * `precision`: 精度到小数点后的位数（推荐 1.2），越大运算就越慢（默认值代表绝对精确）

        注意：若有 PIL 包，请忽略参数 `precision`
        """
        if __PIL:
            new_size = map(
                int, [self.width() * rate_x, self.height() * rate_y])
            image = Image.open(self.path).resize(new_size)
            return ImageTk.PhotoImage(image)
        if precision is not None:
            limit = round(10**precision)
            rate_x = fractions.Fraction(str(rate_x)).limit_denominator(
                limit)  # type: fractions.Fraction
            rate_y = fractions.Fraction(str(rate_y)).limit_denominator(
                limit)  # type: fractions.Fraction
            image = tkinter.PhotoImage.zoom(
                self, rate_x.numerator, rate_y.numerator)
            image = image.subsample(rate_x.denominator, rate_y.denominator)
        else:
            width, height = int(
                self.width() * rate_x), int(self.height() * rate_y)
            image = tkinter.PhotoImage(width=width, height=height)
            for x in range(width):
                for y in range(height):
                    r, g, b = self.get(int(x/rate_x), int(y/rate_y))
                    image.put(f"#{r:02X}{g:02X}{b:02X}", (x, y))

        return image

    def destroy(self) -> None:
        """"""


__all__ = [
    "NoImage",
    "StillImage",
    "DynamicImage",
]
