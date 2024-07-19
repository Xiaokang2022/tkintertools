"""All standard Widgets"""

import math
import typing

from ..animation import animations, controllers
from ..core import constants, containers, virtual
from ..toolbox import enhanced
from . import features, images, shapes, texts

__all__ = [
    "Information",
    "Label",
    "Button",
    "Switch",
    "Entry",
    "CheckButton",
    "RadioButton",
    "ProgressBar",
    "UnderlineButton",
    "HighlightButton",
    "IconButton",
    "Slider",
]


class Information(virtual.Widget):
    """Information widget, generally used to display plain text"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (0, 0),
        *,
        text: str = "Information",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s",
                               "nw", "ne", "sw", "se"] = "center",
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `text`: text of the widget
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the text
        * `slant`: slant of the text
        * `underline`: whether the text is underline
        * `overstrike`: whether the text is overstrike
        * `justify`: justify mode of the text
        * `anchor`: anchor of the text
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize, weight=weight, slant=slant,
                          underline=underline, overstrike=overstrike, justify=justify, anchor=anchor)


class Label(virtual.Widget):
    """Label widget, which is generally used to display key information"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (100, 40),
        *,
        text: str = "Label",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s",
                               "nw", "ne", "sw", "se"] = "center",
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `text`: text of the widget
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the text
        * `slant`: slant of the text
        * `underline`: whether the text is underline
        * `overstrike`: whether the text is overstrike
        * `justify`: justify mode of the text
        * `anchor`: anchor of the text
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize, weight=weight, slant=slant,
                          underline=underline, overstrike=overstrike, justify=justify, anchor=anchor)
        features.Label(self)


class Button(virtual.Widget):
    """Button widget, typically used to trigger a function"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (100, 40),
        *,
        text: str = "Button",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s",
                               "nw", "ne", "sw", "se"] = "center",
        command: typing.Callable | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `text`: text of the widget
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the text
        * `slant`: slant of the text
        * `underline`: whether the text is underline
        * `overstrike`: whether the text is overstrike
        * `justify`: justify mode of the text
        * `anchor`: anchor of the text
        * `command`: a function that is triggered when the button is pressed
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize, weight=weight, slant=slant,
                          underline=underline, overstrike=overstrike, justify=justify, anchor=anchor)
        features.Button(self, command=command)


class Switch(virtual.Widget):
    """Switch widget, typically used to control the turning of a function on and off"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        length: int = 50,
        *,
        default: bool = False,
        command: typing.Callable[[bool], typing.Any] | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `length`: length of the widget
        * `default`: default state of the widget
        * `command`: a function that is triggered when the switch is changed
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, (length, length / 2),
                                state=f"normal-{'on' if default else 'off'}",
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self, name=".out")
            shapes.Rectangle(self, name=".in", relative_position=(
                length/12, length/12), size=(length/3, length/3), animation=False)
        else:
            shapes.SemicircularRectangle(self)
            shapes.Oval(self, relative_position=(length/12, length/12),
                        size=(length/3, length/3), animation=False)
        if image is not None:
            images.StillImage(self, image=image)
        features.Switch(self, command=command)
        if default:
            self.set(default)

    def get(self) -> bool:
        """Get the state of the switch"""
        return self.state.endswith("on")

    def set(self, value: bool) -> None:
        """Set the state of the switch"""
        self.update(
            f"{self.state.split('-')[0]}-{'on' if value else 'off'}", no_delay=True)
        dx = self._shapes[0].size[0]/2 if value else -self._shapes[0].size[0]/2
        animations.MoveComponent(
            self._shapes[1], 250, (dx, 0), controller=controllers.smooth, fps=60).start()


