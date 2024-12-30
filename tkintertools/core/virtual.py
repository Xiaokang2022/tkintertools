"""Various virtual classes

The virtual `Widget` consists of 5 parts, which are `Widget`, `Shape`, `Text`, `Image` and
`Feature`.

Where `Feature` is the function of widgets, and each widget can be bound to up to one, but in terms
of appearance, there is no limit to the number of `Shape`, `Text`, and `Image`.

`Shape`, `Text`, and `Image` are all appearance components that inherit from abstract base class
`Components`.
"""

from __future__ import annotations

__all__ = [
    "Element",
    "Shape",
    "Text",
    "Image",
    "Feature",
    "Widget",
]

import abc
import collections.abc
import copy
import math
import re
import tkinter
import tkinter.font
import traceback
import typing
import warnings

import typing_extensions

from ..animation import animations
from ..color import convert, rgb
from ..style import parser
from ..toolbox import enhanced
from . import configurations, containers


class Element(abc.ABC):
    """The basic visible part of a `Widget`."""

    def __init__(
        self,
        widget: Widget,
        position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        gradient_animation: bool = True,
        auto_update: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `position`: position relative to its widgets
        * `size`: size of element
        * `name`: name of element
        * `animation`: Wether use animation to change color
        * `styles`: style dict of element
        * `kwargs`: extra parameters for CanvasItem
        """
        self.widget = widget
        offset = widget.offset
        self.position: list[int | float] = [
            widget.position[0] + position[0] - offset[0],
            widget.position[1] + position[1] - offset[1]]
        self.size: list[int | float] = widget.size.copy() if size is None else list(size)
        self.name = self.__class__.__name__ if name is None else name
        self.gradient_animation = gradient_animation
        self.auto_update = auto_update
        self.styles = styles if styles else parser.get(widget, self)

        self.items: list[int] = []
        self.gradients: list[animations.GradientItem] = []
        self.visible: bool = True

        self.kwargs = kwargs

        widget.register(self)

    def move(self, dx: float, dy: float) -> None:
        """Move the `Element`"""
        self.position[0] += dx
        self.position[1] += dy
        for item in self.items:
            self.widget.master.move(item, dx, dy)

    def moveto(self, x: float, y: float) -> None:
        """Move the `Element` to a certain position"""
        return self.move(x-self.position[0], y-self.position[1])

    def destroy(self) -> None:
        """Destroy the `Element`"""
        for gradient in self.gradients:
            gradient.stop()
        self.widget.deregister(self)
        self.widget.master.delete(*self.items)

    def center(self) -> tuple[float, float]:
        """Return the geometric center of the `Element`"""
        return self.position[0] + self.size[0]/2, self.position[1] + self.size[1]/2

    def region(self) -> tuple[float, float, float, float]:
        """Return the decision region of the `Element`"""
        return self.position[0], self.position[1], \
            self.position[0]+self.size[0], self.position[1]+self.size[1]

    def detect(self, x: int, y: int) -> bool:
        """Detect whether the specified coordinates are within `Element`"""
        x1, y1, x2, y2 = self.region()
        return x1 <= x <= x2 and y1 <= y <= y2

    def update(self, state: str | None = None, *, no_delay: bool = False) -> None:
        """Update the style of the `Element` to the corresponding state

        * `state`: the state of the `Element`
        """
        if not self.visible:
            return
        if state is None:
            state = self.widget.state
        for gradient in self.gradients:
            gradient.stop()
        self.gradients.clear()
        if self.styles.get(state) is not None:
            self.configure(self.styles[state], no_delay=no_delay)

    def get_disabled_style(self, refer_state: str | None = None) -> dict[str, str]:
        """Get the style data of disabled state"""
        if refer_state is None:
            refer_state = self.widget.state
        if self.styles.get("disabled") is None:
            self.styles["disabled"] = copy.deepcopy(self.styles.get(refer_state, {}))
            for key, value in self.styles["disabled"].items():
                self.styles["disabled"][key] = convert.rgb_to_hex(rgb.transition(
                    convert.hex_to_rgb(value), convert.str_to_rgb(self.widget.master["bg"]),
                    configurations.Constant.GOLDEN_RATIO))
        return self.styles["disabled"]

    def configure(self, style: dict[str, str], *, no_delay: bool = False) -> None:
        """Configure properties of `Element` and update them immediately"""
        for item in self.items:
            tags = self.widget.master.itemcget(item, "tags").split()
            kwargs = {key: value for key, param
                      in zip(tags[0:-1:2], tags[1:len(tags):2])
                      if (value := style.get(param)) is not None}
            if self.widget.gradient_animation and self.gradient_animation and not no_delay:
                for key, value in kwargs.items():
                    start_color: str = self.widget.master.itemcget(item, key)
                    if start_color.startswith("#") and len(start_color) == 9:
                        start_color = convert.rgb_to_hex(convert.rgba_to_rgb(convert.hex_to_rgba(start_color), refer=convert.hex_to_rgb(self.widget.master["bg"])))
                    if value.startswith("#") and len(value) == 9:
                        value = convert.rgb_to_hex(convert.rgba_to_rgb(convert.hex_to_rgba(value), refer=convert.hex_to_rgb(self.widget.master["bg"])))
                    if value == "" or start_color == "":
                        # Null characters cannot be parsed
                        self.widget.master.itemconfigure(item, {key: value})
                    else:
                        self.gradients.append(animations.GradientItem(
                            self.widget.master, item, key, (start_color, value), 150))
            else:
                for key, value in kwargs.items():
                    if value.startswith("#") and len(value) == 9:
                        kwargs[key] = convert.rgb_to_hex(convert.rgba_to_rgb(convert.hex_to_rgba(start_color), refer=convert.hex_to_rgb(self.widget.master["bg"])))
                self.widget.master.itemconfigure(item, kwargs)

        for gradient in self.gradients:
            gradient.start()

    def disappear(self, value: bool = True, *, no_delay: bool = True) -> None:
        """Let the element to disappear"""
        self.visible = not value
        if value:
            temp_style = copy.deepcopy(self.styles.get(self.widget.state, None))
            if temp_style is None:
                return
            for arg in temp_style:
                temp_style[arg] = ""
            self.configure(temp_style, no_delay=no_delay)
        else:
            self.update(self.widget.state, no_delay=no_delay)

    def __getitem__(self, key: str) -> dict[str, str]:
        """Easy to get style data"""
        return self.styles[key]

    def __setitem__(self, key: str, value: dict[str, str]) -> None:
        """Easy to set style data"""
        self.styles[key].update(value)
        self.update(no_delay=True)

    def zoom(
        self,
        ratios: tuple[float, float],
        *,
        zoom_position: bool = True,
        zoom_size: bool = True,
    ) -> None:
        """Zoom the `Element`"""
        if not zoom_position and not zoom_size:
            warnings.warn("This is a no-effect call.", UserWarning, 2)
            return

        if zoom_size:
            self.size[0] *= ratios[0]
            self.size[1] *= ratios[1]
        if zoom_position:
            self.position[0] *= ratios[0]
            self.position[1] *= ratios[1]

        if not zoom_size:
            x = self.position[0]*ratios[0]
            y = self.position[1]*ratios[1]
            for item in self.items:
                self.widget.master.moveto(item, x, y)
        elif not zoom_position:
            for item in self.items:
                self.widget.master.scale(item, *self.position, *ratios)
        else:
            for item in self.items:
                self.widget.master.scale(item, 0, 0, *ratios)

    @abc.abstractmethod
    def display(self) -> None:
        """Display the `Element` on a `Canvas`"""

    @abc.abstractmethod
    def coords(
        self,
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`"""
        if size is not None:
            self.size = list(size)
        if position is not None:
            self.position = list(position)


class Shape(Element):
    """The Shape of a `Widget`"""

    @typing_extensions.override
    def zoom(
        self,
        ratios: tuple[float, float],
        *,
        zoom_position: bool = True,
        zoom_size: bool = True,
    ) -> None:
        """Scale the shape"""
        if zoom_size:
            self.size[0] *= ratios[0]
            self.size[1] *= ratios[1]
        if zoom_position:
            self.position[0] *= ratios[0]
            self.position[1] *= ratios[1]

        self.coords(self.size, self.position)


class Text(Element):
    """The Text of a `Widget`"""

    def __init__(
        self,
        widget: Widget,
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        text: str = "",
        limit: int = -1,
        show: str | None = None,
        placeholder: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal["normal", "bold"] = "normal",
        slant: typing.Literal["roman", "italic"] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of element
        * `text`: text value
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the font
        * `slant`: slant of the font
        * `underline`: wether text is underline
        * `overstrike`: wether text is overstrike
        * `limit`: limit on the number of characters
        * `show`: display a value that obscures the original content
        * `placeholder`: a placeholder for the prompt
        * `name`: name of element
        * `animation`: Wether use animation to change color
        * `styles`: style dict of element
        * `kwargs`: extra parameters for CanvasItem
        """
        self.text = text
        self.show = show
        self.placeholder = placeholder
        self.limit = limit
        self.font = tkinter.font.Font(
            family=family if family else configurations.Font.family,
            size=-abs(fontsize if fontsize else configurations.Font.size),
            weight=weight, slant=slant,
            underline=underline, overstrike=overstrike)
        self._initial_fontsize = self.font.cget("size")
        Element.__init__(self, widget, relative_position, size, name=name,
                         styles=styles, gradient_animation=animation, **kwargs)

    def region(self) -> tuple[int, int, int, int]:
        """Return the decision region of the `Text`"""
        return self.widget.master.bbox(self.items[0])

    @typing_extensions.override
    def zoom(
        self,
        ratios: tuple[float, float],
        *,
        zoom_position: bool = True,
        zoom_size: bool = True,
    ) -> None:
        """Scale the text"""
        Element.zoom(self, ratios, zoom_position=zoom_position, zoom_size=zoom_size)
        ratios = self.widget.master.ratios
        self.font.config(size=round(self._initial_fontsize*math.sqrt(ratios[0]*ratios[1])))


class Image(Element):
    """The Image of a `Widget`"""

    def __init__(
        self,
        widget: Widget,
        relative_position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        animation: bool = True,
        styles: dict[str, dict[str, str]] | None = None,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of element
        * `image`: image object of the element
        * `name`: name of element
        * `animation`: Wether use animation to change color
        * `styles`: style dict of element
        * `kwargs`: extra parameters for CanvasItem
        """
        self.image = image
        self.initail_image = image
        Element.__init__(self, widget, relative_position, size, name=name,
                         gradient_animation=animation, styles=styles, **kwargs)

    @typing_extensions.override
    def zoom(
        self,
        ratios: tuple[float, float],
        *,
        zoom_position: bool = True,
        zoom_size: bool = True,
    ) -> None:
        """Scale the image"""
        Element.zoom(self, ratios, zoom_position=zoom_position, zoom_size=zoom_size)
        if self.initail_image is None:
            raise RuntimeError("Image is empty.")
        self.image = self.initail_image.scale(*self.widget.master.ratios)
        for item in self.items:
            self.widget.master.itemconfigure(item, image=self.image)


class Feature:
    """The features of a `Widget`"""

    def __init__(self, widget: Widget) -> None:
        """
        * `widget`: parent widget
        """
        self.widget, widget.feature = widget, self
        self.extras: dict[str, list[collections.abc.Callable[[tkinter.Event], typing.Any]]] = {}

    @staticmethod
    def _parse_method_name(name: str) -> str:
        name = re.sub("[<\\->]", "", name)
        name = re.sub("([0-9A-Z])", "_\\1", name)
        return name.lower()

    def get_method(self, name: str) -> collections.abc.Callable:
        """Return method by name"""
        extra_commands = self.extras.get(name)
        method = getattr(self, self._parse_method_name(name), lambda _: False)

        if extra_commands is None:
            return method

        def _wrapper(event: tkinter.Event) -> typing.Any:
            return_value = method(event)
            for command in extra_commands:
                try:
                    command(event)
                except Exception as exc:
                    traceback.print_exception(exc)
            return return_value

        return _wrapper


class Widget:
    """Base Widget Class

    `Widget` = `Shape` + `Text` + `Image` + `Feature` + `Widget`
    """

    def __init__(
        self,
        master: containers.Canvas | Widget,
        position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        state: str = "normal",
        anchor: typing.Literal["n", "s", "w", "e", "nw", "ne", "sw", "se", "center"] = "nw",
        capture_events: bool | None = None,
        gradient_animation: bool | None = None,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `name`: name of the widget
        * `state`: default state of the widget
        * `anchor`: layout anchor of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        if isinstance(master, Widget):
            self.master, self.widget = master.master, master
            self.widget.widgets.append(self)
            self.position: list[int | float] = [
                master.position[0] + position[0], master.position[1] + position[1]]
            self.size: list[int | float] = master.size.copy() if size is None else list(size)
        else:
            self.master, self.widget = master, None
            self.position: list[int | float] = list(position)
            self.size: list[int | float] = [0, 0] if size is None else list(size)

        self.name = name
        self.state = state
        self.anchor = anchor
        self.capture_events = capture_events
        if self.capture_events is None and self.is_nested():
            self.capture_events = True  # Boolean indicate enforce the operation
        self.gradient_animation = configurations.Env.default_animation if gradient_animation is None else gradient_animation

        self.widgets: list[Widget] = []
        self.texts: list[Text] = []
        self.shapes: list[Shape] = []
        self.images: list[Image] = []
        self.feature: Feature = Feature(self)
        self.state_before_disabled: str = ""
        self._update_hooks: list[collections.abc.Callable[[str, bool], typing.Any]] = []
        self._is_disappeared: bool = False

        self.master.widgets.append(self)

    @property
    def elements(self) -> tuple[Element, ...]:
        """Return all elements of the widget"""
        return tuple(self.shapes + self.texts + self.images)

    @property
    def is_disappeared(self) -> bool:
        """Whether the widget is forgoted"""
        return self._is_disappeared

    @property
    def offset(self) -> tuple[float, float]:
        """Return the offset of the anchor relative to nw"""
        match self.anchor:
            case "n": _offset = self.size[0]/2, 0
            case "w": _offset = 0, self.size[1]/2
            case "s": _offset = self.size[0]/2, self.size[1]
            case "e": _offset = self.size[0], self.size[1]/2
            case "ne": _offset = self.size[0], 0
            case "sw": _offset = 0, self.size[1]
            case "nw": _offset = 0, 0
            case "se": _offset = self.size[0], self.size[1]
            case _: _offset = self.size[0]/2, self.size[1]/2
        return _offset

    def is_nested(self) -> bool:
        """Whether the widget is a nested widget"""
        return self.widget is not None

    def register(self, element: Element) -> None:
        """Register a element to the widget"""
        if isinstance(element, Shape):
            self.shapes.append(element)
        elif isinstance(element, Text):
            self.texts.append(element)
        elif isinstance(element, Image):
            self.images.append(element)
        element.display()
        element.coords()
        element.update(no_delay=True)

    def deregister(self, element: Element) -> None:
        """Deregister a element from the widget"""
        if isinstance(element, Shape):
            self.shapes.remove(element)
        elif isinstance(element, Text):
            self.texts.remove(element)
        elif isinstance(element, Image):
            self.images.remove(element)

    def update(
        self,
        state: str | None = None,
        *,
        no_delay: bool = False,
        nested: bool = True,
    ) -> None:
        """Update the widget"""
        if state != "disabled" and self.state_before_disabled:
            return  # It is currently disabled
        if nested:
            for widget in self.widgets:
                widget.update(state, no_delay=no_delay)
        for element in self.elements:
            element.update(state, no_delay=no_delay)
        if state is None:
            state = self.state
        else:
            self.state = state
        for command in self._update_hooks:
            try:
                command(state, no_delay)
            except Exception as exc:
                traceback.print_exception(exc)

    def bind_on_update(
        self,
        command: collections.abc.Callable[[str, bool], typing.Any],
    ) -> None:
        """Bind an extra function to the widget on update

        This extra function has two positional arguments, both of which are arguments to the method
        `update`. And this extra function will be called when the widget is updated (whether it's
        automatically updated or manually updated).

        * `command`: the extra function that is bound
        """
        self._update_hooks.append(command)

    def unbind_on_update(self, command: collections.abc.Callable[[str, bool], typing.Any]) -> None:
        """Unbind an extra function to the widget on update

        * `command`: the extra function that is bound
        """
        self._update_hooks.remove(command)

    def bind(
        self,
        sequence: str,
        func: collections.abc.Callable[[tkinter.Event], typing.Any],
        add: bool | typing.Literal["", "+"] | None = None,
    ) -> None:
        """Bind to this widget at event SEQUENCE a call to function FUNC.

        * `sequence`: event name
        * `func`: callback function
        * `add`: if True, original callback function will not be overwritten
        """
        if sequence not in configurations.Constant.PREDEFINED_EVENTS:
            if sequence not in configurations.Constant.PREDEFINED_VIRTUAL_EVENTS:
                if sequence not in self.master.events:
                    self.master.events.append(sequence)
                    self.master.register_event(sequence)

        if self.feature.extras.get(sequence) is None or add:
            self.feature.extras[sequence] = [func]
        else:
            self.feature.extras[sequence].append(func)

    def unbind(
        self,
        sequence: str,
        funcid: collections.abc.Callable[[tkinter.Event], typing.Any],
    ) -> None:
        """Unbind for this widget the event SEQUENCE.

        * `sequence`: event name
        * `funcid`: callback function
        """
        if self.feature.extras.get(sequence) is not None:
            self.feature.extras[sequence].remove(funcid)

    def generate_event(
        self,
        sequence: str,
        event: tkinter.Event | None = None,
        **kwargs,
    ) -> None:
        """Generate an event SEQUENCE. Additional keyword arguments specify parameter of the event

        * `sequence`: event name
        * `event`: event
        * `kwargs`: attr of event
        """
        if event is None:
            event = tkinter.Event()
        for key, value in kwargs.items():
            setattr(event, key, value)
        self.feature.get_method(sequence)(event)

    def disabled(self, value: bool = True) -> None:
        """Disable the widget"""
        if value:
            if not self.state_before_disabled:
                self.state_before_disabled = self.state
            for element in self.elements:
                element.get_disabled_style(self.state_before_disabled)
            self.update("disabled", no_delay=True, nested=False)
        else:
            self.state_before_disabled, last_state = "", self.state_before_disabled
            self.update(last_state, no_delay=True, nested=False)
        for widget in self.widgets:
            widget.disabled(value)

    def disappear(self, value: bool = True) -> None:
        """Let all elements of the widget to disappear"""
        for widget in self.widgets:
            widget.disappear(value)
        self._is_disappeared = value
        for element in self.elements:
            element.disappear(value)

    def move(self, dx: int | float, dy: int | float) -> None:
        """Move the widget"""
        self.position[0] += dx
        self.position[1] += dy
        for widget in self.widgets:
            widget.move(dx, dy)
        for element in self.elements:
            element.move(dx, dy)

    def moveto(self, x: int, y: int) -> None:
        """Move the Widget to a certain position"""
        return self.move(x-self.position[0], y-self.position[1])

    def destroy(self) -> None:
        """Destroy the widget"""
        self.master.widgets.remove(self)
        del self.feature

        if self.widget is not None:
            self.widget.widgets.remove(self)

        for widget in tuple(self.widgets):
            widget.destroy()
        for element in self.elements:
            element.destroy()

    def detect(self, x: int, y: int) -> bool:
        """Detect whether the specified coordinates are within the `Widget`"""
        x1, y1, w, h = *self.position, *self.size
        x2, y2 = x1 + w, y1 + h
        return x1 <= x+self.offset[0] <= x2 and y1 <= y+self.offset[1] <= y2

    def zoom(
        self,
        ratios: tuple[float, float] | None = None,
        *,
        zoom_position: bool = True,
        zoom_size: bool = True,
    ) -> None:
        """Zoom self"""
        if not zoom_position and not zoom_size:
            warnings.warn("This is a no-effect call.", UserWarning, 2)
            return

        if ratios is None:
            ratios = self.master.ratios
            for widget in self.widgets:
                widget.zoom(ratios, zoom_position=zoom_position, zoom_size=zoom_size)

        if zoom_size:
            self.size[0] *= ratios[0]
            self.size[1] *= ratios[1]
        if zoom_position:
            self.position[0] *= ratios[0]
            self.position[1] *= ratios[1]

        for element in self.elements:
            element.zoom(ratios, zoom_position=zoom_position, zoom_size=zoom_size)
