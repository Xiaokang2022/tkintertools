""" 3D support """

import math  # 数学支持
import statistics  # 数据统计
from typing import Iterable  # 类型提示

from .__main__ import Canvas, Tk, Toplevel  # 继承和类型提示
from .constants import *


class Canvas_3D(Canvas):
    """ 3D画布，支持3d绘图 """

    def __init__(
        self,
        master,  # type: Tk | Toplevel
        width,  # type: int
        height,  # type: int
        x=None,  # type: int | None
        y=None,  # type: int | None
        *,
        lock=True,  # type: bool
        expand=True,  # type: bool
        keep=True,  # type: bool
        cfg_3d=CFG_3D,  # type: Iterable[float, float | None, float | None]
        **kw
    ):  # type: (...) -> None
        """
        `master`: 父控件\n
        `width`: 画布宽度\n
        `height`: 画布高度\n
        `x`: 画布左上角的横坐标\n
        `y`: 画布左上角的纵坐标\n
        `lock`: 画布内控件的功能锁，False 时功能暂时失效\n
        `expand`: 画布内控件是否能缩放\n
        `keep`: 画布比例是否保持不变\n
        `cfg_3d`: 3d绘图的配置，一个包含三个值的列表，[相机距离，横坐标偏移，纵坐标偏移]，默认值相机距离500，图像居中\n
        `**kw`: 与 tkinter.Canvas 类的参数相同\n
        """
        Canvas.__init__(self, master, width, height, x, y,
                        lock=lock, expand=expand, keep=keep)
        self.distance = cfg_3d[0]
        self.dx = width / 2 if cfg_3d[1] is None else cfg_3d[1]
        self.dy = height / 2 if cfg_3d[2] is None else cfg_3d[2]
        self._items_3d = []  # type: list[Point | Line | Side | Geometry]

    def items_3d(self):  # type: () -> tuple[Point | Line | Side | Geometry]
        """ 返回`Canvas_3d`类的`items_3d`元组 """
        return tuple(self._items_3d)


class _Point:
    """ 点 """

    def __init__(self, coords):  # type: (list[float]) -> None
        self.coords = coords  # 利用列表引用

    def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> None
        """ 平移 """
        self.coords[0] += dx
        self.coords[1] += dy
        self.coords[2] += dz

    def rotate(self, dx=1, dy=1, dz=1, *, center=[0, 0, 0]):
        # type: (float, float, float, ..., Iterable[float]) -> None
        """ 旋转 """
        sx, sy, sz = math.sin(dx), math.sin(dy), math.sin(dz)
        cx, cy, cz = math.cos(dx), math.cos(dy), math.cos(dz)

        matrix = [[cz*cy, cz*sy*sx-sz*cx, cz*sy*cx+sz*sx],
                  [sz*cy, sz*sy*sx+cz*cx, sz*sy*cx-cz*sx],
                  [-sy,   cy*sx,          cy*cx]]

        for i in range(3):
            matrix[0][i] = center[i] + \
                sum(matrix[i][j]*(self.coords[j]-center[j]) for j in range(3))

        self.coords[:] = matrix[0]

    def scale(self, kx=1, ky=1, kz=1, *, center=None):
        # type: (float, float, float, ..., Iterable[float] | None) -> None
        """ 缩放 """
        for i, k in zip(range(3), (kx, ky, kz)):
            self.coords[i] += (self.coords[i] - center[i]) * (k - 1)

    def project(self, distance):  # type: (float) -> list[float]
        """ 投影 """
        try:
            k = distance/(distance - self.coords[0])
        except ZeroDivisionError:
            return [distance, distance]
        return [self.coords[1]*k, self.coords[2]*k]


class _Line:
    """ 线 """

    def __init__(
        self,
        point1,  # type: list[float]
        point2,  # type: list[float]
    ):  # type: (...) -> None
        self.coords = [point1, point2]
        self.points = [_Point(point) for point in self.coords]

    def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> None
        """ 平移 """
        for point in self.points:
            point.translate(dx, dy, dz)

    def rotate(self, dx=1, dy=1, dz=1, *, center=[0, 0, 0]):
        # type: (float, float, float, ..., Iterable[float]) -> None
        """ 旋转 """
        for point in self.points:
            point.rotate(dx, dy, dz, center=center)

    def scale(self, kx=1, ky=1, kz=1, *, center=None):
        # type: (float, float, float, ..., Iterable[float] | None) -> None
        """ 缩放 """
        if center is None:
            center = [statistics.mean(axis) for axis in zip(*self.coords)]
        for point in self.points:
            point.scale(kx, ky, kz, center=center)

    def project(self, distance):  # type: (float) -> list[list[float]]
        """ 投影 """
        return [point.project(distance) for point in self.points]


