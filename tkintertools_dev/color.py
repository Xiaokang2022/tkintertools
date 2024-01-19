"""Color support"""

import tkinter
import typing

from . import _tools, constants, exceptions


@typing.overload
def color(
    __color,  # type: tuple[str, str]
    /,
    proportion=constants.PROPORTION,  # type: float
    *,
    seqlength=constants.SEQLENGTH,  # type: int
    num=constants.NUM,  # type: typing.Literal[1, 2, 3, 4]
    controller=constants.CONTROLLER,
    # type: tuple[typing.Callable[[float], float], float, float] | None
):  # type: (...) -> str | list[str]
    ...


@typing.overload
def color(
    __color,  # type: str
    /,
    proportion=constants.PROPORTION,  # type: float
    *,
    seqlength=constants.SEQLENGTH,  # type: int
    num=constants.NUM,  # type: typing.Literal[1, 2, 3, 4]
    controller=constants.CONTROLLER,
    # type: tuple[typing.Callable[[float], float], float, float] | None
):  # type: (...) -> str | list[str]
    ...


def color(
    __color,  # type: str | tuple[str, str]
    /,
    proportion=constants.PROPORTION,  # type: float
    *,
    seqlength=constants.SEQLENGTH,  # type: int
    num=constants.NUM,  # type: typing.Literal[1, 2, 3, 4]
    controller=constants.CONTROLLER,
    # type: tuple[typing.Callable[[float], float], float, float] | None
):  # type: (...) -> str | list[str]
    """按一定比例给出已有 RGB 颜色字符串的渐变 RGB 颜色字符串，或者给出已有 RGB 颜色字符串的对比色

    * `color`: 颜色元组或列表 (初始颜色, 目标颜色)，或者一个颜色字符串（此时返回其对比色）
    * `proportion`: 改变比例（浮点数，范围为 0 ~ 1），默认值为 1
    * `seqlength`: 如果值为 1，则直接返回结果，其余情况返回长度为 `seqlength` 的渐变颜色列表，默认为 1
    * `num`: 每一通道的 16 进制位数，默认为 2 位，可选值为 1 ~ 4
    * `controller`: 比例值变化的控制器，为元组 (控制函数, 初始值, 终止值)，仅当参数 `seqlength` 大于 1 时生效，默认为等差变化
    """
    if not 0 <= proportion <= 1:
        raise exceptions.ColorArgsValueError(proportion)

    key = 16 - (num << 2)
    format_ = f"#%0{num}X%0{num}X%0{num}X"

    if tkinter._default_root is None:
        tkinter.Tk().withdraw()

    if isinstance(__color, str):  # 对比色的情况处理
        start = [c >> key for c in tkinter._default_root.winfo_rgb(__color)]
        end = [(1 << (num << 2)) - c - 1 for c in start]
    else:
        start = [c >> key for c in tkinter._default_root.winfo_rgb(__color[0])]
        end = [c >> key for c in tkinter._default_root.winfo_rgb(__color[1])]

    end = [s + round((e - s) * proportion) for s, e in zip(start, end)]

    if controller is None:
        controller = (lambda _: _), 0, 1

    proportion_lst = _tools._get_control_lst(controller, seqlength)

    lst = [(format_ % tuple(c1 + round((c2-c1) * p)
            for c1, c2 in zip(start, end))) for p in proportion_lst]

    return lst[0] if seqlength == 1 else lst


def str_to_hex(__color: str, /, *, reverse: bool = False, add: int = 0) -> int:
    """"""
    RGB = tkinter._get_temp_root().winfo_rgb(__color)
    tup = tuple(value >> 8 for value in RGB)
    for i in reversed(tup) if reverse else tup:
        add <<= 8
        add += i
    return add
