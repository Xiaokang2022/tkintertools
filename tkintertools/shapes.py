"""All standard Shapes"""

import math

from . import _tools, core


class NoShape(core.Shape):
    """"""

    def display(self, master: core.Canvas, position: tuple[int, int], size: tuple[int, int]) -> None:
        self._master = master
        self._size = list(size)
        self._position = list(position)


class Rectangle(core.Shape):
    """"""


class Oval(core.Shape):
    """"""

    def display(self, master: core.Canvas, position: tuple[int, int], size: tuple[int, int]) -> None:
        self._master = master
        self._size = list(size)
        self._position = list(position)
        item = master.create_oval(*self.region(), tags=id(self))
        self._items_inside.append(item)
        self._items_outline.append(item)


class RegularPolygon(core.Shape):
    """"""

    def __init__(
        self,
        *,
        radius: int,
        side: int = 3,
        theta: float = 0,
    ) -> None:
        core.Shape.__init__(self)
        self.radius = radius
        self.side = side
        self.theta = theta

    def display(self, master: core.Canvas, position: tuple[int, int], size: tuple[int, int]) -> None:
        if self.side < 3 or self.radius < 1:
            raise ValueError
        self._master = master
        self._size = [self.radius*2]*2
        self._position = list(position)
        points = []
        for i in range(self.side):
            theta = math.tau*i/self.side+self.theta
            points.append(math.cos(theta)*self.radius+position[0]+size[0]/2)
            points.append(math.sin(theta)*self.radius+position[1]+size[1]/2)
        item = master.create_polygon(*points, tags=id(self))
        self._items_inside.append(item)
        self._items_outline.append(item)


class RoundedRectangle(core.Shape):
    """"""

    def __init__(
        self,
        *,
        radius: int = 5,
    ) -> None:
        core.Shape.__init__(self)
        self.radius = radius

    def display(self, master: core.Canvas, position: tuple[int, int], size: tuple[int, int]) -> None:
        """"""
        self._master = master
        self._size = list(size)
        self._position = list(position)

        x, y, w, h = *position, *size
        x1, y1, x2, y2 = x, y, x + w, y + h
        r, d = self.radius, self.radius*2

        if d > size[0] or d > size[1]:
            _tools._warning("选择 `Shapes.Oval` 会更好")
            raise ValueError
        elif d == 0:
            _tools._info("选择 `Shapes.Rectangle` 会更好")
        elif size[0] < d < size[1] or size[1] < d < size[0]:
            _tools._warning("选择 `Shapes.SemicircularRectangle` 会更好")
            raise ValueError

        self._items_inside = [
            master.create_arc(x1, y1, x1+d, y1+d, outline="", start=90),
            master.create_arc(x2-d, y1, x2, y1+d, outline="", start=0),
            master.create_arc(x1, y2-d, x1+d, y2, outline="", start=180),
            master.create_arc(x2-d, y2-d, x2, y2, outline="", start=-90),
            master.create_rectangle(x1+r, y1, x2-r, y2, outline=""),
            master.create_rectangle(x1, y1+r, x2, y2-r, outline="")
        ]
        self._items_outline = [
            master.create_arc(x1, y1, x1+d, y1+d, style="arc", start=90),
            master.create_arc(x2-d, y1, x2, y1+d, style="arc", start=0),
            master.create_arc(x1, y2-d, x1+d, y2, style="arc", start=180),
            master.create_arc(x2-d, y2-d, x2, y2, style="arc", start=-90),
            master.create_line(x1+r, y1, x2-r, y1),
            master.create_line(x1+r, y2, x2-r, y2),
            master.create_line(x1, y1+r, x1, y2-r),
            master.create_line(x2, y1+r, x2, y2-r)
        ]

    def configure(self, fill: str | None = None, outline: str | None = None) -> None:
        """"""
        if fill is not None:
            for item in self._items_inside:
                self._master.itemconfigure(item, fill=fill)
        if outline is not None:
            for item in self._items_outline[:4]:
                self._master.itemconfigure(item, outline=outline)
            for item in self._items_outline[4:]:
                self._master.itemconfigure(item, fill=outline)