class Entry(virtual.Widget):
    """Input box widget, generally used to enter certain information on a single line"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (200, 40),
        *,
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        align: typing.Literal["left", "right", "center"] = "left",
        placeholder: str = "",
        show: str | None = None,
        limit: int = math.inf,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the text
        * `slant`: slant of the text
        * `underline`: whether the text is underline
        * `overstrike`: whether the text is overstrike
        * `align`: align mode of the text
        * `show`: display a value that obscures the original content
        * `placeholder`: a placeholder for the prompt
        * `limit`: limit on the number of characters
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self, name=".out")
            shapes.RoundedRectangle(
                self, name=".in", size=(self.size[0], self.size[1]-3))
        if image is not None:
            images.StillImage(self, image=image)
        texts.SingleLineText(self, family=family, fontsize=fontsize, weight=weight, slant=slant,
                             underline=underline, overstrike=overstrike, align=align, limit=limit,
                             show=show, placeholder=placeholder)
        features.Entry(self)

    def get(self) -> str:
        """"""
        return self._texts[0].get()

    def set(self, value: str) -> None:
        """"""
        self._texts[0].set(value)

    def append(self, value: str) -> None:
        """"""
        self._texts[0].append(value)

    def delete(self, count: int) -> None:
        """"""
        self._texts[0].pop(count)

    def clear(self) -> None:
        """"""
        self.set("")


class CheckButton(virtual.Widget):
    """Checkbox button widget, generally used to check some options"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        length: int = 25,
        *,
        default: bool = False,
        command: typing.Callable[[bool], typing.Any] | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `length`: length of the widget
        * `default`: default state of the widget
        * `command`: a function that is triggered when the state of check button is on
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, (length, length),
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self).set("✔")
        features.CheckButton(self, command=command)
        self.set(default)

    def get(self) -> bool:
        """Get the state of the check button"""
        return self._texts[0].visible

    def set(self, value: bool) -> None:
        """Set the state of the check button"""
        if value:
            return self._texts[0].appear()
        self._texts[0].disappear()


class RadioButton(virtual.Widget):
    """Radio button widget, generally used to select one of several options"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        length: int = 25,
        *,
        default: bool = False,
        command: typing.Callable[[int], typing.Any] | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `length`: length of the widget
        * `default`: default state of the widget
        * `command`: a function that is triggered when the state of radio button is on
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, (length, length),
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self, name=".out")
            shapes.Rectangle(self, name=".in", relative_position=(
                self.size[0]/4, self.size[1]/4), size=(self.size[0]/2, self.size[1]/2)).disappear()
        else:
            shapes.Oval(self, name=".out")
            shapes.Oval(self, name=".in", relative_position=(
                self.size[0]/4, self.size[1]/4), size=(self.size[0]/2, self.size[1]/2)).disappear()
        if image is not None:
            images.StillImage(self, image=image)
        features.RadioButton(self, command=command)
        if default:
            self._shapes[1].appear()

    def get(self) -> bool:
        """Get the state of the radio button"""
        return self._shapes[1].visible

    def set(self, value: bool) -> None:
        """Set the state of the radio button"""
        if value:
            return self._shapes[1].appear()
        self._shapes[1].disappear()


class ProgressBar(virtual.Widget):
    """Progress bar widget, typically used to show the progress of an event"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (400, 20),
        *,
        command: typing.Callable[[], typing.Any] | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `command`: a function that is triggered when the progress of progress bar is 100%
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        self.value: float = 0
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self, name=".out")
            shapes.Rectangle(self, name=".in", size=(
                0, self.size[1]*0.8), relative_position=(self.size[1]*0.1, self.size[1]*0.1))
        else:
            shapes.SemicircularRectangle(self, name=".out")
            shapes.SemicircularRectangle(self, name=".in", size=(
                self.size[1]*0.7, self.size[1]*0.7), relative_position=(self.size[1]*0.15, self.size[1]*0.15))
        if image is not None:
            images.StillImage(self, image=image)
        features.ProgressBar(self)
        self._shapes[1].disappear()
        self.command = command

    def get(self) -> float:
        """Get the progress of the progress bar"""
        return self.value

    def set(self, value: float) -> None:
        """Set the progress of the progress bar"""
        self.value = 0 if value < 0 else 1 if value > 1 else value
        if self.value == 0:
            return self._shapes[1].disappear()
        elif not self._shapes[1].visible:
            self._shapes[1].appear()

        if isinstance(self._shapes[1], shapes.Rectangle):
            self._shapes[1].coords(
                ((self.size[0]-self.size[1]*0.2) * self.value, self._shapes[1].size[1]))
        else:
            self._shapes[1].coords(
                (self.size[1]*0.7 + (self.size[0]-self.size[1]*0.3-self._shapes[1].size[1]) * self.value, self._shapes[1].size[1]))

        if self.value == 1 and self.command is not None:
            self.command()