class _Side:
    """ 面 """

    def __init__(self, *points):  # type: (list[float]) -> None
        self.coords = list(points)
        self.lines = [_Line(points[ind-1], points[ind])
                      for ind in range(len(points))]

    def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> None
        """ 平移 """
        for point in set(point for line in self.lines for point in line.points):
            point.translate(dx, dy, dz)

    def rotate(self, dx=1, dy=1, dz=1, *, center=[0, 0, 0]):
        # type: (float, float, float, ..., Iterable[float]) -> None
        """ 旋转 """
        for point in set(point for line in self.lines for point in line.points):
            point.rotate(dx, dy, dz, center=center)

    def scale(self, kx=1, ky=1, kz=1, *, center=None):
        # type: (float, float, float, ..., Iterable[float] | None) -> None
        """ 缩放 """
        if center is None:
            center = [statistics.mean(axis) for axis in zip(*self.coords)]
        for point in set(point for line in self.lines for point in line.points):
            point.scale(kx, ky, kz, center=center)

    def project(self, distance):  # type: (float) -> list[list[list[float]]]
        """ 投影 """
        return [line.project(distance) for line in self.lines]


class Point(_Point):
    """ 点 """

    def __init__(
        self,
        canvas,  # type: Canvas_3D
        coords,  # type: list[float]
        *,
        size=POINT_SIZE,  # type: float
        width=POINT_WIDTH,  # type: float
        fill=COLOR_POINT_FILL,  # type: str
        outline=COLOR_POINT_OUTLINE,  # type: str
    ):  # type: (...) -> None
        """
        `canvas`: 父画布\n
        `coords`: 点的空间坐标\n
        `size`: 点的大小\n
        `width`: 点轮廓的宽度\n
        `fill`: 点内部的填充颜色\n
        `outline`: 点轮廓的颜色\n
        """
        _Point.__init__(self, coords)
        canvas._items_3d.append(self)
        self.canvas = canvas
        self.size = size
        self.width = width
        self.fill = fill
        self.item = canvas.create_oval(
            -1, -1, -1, -1, fill=fill, outline=outline, width=width)
        self.update()

    def update(self) -> None:
        """ 更新 """
        x, y = self.project(self.canvas.distance)
        kx, ky = self.canvas.rx, self.canvas.ry
        x += self.canvas.dx
        y += self.canvas.dy
        self.canvas.coords(
            self.item, (x-self.size)*kx, (y-self.size)*ky, (x+self.size)*kx, (y+self.size)*ky)


class Line(_Line):
    """ 线 """

    def __init__(
        self,
        canvas,  # type: Canvas_3D
        point1,  # type: list[float]
        point2,  # type: list[float]
        *,
        width=LINE_WDITH,  # type: float
        fill=COLOR_LINE_FILL,  # type: str
    ):  # type: (...) -> None
        """
        `canvas`: 父画布\n
        `point1`: 起点坐标\n
        `point2`: 终点坐标\n
        `width`: 线的宽度\n
        `fill`: 线的颜色\n
        """
        _Line.__init__(self, point1, point2)
        canvas._items_3d.append(self)
        self.canvas = canvas
        self.width = width
        self.fill = fill
        self.item = canvas.create_line(-1, -1, -1, -1, width=width, fill=fill)
        self.update()

    def update(self) -> None:
        """ 更新 """
        kx, ky = self.canvas.rx, self.canvas.ry
        data = self.project(self.canvas.distance)
        for point in data:
            point[0] += self.canvas.dx
            point[1] += self.canvas.dy
        self.canvas.coords(
            self.item, *[coord*(ky if i else kx) for point in data for i, coord in enumerate(point)])


