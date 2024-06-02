"""
Various virtual classes

The virtual `Widget` consists of 4 parts, which are `Shape`, `Text`, `Image`, and `Feature`

where `Feature` is the function of widgets, and each widget can be bound to up to one,
but in terms of appearance, there is no limit to the number of `Shape`, `Text`, and `Image`

`Shape`, `Text`, and `Image` are all appearance components that inherit from abstract base class `Components`
"""

import abc
import copy
import math
import tkinter
import tkinter.font as font
import typing

from ..animation import animations
from ..color import rgb
from ..style import parser
from ..toolbox import enhanced
from . import constants, containers

__all__ = [
    "Feature",
    "Component",
    "Shape",
    "Text",
    "Image",
    "Widget",
]


class Feature(abc.ABC):
    """The features of a `Widget`"""

    def __init__(self, widget: "Widget") -> None:
        self.widget: Widget = widget
        widget.feature = self

    def _move_none(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of moving the mouse"""
        return False

    def _move_left(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of holding down the left mouse button to move the mouse"""
        return False

    def _move_center(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of holding down the center mouse button to move the mouse"""
        return False

    def _move_right(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of holding down the right mouse button to move the mouse"""
        return False

    def _click_left(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of pressing the left mouse button"""
        return False

    def _click_center(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of pressing the center mouse button"""
        return False

    def _click_right(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of pressing the right mouse button"""
        return False

    def _release_left(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of releasing the left mouse button"""
        return False

    def _release_center(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of releasing the center mouse button"""
        return False

    def _release_right(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of releasing the right mouse button"""
        return False

    def _wheel(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of scrolling the mouse wheel"""
        return False

    def _input(self, event: tkinter.Event) -> bool:
        """Internal Method: Event of typing"""
        return False


class Component(abc.ABC):
    """The basic part of a `Widget`"""

    def __init__(
        self,
        widget: "Widget",
        rel_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
    ) -> None:
        self.widget: Widget = widget
        self.x = rel_position[0] + widget.x
        self.y = rel_position[1] + widget.y
        self.w, self.h = size if size else (widget.w, widget.h)
        self.name: str | None = name
        self.styles = styles if styles else parser.get(widget, self)
        self.items: list[int] = []
        self.visible: bool = True
        self.animation = animation
        widget.register(self)

    def move(self, dx: float, dy: float) -> None:
        """Move the `Component`"""
        self.x += dx
        self.y += dy
        for item in self.items:
            self.widget.master.move(item, dx, dy)

    def moveto(self, x: float, y: float) -> None:
        """Move the `Component` to a certain position"""
        return self.move(x - self.x, y - self.y)

    def destroy(self) -> None:
        """Destroy the `Component`"""
        self.widget.master.delete(*self.items)

    def center(self) -> tuple[int, int]:
        """Return the geometric center of the `Component`"""
        return self.x + self.w/2, self.y + self.h/2

    def region(self) -> tuple[int, int, int, int]:
        """Return the decision region of the `Component`"""
        return self.x, self.y, self.x + self.w, self.y + self.h

    def detect(self, x: int, y: int) -> bool:
        """Detect whether the specified coordinates are within the `Component`"""
        x1, y1, x2, y2 = self.region()
        return x1 <= x <= x2 and y1 <= y <= y2

    def update(self, state: str | None = None, *, no_delay: bool = False) -> None:
        """
        Update the style of the `Component` to the corresponding state

        * `state`: the state of the `Component`
        """
        if state is None:
            state = self.widget.state
        if not self.visible:
            return
        if self.styles.get(state) is not None:
            self.configure(self.styles[state], no_delay=no_delay)

    def _get_disabled_style(self, refer_state: str = "normal") -> dict[str, str]:
        """"""
        if self.styles.get("disabled") is None:
            self.styles["disabled"] = copy.deepcopy(
                self.styles.get(refer_state, {}))
            for key, value in self.styles["disabled"].items():
                self.styles["disabled"][key] = rgb.rgb_to_str(rgb.convert(
                    rgb.str_to_rgb(value), rgb.str_to_rgb(self.widget.master["bg"]), 0.618))
        return self.styles["disabled"]

    def configure(self, style: dict[str, str], *, no_delay: bool = False) -> None:
        """Configure properties of the `Component` and update them immediately"""
        for item in self.items:
            tags = self.widget.master.itemcget(item, "tags").split()
            kwargs = {key: value for key, param in zip(
                tags[0:-1:2], tags[1:len(tags):2]) if (value := style.get(param)) is not None}
            if self.widget.animation and self.animation and not no_delay:
                for key, value in kwargs.items():
                    start_color: str = self.widget.master.itemcget(item, key)
                    if start_color.startswith("#") and len(start_color) == 9:
                        start_color = rgb.rgb_to_str(rgb._str_to_rgba(
                            start_color, reference=self.widget.master["bg"]))
                    if value.startswith("#") and len(value) == 9:
                        value = rgb.rgb_to_str(rgb._str_to_rgba(
                            value, reference=self.widget.master["bg"]))
                    if value == "" or start_color == "":  # Null characters cannot be parsed
                        self.widget.master.itemconfigure(item, **{key: value})
                    else:
                        animations.Gradient(
                            self.widget.master, item, key, 150, (start_color, value)).start()
            else:
                for key, value in kwargs.items():
                    if value.startswith("#") and len(value) == 9:
                        kwargs[key] = rgb.rgb_to_str(rgb._str_to_rgba(
                            value, reference=self.widget.master["bg"]))
                self.widget.master.itemconfigure(item, **kwargs)

    def appear(self, *, no_delay: bool = True) -> None:
        """"""
        self.visible = True
        self.update(self.widget.state, no_delay=no_delay)

    def disappear(self, *, no_delay: bool = True) -> None:
        """"""
        self.visible = False
        temp_style = copy.deepcopy(self.styles.get(self.widget.state))
        if temp_style is None:
            return
        for arg in temp_style:
            temp_style[arg] = ""
        self.configure(temp_style, no_delay=no_delay)

    def __getitem__(self, key: str) -> dict[str, str]:
        """"""
        return self.styles[key]

    def __setitem__(self, key: str, value: dict[str, str]) -> None:
        """"""
        self.styles[key].update(value)
        self.update(no_delay=True)

    @abc.abstractmethod
    def zoom(self, ratio: tuple[float, float]) -> None:
        """Scale the `Component`"""

    @abc.abstractmethod
    def display(self) -> None:
        """Display the `Component` on a `Canvas`"""


class Shape(Component):
    """Base Class: The Shape of a `Widget`"""

    # @typing.override
    def zoom(self, ratio: tuple[float, float]) -> None:
        """Scale the items"""
        for item in self.items:
            self.widget.master.scale(item, 0, 0, *ratio)


class Text(Component):
    """Base Class: The text of a `Widget`"""

    def __init__(
        self,
        widget: "Widget",
        rel_position: tuple[int, int] = (0, 0),
        *,
        styles: dict[str, dict[str, str]] | None = None,
        animation: bool = True,
        text: str = "",
        family: str | None = None,
        size: int | None = None,
        weight: typing.Literal["normal", "bold"] = "normal",
        slant: typing.Literal["roman", "italic"] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        limit: int = math.inf,
    ) -> None:
        """
        * `text`: the value of `Text`
        * `limit`: the limitation of value length
        """
        self.value: str = text
        self.limit: int = limit
        self.left: int = 0
        self.right: int = 0
        self.font: font.Font = font.Font(
            family=family if family else constants.FONT,
            size=-abs(size if size else constants.SIZE),
            weight=weight, slant=slant,
            underline=underline, overstrike=overstrike)
        Component.__init__(self, widget, rel_position,
                           styles=styles, animation=animation)

    def region(self) -> tuple[int, int, int, int]:
        """Return the decision region of the `Text`"""
        width_half = self.font.measure(self.value)/2
        height_half = -self.font.cget("size") / 2
        x, y = self.center()
        return x-width_half, y-height_half, x+width_half, y+height_half

    # @typing.override
    def zoom(self, ratio: tuple[float, float]) -> None:
        """Scale the text"""
        for item in self.items:
            value = self.widget.master._texts[item]
            value[0] *= math.sqrt(ratio[0]*ratio[1])
            value[1].config(size=round(value[0]))
            self.widget.master.itemconfigure(item, font=value[1])
            self.widget.master.scale(item, 0, 0, *ratio)


class Image(Component):
    """Base Class: an image of a `Widget`"""

    def __init__(
        self,
        widget: "Widget",
        rel_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
    ) -> None:
        """"""
        self.image = image
        Component.__init__(self, widget, rel_position, size,
                           name=name, animation=animation, styles=styles)

    # @typing.override
    def zoom(self, ratio: tuple[float, float]) -> None:
        """"""
        for item in self.items:
            self.widget.master.scale(item, 0, 0, *ratio)


class Widget:
    """
    Base Widget Class

    `Widget` = `Shape` + `Text` + `Image` + `Feature`
    """

    def __init__(
        self,
        master: "containers.Canvas",
        position: tuple[int, int],
        size: tuple[int, int],
        *,
        name: str | None = None,
        state: str = "normal",
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """"""
        self.master = master
        self.x, self.y = position
        self.w, self.h = size
        self.through = through
        self.animation = animation
        self.name = name

        self.texts: list[Text] = []
        self.shapes: list[Shape] = []
        self.images: list[Image] = []

        self.feature: Feature = None

        self.state: str = state
        self._before_disabled: str = ""

        master._widgets.append(self)

    def register(self, component: Component) -> None:
        """"""
        if isinstance(component, Shape):
            self.shapes.append(component)
        elif isinstance(component, Text):
            self.texts.append(component)
        elif isinstance(component, Image):
            self.images.append(component)
        component.display()
        component.update(no_delay=True)

    def zoom(self, ratio: tuple[float, float] | None = None) -> None:
        """Zoom self"""
        if ratio is None:
            ratio = self.master.ratios
        self.w *= ratio[0]
        self.h *= ratio[1]
        self.x *= ratio[0]
        self.y *= ratio[1]
        for elem in self.shapes + self.texts + self.images:
            elem.zoom(ratio)

    def update(self, state: str | None = None, *, no_delay: bool = False) -> None:
        """Update the widget"""
        if self._before_disabled:
            return
        if state is not None:
            self.state = state
        for elem in self.shapes + self.texts:
            elem.update(state, no_delay=no_delay)

    def move(self, dx: int, dy: int) -> None:
        """Move the widget"""
        self.x += dx
        self.y += dy
        for elem in self.shapes + self.texts + self.images:
            elem.move(dx, dy)

    def moveto(self, x: int, y: int) -> None:
        """Move the Widget to a certain position"""
        return self.move(x - self.x, y - self.y)

    def disabled(self, flag: bool = True) -> None:
        """"""
        if flag:
            if not self._before_disabled:
                self._before_disabled = self.state
            for elem in self.shapes + self.texts:
                elem._get_disabled_style(self._before_disabled)
            self._before_disabled, last_state = "", self._before_disabled  # Let theme to change
            self.update("disabled", no_delay=True)
            self._before_disabled = last_state
        else:
            self._before_disabled, last_state = "", self._before_disabled  # Unlock
            self.update(last_state, no_delay=True)

    def destroy(self) -> None:
        """Destroy the widget"""
        self.master._widgets.remove(self)
        for elem in self.shapes + self.texts + self.images:
            elem.destroy()

    def focus_set(self, *args) -> None:
        """"""
        self.master.focus(*args)

    def disappear(self) -> None:
        """"""
        for elem in self.shapes + self.texts:
            elem.disappear()

    def appear(self) -> None:
        """"""
        for elem in self.shapes + self.texts:
            elem.appear()
