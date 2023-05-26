""" 3D support """

import math  # 数学支持
import statistics  # 数据统计
import tkinter  # 基础模块
from typing import Iterable  # 类型提示

import tkintertools  # 类型提示


def _cross(
    matrix,  # type: list[list[float]]
    vector,  # type: list[float]
):  # type: (...) -> list[float]
    """ 转换矩阵 """
    for i in range(3):
        matrix[0][i] = sum(matrix[i][j]*vector[j] for j in range(3))
    return matrix[0]


class Point:
    """ 点 """

    def __init__(self, coords):  # type: (list[float]) -> None
        self.coords = list(coords)  # 利用列表引用

    def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> Point
        """ 平移 """
        self.coords[0] += dx
        self.coords[1] += dy
        self.coords[2] += dz
        return self

    def rotate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> Point
        """ 旋转 """
        sa, sb, sc = math.sin(dx), math.sin(dy), math.sin(dz)
        ca, cb, cc = math.cos(dx), math.cos(dy), math.cos(dz)
        M = [[cc*cb, cc*sb*sa-sc*ca, cc*sb*ca+sc*sa],
             [sc*cb, sc*sb*sa+cc*ca, sc*sb*ca-cc*sa],
             [-sb,   cb*sa,          cb*ca]]
        self.coords[0], self.coords[1], self.coords[2] = _cross(M, self.coords)
        return self

    def project(self, distance):  # type: (float) -> list[float]
        """ 投影 """
        try:
            coefficient = distance/(distance - self.coords[0])
        except:
            return [distance, distance]
        return [self.coords[1]*coefficient, self.coords[2]*coefficient]


class Line:
    """ 线 """

    def __init__(
        self,
        x1,  # type: float
        y1,  # type: float
        z1,  # type: float
        x2,  # type: float
        y2,  # type: float
        z2,  # type: float
    ):  # type: (...) -> None
        self.coords = [[x1, y1, z1], [x2, y2, z2]]
        self.points = [Point(coord) for coord in self.coords]

    def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> Line
        """ 平移 """
        for point in self.points:
            point.translate(dx, dy, dz)
        return self

    def rotate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> Line
        """ 旋转 """
        for point in self.points:
            point.rotate(dx, dy, dz)
        return self

    def project(self, distance):  # type: (float) -> list[list[float]]
        """ 投影 """
        return [point.project(distance) for point in self.points]


class Side:
    """ 面 """

    def __init__(self, *coords):  # type: (list[float]) -> None
        self.coords = list(coords)
        self.lines = [Line(*coords[ind-1], *coords[ind])
                      for ind in range(len(coords))]

    def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> Side
        """ 平移 """
        for line in self.lines:
            line.translate(dx, dy, dz)
        return self

    def rotate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> Side
        """ 旋转 """
        for line in self.lines:
            line.rotate(dx, dy, dz)
        return self

    def project(self, distance):  # type: (float) -> list[list[list[float]]]
        """ 投影 """
        return [line.project(distance) for line in self.lines]


class Geometry:
    """ 几何体 """

    def __init__(self, canvas, *sides):  # type: (tkintertools.Canvas, Side) -> None
        """
        `canvas`: 显示的画布\n
        `size`: 平面类`Side`\n
        """
        self.canvas = canvas
        self.coords = []  # type: list[list[float]]
        self.sides = []  # type: list[Side]
        self.items = []  # type: list[tkinter._CanvasItemId]
        if sides:
            self.append(*sides)

    def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> None
        """ 平移 """
        for side in self.sides:
            side.translate(dx, dy, dz)

    def rotate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> None
        """ 旋转 """
        for side in self.sides:
            side.rotate(dx, dy, dz)

    def center(self):  # type: () -> tuple[float, float, float]
        """ 几何中心 """  # NOTE: 对凹面几何体无效
        data = list(zip(*self.coords))  # 转置
        x_c = statistics.mean(data[0])
        y_c = statistics.mean(data[1])
        z_c = statistics.mean(data[2])
        return x_c, y_c, z_c

    def append(self, *sides):  # type: (Side) -> None
        """ 添加面 """
        for side in sides:
            for line in side.lines:
                for point in line.points:
                    if point not in self.coords:
                        self.coords.append(point)
            self.sides.append(side)

    def update(self, distance, dx=0, dy=0):  # type: (float, float, float) -> None
        """ 更新几何体 """
        c = 0
        for side in self.sides:
            coords = side.project(distance)
            for coord in coords:

                k = []

                for lst in coord:
                    if dx or dy:
                        lst[0] += 640
                        lst[1] += 360
                    k.append(lst[0])
                    k.append(lst[1])

                self.canvas.coords(self.items[c], k)
                c += 1

    def draw(self, distance, dx=0, dy=0):  # type: (float, float, float) -> None
        """ 绘制 """
        for side in self.sides:
            coords = side.project(distance)
            for coord in coords:

                if dx or dy:
                    for lst in coord:
                        lst[0] += dx
                        lst[1] += dy

                self.items.append(self.canvas.create_polygon(
                    *coord, outline='black'))


