"""All standard Widgets"""

import itertools
import math
import typing
import warnings

from ..animation import animations, controllers
from ..core import constants, containers, virtual
from ..toolbox import enhanced, tools
from . import features, images, shapes, texts
from ._auxiliary import _AuxiliaryButton, _AuxiliaryInputBox, _AuxiliaryLabel

__all__ = [
    "Text",
    "Image",
    "Label",
    "Button",
    "Switch",
    "InputBox",
    "ToggleButton",
    "CheckButton",
    "RadioButton",
    "ProgressBar",
    "UnderlineButton",
    "HighlightButton",
    "IconButton",
    "Slider",
    "SegmentedButton",
    "SpinBox",
]


class Text(virtual.Widget):
    """Text widget, generally used to display plain text"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s",
                               "nw", "ne", "sw", "se", "center"] = "nw",
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `text`: text of the widget
        * `family`: font family
        * `fontsize`: font size
        * `weight`: weight of the text
        * `slant`: slant of the text
        * `underline`: whether the text is underline
        * `overstrike`: whether the text is overstrike
        * `justify`: justify mode of the text
        * `anchor`: anchor of the text
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, (0, 0),
                                name=name, through=through, animation=animation)
        texts.Information(self, text=text, family=family, fontsize=fontsize,
                          weight=weight, slant=slant, underline=underline,
                          overstrike=overstrike, justify=justify, anchor=anchor)

    def get(self) -> str:
        """Get the text of the widget"""
        return self._texts[0].get()

    def set(self, text: str) -> None:
        """Set the text of the widget"""
        return self._texts[0].set(text)


class Image(virtual.Widget):
    """Image widget, generally used to display normal still image"""

    def __init__(
        self,
        master: "containers.Canvas",
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
        *,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, (0, 0),
                                name=name, through=through, animation=animation)
        if image is not None:
            if size is None:
                images.StillImage(self, image=image)
            else:
                images.StillImage(self, image=image.scale(
                    size[0]/image.width(), size[1]/image.height()))

    def get(self) -> enhanced.PhotoImage:
        """Get the image of the widget"""
        if (image := self._images[0].image) is not None:
            return image
        return self._images[0]._initail_image

    def set(self, image: enhanced.PhotoImage | None) -> None:
        """Set the image of the widget"""
        self._images[0]._initail_image = image
        if image is not None:
            image = image.scale(*self.master.ratios)
        self._images[0].image = image
        self.master.itemconfigure(self._images[0].items[0], image=image)


class Label(virtual.Widget):
    """Label widget, which is generally used to display key information"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s", "nw",
                               "ne", "sw", "se", "center"] = "center",
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
        if size is None:
            size = tools.get_text_size(text, family, fontsize, padding=10)
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize,
                          weight=weight, slant=slant, underline=underline,
                          overstrike=overstrike, justify=justify, anchor=anchor)
        features.LabelFeature(self)


class Button(virtual.Widget):
    """Button widget, typically used to trigger a function"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s", "nw",
                               "ne", "sw", "se", "center"] = "center",
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
        if size is None:
            size = tools.get_text_size(text, family, fontsize, padding=10)
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize,
                          weight=weight, slant=slant, underline=underline,
                          overstrike=overstrike, justify=justify, anchor=anchor)
        features.ButtonFeature(self, command=command)


class Switch(virtual.Widget):
    """Switch widget, typically used to control the turning of a function on and off"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        length: int = 60,
        *,
        default: bool | None = None,
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
        * `default`: default value of the widget
        * `command`: a function that is triggered when the switch is changed
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        virtual.Widget.__init__(self, master, position, (length, length / 2),
                                state="normal-off", name=name,
                                through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self, name=".out")
            shapes.Rectangle(self, name=".in", relative_position=(
                length/10, length/10), size=(length*3/10, length*3/10), animation=False)
        else:
            shapes.SemicircularRectangle(self)
            shapes.Oval(self, relative_position=(length/10, length/10),
                        size=(length*3/10, length*3/10), animation=False)
        if image is not None:
            images.StillImage(self, image=image)
        features.SwitchFeature(self, command=command)
        if default is not None:
            self.set(default)

    def get(self) -> bool:
        """Get the state of the switch"""
        return self.state.endswith("on")

    def set(self, value: bool) -> None:
        """Set the state of the switch"""
        if self.get() == bool(value):
            return
        self.update(
            f"{self.state.split('-')[0]}-{'on' if value else 'off'}", no_delay=True)
        dx = self._shapes[0].size[0]/2 if value else -self._shapes[0].size[0]/2
        animations.MoveComponent(
            self._shapes[1], 250, (dx, 0), controller=controllers.smooth, fps=60).start()


