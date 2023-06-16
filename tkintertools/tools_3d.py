""" 3D support """

import math  # 数学支持
import statistics  # 数据统计
from tkinter import Event  # 类型提示
from typing import Iterable  # 类型提示

from .__main__ import Canvas, Tk, Toplevel  # 继承和类型提示
from .constants import *


def translate(coords, dx=0, dy=0, dz=0):
    # type: (list[float], float, float, float) -> None
    """
    ### 平移
    将一个空间三维中的点进行平移\n
    ---
    `coords`: 被平移点的空间坐标列表\n
    `dx`: x方向位移\n
    `dy`: y方向位移\n
    `dz`: z方向位移\n
    """
    coords[0] += dx
    coords[1] += dy
    coords[2] += dz


def rotate(coords, dx=0, dy=0, dz=0, *, center=[0, 0, 0]):
    # type: (list[float], float, float, float, ..., Iterable[float]) -> None
    """
    ### 旋转
    将一个空间三维中的点以另一个点为旋转中心进行旋转\n
    ---
    `coords`: 被旋转点的空间坐标列表\n
    `dx`: x方向旋转弧度\n
    `dy`: y方向旋转弧度\n
    `dz`: z方向旋转弧度\n
    `center`: 旋转中心的空间坐标列表\n
    """
    sx, sy, sz = math.sin(dx), math.sin(dy), math.sin(dz)
    cx, cy, cz = math.cos(dx), math.cos(dy), math.cos(dz)

    matrix = [[cz*cy, cz*sy*sx-sz*cx, cz*sy*cx+sz*sx],
              [sz*cy, sz*sy*sx+cz*cx, sz*sy*cx-cz*sx],
              [-sy,   cy*sx,          cy*cx]]

    for i in range(3):
        matrix[0][i] = center[i] + \
            sum(matrix[i][j]*(coords[j]-center[j]) for j in range(3))

    coords[:] = matrix[0]