class Cuboid(Geometry):
    """ 长方体 """

    def __init__(
        self,
        canvas,  # type: tkintertools.Canvas
        x,  # type: float
        y,  # type: float
        z,  # type: float
        length,  # type: float
        width,  # type: float
        height,  # type: float
    ):  # type: (...) -> None
        """
        `canvas`: 父画布\n
        `x`: 左上角x坐标\n
        `y`: 左上角y坐标\n
        `z`: 左上角z坐标\n
        `length`: 长度\n
        `width`: 宽度\n
        `height`: 高度\n
        """
        self.canvas = canvas
        self.coords = [[x+l, y+w, z+h]
                       for l in (0, length)
                       for w in (0, width)
                       for h in (0, height)]
        self.sides = [
            Side(self.coords[0], self.coords[1],
                 self.coords[3], self.coords[2]),
            Side(self.coords[0], self.coords[1],
                 self.coords[5], self.coords[4]),
            Side(self.coords[0], self.coords[2],
                 self.coords[6], self.coords[4]),
            Side(self.coords[1], self.coords[3],
                 self.coords[7], self.coords[5]),
            Side(self.coords[2], self.coords[3],
                 self.coords[7], self.coords[6]),
            Side(self.coords[4], self.coords[5],
                 self.coords[7], self.coords[6]),
        ]
        self.items = []  # type: list[tkinter._CanvasItemId]


class Tetrahedron(Geometry):
    """ 四面体 """

    def __init__(
        self,
        canvas,  # type: tkintertools.Canvas
        p1,  # type: Iterable[float]
        p2,  # type: Iterable[float]
        p3,  # type: Iterable[float]
        p4,  # type: Iterable[float]
    ):  # type: (...) -> None
        """
        `canvas`: 父画布\n
        `p1`: 第一个顶点\n
        `p2`: 第二个顶点\n
        `p3`: 第三个顶点\n
        `p4`: 第四个顶点\n
        """
        self.canvas = canvas
        self.coords = [list(p1), list(p2), list(p3), list(p4)]
        self.sides = [
            Side(p1, p2, p3),
            Side(p1, p2, p4),
            Side(p1, p3, p4),
            Side(p2, p3, p4),
        ]
        self.items = []  # type: list[tkinter._CanvasItemId]


ORIGIN = Point((0,)*3)
""" 原点 """

LINE_X = Line(0, 0, 0, 1, 0, 0)
""" X 轴单位直线 """
LINE_Y = Line(0, 0, 0, 0, 1, 0)
""" Y 轴单位直线 """
LINE_Z = Line(0, 0, 0, 0, 0, 1)
""" Z 轴单位直线 """

SIDE_YZ = Side((0, 1, 1), (0, 1, -1), (0, -1, -1), (0, -1, 1))
""" 垂直 X 轴单位平面 """
SIDE_ZX = Side((1, 0, 1), (1, 0, -1), (-1, 0, -1), (-1, 0, 1))
""" 垂直 Y 轴单位平面 """
SIDE_XY = Side((1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0))
""" 垂直 Z 轴单位平面 """


# class Ellipsoid:
#     """ 椭球体 """

#     def __init__(
#         self,
#         x,  # type: float
#         y,  # type: float
#         z,  # type: float
#         length,  # type: float
#         width,  # type: float
#         height  # type: float
#     ):  # type: (...) -> None
#         self.coords = [[x+l, y+w, z+h]
#                        for l in (0, length)
#                        for w in (0, width)
#                        for h in (0, height)]
#         self.points = [Point(coord) for coord in self.coords]

#     def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> None
#         """ 平移 """
#         for point in self.points:
#             point.translate(dx, dy, dz)

#     def rotate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> None
#         """ 旋转 """
#         for point in self.points:
#             point.rotate(dx, dy, dz)

#     # type: (float) -> tuple[list[float], list[float]]
#     def project(self, distance):
#         """ 投影 """
#         coefficient = distance/(distance - self.coords[0])
#         return [self.coords[1]*coefficient, self.coords[2]*coefficient]