class InputBox(virtual.Widget):
    """Input box widget, generally used to enter certain information on a single line"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
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
        if size is None:
            size = 200, tools.get_text_size(
                "", family, fontsize, padding=10)[1]
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
        texts.SingleLineText(self, family=family, fontsize=fontsize,
                             weight=weight, slant=slant, underline=underline,
                             overstrike=overstrike, align=align, limit=limit,
                             show=show, placeholder=placeholder)
        features.InputBoxFeature(self)

    def get(self) -> str:
        """Get the value of the Entry"""
        return self._texts[0].get()

    def set(self, value: str) -> None:
        """Set the text value of the Entry"""
        self._texts[0].set(value)

    def append(self, value: str) -> None:
        """Append text to Entry"""
        self._texts[0].append(value)

    def delete(self, count: int) -> None:
        """Delete a specified amount of text"""
        self._texts[0].pop(count)

    def clear(self) -> None:
        """Clear the text value of the Entry"""
        self.set("")


class CheckButton(virtual.Widget):
    """Checkbox button widget, generally used to check some options"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        length: int = 30,
        *,
        default: bool | None = None,
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
        features.CheckButtonFeature(self, command=command)
        self._texts[0].disappear()
        if default is not None:
            self.set(default)

    def get(self) -> bool:
        """Get the state of the check button"""
        return self._texts[0].visible

    def set(self, value: bool) -> None:
        """Set the state of the check button"""
        if self.get() == bool(value):
            return
        if value:
            return self._texts[0].appear()
        self._texts[0].disappear()


class ToggleButton(virtual.Widget):
    """A button that can display information and switch statuses"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s", "nw",
                               "ne", "sw", "se", "center"] = "center",
        default: bool | None = None,
        command: typing.Callable[[bool], typing.Any] | None = None,
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
        * `default`: default state of the widget
        * `command`: a function that is triggered when the state of check button is on
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        if size is None:
            size = tools.get_text_size(text, family, fontsize, padding=10)
        virtual.Widget.__init__(self, master, position, size, state="normal-off",
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize,
                          weight=weight, slant=slant, underline=underline,
                          overstrike=overstrike, justify=justify, anchor=anchor)
        features.ToggleButtonFeature(self, command=command)
        if default is not None:
            self.set(default)

    def get(self) -> bool:
        """Get the state of the check button"""
        return self.state.endswith("on")

    def set(self, value: bool) -> None:
        """Set the state of the switch"""
        if self.get() == bool(value):
            return
        self.update(f"{self.state.split('-')[0]}-{'on' if value else 'off'}")


class RadioButton(virtual.Widget):
    """Radio button widget, generally used to select one of several options"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        length: int = 30,
        *,
        default: bool | None = None,
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
        features.RadioButtonFeature(self, command=command)
        if default is not None:
            self.set(default)

    def get(self) -> bool:
        """Get the state of the radio button"""
        return self._shapes[1].visible

    def set(self, value: bool) -> None:
        """Set the state of the radio button"""
        if self.get() == bool(value):
            return
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
            shapes.SemicircularRectangle(self, name=".in", size=(self.size[1]*0.7, self.size[1]*0.7),
                                         relative_position=(self.size[1]*0.15, self.size[1]*0.15))
        if image is not None:
            images.StillImage(self, image=image)
        features.ProgressBarFeature(self)
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
            self._shapes[1].coords((self.size[1]*0.7 + (self.size[0]-self.size[1]
                                   * 0.3-self._shapes[1].size[1]) * self.value, self._shapes[1].size[1]))

        if self.value == 1 and self.command is not None:
            self.command()


