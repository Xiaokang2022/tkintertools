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
import types
import typing
import warnings

import typing_extensions

from ..animation import animations
from ..color import convert, rgb
from ..theme import manager
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
        gradient_animation: bool | None = None,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `position`: position relative to its widgets
        * `size`: size of element
        * `name`: name of element
        * `gradient_animation`: Wether use animation to change color
        * `kwargs`: extra parameters for CanvasItem
        """
        self.widget = widget

        if gradient_animation is None:
            self.gradient_animation = widget.gradient_animation
        else:
            self.gradient_animation = gradient_animation

        self.position: tuple[float, float] = (
            widget.position[0] + position[0] - widget.offset[0],
            widget.position[1] + position[1] - widget.offset[1],
        )

        self.size: tuple[float, float] = widget.size if size is None else size

        self.name = self.__class__.__name__

        if name is not None:
            self.name += name

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
        """Move the `Element` to a certain position.

        * `x`: x-coordinate of the target location
        * `y`: y-coordinate of the target location
        """
        return self.move(x-self.position[0], y-self.position[1])

    def destroy(self) -> None:
        """Destroy the `Element`."""
        for gradient in self.gradients:
            gradient.stop()

        self.widget.deregister_elements(self)
        self.widget.master.delete(*self.items)

    def center(self) -> tuple[float, float]:
        """Return the geometric center of the `Element`."""
        return self.position[0] + self.size[0]/2, self.position[1] + self.size[1]/2

    def region(self) -> tuple[int, int, int, int]:
        """Return the decision region of the `Element`."""
        x, y, w, h = *self.position, *self.size
        return round(x), round(y), round(x+w), round(y+h)

    def detect(self, x: float, y: float) -> bool:
        """Detect whether the specified coordinates are within `Element`.

        * `x`: x-coordinate of the location to be detected
        * `y`: y-coordinate of the location to be detected
        """
        x1, y1, x2, y2 = self.region()
        return x1 <= x <= x2 and y1 <= y <= y2

    def update(
        self,
        state: str | None = None,
        *,
        gradient_animation: bool = False,
    ) -> None:
        """Update the style of the `Element` to the corresponding state.

        * `state`: the state of the `Element`
        * `gradient_animation`: whether use gradient animation
        """
        if not self.visible:
            return

        if state is None:
            state = self.widget.state

        if data := self.widget.style[self].get(state):
            self.configure(data, gradient_animation=gradient_animation)

    def configure(
        self,
        style: dict[str, str],
        *,
        gradient_animation: bool = True,
    ) -> None:
        """Configure properties of `Element` and update them immediately.

        * `style`: style data
        * `gradient_animation`: whether use gradient animation
        """
        for gradient in self.gradients:
            gradient.stop()

        self.gradients.clear()

        bg = convert.str_to_rgb(self.widget.master.cget("bg"))

        for item in self.items:
            tags = self.widget.master.itemcget(item, "tags").split()
            keys, args = tags[0:-1:2], tags[1:len(tags):2]
            values = (style.get(arg) for arg in args)
            kwargs = {k: v for k, v in zip(keys, values) if v is not None}

            for key, value in kwargs.items():
                if value.startswith("#") and len(value) == 9:
                    rgba_code = convert.hex_to_rgba(value)
                    kwargs[key] = convert.rgb_to_hex(
                        convert.rgba_to_rgb(rgba_code, refer=bg))

            if self.widget.gradient_animation and self.gradient_animation and gradient_animation:
                for key, value in kwargs.items():
                    start: str = self.widget.master.itemcget(item, key)

                    if start.startswith("#") and len(start) == 9:
                        rgba_code = convert.hex_to_rgba(start)
                        start = convert.rgb_to_hex(
                            convert.rgba_to_rgb(rgba_code, refer=bg))

                    if value == "" or start == "":
                        # Null characters cannot be parsed
                        self.widget.master.itemconfigure(item, {key: value})
                    else:
                        self.gradients.append(animations.GradientItem(
                            self.widget.master, item, key, (start, value), 150))
            else:
                self.widget.master.itemconfigure(item, kwargs)

        for gradient in self.gradients:
            gradient.start()

    def forget(
        self,
        value: bool = True,
        *,
        gradient_animation: bool = False,
    ) -> None:
        """Let the element to forget.

        * `value`: whether to forget
        * `gradient_animation`: whether use gradient animation
        """
        self.visible = not value

        if value:
            temp_style = copy.deepcopy(
                self.widget.style[self].get(self.widget.state))

            if temp_style is None:
                return

            for arg in temp_style:
                temp_style[arg] = ""

            self.configure(temp_style, gradient_animation=gradient_animation)
        else:
            self.update(self.widget.state, gradient_animation=gradient_animation)

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
        size: tuple[float, float] | None = None,
        position: tuple[float, float] | None = None,
    ) -> None:
        """Resize the `Element`.

        * `size`: new size of the element
        * `position`: new position of the element
        """
        if size is not None:
            self.size = size

        if position is not None:
            self.position = position

        # override this method to do something here


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
        gradient_animation: bool = True,
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
        * `gradient_animation`: Wether use animation to change color
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
                         gradient_animation=gradient_animation, **kwargs)

    def region(self) -> tuple[int, int, int, int]:
        """Return the decision region of the `Text`."""
        if self.items:
            return self.widget.master.bbox(self.items[0])

        return Element.region(self)

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
        Element.zoom(
            self, ratios, zoom_position=zoom_position, zoom_size=zoom_size)

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
        gradient_animation: bool = True,
        **kwargs,
    ) -> None:
        """
        * `widget`: parent widget
        * `relative_position`: position relative to its widgets
        * `size`: size of element
        * `image`: image object of the element
        * `name`: name of element
        * `gradient_animation`: Wether use animation to change color
        * `kwargs`: extra parameters for CanvasItem
        """
        self.image = image
        self.initail_image = image

        Element.__init__(self, widget, relative_position, size, name=name,
                         gradient_animation=gradient_animation, **kwargs)

    def region(self) -> tuple[int, int, int, int]:
        """Return the decision region of the `Image`."""
        if self.items:
            return self.widget.master.bbox(self.items[0])

        return Element.region(self)

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
        Element.zoom(
            self, ratios, zoom_position=zoom_position, zoom_size=zoom_size)

        if self.initail_image is None:
            raise RuntimeError("Image is empty.")

        self.image = self.initail_image.scale(*self.widget.master.ratios)

        for item in self.items:
            self.widget.master.itemconfigure(item, image=self.image)


class Style:
    """The styles of a `Widget`."""

    states = "normal", "hover", "active", "disabled"

    light: dict[str, dict[str, dict[str, str]]] = {}
    dark: dict[str, dict[str, dict[str, str]]] = {}

    def __init__(
        self,
        widget: Widget,
        *,
        auto_update: bool | None = None,
    ) -> None:
        """
        * `widget`: parent widget
        * `auto_update`: whether the theme manager update it automatically
        """
        self.widget = widget

        if auto_update is None:
            self.auto_update = widget.auto_update
        else:
            self.auto_update = auto_update

        self.light = copy.deepcopy(self.light)
        self.dark = copy.deepcopy(self.dark)

        self._cache: dict[str, dict[str, dict[str, str]]] = {}

    def _get_key(self, key: Element | str | int) -> str:
        """Get the key.

        * `key`: the object related to the key
        """
        if isinstance(key, Element):
            key = key.name
        elif isinstance(key, int):
            key = self.widget.elements[key].name

        return key

    def __getitem__(
        self,
        key: Element | str | int,
        /,
    ) -> dict[str, dict[str, str]]:
        return self.get().get(self._get_key(key), {})

    def get_disabled_style(self, *, element: Element) -> dict[str, str]:
        """Get the style data of disabled state.

        * `element`: element that style to be calculated
        """
        if style := self[element].get("disabled"):
            return style

        if self.widget.state_before_disabled:
            state = self.widget.state_before_disabled
        else:
            state = self.widget.state

        now_style = copy.deepcopy(self.get()[element.name][state])

        bg = convert.str_to_rgb(self.widget.master.cget("bg"))

        for key, value in now_style.items():
            if not value:  # Empty string
                now_style[key] = value
                continue
            now_style[key] = convert.rgb_to_hex(rgb.transition(
                convert.str_to_rgb(value), bg, configs.Constant.GOLDEN_RATIO))

        self[element]["disabled"] = now_style  # cache

        return now_style

    def init(
        self,
        key: Element | str | int,
        *,
        theme: typing.Literal["light", "dark"] | None = None,
    ) -> None:
        """Initialize some style of an element.

        * `name`: the key of the element
        * `theme`: the theme name, None indicates both
        """
        name = self._get_key(key)

        if theme != "light":
            if not self.dark.get(name):
                self.dark[name] = {}
        if theme != "dark":
            if not self.light.get(name):
                self.light[name] = {}

    def get(
        self,
        *,
        theme: typing.Literal["light", "dark"] | None = None,
    ) -> dict[str, dict[str, dict[str, str]]]:
        """Return the style of the widget.

        * `theme`: the theme of the widget, None indicates the current theme
        """
        if not self._cache or self.auto_update:
            self._cache = getattr(
                self, theme if theme else manager.get_color_mode(), {})

        return self._cache

    def reset(
        self,
        *,
        theme: typing.Literal["light", "dark"] | None = None,
    ) -> None:
        """Reset the style of the widget and update.

        * `theme`: the theme to be reset, None indicates both
        """
        if theme != "light":
            self.dark = copy.deepcopy(self.__class__.dark)

        if theme != "dark":
            self.light = copy.deepcopy(self.__class__.light)

        for element in self.widget.elements:
            element.update()

    @staticmethod
    def _wrap_arg(
        arg: tuple[str | types.EllipsisType | None, ...] | str,
        /,
    ) -> tuple[str | types.EllipsisType | None, ...]:
        """Wrap the argument to a tuple.

        * `arg`: argument
        """
        if isinstance(arg, str):
            return (arg,)

        return arg

    def _set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        data: tuple[str | types.EllipsisType, ...] | str | None = None,
        **kwargs: tuple[Element | str | int, ...] | Element | str | int,
    ) -> None:
        """Set the color of a style conveniently.

        * `theme`: the theme name, None indicates both
        * `data`: data of color
        * `kwargs`: { arg name: element key or element keys tuple }
        """
        if data is None:
            return

        for i, color in enumerate(self._wrap_arg(data)):
            if color is Ellipsis:
                continue

            state = self.states[i]

            for arg, keys in kwargs.items():
                for key in keys if isinstance(keys, tuple) else (keys,):
                    key, pair = self._get_key(key), {arg: color}

                    if theme != "dark":
                        self.get(theme="light")[key][state].update(pair)
                    if theme != "light":
                        self.get(theme="dark")[key][state].update(pair)

    def set(self) -> None:
        """Set the style of the widget."""
        # override this method to do something here


class Feature:
    """The features of a `Widget`."""

    def __init__(self, widget: Widget) -> None:
        """
        * `widget`: parent widget
        """
        self.widget = widget
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
                except Exception as exc:  # pylint: disable=W0718
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
        anchor: typing.Literal["n", "s", "w", "e", "nw", "ne", "sw", "se", "center"] = "nw",
        capture_events: bool | None = None,
        gradient_animation: bool | None = None,
        auto_update: bool | None = None,
        style: type[Style] | None = None,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `anchor`: layout anchor of the widget
        * `capture_events`: wether detect another widget under the widget
        * `gradient_animation`: wether enable animation
        * `auto_update`: whether the theme manager update it automatically
        * `style`: style of the widget
        """
        if isinstance(master, Widget):
            self.master, self.widget = master.master, master
            self.widget.widgets.append(self)
            self.position: tuple[float, float] = (
                master.position[0] + position[0],
                master.position[1] + position[1],
            )
            self.size: tuple[float, float] = master.size if size is None else size
        else:
            self.master, self.widget = master, None
            self.position: tuple[float, float] = position
            self.size: tuple[float, float] = (0, 0) if size is None else size

        self.anchor = anchor

        if capture_events is None and self.nested:
            self.capture_events = False  # bool indicates enforce the operation
        else:
            self.capture_events = capture_events

        if gradient_animation is None:
            self.gradient_animation = configs.Env.gradient_animation
        else:
            self.gradient_animation = gradient_animation

        if auto_update is None:
            self.auto_update = configs.Env.auto_update
        else:
            self.auto_update = auto_update

        self.widgets: list[Widget] = []
        self.texts: list[Text] = []
        self.shapes: list[Shape] = []
        self.images: list[Image] = []
        self.style = Style(self) if style is None else style(self)
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
        """Update the widget.

        * `state`: state of the widget
        * `gradient_animation`: whether use gradient animation
        * `nested`: whether nested
        """
        if state != "disabled" and self.state_before_disabled:
            return  # It is currently disabled

        if gradient_animation is None:
            gradient_animation = self.gradient_animation

        if nested:
            for widget in self.widgets:
                widget.update(state, gradient_animation=gradient_animation)

        for element in self.elements:
            element.update(state, gradient_animation=gradient_animation)

        if state is None:
            state = self.state
        else:
            self.state = state  # update self.state

        for command in self._update_hooks:
            try:
                command(state, gradient_animation)
            except Exception as exc:  # pylint: disable=W0718
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
        """Disable the widget.

        * `value`: whether to disable
        """
        if value:
            if not self.state_before_disabled:
                self.state_before_disabled = self.state

            for element in self.elements:
                if isinstance(element, Image):  # No style for Image
                    continue
                self.style.get_disabled_style(element=element)

            self.update("disabled", gradient_animation=True, nested=False)
        else:
            self.state_before_disabled, last_state = "", self.state_before_disabled
            self.update(last_state, gradient_animation=True, nested=False)
        for widget in self.widgets:
            widget.disable(value)

    def forget(self, value: bool = True, /) -> None:
        """Let all elements of the widget to forget.

        * `value`: whether to forget the widget
        """
        self.disappeared = value

        for widget in self.widgets:
            widget.forget(value)

        for element in self.elements:
            element.forget(value)

    def move(self, dx: float, dy: float) -> None:
        """Move the widget.

        * `dx`: x-coordinate offset
        * `dy`: y-coordinate offset
        """
        self.position = self.position[0]+dx, self.position[1]+dy

        for widget in self.widgets:
            widget.move(dx, dy)

        for element in self.elements:
            element.move(dx, dy)

    def moveto(self, x: float, y: float) -> None:
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

    def detect(self, x: float, y: float) -> bool:
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
            widget.zoom(
                ratios, zoom_position=zoom_position, zoom_size=zoom_size)

        for element in self.elements:
            element.zoom(
                ratios, zoom_position=zoom_position, zoom_size=zoom_size)
