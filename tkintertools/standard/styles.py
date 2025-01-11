"""All standard `Style` classes"""

from __future__ import annotations

__all__ = [
    "ButtonStyle",
    "CheckBoxStyle",
    "ToggleButtonStyle",
    "HighlightButtonStyle",
    "IconButtonStyle",
    "InputBoxStyle",
    "LabelStyle",
    "OptionButtonStyle",
    "ProgressBarStyle",
    "RadioBoxStyle",
    "SegmentedButtonStyle",
    "SliderStyle",
    "SwitchStyle",
    "TextStyle",
    "TooltipStyle",
    "SpinnerStyle",
    "UnderlineButtonStyle",
]

import types
import typing

import typing_extensions

from ..core import virtual


class TextStyle(virtual.Style):
    """Style of Text"""

    light = {
        "Information": {
            "normal": {"fill": "#1A1A1A"},
        }
    }

    dark = {
        "Information": {
            "normal": {"fill": "#F1F1F1"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        fg: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `fg`: the foreground color of the widget

        states: "normal", "hover", "active"
        """
        self._set(theme, fg, fill=-1)
        self.widget.update()


class LabelStyle(virtual.Style):
    """Style of Label"""

    light = {
        "Information": {
            "normal": {"fill": "#1A1A1A"},
            "hover": {"fill": "#1A1A1A"},
        },
        "Rectangle": {
            "normal": {"fill": "#FBFBFB", "outline": "#DCDCDC"},
            "hover": {"fill": "#F6F6F6", "outline": "#DCDCDC"},
        },
        "RoundedRectangle": {
            "normal": {"fill": "#FBFBFB", "outline": "#DCDCDC"},
            "hover": {"fill": "#F6F6F6", "outline": "#DCDCDC"},
        }
    }

    dark = {
        "Information": {
            "normal": {"fill": "#F1F1F1"},
            "hover": {"fill": "#F1F1F1"},
        },
        "Rectangle": {
            "normal": {"fill": "#2B2B2B", "outline": "#3D3D3D"},
            "hover": {"fill": "#323232", "outline": "#3D3D3D"},
        },
        "RoundedRectangle": {
            "normal": {"fill": "#2B2B2B", "outline": "#3D3D3D"},
            "hover": {"fill": "#323232", "outline": "#3D3D3D"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        fg: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `fg`: the foreground color of the widget.
        * `bg`: the background color of the widget.
        * `ol`: the outline color of the widget.

        states: "normal", "hover", "active"
        """
        self._set(theme, fg, fill=-1)
        self._set(theme, bg, fill=0)
        self._set(theme, ol, outline=0)
        self.widget.update()


class ButtonStyle(LabelStyle):
    """Style of Button"""

    light = {
        "Information": {
            "normal": {"fill": "#1A1A1A"},
            "hover": {"fill": "#1A1A1A"},
            "active": {"fill": "#1A1A1A"},
        },
        "Rectangle": {
            "normal": {"fill": "#E1E1E1", "outline": "#C0C0C0"},
            "hover": {"fill": "#E5F1FB", "outline": "#288CDB"},
            "active": {"fill": "#CCE4F7", "outline": "#4884B4"},
        },
        "RoundedRectangle": {
            "normal": {"fill": "#FEFEFE", "outline": "#DCDCDC"},
            "hover": {"fill": "#FAFAFA", "outline": "#DCDCDC"},
            "active": {"fill": "#F3F3F3", "outline": "#DCDCDC"},
        }
    }

    dark = {
        "Information": {
            "normal": {"fill": "#F1F1F1"},
            "hover": {"fill": "#F1F1F1"},
            "active": {"fill": "#F1F1F1"},
        },
        "Rectangle": {
            "normal": {"fill": "#333333", "outline": "#333333"},
            "hover": {"fill": "#333333", "outline": "#858585"},
            "active": {"fill": "#666666", "outline": "#666666"},
        },
        "RoundedRectangle": {
            "normal": {"fill": "#373737", "outline": "#3D3D3D"},
            "hover": {"fill": "#3C3C3C", "outline": "#3D3D3D"},
            "active": {"fill": "#323232", "outline": "#3D3D3D"},
        }
    }


class SwitchStyle(virtual.Style):
    """Style of Switch"""

    states = ("normal-off", "hover-off", "active-off",
              "normal-on", "hover-on", "active-on", "disabled")

    light = {
        "Oval": {
            "normal-off": {"fill": "#5D5D5E", "outline": "#5D5D5E"},
            "hover-off": {"fill": "#585859", "outline": "#585859"},
            "active-off": {"fill": "#545556", "outline": "#545556"},
            "normal-on": {"fill": "#FFFFFF", "outline": "#FFFFFF"},
            "hover-on": {"fill": "#FFFFFF", "outline": "#FFFFFF"},
            "active-on": {"fill": "#FFFFFF", "outline": "#FFFFFF"},
        },
        "Rectangle.in": {
            "normal-off": {"fill": "#5D5D5E", "outline": "#5D5D5E"},
            "hover-off": {"fill": "#585859", "outline": "#585859"},
            "active-off": {"fill": "#545556", "outline": "#545556"},
            "normal-on": {"fill": "#FFFFFF", "outline": "#FFFFFF"},
            "hover-on": {"fill": "#FFFFFF", "outline": "#FFFFFF"},
            "active-on": {"fill": "#FFFFFF", "outline": "#FFFFFF"},
        },
        "Rectangle.out": {
            "normal-off": {"fill": "#F5F5F7", "outline": "#B8B8B9"},
            "hover-off": {"fill": "#E7E8EA", "outline": "#858687"},
            "active-off": {"fill": "#DEDFE2", "outline": "#848586"},
            "normal-on": {"fill": "#0067C0", "outline": "#0067C0"},
            "hover-on": {"fill": "#1975C5", "outline": "#1975C5"},
            "active-on": {"fill": "#2D7FC6", "outline": "#2072B9"},
        },
        "SemicircularRectangle": {
            "normal-off": {"fill": "#F5F5F7", "outline": "#B8B8B9"},
            "hover-off": {"fill": "#E7E8EA", "outline": "#858687"},
            "active-off": {"fill": "#DEDFE2", "outline": "#848586"},
            "normal-on": {"fill": "#0067C0", "outline": "#0067C0"},
            "hover-on": {"fill": "#1975C5", "outline": "#1975C5"},
            "active-on": {"fill": "#2D7FC6", "outline": "#2072B9"},
        }
    }

    dark = {
        "Oval": {
            "normal-off": {"fill": "#CECECE", "outline": "#CECECE"},
            "hover-off": {"fill": "#D2D2D2", "outline": "#D2D2D2"},
            "active-off": {"fill": "#D4D4D4", "outline": "#D4D4D4"},
            "normal-on": {"fill": "#000000", "outline": "#000000"},
            "hover-on": {"fill": "#000000", "outline": "#000000"},
            "active-on": {"fill": "#000000", "outline": "#000000"},
        },
        "Rectangle.in": {
            "normal-off": {"fill": "#CECECE", "outline": "#CECECE"},
            "hover-off": {"fill": "#D2D2D2", "outline": "#D2D2D2"},
            "active-off": {"fill": "#D4D4D4", "outline": "#D4D4D4"},
            "normal-on": {"fill": "#000000", "outline": "#000000"},
            "hover-on": {"fill": "#000000", "outline": "#000000"},
            "active-on": {"fill": "#000000", "outline": "#000000"},
        },
        "Rectangle.out": {
            "normal-off": {"fill": "#272727", "outline": "#9E9E9E"},
            "hover-off": {"fill": "#3B3B3B", "outline": "#A3A3A3"},
            "active-off": {"fill": "#404040", "outline": "#A3A3A3"},
            "normal-on": {"fill": "#4CC2FF", "outline": "#4CC2FF"},
            "hover-on": {"fill": "#49B3EB", "outline": "#49B3EB"},
            "active-on": {"fill": "#49A8DA", "outline": "#5DBCED"},
        },
        "SemicircularRectangle": {
            "normal-off": {"fill": "#272727", "outline": "#9E9E9E"},
            "hover-off": {"fill": "#3B3B3B", "outline": "#A3A3A3"},
            "active-off": {"fill": "#404040", "outline": "#A3A3A3"},
            "normal-on": {"fill": "#4CC2FF", "outline": "#4CC2FF"},
            "hover-on": {"fill": "#49B3EB", "outline": "#49B3EB"},
            "active-on": {"fill": "#49A8DA", "outline": "#5DBCED"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        bg_slot: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol_slot: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg_dot: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol_dot: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `bg_slot`: the background color of the widget.
        * `ol_slot`: the outline color of the widget.
        * `bg_dot`: the inside background color of the widget.
        * `ol_dot`: the inside outline color of the widget.

        states: "normal-off", "hover-off", "active-off", "normal-on",
        "hover-on", "active-on"
        """
        self._set(theme, bg_slot, fill=("Rectangle.out", "SemicircularRectangle"))
        self._set(theme, ol_slot, outline=("Rectangle.out", "SemicircularRectangle"))
        self._set(theme, bg_dot, fill=("Rectangle.in", "Oval"))
        self._set(theme, ol_dot, fill=("Rectangle.in", "Oval"))
        self.widget.update()


class InputBoxStyle(virtual.Style):
    """Style of InputBox"""

    light = {
        "Rectangle": {
            "normal": {"fill": "#FBFBFB", "outline": "#C0C0C0"},
            "hover": {"fill": "#F6F6F6", "outline": "#414141"},
            "active": {"fill": "#FFFFFF", "outline": "#288CDB"},
        },
        "RoundedRectangle.in": {
            "normal": {"fill": "#FBFBFB", "outline": "#E5E5E5"},
            "hover": {"fill": "#F6F6F6", "outline": "#E5E5E5"},
            "active": {"fill": "#FFFFFF", "outline": "#E5E5E5"},
        },
        "RoundedRectangle.out": {
            "normal": {"fill": "#868686", "outline": "#868686"},
            "hover": {"fill": "#868686", "outline": "#868686"},
            "active": {"fill": "#0067C0", "outline": "#0067C0"},
        },
        "SingleLineText": {
            "normal": {"fill": "#1A1A1A"},
            "hover": {"fill": "#1A1A1A"},
            "active": {"fill": "#1A1A1A"},
        }
    }

    dark = {
        "Rectangle": {
            "normal": {"fill": "#131313", "outline": "#797979"},
            "hover": {"fill": "#0C0C0C", "outline": "#A5A5A5"},
            "active": {"fill": "#090909", "outline": "#0078D7"},
        },
        "RoundedRectangle.in": {
            "normal": {"fill": "#2D2D2D", "outline": "#303030"},
            "hover": {"fill": "#323232", "outline": "#303030"},
            "active": {"fill": "#1F1F1F", "outline": "#303030"},
        },
        "RoundedRectangle.out": {
            "normal": {"fill": "#8F8F8F", "outline": "#8F8F8F"},
            "hover": {"fill": "#8F8F8F", "outline": "#8F8F8F"},
            "active": {"fill": "#4CC2FF", "outline": "#4CC2FF"},
        },
        "SingleLineText": {
            "normal": {"fill": "#F1F1F1"},
            "hover": {"fill": "#F1F1F1"},
            "active": {"fill": "#F1F1F1"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        fg: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg_bar: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `fg`: the foreground color of the widget.
        * `bg`: the background color of the widget.
        * `ol`: the outline color of the widget.
        * `bg_bar`: the highlight bar of the widget (Only for Windows11 theme)

        states: "normal", "hover", "active"
        """
        self._set(theme, fg, fill="SingleLineText")
        self._set(theme, bg, fill=("Rectangle", "RoundedRectangle.in"))
        self._set(theme, ol, outline=("Rectangle", "RoundedRectangle.in"))
        self._set(theme, bg_bar, fill="RoundedRectangle.out", outline="RoundedRectangle.out")
        self.widget.update()


class ToggleButtonStyle(virtual.Style):
    """Style of ToggleButton"""

    states = ("normal-off", "hover-off", "active-off",
              "normal-on", "hover-on", "active-on", "disabled")

    light = {
        "Information": {
            "normal-off": {"fill": "#1A1A1A"},
            "hover-off": {"fill": "#1A1A1A"},
            "active-off": {"fill": "#1A1A1A"},
            "normal-on": {"fill": "#1A1A1A"},
            "hover-on": {"fill": "#1A1A1A"},
            "active-on": {"fill": "#1A1A1A"},
        },
        "Rectangle": {
            "normal-off": {"fill": "#FEFEFE", "outline": "#DCDCDC"},
            "hover-off": {"fill": "#FAFAFA", "outline": "#DCDCDC"},
            "active-off": {"fill": "#F3F3F3", "outline": "#DCDCDC"},
            "normal-on": {"fill": "#49A8DA", "outline": "#49B3EB"},
            "hover-on": {"fill": "#49B3EB", "outline": "#49B3EB"},
            "active-on": {"fill": "#0078D7", "outline": "#49B3EB"},
        },
        "RoundedRectangle": {
            "normal-off": {"fill": "#FEFEFE", "outline": "#DCDCDC"},
            "hover-off": {"fill": "#FAFAFA", "outline": "#DCDCDC"},
            "active-off": {"fill": "#F3F3F3", "outline": "#DCDCDC"},
            "normal-on": {"fill": "#49A8DA", "outline": "#49B3EB"},
            "hover-on": {"fill": "#49B3EB", "outline": "#49B3EB"},
            "active-on": {"fill": "#0078D7", "outline": "#49B3EB"},
        }
    }

    dark = {
        "Information": {
            "normal-off": {"fill": "#F1F1F1"},
            "hover-off": {"fill": "#F1F1F1"},
            "active-off": {"fill": "#F1F1F1"},
            "normal-on": {"fill": "#F1F1F1"},
            "hover-on": {"fill": "#F1F1F1"},
            "active-on": {"fill": "#F1F1F1"},
        },
        "Rectangle": {
            "normal-off": {"fill": "#333333", "outline": "#333333"},
            "hover-off": {"fill": "#333333", "outline": "#858585"},
            "active-off": {"fill": "#666666", "outline": "#666666"},
            "normal-on": {"fill": "#0067C0", "outline": "#0078D7"},
            "hover-on": {"fill": "#1975C5", "outline": "#1975C5"},
            "active-on": {"fill": "#2D7FC6", "outline": "#2072B9"},
        },
        "RoundedRectangle": {
            "normal-off": {"fill": "#373737", "outline": "#3D3D3D"},
            "hover-off": {"fill": "#3C3C3C", "outline": "#3D3D3D"},
            "active-off": {"fill": "#323232", "outline": "#3D3D3D"},
            "normal-on": {"fill": "#0067C0", "outline": "#0078D7"},
            "hover-on": {"fill": "#1975C5", "outline": "#1975C5"},
            "active-on": {"fill": "#2D7FC6", "outline": "#2072B9"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        fg: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `fg`: the foreground color of the widget.
        * `bg`: the background color of the widget.
        * `ol`: the outline color of the widget.

        states: "normal-off", "hover-off", "active-off", "normal-on",
        "hover-on", "active-on"
        """
        self._set(theme, fg, fill=-1)
        self._set(theme, bg, fill=0)
        self._set(theme, ol, outline=0)
        self.widget.update()


class CheckBoxStyle(ToggleButtonStyle):
    """Style of CheckBox"""

    states = ("normal-off", "hover-off", "active-off",
              "normal-on", "hover-on", "active-on", "disabled")

    light = {
        "Information": {
            "normal-off": {"fill": ""},
            "hover-off": {"fill": ""},
            "active-off": {"fill": ""},
            "normal-on": {"fill": "#F1F1F1"},
            "hover-on": {"fill": "#F1F1F1"},
            "active-on": {"fill": "#F1F1F1"},
        },
        "Rectangle": {
            "normal-off": {"fill": "#E1E1E1", "outline": "#C0C0C0"},
            "hover-off": {"fill": "#E5F1FB", "outline": "#288CDB"},
            "active-off": {"fill": "#CCE4F7", "outline": "#4884B4"},
            "normal-on": {"fill": "#49A8DA", "outline": "#49B3EB"},
            "hover-on": {"fill": "#49B3EB", "outline": "#49B3EB"},
            "active-on": {"fill": "#0078D7", "outline": "#49B3EB"},
        },
        "RoundedRectangle": {
            "normal-off": {"fill": "#FEFEFE", "outline": "#DCDCDC"},
            "hover-off": {"fill": "#FAFAFA", "outline": "#DCDCDC"},
            "active-off": {"fill": "#F3F3F3", "outline": "#DCDCDC"},
            "normal-on": {"fill": "#49A8DA", "outline": "#49B3EB"},
            "hover-on": {"fill": "#49B3EB", "outline": "#49B3EB"},
            "active-on": {"fill": "#0078D7", "outline": "#49B3EB"},
        }
    }

    dark = {
        "Information": {
            "normal-off": {"fill": ""},
            "hover-off": {"fill": ""},
            "active-off": {"fill": ""},
            "normal-on": {"fill": "#1A1A1A"},
            "hover-on": {"fill": "#1A1A1A"},
            "active-on": {"fill": "#1A1A1A"},
        },
        "Rectangle": {
            "normal-off": {"fill": "#333333", "outline": "#333333"},
            "hover-off": {"fill": "#333333", "outline": "#858585"},
            "active-off": {"fill": "#666666", "outline": "#666666"},
            "normal-on": {"fill": "#0067C0", "outline": "#0078D7"},
            "hover-on": {"fill": "#1975C5", "outline": "#1975C5"},
            "active-on": {"fill": "#2D7FC6", "outline": "#2072B9"},
        },
        "RoundedRectangle": {
            "normal-off": {"fill": "#373737", "outline": "#3D3D3D"},
            "hover-off": {"fill": "#3C3C3C", "outline": "#3D3D3D"},
            "active-off": {"fill": "#323232", "outline": "#3D3D3D"},
            "normal-on": {"fill": "#0067C0", "outline": "#0078D7"},
            "hover-on": {"fill": "#1975C5", "outline": "#1975C5"},
            "active-on": {"fill": "#2D7FC6", "outline": "#2072B9"},
        }
    }


class RadioBoxStyle(virtual.Style):
    """Style of RadioGroup"""

    light = {
        "Oval.in": {
            "normal": {"fill": "#32BF42", "outline": "#32BF42"},
            "hover": {"fill": "#06B025", "outline": "#06B025"},
            "active": {"fill": "#06B025", "outline": "#06B025"},
        },
        "Oval.out": {
            "normal": {"fill": "#FEFEFE", "outline": "#DCDCDC"},
            "hover": {"fill": "#FAFAFA", "outline": "#DCDCDC"},
            "active": {"fill": "#F3F3F3", "outline": "#DCDCDC"},
        },
        "Rectangle.in": {
            "normal": {"fill": "#32BF42", "outline": "#32BF42"},
            "hover": {"fill": "#06B025", "outline": "#06B025"},
            "active": {"fill": "#06B025", "outline": "#06B025"},
        },
        "Rectangle.out": {
            "normal": {"fill": "#FEFEFE", "outline": "#DCDCDC"},
            "hover": {"fill": "#FAFAFA", "outline": "#288CDB"},
            "active": {"fill": "#F3F3F3", "outline": "#4884B4"},
        }
    }

    dark = {
        "Oval.in": {
            "normal": {"fill": "#4CC2FF", "outline": "#4CC2FF"},
            "hover": {"fill": "#49B3EB", "outline": "#49B3EB"},
            "active": {"fill": "#49B3EB", "outline": "#49B3EB"},
        },
        "Oval.out": {
            "normal": {"fill": "#373737", "outline": "#3D3D3D"},
            "hover": {"fill": "#3C3C3C", "outline": "#3D3D3D"},
            "active": {"fill": "#323232", "outline": "#3D3D3D"},
        },
        "Rectangle.in": {
            "normal": {"fill": "#4CC2FF", "outline": "#4CC2FF"},
            "hover": {"fill": "#49B3EB", "outline": "#49B3EB"},
            "active": {"fill": "#49B3EB", "outline": "#49B3EB"},
        },
        "Rectangle.out": {
            "normal": {"fill": "#373737", "outline": "#3D3D3D"},
            "hover": {"fill": "#3C3C3C", "outline": "#858585"},
            "active": {"fill": "#323232", "outline": "#666666"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        bg_box: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol_box: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg_dot: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol_dot: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `bg_box`: the background color of the widget.
        * `ol_box`: the outline color of the widget.
        * `bg_dot`: the inside background color of the widget.
        * `ol_dot`: the inside outline color of the widget.

        states: "normal", "hover", "active"
        """
        self._set(theme, bg_box, fill=0)
        self._set(theme, ol_box, outline=0)
        self._set(theme, bg_dot, fill=1)
        self._set(theme, ol_dot, outline=1)
        self.widget.update()


class ProgressBarStyle(virtual.Style):
    """Style of ProgressBar"""

    light = {
        "Rectangle.in": {
            "normal": {"fill": "#32BF42", "outline": "#32BF42"},
            "hover": {"fill": "#06B025", "outline": "#06B025"},
        },
        "Rectangle.out": {
            "normal": {"fill": "#E1E1E1", "outline": "#C0C0C0"},
            "hover": {"fill": "#E5F1FB", "outline": "#288CDB"},
        },
        "SemicircularRectangle.in": {
            "normal": {"fill": "#32BF42", "outline": "#32BF42"},
            "hover": {"fill": "#06B025", "outline": "#06B025"},
        },
        "SemicircularRectangle.out": {
            "normal": {"fill": "#FBFBFB", "outline": "#DCDCDC"},
            "hover": {"fill": "#F6F6F6", "outline": "#DCDCDC"},
        }
    }

    dark = {
        "Rectangle.in": {
            "normal": {"fill": "#4CC2FF", "outline": "#4CC2FF"},
            "hover": {"fill": "#49B3EB", "outline": "#49B3EB"},
        },
        "Rectangle.out": {
            "normal": {"fill": "#333333", "outline": "#333333"},
            "hover": {"fill": "#333333", "outline": "#858585"},
        },
        "SemicircularRectangle.in": {
            "normal": {"fill": "#4CC2FF", "outline": "#4CC2FF"},
            "hover": {"fill": "#49B3EB", "outline": "#49B3EB"},
        },
        "SemicircularRectangle.out": {
            "normal": {"fill": "#2B2B2B", "outline": "#3D3D3D"},
            "hover": {"fill": "#323232", "outline": "#3D3D3D"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        bg_slot: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol_slot: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg_bar: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol_bar: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `bg_slot`: the background color of the widget.
        * `ol_slot`: the outline color of the widget.
        * `bg_bar`: the inside background color of the widget.
        * `ol_bar`: the inside outline color of the widget.

        states: "normal", "hover"
        """
        self._set(theme, bg_slot, fill=0)
        self._set(theme, ol_slot, outline=0)
        self._set(theme, bg_bar, fill=1)
        self._set(theme, ol_bar, outline=1)
        self.widget.update()


class UnderlineButtonStyle(TextStyle):
    """Style of UnderlineButton"""

    light = {
        "Information": {
            "normal": {"fill": "#1A1A1A"},
            "hover": {"fill": "royalblue"},
            "active": {"fill": "#787878"},
        }
    }

    dark = {
        "Information": {
            "normal": {"fill": "#F1F1F1"},
            "hover": {"fill": "royalblue"},
            "active": {"fill": "#787878"},
        }
    }


class HighlightButtonStyle(TextStyle):
    """Style of HighlightButtonStyle"""

    light = {
        "Information": {
            "normal": {"fill": "grey"},
            "hover": {"fill": "#1F1F1F"},
            "active": {"fill": "#000000"},
        }
    }

    dark = {
        "Information": {
            "normal": {"fill": "grey"},
            "hover": {"fill": "#F1F1F1"},
            "active": {"fill": "#FFFFFF"},
        }
    }


class IconButtonStyle(LabelStyle):
    """Style of IconButtonStyle"""

    light = {
        "Information": {
            "normal": {"fill": "#1A1A1A"},
            "hover": {"fill": "#1A1A1A"},
            "active": {"fill": "#1A1A1A"},
        },
        "Rectangle": {
            "normal": {"fill": "#E1E1E1", "outline": "#C0C0C0"},
            "hover": {"fill": "#E5F1FB", "outline": "#288CDB"},
            "active": {"fill": "#CCE4F7", "outline": "#4884B4"},
        },
        "RoundedRectangle": {
            "normal": {"fill": "#FEFEFE", "outline": "#DCDCDC"},
            "hover": {"fill": "#FAFAFA", "outline": "#DCDCDC"},
            "active": {"fill": "#F3F3F3", "outline": "#DCDCDC"},
        }
    }

    dark = {
        "Information": {
            "normal": {"fill": "#F1F1F1"},
            "hover": {"fill": "#F1F1F1"},
            "active": {"fill": "#F1F1F1"},
        },
        "Rectangle": {
            "normal": {"fill": "#333333", "outline": "#333333"},
            "hover": {"fill": "#333333", "outline": "#858585"},
            "active": {"fill": "#666666", "outline": "#666666"},
        },
        "RoundedRectangle": {
            "normal": {"fill": "#373737", "outline": "#3D3D3D"},
            "hover": {"fill": "#3C3C3C", "outline": "#3D3D3D"},
            "active": {"fill": "#323232", "outline": "#3D3D3D"},
        }
    }


class SliderStyle(virtual.Style):
    """Style of Slider"""

    light = {
        "Oval.in": {
            "normal": {"fill": "#0067C0", "outline": "#0067C0"},
        },
        "Oval.out": {
            "normal": {"fill": "#FFFFFF", "outline": "#E8E8E8"},
        },
        "Rectangle.in": {
            "normal": {"fill": "#0078D7", "outline": "#0078D7"},
        },
        "Rectangle": {
            "normal": {"fill": "#0078D7", "outline": "#0078D7"},
            "hover": {"fill": "#000000", "outline": "#000000"},
            "active": {"fill": "#CCCCCC", "outline": "#CCCCCC"},
        },
        "Rectangle.out": {
            "normal": {"fill": "#878787", "outline": "#878787"},
        },
        "SemicircularRectangle.in": {
            "normal": {"fill": "#0067C0", "outline": "#0067C0"},
        },
        "SemicircularRectangle.out": {
            "normal": {"fill": "#878787", "outline": "#878787"},
        }
    }

    dark = {
        "Oval.in": {
            "normal": {"fill": "#4CC2FF", "outline": "#4CC2FF"},
        },
        "Oval.out": {
            "normal": {"fill": "#454545", "outline": "#454545"},
        },
        "Rectangle.in": {
            "normal": {"fill": "#429CE3", "outline": "#429CE3"},
        },
        "Rectangle": {
            "normal": {"fill": "#0078D7", "outline": "#0078D7"},
            "hover": {"fill": "#FFFFFF", "outline": "#FFFFFF"},
            "active": {"fill": "#767676", "outline": "#767676"},
        },
        "Rectangle.out": {
            "normal": {"fill": "#7C7C7C", "outline": "#7C7C7C"},
        },
        "SemicircularRectangle.in": {
            "normal": {"fill": "#4CC2FF", "outline": "#4CC2FF"},
        },
        "SemicircularRectangle.out": {
            "normal": {"fill": "#9E9E9E", "outline": "#9E9E9E"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        fg_slot: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg_slot: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg_pnt: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg_dot: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `fg_slot`: the foreground color of the widget.
        * `bg_slot`: the background color of the widget.
        * `bg_pnt`: the pointer color of the widget.
        * `bg_dot`: the pointer highlight part color of the widget (Only for
        Windows11 theme).

        states: "normal", "hover", "active"
        """
        self._set(theme, fg_slot, fill=1, outline=1)
        self._set(theme, bg_slot, fill=0, outline=0)
        self._set(theme, bg_pnt, fill=2, outline=2)
        self._set(theme, bg_dot, fill="Oval.in", outline="Oval.in")
        # Only works on Windows11 theme, compatible with other themes
        self.widget.update()


class SegmentedButtonStyle(virtual.Style):
    """Style of SegmentedButton"""

    light = {
        "Rectangle": {
            "normal": {"fill": "#FBFBFB", "outline": "#DCDCDC"},
            "hover": {"fill": "#F6F6F6", "outline": "#DCDCDC"},
        },
        "RoundedRectangle": {
            "normal": {"fill": "#FBFBFB", "outline": "#DCDCDC"},
            "hover": {"fill": "#F6F6F6", "outline": "#DCDCDC"},
        }
    }

    dark = {
        "Rectangle": {
            "normal": {"fill": "#2B2B2B", "outline": "#3D3D3D"},
            "hover": {"fill": "#323232", "outline": "#3D3D3D"},
        },
        "RoundedRectangle": {
            "normal": {"fill": "#2B2B2B", "outline": "#3D3D3D"},
            "hover": {"fill": "#323232", "outline": "#3D3D3D"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        bg: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `bg`: the background color of the widget.
        * `ol`: the outline color of the widget.

        states: "normal", "hover"
        """
        self._set(theme, bg, fill=0)
        self._set(theme, ol, outline=0)
        self.widget.update()


class OptionButtonStyle(virtual.Style):
    """Style of OptionButton"""

    light = {
        "Rectangle": {
            "normal": {"fill": "#E1E1E1", "outline": "#C0C0C0"},
            "hover": {"fill": "#E5F1FB", "outline": "#288CDB"},
            "active": {"fill": "#CCE4F7", "outline": "#4884B4"},
        },
        "HalfRoundedRectangle": {
            "normal": {"fill": "#FEFEFE", "outline": "#DCDCDC"},
            "hover": {"fill": "#FAFAFA", "outline": "#DCDCDC"},
            "active": {"fill": "#F3F3F3", "outline": "#DCDCDC"},
        }
    }

    dark = {
        "Rectangle": {
            "normal": {"fill": "#333333", "outline": "#333333"},
            "hover": {"fill": "#333333", "outline": "#858585"},
            "active": {"fill": "#666666", "outline": "#666666"},
        },
        "HalfRoundedRectangle": {
            "normal": {"fill": "#373737", "outline": "#3D3D3D"},
            "hover": {"fill": "#3C3C3C", "outline": "#3D3D3D"},
            "active": {"fill": "#323232", "outline": "#3D3D3D"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        bg: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `bg`: the background color of the widget.
        * `ol`: the outline color of the widget.

        states: "normal", "hover", "active"
        """
        self._set(theme, bg, fill=0)
        self._set(theme, ol, outline=0)
        self.widget.update()


class SpinnerStyle(virtual.Style):
    """Style of Spinner"""

    light = {
        "Oval": {
            "normal": {"outline": "#B4D6FA"},
        },
        "Arc": {
            "normal": {"outline": "#0F6CBD"},
        }
    }

    dark = {
        "Oval": {
            "normal": {"outline": "#0E4775"},
        },
        "Arc": {
            "normal": {"outline": "#479EF5"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        fg: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `fg`: the foreground color of the widget.
        * `bg`: the background color of the widget.

        states: "normal"
        """
        self._set(theme, fg, outline=0)
        self._set(theme, bg, outline=1)
        self.widget.update()


class TooltipStyle(virtual.Style):
    """Style of Tooltip"""

    light = {
        "Information": {
            "normal": {"fill": "#1A1A1A"},
        },
        "Rectangle": {
            "normal": {"fill": "#FBFBFB", "outline": "#DCDCDC"},
        },
        "RoundedRectangle": {
            "normal": {"fill": "#FBFBFB", "outline": "#DCDCDC"},
        }
    }

    dark = {
        "Information": {
            "normal": {"fill": "#F1F1F1"},
        },
        "Rectangle": {
            "normal": {"fill": "#2B2B2B", "outline": "#3D3D3D"},
        },
        "RoundedRectangle": {
            "normal": {"fill": "#2B2B2B", "outline": "#3D3D3D"},
        }
    }

    @typing_extensions.override
    def set(
        self,
        theme: typing.Literal["light", "dark"] | None = None,
        *,
        fg: tuple[str | types.EllipsisType, ...] | str | None = None,
        bg: tuple[str | types.EllipsisType, ...] | str | None = None,
        ol: tuple[str | types.EllipsisType, ...] | str | None = None,
    ) -> None:
        """Set the style of the widget.

        * `theme`: the theme name, None indicates both
        * `fg`: the foreground color of the widget.
        * `bg`: the background color of the widget.
        * `ol`: the outline color of the widget.

        states: "normal"
        """
        self._set(theme, fg, fill=-1)
        self._set(theme, bg, fill=0)
        self._set(theme, ol, outline=0)
        self.widget.update()