class UnderlineButton(virtual.Widget):
    """Underline button, generally used to display web links"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s", "nw",
                               "ne", "sw", "se", "center"] = "center",
        command: typing.Callable | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = False,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
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
        virtual.Widget.__init__(self, master, position, (0, 0),
                                name=name, through=through, animation=animation)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize,
                          weight=weight, slant=slant, underline=underline,
                          overstrike=overstrike, justify=justify, anchor=anchor)
        features.Underline(self, command=command)


class HighlightButton(virtual.Widget):
    """Highlight button, no outline, which added a highlight effect"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s", "nw",
                               "ne", "sw", "se", "center"] = "center",
        command: typing.Callable | None = None,
        image: enhanced.PhotoImage | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
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
        virtual.Widget.__init__(self, master, position, (0, 0),
                                name=name, through=through, animation=animation)
        if image is not None:
            images.StillImage(self, image=image)
        texts.Information(self, text=text, family=family, fontsize=fontsize,
                          weight=weight, slant=slant, underline=underline,
                          overstrike=overstrike, justify=justify, anchor=anchor)
        features.Highlight(self, command=command)


class IconButton(virtual.Widget):
    """A button with an icon on the left side"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
        *,
        text: str = "",
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s", "nw",
                               "ne", "sw", "se", "center"] = "w",
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
        if size is None:
            size = tools.get_text_size(text, family, fontsize, padding=10)
            size = size[0] + size[1] - 10, size[1]
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        if image is not None:
            images.StillImage(self, ((size[1]-size[0]) / 2, 0), image=image)
        texts.Information(self, (size[1] - size[0]/2, 0), text=text,
                          family=family, fontsize=fontsize, weight=weight,
                          slant=slant, underline=underline, overstrike=overstrike,
                          justify=justify, anchor=anchor)
        features.ButtonFeature(self, command=command)


class Slider(virtual.Widget):
    """A slider for visually resizing values"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] = (400, 30),
        *,
        default: float | None = None,
        command: typing.Callable | None = None,
        name: str | None = None,
        through: bool = False,
        animation: bool = True,
    ) -> None:
        """
        * `master`: parent canvas
        * `position`: position of the widget
        * `size`: size of the widget
        * `default`: default value of the widget
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
                self, (0, size[1]*5/11), (size[0], size[1]/11), name=".out")
            shapes.Rectangle(
                self, (0, size[1]*5/11), (size[1]/5, size[1]/11), name=".in")
            shapes.Rectangle(self, (0, 0), (size[1]*2/5, size[1]))
        else:
            shapes.SemicircularRectangle(
                self, (0, size[1]*2/5), (size[0], size[1]/5), name=".out")
            shapes.SemicircularRectangle(
                self, (0, size[1]*2/5), (size[1]/2, size[1]/5), name=".in")
            shapes.Oval(self, (0, 0), (size[1], size[1]), name=".out")
            shapes.Oval(self, (size[1]/4, size[1]/4),
                        (size[1]/2, size[1]/2), name=".in")
        features.SliderFeature(self)
        if default is not None:
            self.set(default)

    def get(self) -> float:
        """Get the value of the slider"""
        return self.value

    def set(self, value: float) -> typing.Any:
        """Set the value of the slider"""
        value = 1 if value > 1 else 0 if value < 0 else value
        if self.get() == value:
            return
        if isinstance(self._shapes[-1], shapes.Oval):
            delta = (value-self.value) * (self.size[0]-self.size[1])
        else:
            delta = (value-self.value) * (self.size[0]-self.size[1]*2/5)
        self.value = value
        for shape in self._shapes[2:]:
            shape.move(delta, 0)
        if isinstance(self._shapes[-1], shapes.Oval):
            self._shapes[1].coords(
                (self.size[1]/2 + (self.size[0]-self.size[1]) * self.value, self._shapes[1].size[1]))
        else:
            self._shapes[1].coords(
                (self.size[1]/5 + (self.size[0]-self.size[1]*2/5) * self.value, self._shapes[1].size[1]))
        if self.command is not None:
            return self.command(self.value)


class SegmentedButton(virtual.Widget):
    """A segmented button that can be used to toggle between multiple states"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        sizes: tuple[tuple[int, int], ...] = (),
        *,
        texts: tuple[str, ...] = (),
        family: str | None = None,
        fontsize: int | None = None,
        weight: typing.Literal['normal', 'bold'] = "normal",
        slant: typing.Literal['roman', 'italic'] = "roman",
        underline: bool = False,
        overstrike: bool = False,
        justify: typing.Literal["left", "center", "right"] = "left",
        anchor: typing.Literal["n", "e", "w", "s", "nw",
                               "ne", "sw", "se", "center"] = "center",
        default: int | None = None,
        commands: tuple[typing.Callable[[], typing.Any] | None, ...] = (),
        images: tuple[enhanced.PhotoImage | None, ...] = (),
        layout: typing.Literal["horizontal", "vertical"] = "horizontal",
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
        * `default`: default value of the widget
        * `commands`: a function that is triggered when the button is pressed
        * `images`: image of the widget
        * `layout`: layout mode of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        self.value: int | None = None
        if not sizes:
            if texts:
                sizes = tuple(tools.get_text_size(
                    text, family, fontsize, padding=10) for text in texts)
            else:
                sizes = (tools.get_text_size(
                    "", family, fontsize, padding=5),)
        widths, heights, length = *zip(*sizes), len(sizes)
        if not texts:
            sizes, length = (), 0
        if layout == "horizontal":
            total_size = sum(widths) + length*5 + 5, max(heights) + 10
        else:
            total_size = max(widths) + 10, sum(heights) + length*5 + 5
        virtual.Widget.__init__(self, master, position, total_size,
                                name=name, through=through, animation=animation)
        if constants.SYSTEM == "Windows10":
            shapes.Rectangle(self)
        else:
            shapes.RoundedRectangle(self)
        total_side_length = 5
        for i, pack in enumerate(itertools.zip_longest(sizes, texts, images, commands)):
            size, text, image, command = pack
            position = (total_side_length, 5) if layout == "horizontal" else (
                5, total_side_length)
            ToggleButton(self, position, size, text=text, family=family,
                         fontsize=fontsize, weight=weight, slant=slant,
                         underline=underline, overstrike=overstrike,
                         justify=justify, anchor=anchor, animation=animation,
                         image=image, through=True,
                         command=lambda _, i=i, command=command: (self.set(i), command() if command else None))
            total_side_length += size[layout == "vertical"] + 5
        if default is not None:
            self.set(default)

    def get(self) -> int | None:
        """
        Get the index of the child toggle button with a value of True.
        If not, None is returned.
        """
        return self.value

    def set(self, value: int | None) -> None:
        """Activate the child toggle button for the specified index"""
        for i, widget in enumerate(self._widgets):
            widget.set(i == value)
        self.value = value