class UnderlineButton(virtual.Widget):
    """Underline button, generally used to display web links"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (0, 0),
        *,
        text: str = "UnderlineButton",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s",
                               "nw", "ne", "sw", "se"] = "center",
        command: typing.Callable | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = False,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `text`: text of the widget
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the text
        * `slant`: slant of the text
        * `underline`: whether the text is underline
        * `overstrike`: whether the text is overstrike
        * `justify`: justify mode of the text
        * `anchor`: anchor of the text
        * `command`: a function that is triggered when the underline button is pressed
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize, weight=weight, slant=slant,
                          underline=underline, overstrike=overstrike, justify=justify, anchor=anchor)
        features.Underline(self, command=command)


class HighlightButton(virtual.Widget):
    """Highlight button, no outline, which added a highlight effect"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (0, 0),
        *,
        text: str = "HighlightButton",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s",
                               "nw", "ne", "sw", "se"] = "center",
        command: typing.Callable | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `text`: text of the widget
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the text
        * `slant`: slant of the text
        * `underline`: whether the text is underline
        * `overstrike`: whether the text is overstrike
        * `justify`: justify mode of the text
        * `anchor`: anchor of the text
        * `command`: a function that is triggered when the hightlight button is pressed
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize, weight=weight, slant=slant,
                          underline=underline, overstrike=overstrike, justify=justify, anchor=anchor)
        features.Highlight(self, command=command)


class IconButton(virtual.Widget):
    """A button with an icon on the left side"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (120, 40),
        *,
        text: str = "Button",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s",
                               "nw", "ne", "sw", "se"] = "w",
        command: typing.Callable | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `text`: text of the widget
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the text
        * `slant`: slant of the text
        * `underline`: whether the text is underline
        * `overstrike`: whether the text is overstrike
        * `justify`: justify mode of the text
        * `anchor`: anchor of the text
        * `command`: a function that is triggered when the button is pressed
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        if image is not None:
            images.StillImage(self, ((size[1]-size[0]) / 2, 0), image=image)
        texts.Information(self, (size[1] - size[0]/2, 0), text=text,
                          family=family, fontsize=fontsize, weight=weight, slant=slant,
                          underline=underline, overstrike=overstrike, justify=justify, anchor=anchor)
        features.Button(self, command=command)


class Slider(virtual.Widget):
    """A slider for visually resizing values"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (400, 30),
        *,
        command: typing.Callable | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `command`: a function that is triggered when the button is pressed
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        self.value: float = 0
        self.command = command
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(
                self, (0, size[1]/3), (size[0], size[1]/3), name=".out")
            shapes.Rectangle(
                self, (0, size[1]/3), (size[0], size[1]/3), name=".in")
            shapes.Rectangle(self, size=(size[1]/3, size[1]))
        else:
            shapes.SemicircularRectangle(
                self, (0, size[1]*2/5), (size[0], size[1]/5), name=".out")
            shapes.SemicircularRectangle(
                self, (0, size[1]*2/5), (size[1]/2, size[1]/5), name=".in")
            shapes.Oval(self, (0, 0), (size[1], size[1]), name=".out")
            shapes.Oval(self, (size[1]/4, size[1]/4),
                        (size[1]/2, size[1]/2), name=".in")
        features.Slider(self)

    def get(self) -> float:
        """Get the value of the slider"""
        return self.value

    def set(self, value: float) -> typing.Any:
        """Set the value of the slider"""
        value = 1 if value > 1 else 0 if value < 0 else value
        delta = (value-self.value) * (self.size[0]-self.size[1])
        if value == self.value:
            return
        self.value = value
        for shape in self._shapes[2:]:
            shape.move(delta, 0)
        self._shapes[1].coords(
            (self.size[1]/2 + (self.size[0]-self.size[1]) * self.value, self._shapes[1].size[1]))
        if self.command is not None:
            return self.command(self.value)
