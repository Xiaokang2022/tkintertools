""" 将 tkintertools.py 转换至 Python3.7 的兼容版本 """


replace_dict = {
    "from typing import Generator, Iterable, Literal, Self, Type  # 类型提示": "",
    ": Type[Self]": "",
    ": Iterable | Literal['smooth', 'rebound', 'flat']": "",
    ": Iterable[str] | str": "",
    ": Literal['normal', 'touch', 'press', 'disabled'] | None": "",
    ": Literal['left', 'center', 'right']": "",
    " -> Generator[int, None, None]": "",
    ": Self": "",
    " -> Self": "",
    " -> str | tuple | None": "",
    ": str | bytes | None": "",
    " | None": "",
    " -> tuple[int, int, int, int]": "",
    " -> None | list[float]": "",
    ": tuple[str] | str": "",
    ": Tk | Canvas | tkinter.Misc | tkinter.BaseWidget": "",
    ": Canvas | _BaseWidget | tkinter.BaseWidget": "",
    "  # type: function": "",
    ": tuple[int, int]": "",
    " -> dict[str, tuple[str, str, str, str, str]]": "",
    ": tuple[str, str, str]": "",
    ": tuple[str, int, str]": "",
    ": tuple[str, str]": "",
    "isinstance(widget, tkinter.Tk | tkinter.Toplevel)": "isinstance(widget, tkinter.Tk) or isinstance(widget, tkinter.Toplevel)",
    "isinstance(widget, CanvasButton | _TextWidget)": "(isinstance(widget, CanvasButton) or isinstance(widget, _TextWidget))",
    "isinstance(self, CanvasLabel | CanvasButton | ProcessBar)": "isinstance(self, CanvasLabel) or isinstance(self, CanvasButton) or isinstance(self, ProcessBar)",
    "if sys.version_info < (3, 10)": "if sys.version_info < (3, 6)"
}

with open('tkintertools.py', 'r', encoding='utf-8') as file:
    data = file.read()

for key, value in replace_dict.items():
    data = data.replace(key, value)
else:
    print("Done!")

with open('Compatible Version/tkintertools.py', 'w', encoding='utf-8') as file:
    file.write(data)
