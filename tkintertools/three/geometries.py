"""Standard Geometry"""


from . import engine

__all__ = [
    "Cuboid",
    "Tetrahedron",
]


class Cuboid(engine.Geometry):
    """长方体"""

    def __init__(
        self,
        canvas: engine.Canvas | engine.Space,
        x: float,
        y: float,
        z: float,
        length: float,
        width: float,
        height: float,
        *,
        boardwidth: int = 1,
        color_fill_up: str = "",
        color_fill_down: str = "",
        color_fill_left: str = "",
        color_fill_right: str = "",
        color_fill_front: str = "",
        color_fill_back: str = "",
        color_outline_up: str = "#000000",
        color_outline_down: str = "#000000",
        color_outline_left: str = "#000000",
        color_outline_right: str = "#000000",
        color_outline_front: str = "#000000",
        color_outline_back: str = "#000000",
    ) -> None:
        """
        * `canvas`: 父画布
        * `x`: 左上角 x 坐标
        * `y`: 左上角 y 坐标
        * `z`: 左上角 z 坐标
        * `length`: 长度
        * `width`: 宽度
        * `height`: 高度
        * `boardwidth`: 边框线条宽度
        * `color_fill_up`: 上表面内部颜色
        * `color_fill_down`: 下表面内部颜色
        * `color_fill_left`: 左侧面内部颜色
        * `color_fill_right`: 右侧面内部颜色
        * `color_fill_front`: 正面内部颜色
        * `color_fill_back`: 后面内部颜色
        * `color_outline_up`: 上表面边框颜色
        * `color_outline_down`: 下表面边框颜色
        * `color_outline_left`: 左侧面边框颜色
        * `color_outline_right`: 右侧面边框颜色
        * `color_outline_front`: 正面边框颜色
        * `color_outline_back`: 后面边框颜色
        """
        canvas._geometries.append(self)
        self.canvas = canvas
        coords = [[x + l, y + w, z + h]
                  for l in (0, length) for w in (0, width) for h in (0, height)]
        self.sides = [
            engine.Side(canvas, coords[0], coords[1], coords[3], coords[2],
                        width=boardwidth, fill=color_fill_back, outline=color_outline_back),
            engine.Side(canvas, coords[0], coords[1], coords[5], coords[4],
                        width=boardwidth, fill=color_fill_left, outline=color_outline_left),
            engine.Side(canvas, coords[0], coords[2], coords[6], coords[4],
                        width=boardwidth, fill=color_fill_down, outline=color_outline_down),
            engine.Side(canvas, coords[1], coords[3], coords[7], coords[5],
                        width=boardwidth, fill=color_fill_up, outline=color_outline_up),
            engine.Side(canvas, coords[2], coords[3], coords[7], coords[6],
                        width=boardwidth, fill=color_fill_right, outline=color_outline_right),
            engine.Side(canvas, coords[4], coords[5], coords[7], coords[6],
                        width=boardwidth, fill=color_fill_front, outline=color_outline_front),
        ]


class Tetrahedron(engine.Geometry):
    """四面体"""

    def __init__(
        self,
        canvas: engine.Canvas | engine.Space,
        point_1: tuple[float, float, float],
        point_2: tuple[float, float, float],
        point_3: tuple[float, float, float],
        point_4: tuple[float, float, float],
        *,
        boardwidth: int = 1,
        color_fill: tuple[str, str, str, str] = ("", "", "", ""),
        color_outline: tuple[str, str, str, str] = (
            "#000000", "#000000", "#000000", "#000000")
    ) -> None:
        """
        * `canvas`: 父画布
        * `point_1`: 第一个顶点
        * `point_2`: 第二个顶点
        * `point_3`: 第三个顶点
        * `point_4`: 第四个顶点
        * `boardwidth`: 边框线条宽度
        * `color_fill`: 内部颜色序列
        * `color_outline`: 边框颜色序列
        """
        canvas._geometries.append(self)
        self.canvas = canvas
        self.sides = [
            engine.Side(canvas, point_1, point_2, point_3, width=boardwidth,
                        fill=color_fill[0], outline=color_outline[0]),
            engine.Side(canvas, point_1, point_2, point_4, width=boardwidth,
                        fill=color_fill[1], outline=color_outline[0]),
            engine.Side(canvas, point_1, point_3, point_4, width=boardwidth,
                        fill=color_fill[2], outline=color_outline[0]),
            engine.Side(canvas, point_2, point_3, point_4, width=boardwidth,
                        fill=color_fill[3], outline=color_outline[0]),
        ]
