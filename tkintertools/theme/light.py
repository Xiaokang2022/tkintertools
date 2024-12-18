"""Light theme"""

from __future__ import annotations

import copy

Canvas = {
    "bg": "#F1F1F1",
    "insertbackground": "#000000",
    "highlightthickness": 0,
}

Frame = {
    "bg": "#EAEAEA",
    "insertbackground": "#000000",
    "highlightthickness": 0,
}

Button = {
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

CheckButton = {
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

ToggleButton = {
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

HighlightButton = {
    "Information": {
        "normal": {"fill": "grey"},
        "hover": {"fill": "#1F1F1F"},
        "active": {"fill": "#000000"},
    }
}

IconButton = {
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

InputBox = {
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

Label = {
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

OptionButton = {
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

ProgressBar = {
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

RadioButton = {
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

SegmentedButton = {
    "Rectangle": {
        "normal": {"fill": "#FBFBFB", "outline": "#DCDCDC"},
        "hover": {"fill": "#F6F6F6", "outline": "#DCDCDC"},
    },
    "RoundedRectangle": {
        "normal": {"fill": "#FBFBFB", "outline": "#DCDCDC"},
        "hover": {"fill": "#F6F6F6", "outline": "#DCDCDC"},
    }
}

Slider = {
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

Switch = {
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

Text = {
    "Information": {
        "normal": {"fill": "#1A1A1A"},
    }
}

Tooltip = {
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

Spinner = {
    "Oval": {
        "normal": {"outline": "#B4D6FA"},
    },
    "Arc": {
        "normal": {"outline": "#0F6CBD"},
    }
}

UnderlineButton = {
    "Information": {
        "normal": {"fill": "#1A1A1A"},
        "hover": {"fill": "blue"},
        "active": {"fill": "purple"},
    }
}

_AuxiliaryLabel = copy.deepcopy(Label)
del _AuxiliaryLabel["RoundedRectangle"]
_AuxiliaryLabel["HalfRoundedRectangle"] = Label["RoundedRectangle"]

_AuxiliaryButton = copy.deepcopy(Button)
del _AuxiliaryButton["RoundedRectangle"]
_AuxiliaryButton["HalfRoundedRectangle"] = Button["RoundedRectangle"]

_AuxiliaryInputBox = copy.deepcopy(InputBox)
del _AuxiliaryInputBox["RoundedRectangle.in"]
del _AuxiliaryInputBox["RoundedRectangle.out"]
_AuxiliaryInputBox["HalfRoundedRectangle.in"] = InputBox["RoundedRectangle.in"]
_AuxiliaryInputBox["HalfRoundedRectangle.out"] = InputBox["RoundedRectangle.out"]
