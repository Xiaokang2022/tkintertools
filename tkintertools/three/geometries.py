"""Standard Geometries"""


from . import engine

__all__ = [
    "Cuboid",
    "Tetrahedron",
    # "Sphere",
    # "Cylinder",
    # "Cone",
    # "Prism",
    # "Pyramid",
    # "RegularPolyhedron",
]


class Cuboid(engine.Geometry):
    """"""

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
        """"""
        canvas._geometries.append(self)
        self.canvas = canvas
        coords = [[x + l, y + w, z + h]
                  for l in (0, length) for w in (0, width) for h in (0, height)]
        self.sides = [
            engine.Plane(canvas, coords[0], coords[1], coords[3], coords[2],
                         width=boardwidth, fill=color_fill_back, outline=color_outline_back),
            engine.Plane(canvas, coords[0], coords[1], coords[5], coords[4],
                         width=boardwidth, fill=color_fill_left, outline=color_outline_left),
            engine.Plane(canvas, coords[0], coords[2], coords[6], coords[4],
                         width=boardwidth, fill=color_fill_down, outline=color_outline_down),
            engine.Plane(canvas, coords[1], coords[3], coords[7], coords[5],
                         width=boardwidth, fill=color_fill_up, outline=color_outline_up),
            engine.Plane(canvas, coords[2], coords[3], coords[7], coords[6],
                         width=boardwidth, fill=color_fill_right, outline=color_outline_right),
            engine.Plane(canvas, coords[4], coords[5], coords[7], coords[6],
                         width=boardwidth, fill=color_fill_front, outline=color_outline_front),
        ]


class Tetrahedron(engine.Geometry):
    """"""

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
        """"""
        canvas._geometries.append(self)
        self.canvas = canvas
        self.sides = [
            engine.Plane(canvas, point_1, point_2, point_3, width=boardwidth,
                         fill=color_fill[0], outline=color_outline[0]),
            engine.Plane(canvas, point_1, point_2, point_4, width=boardwidth,
                         fill=color_fill[1], outline=color_outline[0]),
            engine.Plane(canvas, point_1, point_3, point_4, width=boardwidth,
                         fill=color_fill[2], outline=color_outline[0]),
            engine.Plane(canvas, point_2, point_3, point_4, width=boardwidth,
                         fill=color_fill[3], outline=color_outline[0]),
        ]
