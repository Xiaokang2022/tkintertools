"""All standard Shapes"""

import math

from .. import _tools, core


class NoShape(core.Shape):
    """"""

    def display(self) -> None:
        pass


class Rectangle(core.Shape):
    """"""

    def display(self) -> None:
        self.items = [self.widget.master.create_rectangle(
            *self.region(), width=2, tags="all")]


class Oval(core.Shape):
    """"""

    def display(self) -> None:
        self.items = [self.widget.master.create_oval(
            *self.region(), tags="all")]


class RegularPolygon(core.Shape):
    """"""

    def __init__(
        self,
        *,
        styles: core.Style | None = None,
        side: int = 3,
        angle: float = 0,
    ) -> None:
        core.Shape.__init__(self, styles=styles)
        self.side = side
        self.angle = angle

    def display(self) -> None:
        if self.side < 3 or self.widget.size // 2 < 1:
            raise ValueError
        points = []
        for i in range(self.side):
            angle = math.tau*i/self.side+self.angle
            points.append(
                math.cos(angle)*self.radius+self.widget.position[0]+self.widget.position[0]/2)
            points.append(
                math.sin(angle)*self.radius+self.widget.position[1]+self.widget.position[1]/2)

        self.items = [self.widget.master.create_polygon(*points, tags="all")]


class RoundedRectangle(core.Shape):
    """"""

    def __init__(
        self,
        *,
        styles: core.Style | None = None,
        radius: int = 5,
    ) -> None:
        core.Shape.__init__(self, styles=styles)
        self.radius = radius

    def display(self) -> None:
        """"""
        x, y, w, h = *self.widget.position, *self.widget.size
        x1, y1, x2, y2 = x, y, x + w, y + h
        r, d = self.radius, self.radius*2

        if d > w or d > h:
            _tools.warning("选择 `Shapes.Oval` 会更好")
            raise ValueError
        elif d == 0:
            _tools.info("选择 `Shapes.Rectangle` 会更好")
        elif w < d < h or w < d < h:
            _tools.warning("选择 `Shapes.SemicircularRectangle` 会更好")
            raise ValueError

        self.items = [
            self.widget.master.create_arc(
                x1, y1, x1+d, y1+d, outline="", start=90, tags="in"),
            self.widget.master.create_arc(
                x2-d, y1, x2, y1+d, outline="", start=0, tags="in"),
            self.widget.master.create_arc(
                x1, y2-d, x1+d, y2, outline="", start=180, tags="in"),
            self.widget.master.create_arc(
                x2-d, y2-d, x2, y2, outline="", start=-90, tags="in"),
            self.widget.master.create_rectangle(
                x1+r, y1, x2-r, y2, outline="", tags="in"),
            self.widget.master.create_rectangle(
                x1, y1+r, x2, y2-r, outline="", tags="in"),
            self.widget.master.create_line(
                x1+r, y1, x2-r, y1, width=2, tags="out_line"),
            self.widget.master.create_line(
                x1+r, y2, x2-r, y2, width=2, tags="out_line"),
            self.widget.master.create_line(
                x1, y1+r, x1, y2-r, width=2, tags="out_line"),
            self.widget.master.create_line(
                x2, y1+r, x2, y2-r, width=2, tags="out_line"),
            self.widget.master.create_arc(
                x1, y1, x1+d, y1+d, width=2, style="arc", start=90, tags="out_arc"),
            self.widget.master.create_arc(
                x2-d, y1, x2, y1+d, width=2, style="arc", start=0, tags="out_arc"),
            self.widget.master.create_arc(
                x1, y2-d, x1+d, y2, width=2, style="arc", start=180, tags="out_arc"),
            self.widget.master.create_arc(
                x2-d, y2-d, x2, y2, width=2, style="arc", start=-90, tags="out_arc"),
        ]


class SemicircularRectangle(core.Shape):
    """"""

    def display(self) -> None:
        """"""
        x, y, w, h = *self.widget.position, *self.widget.size
        x1, y1, x2, y2 = x, y, x + w, y + h
        d = w - h
        r = d/2

        if d < 0:
            raise ValueError
        elif d == 0:
            _tools.info("shapes.Rectangle")

        self.items = [
            self.widget.master.create_arc(
                x1, y1, x1+d, y1+d, outline="", extent=180, start=90, tags="in"),
            self.widget.master.create_arc(
                x2-d, y1, x2, y1+d, outline="", extent=180, start=-90, tags="in"),
            self.widget.master.create_rectangle(
                x1+r, y1, x2-r, y2, outline="", tags="in"),
            self.widget.master.create_arc(
                x1, y1, x1+d, y1+d, style="arc", extent=180, start=90, tags="out_arc"),
            self.widget.master.create_arc(
                x2-d, y2-d, x2, y2, style="arc", extent=180, start=-90, tags="out_arc"),
            self.widget.master.create_rectangle(
                x1+r, y1, x2-r, y2, tags="out"),
            self.widget.master.create_rectangle(
                x1+r, y2, x2-r, y2, tags="out"),
        ]


class SharpRectangle(core.Shape):
    """"""

    def __init__(
        self,
        *,
        styles: core.Style | None = None,
        theta: float = math.pi/6,
        ratio: tuple[float, float] = (0.5, 0.5),
    ) -> None:
        core.Shape.__init__(self, styles=styles)
        self.theta = theta
        self.ratio = ratio
        if not 0 <= theta <= math.pi/3:
            raise ValueError
        if math.isclose(abs(self.ratio[0] - self.ratio[1]), 1):
            _tools.info("Parallelogram")

    def display(self) -> None:
        """"""
        x, y, w, h = *self.widget.position, *self.widget.size

        if w < h:
            raise ValueError

        dy = [h*value for value in self.ratio]
        dx = [math.tan(self.theta)*y for y in dy]

        if sum(dx) > w:
            raise RuntimeError

        x1, y1, x2, y2 = x, y, x + w, y + h

        points = [
            x1, y1+dy[0],
            x1+dx[0], y1,
            x2-dx[1], y1,
            x2, y2-dy[1],
            x2-dx[1], y2,
            x1+dx[0], y2
        ]

        self.items = [self.widget.master.create_polygon(*points, tags="all")]


class Parallelogram(core.Shape):
    """"""

    def __init__(
        self,
        *,
        styles: core.Style | None = None,
        theta: float = math.pi/6,
    ) -> None:
        core.Shape.__init__(self, styles=styles)
        self.theta = theta
        if not 0 <= theta <= math.pi/3:
            raise ValueError

    def display(self) -> None:
        """"""
        x, y, w, h = *self.widget.position, *self.widget.size

        if (dx := h*math.tan(self.theta)) >= w:
            raise RuntimeError

        x1, y1, x2, y2 = x, y, x + w, y + h

        points = [
            x1+dx, y1,
            x2, y1,
            x2-dx, y2,
            x1, y2
        ]

        self.items = [self.widget.master.create_polygon(*points, tags="all")]


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
