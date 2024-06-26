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
    "Component",
    "Shape",
    "Text",
    "Image",
    "Feature",
    "Widget",
]


class Component(abc.ABC):
    """The basic part of a `Widget`"""

    def __init__(
        self,
        widget: "Widget",
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of component
        * `name`: name of component
        * `animation`: Wether use animation to change color
        * `styles`: style dict of component
        """
        self.widget = widget
        self.position = [widget.position[0] + relative_position[0],
                         widget.position[1] + relative_position[1]]
        self.size = widget.size.copy() if size is None else list(size)
        self.name = name
        self.animation = animation
        self.styles = styles if styles else parser.get(widget, self)

        self.items: list[int] = []
        self.gradient: animations.GradientItem | None = None
        self.visible: bool = True

        widget.register(self)

    def move(self, dx: float, dy: float) -> None:
        """Move the `Component`"""
        self.position[0] += dx
        self.position[1] += dy
        for item in self.items:
            self.widget.master.move(item, dx, dy)

    def moveto(self, x: float, y: float) -> None:
        """Move the `Component` to a certain position"""
        return self.move(x-self.position[0], y-self.position[1])

    def destroy(self) -> None:
        """Destroy the `Component`"""
        self.widget.deregister(self)
        self.widget.master.delete(*self.items)

    def center(self) -> tuple[int, int]:
        """Return the geometric center of the `Component`"""
        return self.position[0] + self.size[0]/2, self.position[1] + self.size[1]/2

    def region(self) -> tuple[int, int, int, int]:
        """Return the decision region of the `Component`"""
        return self.position[0], self.position[1], self.position[0]+self.size[0], self.position[1]+self.size[1]

    def detect(self, x: int, y: int) -> bool:
        """Detect whether the specified coordinates are within the `Component`"""
        x1, y1, x2, y2 = self.region()
        return x1 <= x <= x2 and y1 <= y <= y2

    def update(self, state: str | None = None, *, no_delay: bool = False) -> None:
        """
        Update the style of the `Component` to the corresponding state

        * `state`: the state of the `Component`
        """
        if not self.visible:
            return
        if state is None:
            state = self.widget.state
        if self.gradient is not None:
            self.gradient.stop()
            self.gradient = None
        if self.styles.get(state) is not None:
            self.configure(self.styles[state], no_delay=no_delay)

    def _get_disabled_style(self, refer_state: str | None = None) -> dict[str, str]:
        """Get the style data of disabled state"""
        if refer_state is None:
            refer_state = self.widget.state
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
                        self.gradient = animations.GradientItem(
                            self.widget.master, item, key, 150, (start_color, value))
                        self.gradient.start()
            else:
                for key, value in kwargs.items():
                    if value.startswith("#") and len(value) == 9:
                        kwargs[key] = rgb.rgb_to_str(rgb._str_to_rgba(
                            value, reference=self.widget.master["bg"]))
                self.widget.master.itemconfigure(item, **kwargs)

    def appear(self, *, no_delay: bool = True) -> None:
        """Let the component to appear"""
        self.visible = True
        self.update(self.widget.state, no_delay=no_delay)

    def disappear(self, *, no_delay: bool = True) -> None:
        """Let the component to disappear"""
        self.visible = False
        temp_style = copy.deepcopy(self.styles.get(self.widget.state, None))
        if temp_style is None:
            return
        for arg in temp_style:
            temp_style[arg] = ""
        self.configure(temp_style, no_delay=no_delay)

    def __getitem__(self, key: str) -> dict[str, str]:
        """Easy to get style data"""
        return self.styles[key]

    def __setitem__(self, key: str, value: dict[str, str]) -> None:
        """Easy to set style data"""
        self.styles[key].update(value)
        self.update(no_delay=True)

    @abc.abstractmethod
    def zoom(self, ratios: tuple[float, float]) -> None:
        """Zoom the `Component`"""

    @abc.abstractmethod
    def display(self) -> None:
        """Display the `Component` on a `Canvas`"""


class Shape(Component):
    """The Shape of a `Widget`"""

    # @typing.override
    def zoom(self, ratios: tuple[float, float]) -> None:
        """Scale the items"""
        for item in self.items:
            self.widget.master.scale(item, 0, 0, *ratios)


class Text(Component):
    """The Text of a `Widget`"""

    def __init__(
        self,
        widget: "Widget",
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        text: str = "",
        limit: int = math.inf,
        show: str | None = None,
        anchor: typing.Literal["n", "e", "w", "s",
                               "nw", "ne", "sw", "se"] = "center",
        justify: typing.Literal["left", "center", "right"] = "left",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal["normal", "bold"] = "normal",
        slant: typing.Literal["roman", "italic"] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of component
        * `text`: text value
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the font
        * `slant`: slant of the font
        * `underline`: wether text is underline
        * `overstrike`: wether text is overstrike
        * `justify`: justify of the text
        * `anchor`: anchor of the text
        * `limit`: limit on the number of characters
        * `show`: display a value that obscures the original content
        * `name`: name of component
        * `animation`: Wether use animation to change color
        * `styles`: style dict of component
        """
        self.value = text
        self.show = show
        self.limit = limit
        self.anchor = anchor
        self.justify = justify
        self.font = font.Font(
            family=family if family else constants.FONT,
            size=-abs(fontsize if fontsize else constants.SIZE),
            weight=weight, slant=slant,
            underline=underline, overstrike=overstrike)
        self.left: int = 0
        self.right: int = 0
        Component.__init__(self, widget, relative_position, size=size,
                           name=name, styles=styles, animation=animation)

    def region(self) -> tuple[int, int, int, int]:
        """Return the decision region of the `Text`"""
        return self.widget.master.bbox(self.items[0])

    # @typing.override
    def zoom(self, ratios: tuple[float, float]) -> None:
        """Scale the text"""
        for item in self.items:
            value = self.widget.master._texts[item]
            value[0] *= math.sqrt(ratios[0]*ratios[1])
            value[1].config(size=round(value[0]))
            self.widget.master.itemconfigure(item, font=value[1])
            self.widget.master.scale(item, 0, 0, *ratios)


class Image(Component):
    """The Image of a `Widget`"""

    def __init__(
        self,
        widget: "Widget",
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of component
        * `image`: image object of the component
        * `name`: name of component
        * `animation`: Wether use animation to change color
        * `styles`: style dict of component
        """
        self.image = image
        Component.__init__(self, widget, relative_position,
                           size, name=name, animation=animation, styles=styles)

    # @typing.override
    def zoom(self, ratios: tuple[float, float]) -> None:
        """"""
        for item in self.items:
            self.widget.master.scale(item, 0, 0, *ratios)


class Feature(abc.ABC):
    """The features of a `Widget`"""

    def __init__(self, widget: "Widget") -> None:
        self.widget = widget
        widget._feature = self

    def _move_none(self, event: tkinter.Event) -> bool:
        """Event of moving the mouse"""
        return False

    def _move_left(self, event: tkinter.Event) -> bool:
        """Event of holding down the left mouse button to move the mouse"""
        return False

    def _move_center(self, event: tkinter.Event) -> bool:
        """Event of holding down the center mouse button to move the mouse"""
        return False

    def _move_right(self, event: tkinter.Event) -> bool:
        """Event of holding down the right mouse button to move the mouse"""
        return False

    def _click_left(self, event: tkinter.Event) -> bool:
        """Event of pressing the left mouse button"""
        return False

    def _click_center(self, event: tkinter.Event) -> bool:
        """Event of pressing the center mouse button"""
        return False

    def _click_right(self, event: tkinter.Event) -> bool:
        """Event of pressing the right mouse button"""
        return False

    def _release_left(self, event: tkinter.Event) -> bool:
        """Event of releasing the left mouse button"""
        return False

    def _release_center(self, event: tkinter.Event) -> bool:
        """Event of releasing the center mouse button"""
        return False

    def _release_right(self, event: tkinter.Event) -> bool:
        """Event of releasing the right mouse button"""
        return False

    def _wheel(self, event: tkinter.Event) -> bool:
        """Event of scrolling the mouse wheel"""
        return False

    def _input(self, event: tkinter.Event) -> bool:
        """Event of typing"""
        return False


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
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `name`: name of the widget
        * `state`: default state of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        self.master = master
        self.position = list(position)
        self.size = list(size)
        self.name = name
        self.state = state
        self.through = through
        self.animation = animation

        self._texts: list[Text] = []
        self._shapes: list[Shape] = []
        self._images: list[Image] = []
        self._feature: Feature = None
        self._state_before_disabled: str = ""

        master._widgets.append(self)

    @property
    def components(self) -> tuple[Component, ...]:
        """Return all components of the widget"""
        return tuple(self._shapes + self._texts + self._images)

    def register(self, component: Component) -> None:
        """Register a component to the widget"""
        if isinstance(component, Shape):
            self._shapes.append(component)
        elif isinstance(component, Text):
            self._texts.append(component)
        elif isinstance(component, Image):
            self._images.append(component)
        component.display()
        component.update(no_delay=True)

    def deregister(self, component: Component) -> None:
        """Deregister a component from the widget"""
        if isinstance(component, Shape):
            self._shapes.remove(component)
        elif isinstance(component, Text):
            self._texts.remove(component)
        elif isinstance(component, Image):
            self._images.remove(component)

    def update(self, state: str | None = None, *, no_delay: bool = False) -> None:
        """Update the widget"""
        if state != "disabled" and self._state_before_disabled:
            return  # It is currently disabled
        if state is not None:
            self.state = state
        for component in self.components:
            component.update(state, no_delay=no_delay)

    def disabled(self, value: bool = True) -> None:
        """Disable the widget"""
        if value:
            if not self._state_before_disabled:
                self._state_before_disabled = self.state
            for component in self.components:
                component._get_disabled_style(self._state_before_disabled)
            self.update("disabled", no_delay=True)
        else:
            self._state_before_disabled, last_state = "", self._state_before_disabled
            self.update(last_state, no_delay=True)

    def move(self, dx: int, dy: int) -> None:
        """Move the widget"""
        self.position[0] += dx
        self.position[1] += dy
        for component in self.components:
            component.move(dx, dy)

    def moveto(self, x: int, y: int) -> None:
        """Move the Widget to a certain position"""
        return self.move(x-self.position[0], y-self.position[1])

    def destroy(self) -> None:
        """Destroy the widget"""
        self.master._widgets.remove(self)
        for component in self.components:
            component.destroy()

    def zoom(self, ratios: tuple[float, float] | None = None) -> None:
        """Zoom self"""
        if ratios is None:
            ratios = self.master.ratios
        self.size[0] *= ratios[0]
        self.size[1] *= ratios[1]
        self.position[0] *= ratios[0]
        self.position[1] *= ratios[1]
        for component in self.components:
            component.zoom(ratios)

    def disappear(self) -> None:
        """Let all components of the widget to disappear"""
        for component in self.components:
            component.disappear()

    def appear(self) -> None:
        """Let all components of the widget to appear"""
        for component in self.components:
            component.appear()