class SemicircularRectangle(core.Shape):
    """"""

    def display(self, master: core.Canvas, position: tuple[int, int], size: tuple[int, int]) -> None:
        """"""
        self._master = master
        self._size = list(size)
        self._position = list(position)

        x, y, w, h = *position, *size
        x1, y1, x2, y2 = x, y, x + w, y + h
        d = size[0] - size[1]
        r = d/2

        if d < 0:
            raise ValueError
        elif d == 0:
            _tools._info("shapes.Rectangle")

        self._items_inside = [
            master.create_arc(x1, y1, x1+d, y1+d, outline="",
                              extent=180, start=90),
            master.create_arc(x2-d, y1, x2, y1+d, outline="",
                              extent=180, start=-90),
            master.create_rectangle(x1+r, y1, x2-r, y2, outline=""),
        ]
        self._items_outline = [
            master.create_arc(x1, y1, x1+d, y1+d, style="arc",
                              extent=180, start=90),
            master.create_arc(x2-d, y2-d, x2, y2, style="arc",
                              extent=180, start=-90),
            master.create_line(x1+r, y1, x2-r, y1),
            master.create_line(x1+r, y2, x2-r, y2)
        ]

    def configure(self, fill: str | None = None, outline: str | None = None) -> None:
        """"""
        if fill is not None:
            for item in self._items_inside:
                self._master.itemconfigure(item, fill=fill)
        if outline is not None:
            for item in self._items_outline[:2]:
                self._master.itemconfigure(item, outline=outline)
            for item in self._items_outline[2:]:
                self._master.itemconfigure(item, fill=outline)


class SharpRectangle(core.Shape):
    """"""

    def __init__(
        self,
        *,
        theta: float = math.pi/6,
        ratio: tuple[float, float] = (0.5, 0.5)
    ) -> None:
        core.Shape.__init__(self)
        self.theta = theta
        self.ratio = ratio
        if not 0 <= theta <= math.pi/3:
            raise ValueError
        if math.isclose(abs(self.ratio[0] - self.ratio[1]), 1):
            _tools._info("Parallelogram")

    def display(self, master: core.Canvas, position: tuple[int, int], size: tuple[int, int]) -> None:
        """"""
        self._master = master
        self._size = list(size)
        self._position = list(position)

        if size[0] < size[1]:
            raise ValueError

        dy = [size[1]*value for value in self.ratio]
        dx = [math.tan(self.theta)*y for y in dy]

        if sum(dx) > size[0]:
            raise RuntimeError

        x, y, w, h = *position, *size
        x1, y1, x2, y2 = x, y, x + w, y + h

        points = [
            x1, y1+dy[0],
            x1+dx[0], y1,
            x2-dx[1], y1,
            x2, y2-dy[1],
            x2-dx[1], y2,
            x1+dx[0], y2
        ]

        item = master.create_polygon(*points, tags=id(self))
        self._items_inside.append(item)
        self._items_outline.append(item)


class Parallelogram(core.Shape):
    """"""

    def __init__(
        self,
        *,
        theta: float = math.pi/6
    ) -> None:
        core.Shape.__init__(self)
        self.theta = theta
        if not 0 <= theta <= math.pi/3:
            raise ValueError

    def display(self, master: core.Canvas, position: tuple[int, int], size: tuple[int, int]) -> None:
        """"""
        self._master = master
        self._size = list(size)
        self._position = list(position)

        if (dx := size[1]*math.tan(self.theta)) >= size[0]:
            raise RuntimeError

        x, y, w, h = *position, *size
        x1, y1, x2, y2 = x, y, x + w, y + h

        points = [
            x1+dx, y1,
            x2, y1,
            x2-dx, y2,
            x1, y2
        ]

        item = master.create_polygon(*points, tags=id(self))
        self._items_inside.append(item)
        self._items_outline.append(item)


__all__ = [
    "NoShape",
    "Rectangle",
    "Oval",
    "RegularPolygon",
    "RoundedRectangle",
    "SemicircularRectangle",
    "SharpRectangle",
    "Parallelogram",
]
