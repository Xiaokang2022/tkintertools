"""All standard `Shape` classes"""

from __future__ import annotations

__all__ = [
    "Line",
    "Rectangle",
    "Oval",
    "Arc",
    "RegularPolygon",
    "RoundedRectangle",
    "HalfRoundedRectangle",
    "SemicircularRectangle",
    "SharpRectangle",
    "Parallelogram",
]

import math
import typing
import warnings

import typing_extensions

from ..core import virtual


class Line(virtual.Shape):
    """Create a line for a widget"""

    def __init__(
        self,
        widget: virtual.Widget,
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        points: list[tuple[float, float]] | None = None,
        name: str | None = None,
        gradient_animation: bool = True,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of element
        * `points`: key points of line
        * `name`: name of element
        * `gradient_animation`: Wether use animation to change color
        * `kwargs`: extra parameters for CanvasItem
        """
        self.points = [] if points is None else points
        virtual.Shape.__init__(
            self, widget, relative_position, size,
            name=name, gradient_animation=gradient_animation, **kwargs)

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [self.widget.master.create_line(
            0, 0, 0, 0, tags=("fill", "fill"), **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        points = [(x+self.position[0], y+self.position[1]) for x, y in self.points]

        self.widget.master.coords(self.items[0], *points)


class Rectangle(virtual.Shape):
    """Create a rectangle for a widget"""

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [self.widget.master.create_rectangle(
            0, 0, 0, 0, tags=("fill", "fill", "outline", "outline"), **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        self.widget.master.coords(self.items[0], *self.region())


class Oval(virtual.Shape):
    """Create a oval for a widget"""

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [self.widget.master.create_oval(
            0, 0, 0, 0, tags=("fill", "fill", "outline", "outline"), **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        self.widget.master.coords(self.items[0], *self.region())

    @typing_extensions.override
    def detect(self, x: int, y: int) -> bool:
        """Detect whether the specified coordinates are within `Element`"""
        x1, y1, w, h = *self.position, *self.size
        return math.hypot(2*(x-x1)/w - 1, 2*(y-y1)/h - 1) <= 1


class Arc(virtual.Shape):
    """Create a arc for a widget"""

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [self.widget.master.create_arc(
            0, 0, 0, 0, tags=("fill", "fill", "outline", "outline"), **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        self.widget.master.coords(self.items[0], *self.region())


class RegularPolygon(virtual.Shape):
    """Create a regular polygon for a widget"""

    def __init__(
        self,
        widget: virtual.Widget,
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        side: int = 3,
        angle: float = 0,
        name: str | None = None,
        gradient_animation: bool = True,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of element
        * `side`: number of sides of a regular polygon
        * `angle`: number of radians of a regular polygon rotated clockwise
        * `name`: name of element
        * `gradient_animation`: Wether use animation to change color
        * `kwargs`: extra parameters for CanvasItem
        """
        self.side = side
        self.angle = angle
        virtual.Shape.__init__(
            self, widget, relative_position, size,
            name=name, gradient_animation=gradient_animation, **kwargs)

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [self.widget.master.create_polygon(
            0, 0, 0, 0, tags=("fill", "fill", "outline", "outline"), **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        r = min(self.size) / 2
        if self.side < 3:
            warnings.warn("Parameters are not suitable", UserWarning, 5)
        points = []
        for i in range(self.side):
            angle = math.tau*i/self.side+self.angle
            points.append(math.cos(angle)*r + self.position[0] + self.size[0]/2)
            points.append(math.sin(angle)*r + self.position[1] + self.size[1]/2)

        self.widget.master.coords(self.items[0], *points)


class RoundedRectangle(virtual.Shape):
    """Create a rounded rectangle for a widget"""

    def __init__(
        self,
        widget: virtual.Widget,
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        radius: int = 5,
        name: str | None = None,
        gradient_animation: bool = True,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of element
        * `radius`: radius of the fillet
        * `name`: name of element
        * `gradient_animation`: Wether use animation to change color
        * `kwargs`: extra parameters for CanvasItem
        """
        self.radius = radius
        virtual.Shape.__init__(
            self, widget, relative_position, size,
            name=name, gradient_animation=gradient_animation, **kwargs)

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [
            self.widget.master.create_rectangle(
                0, 0, 0, 0, outline="", tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_rectangle(
                0, 0, 0, 0, outline="", tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_line(  # n
                0, 0, 0, 0, tags=("fill", "outline"), **self.kwargs),
            self.widget.master.create_line(  # s
                0, 0, 0, 0, tags=("fill", "outline"), **self.kwargs),
            self.widget.master.create_line(  # w
                0, 0, 0, 0, tags=("fill", "outline"), **self.kwargs),
            self.widget.master.create_line(  # e
                0, 0, 0, 0, tags=("fill", "outline"), **self.kwargs),
            self.widget.master.create_arc(  # nw
                0, 0, 0, 0, outline="", start=90, tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_arc(  # sw
                0, 0, 0, 0, outline="", start=180, tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_arc(  # ne
                0, 0, 0, 0, outline="", start=0, tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_arc(  # se
                0, 0, 0, 0, outline="", start=-90, tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_arc(  # nw
                0, 0, 0, 0, style="arc", start=90, tags=("outline", "outline"), **self.kwargs),
            self.widget.master.create_arc(  # sw
                0, 0, 0, 0, style="arc", start=180, tags=("outline", "outline"), **self.kwargs),
            self.widget.master.create_arc(  # ne
                0, 0, 0, 0, style="arc", start=0, tags=("outline", "outline"), **self.kwargs),
            self.widget.master.create_arc(  # se
                0, 0, 0, 0, style="arc", start=-90, tags=("outline", "outline"), **self.kwargs),
        ]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        x, y, w, h = *self.position, *self.size
        x1, y1, x2, y2 = x, y, x + w, y + h
        r, d = self.radius, self.radius*2

        if d > w or d > h:
            warnings.warn("Parameters are not suitable", UserWarning, 5)
        elif d == 0:
            warnings.warn("Parameters are not suitable", UserWarning, 5)
        elif w < d < h or w < d < h:
            warnings.warn("Parameters are not suitable", UserWarning, 5)

        self.widget.master.coords(self.items[0], x1, y1+r, x2, y2-r+1)
        self.widget.master.coords(self.items[1], x1+r, y1, x2-r+1, y2)
        self.widget.master.coords(self.items[2], x1+r, y1, x2-r+1, y1)  # n
        self.widget.master.coords(self.items[3], x1+r, y2, x2-r+1, y2)  # s
        self.widget.master.coords(self.items[4], x1, y1+r, x1, y2-r+1)  # w
        self.widget.master.coords(self.items[5], x2, y1+r, x2, y2-r+1)  # e
        self.widget.master.coords(self.items[6], x1, y1, x1+d, y1+d)  # nw
        self.widget.master.coords(self.items[7], x1, y2-d, x1+d, y2)  # sw
        self.widget.master.coords(self.items[8], x2-d, y1, x2, y1+d)  # ne
        self.widget.master.coords(self.items[9], x2-d, y2-d, x2, y2)  # se
        self.widget.master.coords(self.items[10], x1, y1, x1+d, y1+d)  # nw
        self.widget.master.coords(self.items[11], x1, y2-d, x1+d, y2)  # sw
        self.widget.master.coords(self.items[12], x2-d, y1, x2, y1+d)  # ne
        self.widget.master.coords(self.items[13], x2-d, y2-d, x2, y2)  # se


class HalfRoundedRectangle(virtual.Shape):
    """Create a half rounded rectangle for a widget"""

    def __init__(
        self,
        widget: virtual.Widget,
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        radius: int = 5,
        ignore: typing.Literal["left", "right"] = "left",
        name: str | None = None,
        gradient_animation: bool = True,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of element
        * `radius`: radius of the fillet
        * `ignore`: edges to ignore
        * `name`: name of element
        * `gradient_animation`: Wether use animation to change color
        * `kwargs`: extra parameters for CanvasItem
        """
        self.radius = radius
        self.ignore = ignore
        virtual.Shape.__init__(
            self, widget, relative_position, size,
            name=name, gradient_animation=gradient_animation, **kwargs)

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [
            self.widget.master.create_rectangle(
                0, 0, 0, 0, outline="", tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_rectangle(
                0, 0, 0, 0, outline="", tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_line(  # n
                0, 0, 0, 0, tags=("fill", "outline"), **self.kwargs),
            self.widget.master.create_line(  # s
                0, 0, 0, 0, tags=("fill", "outline"), **self.kwargs),
            self.widget.master.create_line(  # w
                0, 0, 0, 0, tags=("fill", "outline"), **self.kwargs),
            self.widget.master.create_line(  # e
                0, 0, 0, 0, tags=("fill", "outline"), **self.kwargs),
        ]
        self.items += [
            self.widget.master.create_arc(  # ne
                0, 0, 0, 0, outline="", start=0, tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_arc(  # se
                0, 0, 0, 0, outline="", start=-90, tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_arc(  # ne
                0, 0, 0, 0, style="arc", start=0, tags=("outline", "outline"), **self.kwargs),
            self.widget.master.create_arc(  # se
                0, 0, 0, 0, style="arc", start=-90, tags=("outline", "outline"), **self.kwargs),
        ] if self.ignore == "left" else [
            self.widget.master.create_arc(  # nw
                0, 0, 0, 0, outline="", start=90, tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_arc(  # sw
                0, 0, 0, 0, outline="", start=180, tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_arc(  # nw
                0, 0, 0, 0, style="arc", start=90, tags=("outline", "outline"), **self.kwargs),
            self.widget.master.create_arc(  # sw
                0, 0, 0, 0, style="arc", start=180, tags=("outline", "outline"), **self.kwargs),
        ]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        x, y, w, h = *self.position, *self.size
        x1, y1, x2, y2 = x, y, x + w, y + h
        r, d = self.radius, self.radius*2

        if d > w or d > h:
            warnings.warn("Parameters are not suitable", UserWarning, 5)
        elif d == 0:
            warnings.warn("Parameters are not suitable", UserWarning, 5)
        elif w < d < h or w < d < h:
            warnings.warn("Parameters are not suitable", UserWarning, 5)

        a = self.ignore != "left"
        b = not a

        self.widget.master.coords(self.items[0], x1, y1+r, x2, y2-r+1)
        self.widget.master.coords(self.items[1], x1+r*a, y1, x2-r*b+1, y2)
        self.widget.master.coords(self.items[2], x1+r*a, y1, x2-r*b+1, y1)  # n
        self.widget.master.coords(self.items[3], x1+r*a, y2, x2-r*b+1, y2)  # s
        self.widget.master.coords(self.items[4], x1, y1+r*a, x1, y2-r*a+1)  # w
        self.widget.master.coords(self.items[5], x2, y1+r*b, x2, y2-r*b+1)  # e

        if self.ignore == "left":
            self.widget.master.coords(self.items[6], x2-d, y1, x2, y1+d)  # ne
            self.widget.master.coords(self.items[7], x2-d, y2-d, x2, y2)  # se
            self.widget.master.coords(self.items[8], x2-d, y1, x2, y1+d)  # ne
            self.widget.master.coords(self.items[9], x2-d, y2-d, x2, y2)  # se
        else:
            self.widget.master.coords(self.items[6], x1, y1, x1+d, y1+d)  # nw
            self.widget.master.coords(self.items[7], x1, y2-d, x1+d, y2)  # sw
            self.widget.master.coords(self.items[8], x1, y1, x1+d, y1+d)  # nw
            self.widget.master.coords(self.items[9], x1, y2-d, x1+d, y2)  # sw


class SemicircularRectangle(virtual.Shape):
    """Create a semicircular rectangle for a widget"""

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [
            self.widget.master.create_arc(
                0, 0, 0, 0, outline="", extent=180, start=90,
                tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_arc(
                0, 0, 0, 0, outline="", extent=180, start=-90,
                tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_rectangle(
                0, 0, 0, 0, outline="", tags=("fill", "fill"), **self.kwargs),
            self.widget.master.create_arc(
                0, 0, 0, 0, style="arc", extent=180, start=90,
                tags=("outline", "outline"), **self.kwargs),
            self.widget.master.create_arc(
                0, 0, 0, 0, style="arc", extent=180, start=-90,
                tags=("outline", "outline"), **self.kwargs),
            self.widget.master.create_line(
                0, 0, 0, 0, tags=("fill", "outline"), **self.kwargs),
            self.widget.master.create_line(
                0, 0, 0, 0, tags=("fill", "outline"), **self.kwargs),
        ]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        x, y, w, h = *self.position, *self.size
        x1, y1, x2, y2 = x, y, x + w, y + h
        d = h
        r = d/2

        if d < 0:
            warnings.warn("Parameters are not suitable", UserWarning, 5)
        elif d == 0:
            warnings.warn("Parameters are not suitable", UserWarning, 5)

        self.widget.master.coords(self.items[0], x1, y1, x1+d, y1+d)
        self.widget.master.coords(self.items[1], x2-d, y1, x2, y1+d)
        self.widget.master.coords(self.items[2], x1+r, y1, x2-r+1, y2)
        self.widget.master.coords(self.items[3], x1, y1, x1+d, y1+d)
        self.widget.master.coords(self.items[4], x2-d, y2-d, x2, y2)
        self.widget.master.coords(self.items[5], x1+r, y1, x2-r+1, y1)
        self.widget.master.coords(self.items[6], x1+r, y2, x2-r+1, y2)

    @typing_extensions.override
    def detect(self, x: int, y: int) -> bool:
        """Detect whether the specified coordinates are within `Element`"""
        x1, y1, w, h = *self.position, *self.size
        r = h / 2
        if x1+r <= x <= x1+w-r:
            return y1 <= y <= y1+h
        if x1 <= x <= x1 + r:
            return math.hypot(x - (x1+r), y - (y1+r)) <= r
        return math.hypot(x - (x1+w-r), y - (y1+r)) <= r


class SharpRectangle(virtual.Shape):
    """Create a sharp rectangle for a widget"""

    def __init__(
        self,
        widget: virtual.Widget,
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        theta: float = math.pi/6,
        ratio: tuple[float, float] = (0.5, 0.5),
        name: str | None = None,
        gradient_animation: bool = True,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of element
        * `theta`: number of radians of sharp corners
        * `ratio`: height ratio of the left and right sharp corners
        * `name`: name of element
        * `gradient_animation`: Wether use animation to change color
        * `kwargs`: extra parameters for CanvasItem
        """
        self.theta = theta
        self.ratio = ratio
        if not 0 <= theta <= math.pi/3:
            warnings.warn("Parameters are not suitable", UserWarning, 5)
        if math.isclose(abs(self.ratio[0] - self.ratio[1]), 1):
            warnings.warn("Parameters are not suitable", UserWarning, 5)
        virtual.Shape.__init__(
            self, widget, relative_position, size,
            name=name, gradient_animation=gradient_animation, **kwargs)

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [self.widget.master.create_polygon(
            0, 0, 0, 0, tags=("fill", "fill", "outline", "outline"), **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        x, y, w, h = *self.position, *self.size

        if w < h:
            warnings.warn("Parameters are not suitable", UserWarning, 5)

        dy = [h*value for value in self.ratio]
        dx = [math.tan(self.theta)*y for y in dy]

        if sum(dx) > w:
            warnings.warn("Parameters are not suitable", UserWarning, 5)

        x1, y1, x2, y2 = x, y, x + w, y + h

        points = [
            x1, y1+dy[0],
            x1+dx[0], y1,
            x2-dx[1], y1,
            x2, y2-dy[1],
            x2-dx[1], y2,
            x1+dx[0], y2
        ]
        self.widget.master.coords(self.items[0], *points)


class Parallelogram(virtual.Shape):
    """Create a parallelogram for a widget"""

    def __init__(
        self,
        widget: virtual.Widget,
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        theta: float = math.pi/6,
        name: str | None = None,
        gradient_animation: bool = True,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of element
        * `theta`: number of radians that the parallelogram is inclined to
        * `name`: name of element
        * `gradient_animation`: Wether use animation to change color
        * `kwargs`: extra parameters for CanvasItem
        """
        self.theta = theta
        if not abs(theta) <= math.pi/3:
            warnings.warn("Parameters are not suitable", UserWarning, 5)
        virtual.Shape.__init__(
            self, widget, relative_position, size,
            name=name, gradient_animation=gradient_animation, **kwargs)

    @typing_extensions.override
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""
        self.items = [self.widget.master.create_polygon(
            0, 0, 0, 0, tags=("fill", "fill", "outline", "outline"), **self.kwargs)]

    @typing_extensions.override
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        super().coords(size, position)

        x, y, w, h = *self.position, *self.size

        if (dx := h*math.tan(self.theta)) >= w:
            warnings.warn("Parameters are not suitable", UserWarning, 5)

        x1, y1, x2, y2 = x, y, x + w, y + h

        points = [
            x1+dx, y1,
            x2, y1,
            x2-dx, y2,
            x1, y2
        ]

        self.widget.master.coords(self.items[0], *points)