class Side(_Side):
    """ 面 """

    def __init__(
        self,
        canvas,  # type: Canvas_3D
        *points,  # type: list[float]
        width=SIDE_WIDTH,  # type: float
        fill=COLOR_SIDE_FILL,  # type: str
        outline=COLOR_SIDE_OUTLINE,  # type: str
    ):  # type: (...) -> None
        """
        `canvas`: 父画布\n
        `points`: 各点的空间坐标\n
        `width`: 面轮廓的宽度\n
        `fill`: 面内部的填充颜色\n
        `outline`: 面轮廓的颜色\n
        """
        _Side.__init__(self, *points)
        canvas._items_3d.append(self)
        self.canvas = canvas
        self.width = width
        self.fill = fill
        self.outline = outline
        self.item = canvas.create_polygon(-1, -1, -1, -1,
                                          width=width, fill=fill, outline=outline)
        self.update()

    def update(self) -> None:
        """ 更新 """
        kx, ky = self.canvas.rx, self.canvas.ry
        data = self.project(self.canvas.distance)
        for line in data:
            for point in line:
                point[0] += self.canvas.dx
                point[1] += self.canvas.dy
        self.canvas.coords(
            self.item, *[coord*(ky if i else kx) for line in data for point in line for i, coord in enumerate(point)])


class Geometry:
    """ 几何体 """

    def __init__(self, canvas, *sides):  # type: (Canvas_3D, _Side) -> None
        """
        `canvas`: 显示的画布\n
        `sides`: 平面类`Side`\n
        """
        canvas._items_3d.append(self)
        self.canvas = canvas
        self.coords = []  # type: list[list[float]]
        self.sides = []  # type: list[Side]
        if sides:
            self.append(*sides)

    def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> None
        """
        平移\n
        `dx`: x轴方向位移距离\n
        `dy`: y轴方向位移距离\n
        `dz`: z轴方向位移距离\n
        """
        for point in set(point for side in self.sides for line in side.lines for point in line.points):
            point.translate(dx, dy, dz)

    def rotate(self, dx=1, dy=1, dz=1, *, center=[0, 0, 0]):
        # type: (float, float, float, ..., Iterable[float]) -> None
        """
        旋转\n
        `dx`: 绕x轴方向旋转角度\n
        `dy`: 绕y轴方向旋转角度\n
        `dz`: 绕z轴方向旋转角度\n
        `center`: 旋转中心\n
        """
        for point in set(point for side in self.sides for line in side.lines for point in line.points):
            point.rotate(dx, dy, dz, center=center)

    def scale(self, kx=1, ky=1, kz=1, *, center=None):
        # type: (float, float, float, ..., Iterable[float] | None) -> None
        """
        缩放\n
        `kx`: x轴方向缩放比例\n
        `ky`: y轴方向缩放比例\n
        `kz`: z轴方向缩放比例\n
        `center`: 缩放中心，默认为几何中心\n
        """
        if center is None:
            # NOTE: 对凹面几何体无效
            center = [statistics.mean(axis) for axis in zip(*self.coords)]
        for point in set(point for side in self.sides for line in side.lines for point in line.points):
            point.scale(kx, ky, kz, center=center)

    def update(self):  # type: () -> None
        """ 更新几何体 """
        for side in self.sides:
            side.update()

    def append(self, *sides):  # type: (Side) -> None
        """
        添加面\n
        `sides`: `Side`类\n
        """
        for side in sides:
            for line in side.lines:
                for point in line.points:
                    if point not in self.coords:
                        self.coords.append(point)
            self.sides.append(side)


class Cuboid(Geometry):
    """ 长方体 """

    def __init__(
        self,
        canvas,  # type: Canvas_3D
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
            Side(canvas, self.coords[0], self.coords[1],
                 self.coords[3], self.coords[2]),
            Side(canvas, self.coords[0], self.coords[1],
                 self.coords[5], self.coords[4]),
            Side(canvas, self.coords[0], self.coords[2],
                 self.coords[6], self.coords[4]),
            Side(canvas, self.coords[1], self.coords[3],
                 self.coords[7], self.coords[5]),
            Side(canvas, self.coords[2], self.coords[3],
                 self.coords[7], self.coords[6]),
            Side(canvas, self.coords[4], self.coords[5],
                 self.coords[7], self.coords[6]),
        ]


class Tetrahedron(Geometry):
    """ 四面体 """

    def __init__(
        self,
        canvas,  # type: Canvas_3D
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
            Side(canvas, self.coords[0], self.coords[1], self.coords[2]),
            Side(canvas, self.coords[0], self.coords[1], self.coords[3]),
            Side(canvas, self.coords[0], self.coords[2], self.coords[3]),
            Side(canvas, self.coords[1], self.coords[2], self.coords[3]),
        ]


__all__ = [name for name in globals() if '__' not in name]
