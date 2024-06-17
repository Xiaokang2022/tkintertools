"""APIs for Matplotlib"""

import tkinter

import matplotlib
import matplotlib.backends._backend_tk as _backend_tk
import matplotlib.backends.backend_tkagg as backend_tkagg
import matplotlib.figure as figure
import mpl_toolkits.mplot3d as mplot3d

from ..style import manager
from . import tools

__all__ = [
    "FigureCanvas",
    "FigureToolbar",
    "set_mpl_default_theme",
    "DARK_THEME",
    "LIGHT_THEME",
]


class FigureCanvas(tkinter.Canvas, backend_tkagg.FigureCanvasTkAgg):
    """A canvas for interface of `matplotlib`"""

    def __init__(
        self,
        figure: figure.Figure,
        master: tkinter.Misc,
        *args,
        **kwargs,
    ) -> None:
        """
        * `figure`: a `Figure` object from `matplotlib`
        * `master`: parent widget
        """
        self.figure = figure
        self._TkAgg: backend_tkagg.FigureCanvasTkAgg = backend_tkagg.FigureCanvasTkAgg(
            figure, master)

        tools._forward_methods(self._TkAgg._tkcanvas, self)
        tools._forward_methods(self._TkAgg, self)

        self.configure(*args, **kwargs)
        self.bind("<Configure>", self._fix_size, "+")
        manager.register_event(self._theme)
        self._theme(manager.get_color_mode() == "dark")

    def _fix_size(self, event: tkinter.Event) -> None:
        """Correct the size of Figure"""
        self.update()
        self.resize(event)

    def _theme(self, dark: bool) -> None:
        """Change the color theme of the Figure"""
        self.update()
        for key, value in DARK_THEME.items() if dark else LIGHT_THEME.items():
            keys = key.split(".")
            match keys[0]:
                case "figure": self.figure.set(**{keys[-1]: value})
                case "grid":
                    for axes in self.figure.axes:
                        # if getattr(axes.xaxis, "_gridOnMinor", None):  # BUG: It not work now
                        axes.grid(color=value)
                case "axes3d":
                    for axes in self.figure.axes:
                        if isinstance(axes, mplot3d.Axes3D):
                            getattr(axes, keys[1]).set(pane_color=value)
                case "axes":
                    for axes in self.figure.axes:
                        if keys[-1] == "labelcolor":
                            for attr in ("xaxis", "yaxis", "zaxis") if isinstance(axes, mplot3d.Axes3D) else ("xaxis", "yaxis"):
                                getattr(axes, attr).label.set_color(value)
                        elif keys[-1] == "titlecolor":
                            axes.title.set_color(value)
                        else:
                            axes.patch.set(**{keys[-1]: value})
                case "xtick":
                    for axes in self.figure.axes:
                        for attr in ("xaxis", "yaxis", "zaxis") if isinstance(axes, mplot3d.Axes3D) else ("xaxis",):
                            if keys[-1] == "color":
                                getattr(axes, attr).set_tick_params(
                                    colors=value)
                                for k, spine in axes.spines.items():
                                    if k in ("top", "bottom"):
                                        spine.set_color(value)
                case "ytick":
                    for axes in self.figure.axes:
                        if not isinstance(axes, mplot3d.Axes3D):
                            if keys[-1] == "color":
                                axes.yaxis.set_tick_params(colors=value)
                                for k, spine in axes.spines.items():
                                    if k in ("right", "left"):
                                        spine.set_color(value)
        self.draw()

    # @typing.override
    def destroy(self) -> None:
        self.figure.clf()
        manager.remove_event(self._theme)
        return self._TkAgg.get_tk_widget().destroy()


class FigureToolbar(_backend_tk.NavigationToolbar2Tk):
    """An interface class for the matplotlib navigation cursor"""

    def __init__(
        self,
        canvas: FigureCanvas,
        master: tkinter.Misc | FigureCanvas | None = None,
        *,
        pack_toolbar: bool = True,
        **kwargs,
    ) -> None:
        """
        * `canvas`: the figure canvas on which to operate
        * `master`: parent widget
        * `pack_toolbar`: if True, add the toolbar to the parent's pack manager's packing
        list during initialization with `side="bottom"` and `fill="x"`.

        TIPS:

        If you want to use the toolbar with a different layout manager, use `pack_toolbar=False`
        """
        if isinstance(master, FigureCanvas):
            master = master._TkAgg._tkcanvas
        _backend_tk.NavigationToolbar2Tk.__init__(
            self, canvas._TkAgg, master, pack_toolbar=pack_toolbar)
        self.configure(**kwargs)
        self.update()
        manager.register_event(self._theme)
        self._theme(manager.get_color_mode() == "dark")

    def _theme(self, dark: bool) -> None:
        """Change the color theme of the Toolbar"""
        if dark:
            self["bg"] = "#303030"
            for name, child in self.children.items():
                child["bg"] = "#303030"
                if name.startswith("!label"):
                    child["fg"] = "#F1F1F1"
        else:
            self["bg"] = "#F0F0F0"
            for name, child in self.children.items():
                child["bg"] = "#F0F0F0"
                if name.startswith("!label"):
                    child["fg"] = "#F1F1F1"

    # @typing.override
    def destroy(self) -> None:
        manager.remove_event(self._theme)
        return _backend_tk.NavigationToolbar2Tk.destroy(self)


def set_mpl_default_theme(dark: bool) -> None:
    """
    Set default color constants of `matplotlib`

    * `dark`: Wether it is dark mode
    """
    for key, value in DARK_THEME.items() if dark else LIGHT_THEME.items():
        matplotlib.rcParams[key] = value


DARK_THEME: dict[str, str] = {
    "axes.edgecolor": "#AAAAAA",  # outline
    "axes.facecolor": "#202020",  # internal
    "axes.labelcolor": "#CCCCCC",  # label
    "axes.titlecolor": "#CCCCCC",  # title

    "axes3d.xaxis.panecolor": "#2A2A2A",  # x pane
    "axes3d.yaxis.panecolor": "#2A2A2A",  # y pane
    "axes3d.zaxis.panecolor": "#2A2A2A",  # z pane

    # "figure.edgecolor": "#202020",
    "figure.facecolor": "#202020",  # external

    "legend.edgecolor": "#707070",  # outline
    "legend.facecolor": "#202020",  # internal
    "legend.labelcolor": "#CCCCCC",  # label

    "grid.color": "#505050",  # grid
    # "text.color": "#202020",

    "xtick.color": "#CCCCCC",  # ruler (3D)
    "xtick.labelcolor": "#CCCCCC",  # scale (3D)
    "ytick.color": "#CCCCCC",  # ruler
    "ytick.labelcolor": "#CCCCCC",  # scale
}

LIGHT_THEME: dict[str, str] = {
    "axes.edgecolor": "#2A2A2A",
    "axes.facecolor": "#FFFFFF",
    "axes.labelcolor": "#000000",
    "axes.titlecolor": "#000000",

    "axes3d.xaxis.panecolor": "#F5F5F5",
    "axes3d.yaxis.panecolor": "#F5F5F5",
    "axes3d.zaxis.panecolor": "#F5F5F5",

    # "figure.edgecolor": "#FFFFFF",
    "figure.facecolor": "#FFFFFF",

    "legend.edgecolor": "#D6D6D6",
    "legend.facecolor": "#FFFFFF",
    "legend.labelcolor": "#000000",

    "grid.color": "#BDBDBD",
    # "text.color": "#000000",

    "xtick.color": "#000000",
    "xtick.labelcolor": "#000000",
    "ytick.color": "#000000",
    "ytick.labelcolor": "#000000",
}
