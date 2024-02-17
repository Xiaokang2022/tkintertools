"""All standard Shapes"""

import tkinter

from . import core


class NoShape(core.Shape):
    """"""

    def display(self, master: core.Canvas, size: tuple[int, int], position: tuple[int, int]) -> None:
        # Override:
        self._master = master
        self._size = list(size)
        self._position = list(position)


class Rectangle(core.Shape):
    """"""


# class RoundedRectangle(core.Shape):
#     """"""

#     def __init__(
#         self,
#         *,
#         radius: tuple[int, int, int, int] | int = 0,
#         borderwidth: int = 1,
#     ) -> None:
#         """"""
#         core.Shape.__init__(self)
#         self._radius = radius
#         self._borderwidth = borderwidth

#     def display(self, master: core.Canvas, size: tuple[int, int], position: tuple[int, int]) -> None:
#         """"""
#         self._master = master
#         self._size = list(size)
#         self._position = list(position)

#         x, y, w, h = *position, *size
#         x1, y1, x2, y2 = x, y, x + w, y + h

#         if self._radius == 0:  # 矩形
#             self._items.append(master.create_rectangle(x1, y1, x2, y2))

#         if size[0] == size[1]:  # 长 = 宽
#             if self._radius > size[0] / 2:  # 圆形
#                 self._items.append(master.create_oval(x1, y1, x2, y2))
#             else:
#                 pass  # 圆角方形
#         elif size[0] > size[1]:  # 长 > 宽
#             if self._radius > min(size):
#                 pass
#             else:
#                 pass
#         else:  # 宽 > 长
#             if self._radius > min(size):
#                 pass
#             else:
#                 pass

#         # self.radius = radius
#         # self.borderwidth = borderwidth
#         # self.fill = fill
#         # self.outline = outline

#         width, height, x, y = *size, *position

#         if oval:  # oval
#             self._oval = self.master.create_oval(
#                 x, y, x + width, y + height, fill=fill, outline=outline, width=borderwidth)
#         elif isinstance(radius, (int, float)):
#             if radius < 0.5:  # rectangle
#                 self._rectangle = self.master.create_rectangle(
#                     x, y, x + width, y + height, fill=fill, outline=outline, width=borderwidth)
#             else:
#                 diameter = radius * 2
#                 if diameter >= width and width == height:  # circle
#                     self.radius = width / 2
#                     self._circle = self.master.create_oval(
#                         x, y, x + width, y + height, fill=fill, outline=outline, width=borderwidth)
#                 elif diameter >= width and diameter < height:  # vertical semicircle
#                     self.radius = width / 2
#                     up = x, y, x + width, y + diameter
#                     down = x, y + height - diameter, x + width, y + height

#                     kw = {"extent": 180, "fill": fill,
#                           "outline": "", "tags": "fill"}
#                     self._in = [
#                         self.master.create_rectangle(
#                             x, y + radius, x + width, y + height - radius, fill=fill, outline=""),
#                         self.master.create_arc(*up, **kw, start=0),
#                         self.master.create_arc(*down, **kw, start=180),
#                     ]
#                     kw = {"extent": 180, "style": tkinter.ARC,
#                           "outline": outline, "width": borderwidth}
#                     self._out = [
#                         self.master.create_line(
#                             x, y + radius, x, y + height - radius, fill=outline, width=borderwidth, tags="fill"),
#                         self.master.create_line(
#                             x + width, y + radius, x + width, y + height - radius, fill=outline, width=borderwidth, tags="fill"),
#                         self.master.create_arc(*up, **kw, start=0),
#                         self.master.create_arc(*down, **kw, start=180),
#                     ]
#                 elif diameter < width and diameter >= height:  # horizontal semicircle
#                     self.radius = height / 2
#                     left = x, y, x + diameter, y + height
#                     right = x + width - diameter, y, x + width, y + height

#                     kw = {"extent": 180, "fill": fill, "outline": ""}
#                     self._in = [
#                         self.master.create_rectangle(
#                             x + radius, y, x + width - radius, y + height, fill=fill, outline=""),
#                         self.master.create_arc(*left, **kw, start=90),
#                         self.master.create_arc(*right, **kw, start=-90),
#                     ]
#                     kw = {"extent": 180, "style": tkinter.ARC,
#                           "outline": outline, "width": borderwidth}
#                     self._out = [
#                         self.master.create_line(
#                             x + radius, y, x + width - radius, y, fill=outline, width=borderwidth, tags="fill"),
#                         self.master.create_line(
#                             x + radius, y + height, x + width - radius, y + height, fill=outline, width=borderwidth, tags="fill"),
#                         self.master.create_arc(*left, **kw, start=90),
#                         self.master.create_arc(*right, **kw, start=-90),
#                     ]
#                 else:  # regular rounded rectangle
#                     up_left = x, y, x + diameter, y + diameter
#                     up_right = x + width, y, x + width - diameter, y + diameter
#                     down_left = x, y + height, x + diameter, y + height - diameter
#                     down_right = x + width, y + height, x + width - diameter, y + height - diameter

#                     kw = {"fill": fill, "outline": ""}
#                     self._in = [
#                         self.master.create_rectangle(
#                             x, y + radius, x + width, y + height - radius, **kw),
#                         self.master.create_rectangle(
#                             x + radius, y, x + width - radius, y + height, **kw),
#                         self.master.create_arc(*up_left, **kw, start=90),
#                         self.master.create_arc(*up_right, **kw, start=0),
#                         self.master.create_arc(*down_left, **kw, start=180),
#                         self.master.create_arc(*down_right, **kw, start=-90),
#                     ]
#                     kw = {"style": tkinter.ARC, "outline": outline,
#                           "width": borderwidth, "tags": None}
#                     self._out = [
#                         self.master.create_line(
#                             x, y + radius, x, y + height - radius, fill=outline, width=borderwidth, tags="fill"),
#                         self.master.create_line(
#                             x + width, y + radius, x + width, y + height - radius, fill=outline, width=borderwidth, tags="fill"),
#                         self.master.create_line(
#                             x + radius, y, x + width - radius, y, fill=outline, width=borderwidth, tags="fill"),
#                         self.master.create_line(
#                             x + radius, y + height, x + width - radius, y + height, fill=outline, width=borderwidth, tags="fill"),
#                         self.master.create_arc(*up_left, **kw, start=90),
#                         self.master.create_arc(*up_right, **kw, start=0),
#                         self.master.create_arc(*down_left, **kw, start=180),
#                         self.master.create_arc(*down_right, **kw, start=-90),
#                     ]
#         else:  # TODO: irregular rounded rectangle
#             pass

#         for shape in "_rectangle", "_circle", "_oval":
#             if hasattr(self, shape):
#                 self._items = [getattr(self, shape)]
#                 break
#         else:
#             self._items = self._in + self._out

#     def configure(self, *, fill=None, outline=None):
#         # type: (..., str | None, str | None) -> None
#         """
#         change property
#         #### Keyword-only Arguments
#         * `fill`:
#         * `outline`:
#         """
#         if len(self._items) == 1:
#             self.master.itemconfigure(
#                 self._items[0], fill=fill, outline=outline)
#         else:
#             start = (len(self._items) - 1) // 2
#             end = start + 2 * (start // 3)
#             if fill is not None:
#                 for item in self._items[:start]:
#                     self.master.itemconfigure(item, fill=fill)
#             if outline is not None:
#                 for item in self._items[start:end]:
#                     self.master.itemconfigure(item, fill=outline)
#                 for item in self._items[end:]:
#                     self.master.itemconfigure(item, outline=outline)