class SpinBox(virtual.Widget):
    """A widget that makes it easy to enter numeric type data"""

    def __init__(
        self,
        master: containers.Canvas,
        position: tuple[int, int],
        size: tuple[int, int] | None = None,
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
        command: typing.Callable[[bool], typing.Any] | None = None,
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
        * `command`: a function that is triggered when the button is pressed
        * `image`: image of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        if size is None:
            size = 200, tools.get_text_size(
                "", family, fontsize, padding=10)[1]
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        InputBox(self, (0, 0), size, family=family, fontsize=fontsize, weight=weight,
                 slant=slant, underline=underline, overstrike=overstrike, align=align,
                 placeholder=placeholder, show=show, limit=limit, image=image,
                 through=through, animation=animation)
        h = size[1]/2 - 6
        w = h/constants.GOLDEN_RATIO if constants.SYSTEM == "Windows10" else 2*h
        Button(self, (size[0]-w-4, 4), (w, h), text="▲", fontsize=14, through=True,
               command=lambda: command(True) if command is not None else self.change(True))
        Button(self, (size[0]-w-4, size[1]/2 + 2), (w, h), text="▼", fontsize=14, through=True,
               command=lambda: command(False) if command is not None else self.change(False))
        features.SpinBoxFeature(self, command=command)

    def change(self, up: bool) -> None:
        """Try change the current value"""
        if not (value := self._widgets[0].get()):
            return self._widgets[0].set("0")
        try:
            value = float(value) + (1 if up else -1)
            if math.isclose(value, int_value := int(value)):
                value = int_value
            self._widgets[0].set(value)
        except ValueError:
            pass

    def get(self) -> str:
        """Get the value of the Entry"""
        return self._widgets[0].get()

    def set(self, value: str) -> None:
        """Set the text value of the Entry"""
        self._widgets[0].set(value)

    def append(self, value: str) -> None:
        """Append text to Entry"""
        self._widgets[0].append(value)

    def delete(self, count: int) -> None:
        """Delete a specified amount of text"""
        self._widgets[0].delete(count)

    def clear(self) -> None:
        """Clear the text value of the Entry"""
        self._widgets[0].clear()


class OptionButton(virtual.Widget):
    """A Button with multiple options"""

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
        default: str | None = None,
        options: tuple[tuple[str, typing.Callable | None], ...] | None = None,
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
        * `default`: default value of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        warnings.warn("The class is not fully implemented yet!",
                      FutureWarning, stacklevel=2)
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        _AuxiliaryLabel(self, (0, 0), (size[0]-size[1]-1, size[1]), ignore="right",
                        family=family, fontsize=fontsize, weight=weight, slant=slant,
                        underline=underline, overstrike=overstrike)
        _AuxiliaryButton(self, (size[0]-size[1], 0),
                         (size[1], size[1]), ignore="left", text="▼",
                         through=True, command=self.pop_menu)
        features.OptionButtonFeature(self)
        self.options = options
        if default is not None:
            self.set(default)

    def pop_menu(self) -> None:
        """"""
        if isinstance(self._widgets[-1], SegmentedButton):
            return self._widgets[-1].destroy()
        if self.options is None:
            return
        sizes = ((self.size[0]-10, self.size[1]),)*len(self.options)
        texts, commands = zip(*self.options)
        commands = tuple((lambda i=i, command=command: (self._widgets[0]._texts[0].set(texts[i]), command(
        ) if command is not None else None, print(i), self.pop_menu())) for i, command in enumerate(commands))
        SegmentedButton(
            self, (0, self.size[1]+5), sizes, texts=texts, commands=commands, layout="vertical")

    def get(self) -> str:
        """"""

    def set(self, value: str) -> None:
        """"""

    def append(self, *values: str) -> None:
        """"""

    def remove(self, *values: str) -> None:
        """"""


class ComboBox(virtual.Widget):
    """"""

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
        default: str | None = None,
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
        * `default`: default value of the widget
        * `name`: name of the widget
        * `through`: wether detect another widget under the widget
        * `animation`: wether enable animation
        """
        warnings.warn("The class is not fully implemented yet!",
                      FutureWarning, stacklevel=2)
        virtual.Widget.__init__(self, master, position, size,
                                name=name, through=through, animation=animation)
        _AuxiliaryInputBox(
            self, (0, 0), (size[0]-size[1]-1, size[1]), ignore="right")
        _AuxiliaryButton(self, (size[0]-size[1], 0),
                         (size[1], size[1]), ignore="left", text="▼")
        if default is not None:
            self.set(default)
