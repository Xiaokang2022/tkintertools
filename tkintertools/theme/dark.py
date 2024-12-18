"""Dark theme"""

from __future__ import annotations

import copy

Canvas = {
    "bg": "#202020",
    "insertbackground": "#FFFFFF",
    "highlightthickness": 0,
}

Frame = {
    "bg": "#1C1C1C",
    "insertbackground": "#FFFFFF",
    "highlightthickness": 0,
}

Button = {
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

CheckButton = {
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

ToggleButton = {
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

HighlightButton = {
    "Information": {
        "normal": {"fill": "grey"},
        "hover": {"fill": "#F1F1F1"},
        "active": {"fill": "#FFFFFF"},
    }
}

IconButton = {
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

InputBox = {
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

Label = {
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

OptionButton = {
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

ProgressBar = {
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

RadioButton = {
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

SegmentedButton = {
    "Rectangle": {
        "normal": {"fill": "#2B2B2B", "outline": "#3D3D3D"},
        "hover": {"fill": "#323232", "outline": "#3D3D3D"},
    },
    "RoundedRectangle": {
        "normal": {"fill": "#2B2B2B", "outline": "#3D3D3D"},
        "hover": {"fill": "#323232", "outline": "#3D3D3D"},
    }
}

Slider = {
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

Switch = {
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

Text = {
    "Information": {
        "normal": {"fill": "#F1F1F1"},
    }
}

Tooltip = {
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

Spinner = {
    "Oval": {
        "normal": {"outline": "#0E4775"},
    },
    "Arc": {
        "normal": {"outline": "#479EF5"},
    }
}

UnderlineButton = {
    "Information": {
        "normal": {"fill": "#F1F1F1"},
        "hover": {"fill": "royalblue"},
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
