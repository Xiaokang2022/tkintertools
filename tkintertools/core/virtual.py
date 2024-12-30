"""All virtual classes.

The `virtual.Widget` consists of five parts, which are `Shape`, `Text`, `Image`,
`Style` and `Feature`. In addition, they can be nested within each other.

Where `Feature` is the function of widgets, `Style` control the color of the
widget, and each widget can be bound to up to one `Feature` and one `Style`,
but in terms of appearance, there is no limit to the number of `Shape`, `Text`,
and `Image`.

`Shape`, `Text`, and `Image` are all appearance elements that inherit from
abstract base class `Elements`.
"""

from __future__ import annotations

__all__ = [
    "Element",
    "Shape",
    "Text",
    "Image",
    "Style",
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
from . import configs, containers


class Element(abc.ABC):
    """The basic visible part of a `virtual.Widget`."""

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
        * `gradient_animation`: Wether use animation to change color
        * `auto_update`: 
        * `styles`: style dict of element
        * `kwargs`: extra parameters for CanvasItem
        """
        self.widget = widget
        self.gradient_animation = gradient_animation
        self.auto_update = auto_update

        self.position: tuple[int | float, int | float] = (
            widget.position[0] + position[0] - widget.offset[0],
            widget.position[1] + position[1] - widget.offset[1],
        )
        self.size: tuple[int | float, int | float] = widget.size if size is None else size
        self.name = self.__class__.__name__ if name is None else name
        self.styles = styles if styles else parser.get(widget, self)

        self.items: list[int] = []
        self.gradients: list[animations.GradientItem] = []
        self.visible: bool = True

        self.kwargs = kwargs

        widget.register_elements(self)

    def move(self, dx: float, dy: float) -> None:
        """Move the `Element`.

        * `dx`: x-coordinate offset
        * `dy`: y-coordinate offset
        """
        self.position = self.position[0]+dx, self.position[1]+dy

        for item in self.items:
            self.widget.master.move(item, dx, dy)

    def moveto(self, x: float, y: float) -> None:
        """Move the `Element` to a certain position"""
        return self.move(x-self.position[0], y-self.position[1])

    def destroy(self) -> None:
        """Destroy the `Element`"""
        for gradient in self.gradients:
            gradient.stop()
        self.widget.deregister_elements(self)
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

    def update(self, state: str | None = None, *, gradient_animation: bool = False) -> None:
        """Update the style of the `Element` to the corresponding state

        * `state`: the state of the `Element`
        """
        gradient_animation = not gradient_animation
        if not self.visible:
            return
        if state is None:
            state = self.widget.state
        for gradient in self.gradients:
            gradient.stop()
        self.gradients.clear()
        if self.styles.get(state) is not None:
            self.configure(self.styles[state], no_delay=gradient_animation)

    def get_disabled_style(self, refer_state: str | None = None) -> dict[str, str]:
        """Get the style data of disabled state"""
        if refer_state is None:
            refer_state = self.widget.state
        if self.styles.get("disabled") is None:
            self.styles["disabled"] = copy.deepcopy(self.styles.get(refer_state, {}))
            for key, value in self.styles["disabled"].items():
                self.styles["disabled"][key] = convert.rgb_to_hex(rgb.transition(
                    convert.hex_to_rgb(value), convert.str_to_rgb(self.widget.master["bg"]),
                    configs.Constant.GOLDEN_RATIO))
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
            self.update(self.widget.state, gradient_animation=no_delay)

    def zoom(
        self,
        ratios: tuple[float, float],
        *,
        zoom_position: bool = True,
        zoom_size: bool = True,
    ) -> None:
        """Zoom the `Element`.

        * `ratios`: ratios of zooming
        * `zoom_position`: whether or not to zoom the location of the element
        * `zoom_size`: whether or not to zoom the size of the element
        """
        if not zoom_position and not zoom_size:
            warnings.warn("This is a no-effect call.", UserWarning, 2)
            return

        if zoom_size:
            self.size = self.size[0]*ratios[0], self.size[1]*ratios[1]

        if zoom_position:
            self.position = self.position[0]*ratios[0], self.position[1]*ratios[1]

        if not zoom_size:
            for item in self.items:
                self.widget.master.moveto(
                    item, self.position[0]*ratios[0], self.position[1]*ratios[1])
        elif not zoom_position:
            for item in self.items:
                self.widget.master.scale(item, *self.position, *ratios)
        else:
            for item in self.items:
                self.widget.master.scale(item, 0, 0, *ratios)

    @abc.abstractmethod
    def display(self) -> None:
        """Display the `Element` on a `Canvas`."""

    @abc.abstractmethod
    def coords(
        self,
        size: tuple[int | float, int | float] | None = None,
        position: tuple[int | float, int | float] | None = None,
    ) -> None:
        """Resize the `Element`.

        * `size`: new size of the element
        * `position`: new position of the element
        """
        if size is not None:
            self.size = size

        if position is not None:
            self.position = position

        # overload this method to do something here


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
        """Scale the shape.

        * `ratios`: ratios of zooming
        * `zoom_position`: whether or not to zoom the location of the shape
        * `zoom_size`: whether or not to zoom the size of the shape
        """
        if zoom_size:
            self.size = self.size[0]*ratios[0], self.size[1]*ratios[1]

        if zoom_position:
            self.position = self.position[0]*ratios[0], self.position[1]*ratios[1]

        self.coords(self.size, self.position)


class Text(Element):
    """The Text of a `Widget`."""

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
            family=family if family else configs.Font.family,
            size=-abs(fontsize if fontsize else configs.Font.size),
            weight=weight, slant=slant,
            underline=underline, overstrike=overstrike)

        self._initial_fontsize = self.font.cget("size")

        Element.__init__(self, widget, relative_position, size, name=name,
                         styles=styles, gradient_animation=animation, **kwargs)

    def region(self) -> tuple[int, int, int, int]:
        """Return the decision region of the `Text`."""
        return self.widget.master.bbox(self.items[0])

    @typing_extensions.override
    def zoom(
        self,
        ratios: tuple[float, float],
        *,
        zoom_position: bool = True,
        zoom_size: bool = True,
    ) -> None:
        """Scale the text.

        * `ratios`: ratios of zooming
        * `zoom_position`: whether or not to zoom the location of the text
        * `zoom_size`: whether or not to zoom the size of the text
        """
        Element.zoom(self, ratios, zoom_position=zoom_position, zoom_size=zoom_size)

        self.font.config(size=round(self._initial_fontsize*math.sqrt(
            self.widget.master.ratios[0]*self.widget.master.ratios[1])))


class Image(Element):
    """The Image of a `Widget`."""

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
        """Scale the image.

        * `ratios`: ratios of zooming
        * `zoom_position`: whether or not to zoom the location of the image
        * `zoom_size`: whether or not to zoom the size of the image
        """
        Element.zoom(self, ratios, zoom_position=zoom_position, zoom_size=zoom_size)

        if self.initail_image is None:
            raise RuntimeError("Image is empty.")

        self.image = self.initail_image.scale(*self.widget.master.ratios)

        for item in self.items:
            self.widget.master.itemconfigure(item, image=self.image)


class Style:
    """The styles of a `Widget`."""

    light: dict[str, dict[str, dict[str, str]]]
    dark: dict[str, dict[str, dict[str, str]]]

    def __init__(self, widget: Widget, *, auto_update: bool = True) -> None:
        """
        * `widget`: parent widget
        * `auto_update`: 
        """
        self.widget, widget.style = widget, self
        self.auto_update = auto_update

    def update(
        self,
        state: str,
        *,
        gradient_animation: bool | None = None,
    ) -> None:
        """Update the style of the widget."""

    def configure(self) -> None:
        """Configure the style."""


class Feature:
    """The features of a `Widget`."""

    def __init__(self, widget: Widget) -> None:
        """
        * `widget`: parent widget
        """
        self.widget, widget.feature = widget, self
        self.extra_commands: dict[str, list[collections.abc.Callable[[tkinter.Event], typing.Any]]] = {}

    @staticmethod
    def _parse_method_name(name: str) -> str:
        """Parse the name to method name.

        * `name`: original name

        Example:

        * `"<Ctrl-C>"` -> `"_ctrl_c"`
        * `"<MouseWheel>"` -> `"_mouse_wheel"`
        """
        name = re.sub("[<\\->]", "", name)
        name = re.sub("([0-9A-Z])", "_\\1", name)
        return name.lower()

    def get_method(self, name: str) -> collections.abc.Callable:
        """Return method by name.

        * `name`: name of the method
        """
        extra_commands = self.extra_commands.get(name)
        method = getattr(self, self._parse_method_name(name), lambda _: False)

        if extra_commands is None:
            return method

        def wrapper(event: tkinter.Event) -> typing.Any:
            result = method(event)

            for command in extra_commands:
                try:
                    command(event)
                except Exception as exc:
                    traceback.print_exception(exc)

            return result

        return wrapper


class Widget:
    """Base Widget Class.

    `Widget` = `Element` + `Style` + `Feature`
    """

    def __init__(
        self,
        master: containers.Canvas | Widget,
        position: tuple[int, int] = (0, 0),
        size: tuple[int, int] | None = None,
        *,
        name: str | None = None,
        anchor: typing.Literal["n", "s", "w", "e", "nw", "ne", "sw", "se", "center"] = "nw",
        capture_events: bool | None = None,
        gradient_animation: bool | None = None,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `name`: name of the widget
        * `anchor`: layout anchor of the widget
        * `capture_events`: wether detect another widget under the widget
        * `gradient_animation`: wether enable animation
        """
        if isinstance(master, Widget):
            self.master, self.widget = master.master, master
            self.widget.widgets.append(self)
            self.position: tuple[int | float, int | float] = (
                master.position[0] + position[0],
                master.position[1] + position[1],
            )
            self.size: tuple[int | float, int | float] = master.size if size is None else size
        else:
            self.master, self.widget = master, None
            self.position: tuple[int | float, int | float] = position
            self.size: tuple[int | float, int | float] = (0, 0) if size is None else size

        self.name = name
        self.anchor = anchor

        if capture_events is None and self.nested:
            self.capture_events = False  # bool indicates enforce the operation
        else:
            self.capture_events = capture_events

        if gradient_animation is None:
            self.gradient_animation = configs.Env.default_animation
        else:
            self.gradient_animation = gradient_animation

        self.widgets: list[Widget] = []
        self.texts: list[Text] = []
        self.shapes: list[Shape] = []
        self.images: list[Image] = []
        self.style = Style(self)
        self.feature = Feature(self)

        self.state: str = "normal"
        self.state_before_disabled: str = ""
        self.disappeared: bool = False

        self._update_hooks: list[collections.abc.Callable[[str, bool], typing.Any]] = []

        self.master.widgets.append(self)

    @property
    def elements(self) -> tuple[Element, ...]:
        """Return all elements of the widget."""
        return tuple(self.shapes + self.texts + self.images)

    @property
    def nested(self) -> bool:
        """Whether the widget is a nested widget."""
        return self.widget is not None

    @property
    def offset(self) -> tuple[float, float]:
        """Return the offset of the anchor relative to "nw"."""
        match self.anchor:
            case "n": result = self.size[0]/2, 0
            case "w": result = 0, self.size[1]/2
            case "s": result = self.size[0]/2, self.size[1]
            case "e": result = self.size[0], self.size[1]/2
            case "ne": result = self.size[0], 0
            case "sw": result = 0, self.size[1]
            case "nw": result = 0, 0
            case "se": result = self.size[0], self.size[1]
            case _: result = self.size[0]/2, self.size[1]/2

        return result

    def register_elements(self, *elements: Element) -> None:
        """Register elements to the widget.

        * `elements`: elements to be registered
        """
        for element in elements:
            if isinstance(element, Shape):
                self.shapes.append(element)
            elif isinstance(element, Text):
                self.texts.append(element)
            elif isinstance(element, Image):
                self.images.append(element)

            element.display()
            element.coords()
            element.update(gradient_animation=True)

    def deregister_elements(self, *elements: Element) -> None:
        """Deregister a element from the widget.

        * `elements`: elements to be deregistered
        """
        for element in elements:
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
        gradient_animation: bool | None = None,
        nested: bool = True,
    ) -> None:
        """Update the widget"""
        if state != "disabled" and self.state_before_disabled:
            return  # It is currently disabled

        if gradient_animation is None:
            gradient_animation = self.gradient_animation

        if nested:
            for widget in self.widgets:
                widget.update(state, gradient_animation=gradient_animation)

        for element in self.elements:
            element.update(state, gradient_animation=gradient_animation)

        # self.style.update(state, gradient_animation=gradient_animation)

        if state is None:
            state = self.state
        else:
            self.state = state  # update self.state

        for command in self._update_hooks:
            try:
                command(state, gradient_animation)
            except Exception as exc:
                traceback.print_exception(exc)

    def bind_on_update(
        self,
        command: collections.abc.Callable[[str, bool], typing.Any],
    ) -> None:
        """Bind an extra function to the widget on update.

        This extra function has two positional arguments, both of which are
        arguments to the method `update`. And this extra function will be
        called when the widget is updated (whether it's automatically updated
        or manually updated).

        * `command`: the extra function that is bound
        """
        self._update_hooks.append(command)

    def unbind_on_update(
        self,
        command: collections.abc.Callable[[str, bool], typing.Any],
    ) -> None:
        """Unbind an extra function to the widget on update.

        * `command`: the extra function that is bound
        """
        self._update_hooks.remove(command)

    def bind(
        self,
        sequence: str,
        command: collections.abc.Callable[[tkinter.Event], typing.Any],
        add: bool | typing.Literal["", "+"] | None = None,
    ) -> None:
        """Bind to this widget at event sequence a call to function command.

        * `sequence`: event name
        * `command`: callback function
        * `add`: if True, original callback function will not be overwritten
        """
        if sequence not in configs.Constant.PREDEFINED_EVENTS:
            if sequence not in configs.Constant.PREDEFINED_VIRTUAL_EVENTS:
                if sequence not in self.master.events:
                    self.master.events.append(sequence)
                    self.master.register_event(sequence)

        if self.feature.extra_commands.get(sequence) is None or add:
            self.feature.extra_commands[sequence] = [command]
        else:
            self.feature.extra_commands[sequence].append(command)

    def unbind(
        self,
        sequence: str,
        command: collections.abc.Callable[[tkinter.Event], typing.Any],
    ) -> None:
        """Unbind for this widget the event sequence.

        * `sequence`: event name
        * `command`: callback function
        """
        if self.feature.extra_commands.get(sequence) is not None:
            self.feature.extra_commands[sequence].remove(command)

    def generate_event(
        self,
        sequence: str,
        event: tkinter.Event | None = None,
        **kwargs,
    ) -> None:
        """Generate an event sequence. Additional keyword arguments specify
        parameter of the event.

        * `sequence`: event name
        * `event`: event
        * `kwargs`: attr of event
        """
        if event is None:
            event = tkinter.Event()

        for key, value in kwargs.items():
            setattr(event, key, value)

        self.feature.get_method(sequence)(event)

    def disable(self, value: bool = True, /) -> None:
        """Disable the widget."""
        if value:
            if not self.state_before_disabled:
                self.state_before_disabled = self.state
            for element in self.elements:
                element.get_disabled_style(self.state_before_disabled)
            self.update("disabled", gradient_animation=True, nested=False)
        else:
            self.state_before_disabled, last_state = "", self.state_before_disabled
            self.update(last_state, gradient_animation=True, nested=False)
        for widget in self.widgets:
            widget.disable(value)

    def disappear(self, value: bool = True, /) -> None:
        """Let all elements of the widget to disappear."""
        self.disappeared = value

        for widget in self.widgets:
            widget.disappear(value)

        for element in self.elements:
            element.disappear(value)

    def move(self, dx: int | float, dy: int | float) -> None:
        """Move the widget.

        * `dx`: x-coordinate offset
        * `dy`: y-coordinate offset
        """
        self.position = self.position[0]+dx, self.position[1]+dy

        for widget in self.widgets:
            widget.move(dx, dy)

        for element in self.elements:
            element.move(dx, dy)

    def moveto(self, x: int, y: int) -> None:
        """Move the Widget to a certain position.

        * `x`: x-coordinate of the target location
        * `y`: y-coordinate of the target location
        """
        return self.move(x-self.position[0], y-self.position[1])

    def destroy(self) -> None:
        """Destroy the widget."""
        self.master.widgets.remove(self)
        del self.feature, self.style

        if self.widget is not None:
            self.widget.widgets.remove(self)

        for widget in tuple(self.widgets):
            widget.destroy()

        for element in self.elements:
            element.destroy()

    def detect(self, x: int, y: int) -> bool:
        """Detect whether the specified coordinates are within the `Widget`.

        * `x`: x-coordinate of the location to be detected
        * `y`: y-coordinate of the location to be detected
        """
        x1, y1, w, h = *self.position, *self.size
        x2, y2 = x1+w, y1+h
        return x1 <= x+self.offset[0] <= x2 and y1 <= y+self.offset[1] <= y2

    def zoom(
        self,
        ratios: tuple[float, float] | None = None,
        *,
        zoom_position: bool = True,
        zoom_size: bool = True,
    ) -> None:
        """Zoom widget ifself.

        * `ratios`: ratios of zooming
        * `zoom_position`: whether or not to zoom the location of the widget
        * `zoom_size`: whether or not to zoom the size of the widget
        """
        if not zoom_position and not zoom_size:
            warnings.warn("This is a no-effect call.", UserWarning, 2)
            return

        if ratios is None:
            ratios = self.master.ratios

        if zoom_size:
            self.size = self.size[0]*ratios[0], self.size[1]*ratios[1]

        if zoom_position:
            self.position = self.position[0]*ratios[0], self.position[1]*ratios[1]

        for widget in self.widgets:
            widget.zoom(ratios, zoom_position=zoom_position, zoom_size=zoom_size)

        for element in self.elements:
            element.zoom(ratios, zoom_position=zoom_position, zoom_size=zoom_size)