def scale(coords, kx=1, ky=1, kz=1, *, center=None):
    # type: (list[float], float, float, float, ..., Iterable[float] | None) -> None
    """
    ### 缩放
    将一个空间三维中的点以另一个点为缩放中心进行位置缩放\n
    ---
    `coords`: 被缩放点的空间坐标列表\n
    `dx`: x方向缩放比例\n
    `dy`: y方向缩放比例\n
    `dz`: z方向缩放比例\n
    `center`: 缩放中心的空间坐标列表\n
    """
    for i, k in zip(range(3), (kx, ky, kz)):
        coords[i] += (coords[i] - center[i]) * (k - 1)


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
        camera_distance=CAMERA_DISTANCE,  # type: float
        dx=None,  # type: float | None
        dy=None,  # type: float | None
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
        `camera_distance`: 3d绘图时相机与原点的距离，默认值为1000\n
        `dx`: 画面在横坐标方向的偏移，None表示居中\n
        `dy`: 画面在纵坐标方向的偏移，None表示居中\n
        `**kw`: 与 tkinter.Canvas 类的参数相同\n
        """
        Canvas.__init__(self, master, width, height, x, y,
                        lock=lock, expand=expand, keep=keep, **kw)
        self.distance = camera_distance
        self.dx = width / 2 if dx is None else dx
        self.dy = height / 2 if dy is None else dy
        self._items_3d = []  # type: list[Point | Line | Side]
        self._geos = []  # type: list[Geometry]

    def items_3d(self):  # type: () -> tuple[Point | Line | Side]
        """ 返回`Canvas_3d`类的`items_3d`元组 """
        return tuple(self._items_3d)

    def geos(self):  # type: () -> tuple[Geometry]
        """ 返回`Canvas_3d`类的`geos`元组 """
        return tuple(self._geos)

    def space_sort(self):  # type: () -> None
        """ 空间位置排序 """
        self._items_3d.sort(key=lambda item: item.camera_distance())
        for item in self._items_3d:
            self.lower(item.item)


class Space(Canvas_3D):
    """ 三维空间 """

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
        camera_distance=CAMERA_DISTANCE,  # type: float
        dx=None,  # type: float | None
        dy=None,  # type: float | None
        origin_color='',  # type: str
        **kw
    ):  # type: (...) -> None
        Canvas_3D.__init__(self, master, width, height, x, y, lock=lock, expand=expand,
                           keep=keep, camera_distance=camera_distance, dx=dx, dy=dy, **kw)
        self._origin = Point(self, [0, 0, 0], size=1,
                             fill=origin_color, outline=origin_color)
        self.space_sort()
        self.bind('<B3-Motion>', self._translate)
        self.bind('<Button-3>', lambda _: self._translate(_, True))
        self.bind('<ButtonRelease-3>', lambda _: self._translate(_, False))
        self.bind('<B1-Motion>', self._rotate)
        self.bind('<Button-1>', lambda _: self._rotate(_, True))
        self.bind('<ButtonRelease-1>', lambda _: self._rotate(_, False))
        if SYSTEM == 'Linux':  # 兼容 Linux 系统
            self.bind('<Button-4>', lambda _: self._zoom(_, True))
            self.bind('<Button-5>', lambda _: self._zoom(_, False))
        else:
            self.bind('<MouseWheel>', self._zoom)

    def _translate(self, event, flag=None, cache=[]):
        # type: (Event, bool | None, list[float]) -> None
        """ 平移视角 """
        if flag is True:  # 按下
            cache[:] = [event.x, event.y]
            return self.configure(cursor='fleur')
        elif flag is False:  # 松开
            return self.configure(cursor='arrow')
        dx, dy = event.x-cache[0], event.y-cache[1]
        cache[:] = [event.x, event.y]
        for item in self._geos+[self._origin]:
            item.translate(0, dx, dy)
            item.update()
        self.space_sort()

    def _rotate(self, event, flag=None, cache=[]):
        # type: (Event, bool | None, list[float]) -> None
        """ 旋转视角 """
        if flag is True:
            cache[:] = [event.x, event.y]
            return self.configure(cursor='fleur')
        elif flag is False:
            return self.configure(cursor='arrow')
        dx, dy = event.x-cache[0], event.y-cache[1]
        cache[:] = [event.x, event.y]
        for item in self._geos+[self._origin]:
            item.rotate(0, -dy/self.dx*math.pi, dx /
                        self.dy*math.pi, center=self._origin.coords)
            item.update()
        self.space_sort()

    def _zoom(self, event, flag=None):  # type: (Event, bool | None) -> None
        """ 缩放视角 """
        if flag is not None:
            event.delta = flag
        k = 1.1 if event.delta > 0 else 0.9
        for item in self.geos():
            item.scale(k, k, k, center=self._origin.coords)
            item.update()
        self.space_sort()


class _Point:
    """ 点 """

    def __init__(self, coords):  # type: (list[float]) -> None
        self.coords = coords  # 利用列表引用

    def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> None
        """ 平移 """
        translate(self.coords, dx, dy, dz)

    def rotate(self, dx=0, dy=0, dz=0, *, center=[0, 0, 0]):
        # type: (float, float, float, ..., Iterable[float]) -> None
        """ 旋转 """
        rotate(self.coords, dx, dy, dz, center=center)

    def scale(self, kx=1, ky=1, kz=1, *, center=None):
        # type: (float, float, float, ..., Iterable[float] | None) -> None
        """ 缩放 """
        scale(self.coords, kx, ky, kz, center=center)

    def project(self, distance):  # type: (float) -> list[float]
        """ 投影 """
        relative_dis = distance - self.coords[0]
        if relative_dis <= 1e-16:
            return [float('INF')]*2  # BUG
        k = distance/relative_dis
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
        for coord in self.coords:
            translate(coord, dx, dy, dz)

    def rotate(self, dx=0, dy=0, dz=0, *, center=[0, 0, 0]):
        # type: (float, float, float, ..., Iterable[float]) -> None
        """ 旋转 """
        for coord in self.coords:
            rotate(coord, dx, dy, dz, center=center)

    def scale(self, kx=1, ky=1, kz=1, *, center=None):
        # type: (float, float, float, ..., Iterable[float] | None) -> None
        """ 缩放 """
        if center is None:
            center = [statistics.mean(axis) for axis in zip(*self.coords)]
        for coord in self.coords:
            scale(coord, kx, ky, kz, center=center)

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
        for coord in self.coords:
            translate(coord, dx, dy, dz)

    def rotate(self, dx=0, dy=0, dz=0, *, center=[0, 0, 0]):
        # type: (float, float, float, ..., Iterable[float]) -> None
        """ 旋转 """
        for coord in self.coords:
            rotate(coord, dx, dy, dz, center=center)

    def scale(self, kx=1, ky=1, kz=1, *, center=None):
        # type: (float, float, float, ..., Iterable[float] | None) -> None
        """ 缩放 """
        if center is None:
            center = [statistics.mean(axis) for axis in zip(*self.coords)]
        for coord in self.coords:
            scale(coord, kx, ky, kz, center=center)

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

    def camera_distance(self):  # type: () -> float
        """ 与相机距离 """
        return math.hypot(self.canvas.distance-self.coords[0], self.coords[1], self.coords[2])


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

    def camera_distance(self):  # type: () -> float
        """ 与相机距离 """
        return statistics.mean(math.hypot(self.canvas.distance-coord[0], coord[1], coord[2]) for coord in self.coords)


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
        self.item = canvas.create_polygon(
            -1, -1, -1, -1, width=width, fill=fill, outline=outline)
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

    def camera_distance(self):  # type: () -> float
        """ 与相机距离 """
        return statistics.mean(math.hypot(self.canvas.distance-coord[0], coord[1], coord[2]) for coord in self.coords)


class Geometry:
    """ 几何体 """

    def __init__(self, canvas, *sides):  # type: (Canvas_3D, _Side) -> None
        """
        `canvas`: 显示的画布\n
        `sides`: 平面类`Side`\n
        """
        canvas._geos.append(self)
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
        coords = [coord for side in self.sides for coord in side.coords]
        for ind, coord in enumerate(coords):
            if coord not in coords[:ind]:
                translate(coord, dx, dy, dz)

    def rotate(self, dx=0, dy=0, dz=0, *, center=[0, 0, 0]):
        # type: (float, float, float, ..., Iterable[float]) -> None
        """
        旋转\n
        `dx`: 绕x轴方向旋转弧度\n
        `dy`: 绕y轴方向旋转弧度\n
        `dz`: 绕z轴方向旋转弧度\n
        `center`: 旋转中心\n
        """
        coords = [coord for side in self.sides for coord in side.coords]
        for ind, coord in enumerate(coords):
            if coord not in coords[:ind]:
                rotate(coord, dx, dy, dz, center=center)

    def scale(self, kx=1, ky=1, kz=1, *, center=None):
        # type: (float, float, float, ..., Iterable[float] | None) -> None
        """
        缩放\n
        `kx`: x轴方向缩放比例\n
        `ky`: y轴方向缩放比例\n
        `kz`: z轴方向缩放比例\n
        `center`: 缩放中心，默认为几何中心\n
        """
        if center is None:  # NOTE: 对凹面几何体无效
            center = [statistics.mean(axis) for axis in zip(*self.coords)]
        coords = [coord for side in self.sides for coord in side.coords]
        for ind, coord in enumerate(coords):
            if coord not in coords[:ind]:
                scale(coord, kx, ky, kz, center=center)

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
        *,
        color_up='',  # type: str
        color_down='',  # type: str
        color_left='',  # type: str
        color_right='',  # type: str
        color_front='',  # type: str
        color_back='',  # type: str
    ):  # type: (...) -> None
        """
        `canvas`: 父画布\n
        `x`: 左上角x坐标\n
        `y`: 左上角y坐标\n
        `z`: 左上角z坐标\n
        `length`: 长度\n
        `width`: 宽度\n
        `height`: 高度\n
        `color_up`: 上表面颜色\n
        `color_down`: 下表面颜色\n
        `color_left`: 左侧面颜色\n
        `color_right`: 右侧面颜色\n
        `color_front`: 正面颜色\n
        `color_back`: 后面颜色\n
        """
        canvas._geos.append(self)
        self.canvas = canvas
        self.coords = [[x+l, y+w, z+h]
                       for l in (0, length)
                       for w in (0, width)
                       for h in (0, height)]
        self.sides = [
            Side(canvas, self.coords[0], self.coords[1],
                 self.coords[3], self.coords[2], fill=color_back),
            Side(canvas, self.coords[0], self.coords[1],
                 self.coords[5], self.coords[4], fill=color_left),
            Side(canvas, self.coords[0], self.coords[2],
                 self.coords[6], self.coords[4], fill=color_up),
            Side(canvas, self.coords[1], self.coords[3],
                 self.coords[7], self.coords[5], fill=color_down),
            Side(canvas, self.coords[2], self.coords[3],
                 self.coords[7], self.coords[6], fill=color_right),
            Side(canvas, self.coords[4], self.coords[5],
                 self.coords[7], self.coords[6], fill=color_front),
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
        *,
        colors=('',)*4  # type: Iterable[str]
    ):  # type: (...) -> None
        """
        `canvas`: 父画布\n
        `p1`: 第一个顶点\n
        `p2`: 第二个顶点\n
        `p3`: 第三个顶点\n
        `p4`: 第四个顶点\n
        `colors`: 颜色序列\n
        """
        canvas._geos.append(self)
        self.canvas = canvas
        self.coords = [list(p1), list(p2), list(p3), list(p4)]
        self.sides = [
            Side(canvas, self.coords[0], self.coords[1],
                 self.coords[2], fill=colors[0]),
            Side(canvas, self.coords[0], self.coords[1],
                 self.coords[3], fill=colors[1]),
            Side(canvas, self.coords[0], self.coords[2],
                 self.coords[3], fill=colors[2]),
            Side(canvas, self.coords[1], self.coords[2],
                 self.coords[3], fill=colors[3]),
        ]


__all__ = [name for name in globals() if '__' not in name]
