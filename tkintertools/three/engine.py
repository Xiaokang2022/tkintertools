"""Core codes of 3D"""

import abc
import array
import math
import platform
import statistics
import tkinter
import typing

from ..core import constants, containers

__all__ = [
    "Canvas",
    "Space",
    "translate",
    "rotate",
    "scale",
    "project",
    "Component",
    "Point",
    "Line",
    "Plane",
    "Text3D",
    "Geometry",
]


class Canvas(containers.Canvas):
    """Base class of 3D Canvas"""

    def __init__(
        self,
        master: containers.Tk | containers.Canvas,
        *,
        expand: typing.Literal["", "x", "y", "xy"] = "xy",
        zoom_item: bool = False,
        keep_ratio: typing.Literal["min", "max"] | None = None,
        free_anchor: bool = False,
        **kwargs,
    ) -> None:
        containers.Canvas.__init__(
            self, master, expand=expand, zoom_item=zoom_item,
            keep_ratio=keep_ratio, free_anchor=free_anchor, **kwargs)
        self._components: list[Component] = []
        self._geometries: list[Geometry] = []
        self._distance: int = 1000

    @property
    def components(self) -> tuple["Component", ...]:
        """Return all `Component` of this Canvas"""
        return tuple(self._components)

    @property
    def geometries(self) -> tuple["Geometry", ...]:
        """Return all `Geometry` of this Canvas"""
        return tuple(self._geometries)

    def space_sort(self) -> None:
        """Sort the contextual relationship between the spatial positions of the components"""
        self._components.sort(key=lambda item: item._camera_distance())
        for item in self._components:
            self.lower(item.item)


class Space(Canvas):
    """A canvas where you can view 3D objects"""

    def __init__(
        self,
        master: containers.Tk | containers.Canvas,
        *,
        expand: typing.Literal["", "x", "y", "xy"] = "xy",
        zoom_item: bool = False,
        keep_ratio: typing.Literal["min", "max"] | None = None,
        free_anchor: bool = False,
        **kwargs,
    ) -> None:
        Canvas.__init__(
            self, master, expand=expand, zoom_item=zoom_item,
            keep_ratio=keep_ratio, free_anchor=free_anchor, **kwargs)

        self.bind("<B3-Motion>", self._translate, "+")
        self.bind("<Button-3>", lambda event: self._translate(event, True), "+")
        self.bind("<ButtonRelease-3>",
                  lambda event: self._translate(event, False), "+")

        self.bind("<B2-Motion>", self._rotate, "+")
        self.bind("<Button-2>", lambda event: self._rotate(event, True), "+")
        self.bind("<ButtonRelease-2>",
                  lambda event: self._rotate(event, False), "+")

        if platform.system() == "Linux":
            self.bind("<Button-4>", lambda event: self._scale(event, True), "+")
            self.bind("<Button-5>", lambda event: self._scale(event, False), "+")
        else:
            self.bind("<MouseWheel>", self._scale, "+")

    # @typing.override
    def _initialization(self) -> None:
        Canvas._initialization(self)
        # _Widget(self, _SpaceFeature)
        self._origin = Point(self, (0, 0, 0), fill="", outline="")
        self._components.clear()

    # @typing.override
    def _zoom_self(self) -> None:
        Canvas._zoom_self(self)
        for item in self._components:
            item.update()
        self.space_sort()

    def _translate(
        self,
        event: tkinter.Event,
        press: bool | None = None,
        _cache: list[float] = []
    ) -> None:
        """
        Triggering of a translation event

        * `event`: Event
        * `press`: True, False, and None represent press, release, and move events, respectively
        * `_cache`: cache values that record the coordinates of mouse presses
        """
        if press is True:  # Press
            _cache[:] = [event.x, event.y]
            self.configure(cursor="fleur")
            self._trigger_config.lock()
            return

        elif press is False:  # Release
            self._trigger_config.unlock()
            self.configure(cursor="arrow")
            return

        dx, dy = event.x - _cache[0], event.y - _cache[1]
        _cache[:] = [event.x, event.y]

        for item in self._components + [self._origin]:
            item.translate(
                0, dx*self._initial_size[0]/self._size[0], -dy*self._initial_size[1]/self._size[1])
            item.update()
        self.space_sort()

    def _rotate(
        self,
        event: tkinter.Event,
        press: bool | None = None,
        _cache: list[float] = []
    ) -> None:
        """
        Triggering of a rotation event

        * `event`: Event
        * `press`: True, False, and None represent press, release, and move events, respectively
        * `_cache`: cache values that record the coordinates of mouse presses
        """
        if press is True:  # Press
            _cache[:] = [event.x, event.y]
            self.configure(cursor="fleur")
            self._trigger_config.lock()
            return

        elif press is False:  # Release
            self._trigger_config.unlock()
            self.configure(cursor="arrow")
            return

        dx, dy = event.x - _cache[0], event.y - _cache[1]
        _cache[:] = [event.x, event.y]

        for item in self._components:
            item.rotate(0, 2*dy/self._size[0]*math.tau, 2*dx/self._size[1]*math.tau,
                        center=self._origin.coordinates[0])
            item.update()
        self.space_sort()

    def _scale(self, event: tkinter.Event, flag: bool | None = None) -> None:
        """Triggering of a scaling event"""
        if flag is not None:
            event.delta = flag
        k = 11/10 if event.delta > 0 else 10/11

        for item in self._components:
            item.scale(k, k, k, center=self._origin.coordinates[0])
            item.update()
        self.space_sort()


def translate(coordinate: tuple[float, float, float], dx: float = 0, dy: float = 0, dz: float = 0) -> None:
    """将一个三维空间中的点进行平移

    * `coordinate`: 点的空间坐标
    * `dx`: x 方向位移长度
    * `dy`: y 方向位移长度
    * `dz`: z 方向位移长度
    """
    for i, delta in enumerate((dx, dy, dz)):
        coordinate[i] += delta


@typing.overload
def rotate(coordinate, dx=0, dy=0, dz=0, *, center):
    # type: (tuple[float, float, float], float, float, float, ..., tuple[float, float, float]) -> None
    ...


@typing.overload
def rotate(coordinate, dx=0, *, axis):
    # type: (tuple[float, float, float], float,  ..., tuple[tuple[float, float, float], tuple[float, float, float]]) -> None
    ...


def rotate(coordinate, dx=0, dy=0, dz=0, *, center, axis=None):
    # type: (tuple[float, float, float], float, float, float, ..., tuple[float, float, float], tuple[tuple[float, float, float], tuple[float, float, float]] | None) -> None
    """将一个三维空间中的点以一个点或线为参照进行旋转（实现方式为欧拉角）

    * `coordinate`: 点的空间坐标
    * `dx`: x 方向逆时针旋转弧度，或者绕旋转轴线的旋转弧度
    * `dy`: y 方向逆时针旋转弧度
    * `dz`: z 方向逆时针旋转弧度
    * `center`: 旋转中心的空间坐标
    * `axis`: 旋转轴线的空间坐标
    """
    if axis is not None:  # 参照为线（定轴转动）
        center = Component(*axis).center()  # 旋转轴中点
        n = list(axis[0])
        for i in range(3):
            n[i] -= axis[1][i]
            coordinate[i] -= center[i]
        n_m = math.hypot(*n)
        for i in range(3):
            n[i] /= n_m
        x_2, y_2, z_2 = map(lambda _: _*_, n)
        zx, xy, yz = [n[i-1]*v for i, v in enumerate(n)]
        s_θ, c_θ = math.sin(dx), math.cos(dx)
        _c_θ = 1 - c_θ

        matrix = [
            [x_2*_c_θ + c_θ, xy*_c_θ + n[2]*s_θ, zx*_c_θ - n[1]*s_θ],
            [xy*_c_θ - n[2]*s_θ, y_2*_c_θ + c_θ, yz*_c_θ + n[0]*s_θ],
            [zx*_c_θ + n[1]*s_θ, yz*_c_θ - n[0]*s_θ, z_2*_c_θ + c_θ]
        ]

        for i, δ in enumerate(center):
            matrix[i] = δ + sum(matrix[i][j]*coordinate[j] for j in range(3))

    else:  # 参照为点（定点转动）
        sx, sy, sz = math.sin(dx), math.sin(dy), math.sin(dz)
        cx, cy, cz = math.cos(dx), math.cos(dy), math.cos(dz)

        matrix = [
            [cz*cy, cz*sy*sx - sz*cx, cz*sy*cx + sz*sx],
            [sz*cy, sz*sy*sx + cz*cx, sz*sy*cx - cz*sx],
            [-sy, cy*sx, cy*cx]
        ]

        for i, δ in enumerate(center):
            matrix[i] = δ + sum(matrix[i][j] * (coordinate[j]-center[j])
                                for j in range(3))

    for i, mat in enumerate(matrix):
        coordinate[i] = mat


def scale(coordinate, kx=1, ky=1, kz=1, *, center):
    # type: (tuple[float, float, float], float, float, float, ..., tuple[float, float, float]) -> None
    """将一个三维空间中的点以另一个点为缩放中心进行缩放

    * `coordinate`: 点的空间坐标
    * `kx`: x 方向缩放比例
    * `ky`: y 方向缩放比例
    * `kz`: z 方向缩放比例
    * `center`: 缩放中心的空间坐标
    """
    for i, k in enumerate((kx, ky, kz)):
        coordinate[i] += (coordinate[i] - center[i]) * (k-1)


def project(coordinate, distance):
    # type: (tuple[float, float, float], float) -> tuple[float, float]
    """将一个三维空间中的点投影到指定距离的正向平面上，并返回在该平面上的坐标

    * `coordinate`: 点的空间坐标
    * `distance`: 正向平面的距离（平面正对着我们）
    """
    relative_dis = distance - coordinate[0]
    if relative_dis <= 1e-16:
        return [math.inf]*2
    k = distance / relative_dis
    return coordinate[1]*k, coordinate[2]*k


class Component(abc.ABC):
    """3D 对象基类"""

    def __init__(self, *coordinates):
        # type: (tuple[float, float, float]) -> None
        self.coordinates = [array.array("f", lst) for lst in coordinates]

    def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> None
        """平移对象本身

        * `dx`: x 方向位移长度
        * `dy`: y 方向位移长度
        * `dz`: z 方向位移长度
        """
        for coordinate in self.coordinates:
            translate(coordinate, dx, dy, dz)

    @typing.overload
    def rotate(self, dx=0, dy=0, dz=0, *, center=(0, 0, 0)):
        # type: (float, float, float, ..., tuple[float, float, float]) -> None
        ...

    @typing.overload
    def rotate(self, dx=0, *, axis):
        # type: (float, ..., tuple[tuple[float, float, float], tuple[float, float, float]]) -> None
        ...

    def rotate(self, dx=0, dy=0, dz=0, *, center=(0, 0, 0), axis=None):
        # type: (float, float, float, ..., tuple[float, float, float], tuple[tuple[float, float, float], tuple[float, float, float]] | None) -> None
        """旋转对象本身

        * `dx`: x 方向逆时针旋转弧度，或者绕旋转轴线的旋转弧度
        * `dy`: y 方向逆时针旋转弧度
        * `dz`: z 方向逆时针旋转弧度
        * `center`: 旋转中心，默认为原点
        * `axis`: 旋转轴线，无默认值
        """
        for i, coordinate in enumerate(self.coordinates):
            # if dx != 0:
            #     coordinate = q_rotate(coordinate, (1, 0, 0), dx)
            # if dy != 0:
            #     coordinate = q_rotate(coordinate, (0, 1, 0), dy)
            # if dz != 0:
            #     coordinate = q_rotate(coordinate, (0, 0, 1), dz)
            # coordinate = array.array('f', coordinate)
            # for j in range(3):
            #     coordinate[j] += center[j]
            # self.coordinates[i] = coordinate
            rotate(coordinate, dx, dy, dz, center=center, axis=axis)

    def scale(self, kx=1, ky=1, kz=1, *, center=None):
        # type: (float, float, float, ..., tuple[float, float, float] | None) -> None
        """缩放对象本身

        * `kx`: x 方向缩放比例
        * `ky`: y 方向缩放比例
        * `kz`: z 方向缩放比例
        * `center`: 缩放中心，默认为几何中心
        """
        if center is None:
            center = self.center()
        for coordinate in self.coordinates:
            scale(coordinate, kx, ky, kz, center=center)

    def center(self):  # type: () -> tuple[float, float, float]
        """几何中心"""
        return tuple(statistics.mean(xyz) for xyz in zip(*self.coordinates))

    def _project(self, distance, canvas=None):
        # type: (float, Canvas | Space | None) -> list[tuple[float, float]]
        """投影对象自身

        * `distance`: 对象与观察者的距离
        * `canvas`: 投影到的画布
        """
        lst = [project(point, distance) for point in self.coordinates]
        if canvas is not None:
            lst = [(pos[0] + canvas._initial_size[0]/2, canvas._initial_size[1]/2 - pos[1])
                   for pos in lst]
        return lst

    @abc.abstractmethod
    def update(self) -> None: ...


class Point(Component):
    """点"""

    def __init__(
        self,
        canvas,  # type: Canvas | Space
        coords,  # type: tuple[float, float, float]
        *,
        size=1,  # type: float
        width=1,  # type: float
        fill="#000000",  # type: str
        outline="#000000",  # type: str
        markuptext="",  # type: str
        markupdelta=(0, 0),  # type: tuple[float, float]
        markupfont=(constants.FONT, constants.SIZE),
        # type: tuple[str, int, str]
        markupfill="#000000",  # type: str
        markupjustify="center",  # type: str
    ):  # type: (...) -> None
        """
        * `canvas`: 父画布
        * `coords`: 点的空间坐标
        * `size`: 点的大小
        * `width`: 点轮廓的宽度
        * `fill`: 点内部的填充颜色
        * `outline`: 点轮廓的颜色
        * `markuptext`: 标记文本
        * `markupdelta`: 标记文本显示位置的偏移量
        * `markupfont`: 标记文本字体
        * `markupfill`: 标记文本颜色
        * `markupjustify`: 标记文本多行对齐方式
        """
        Component.__init__(self, list(coords))
        canvas._components.append(self)
        self.canvas = canvas
        self.size = size
        self.width = width
        self.fill = fill
        self.item = canvas.create_oval(-1, -1, -1, -1,
                                       fill=fill, outline=outline, width=width)
        self.text = None
        if markuptext:
            self.text = canvas.create_text(-1, -1, text=markuptext,
                                           font=markupfont, fill=markupfill, justify=markupjustify)
            self.delta = markupdelta
        self.update()

    def update(self):  # type: () -> None
        """更新对象的显示"""
        x, y = self._project(self.canvas._distance, self.canvas)[0]
        self.canvas.coords(self.item, (x-self.size) * self.canvas.ratios[0], (y-self.size) *
                           self.canvas.ratios[1], (x+self.size) * self.canvas.ratios[0], (y+self.size) * self.canvas.ratios[1])
        if self.text is not None:
            self.canvas.coords(
                self.text, (x+self.delta[0]) * self.canvas.ratios[0], (y-self.delta[1]) * self.canvas.ratios[1])

    def _camera_distance(self):  # type: () -> float
        """与相机距离"""
        sign = math.copysign(1, self.canvas._distance - self.coordinates[0][0])
        return sign * math.dist([self.canvas._distance, 0, 0], self.coordinates[0])


class Line(Component):
    """线"""

    def __init__(
        self,
        canvas,  # type: Canvas | Space
        point_start,  # type: tuple[float, float, float]
        point_end,  # type: tuple[float, float, float]
        *,
        width=1,  # type: float
        fill="#000000",  # type: str
    ):  # type: (...) -> None
        """
        * `canvas`: 父画布
        * `point_start`: 起点坐标
        * `point_end`: 终点坐标
        * `width`: 线的宽度
        * `fill`: 线的颜色
        """
        Component.__init__(self, list(point_start), list(point_end))
        canvas._components.append(self)
        self.canvas = canvas
        self.width = width
        self.fill = fill
        self.item = canvas.create_line(-1, -1, -1, -1, width=width, fill=fill)
        self.update()

    def update(self):  # type: () -> None
        """更新对象的显示"""
        self.canvas.coords(self.item, *[coord * self.canvas.ratios[i]
                           for point in self._project(self.canvas._distance, self.canvas) for i, coord in enumerate(point)])

    def _camera_distance(self):  # type: () -> float
        """与相机距离"""
        center = self.center()
        sign = math.copysign(1, self.canvas._distance - center[0])
        return sign * math.dist([self.canvas._distance, 0, 0], center)


class Plane(Component):
    """面"""

    def __init__(
        self,
        canvas,  # type: Canvas | Space
        *points,  # type: tuple[float, float, float]
        width=1,  # type: float
        fill="",  # type: str
        outline="#000000",  # type: str
    ):  # type: (...) -> None
        """
        * `canvas`: 父画布
        * `points`: 各点的空间坐标
        * `width`: 面轮廓的宽度
        * `fill`: 面内部的填充颜色
        * `outline`: 面轮廓的颜色
        """
        Component.__init__(self, *[list(point) for point in points])
        canvas._components.append(self)
        self.canvas = canvas
        self.width = width
        self.fill = fill
        self.outline = outline
        self.item = canvas.create_polygon(-1, -1, -1, -1,
                                          width=width, fill=fill, outline=outline)
        self.update()

    def update(self):  # type: () -> None
        """更新对象的显示"""
        self.canvas.coords(
            self.item, *[coord * self.canvas.ratios[i] for point in self._project(self.canvas._distance, self.canvas) for i, coord in enumerate(point)])

    def _camera_distance(self):  # type: () -> float
        """与相机距离"""
        center = self.center()
        sign = math.copysign(1, self.canvas._distance - center[0])
        return sign * math.dist([self.canvas._distance, 0, 0], center)


class Text3D(Component):
    """三维文本"""

    def __init__(
        self,
        canvas,  # type: Canvas | Space
        coords,  # type: tuple[float, float, float]
        text="",  # type: str
        *,
        # type: tuple[str, int, str]
        font=(constants.FONT, constants.SIZE),
        justify="center",  # type: typing.Literal["center", "left", "right"]
        fill="#000000",  # type: str
    ):  # type: (...) -> None
        """
        * `canvas`: 父画布
        * `coords`: 点的空间坐标
        * `text`: 显示的文本
        * `size`: 点的大小
        * `font`: 点轮廓的宽度
        * `justify`: 多行文本对齐方式
        * `fill`: 点内部的填充颜色
        """
        Component.__init__(self, list(coords))
        canvas._components.append(self)
        self.canvas = canvas
        self.font = font
        self.fill = fill
        self.text = text
        self.item = canvas.create_text(-1, -1,
                                       text=text, fill=fill, justify=justify)
        self.update()

    def update(self):  # type: () -> None
        """更新对象的显示"""
        x, y = self._project(self.canvas._distance, self.canvas)[0]
        self.canvas.coords(
            self.item, x*self.canvas.ratios[0], y*self.canvas.ratios[1])
        font = list(self.font)
        font[1] = round(font[1] * self.canvas._distance *
                        math.sqrt(self.canvas.ratios[0]*self.canvas.ratios[1]) / self._camera_distance())
        self.canvas.itemconfigure(self.item, font=font)

    def _camera_distance(self):  # type: () -> float
        """与相机距离"""
        sign = math.copysign(1, self.canvas._distance - self.coordinates[0][0])
        return sign * math.dist([self.canvas._distance, 0, 0], self.coordinates[0])


class Geometry:
    """几何体"""

    def __init__(
        self,
        canvas,  # type: Canvas | Space
        *sides,  # type: Plane
    ):  # type: (...) -> None
        """
        * `canvas`: 父画布
        * `sides`: 组成几何体的面
        """
        canvas._geometries.append(self)
        self.canvas = canvas
        self.sides = list(sides)

    def translate(self, dx=0, dy=0, dz=0):  # type: (float, float, float) -> None
        """平移几何体中的所有 3D 对象

        * `dx`: x 方向位移长度
        * `dy`: y 方向位移长度
        * `dz`: z 方向位移长度
        """
        for side in self.sides:
            side.translate(dx, dy, dz)

    @typing.overload
    def rotate(self, dx=0, dy=0, dz=0, *, center=(0, 0, 0)):
        # type: (float, float, float, ..., tuple[float, float, float]) -> None
        ...

    @typing.overload
    def rotate(self, dx=0, *, axis):
        # type: (float, ..., tuple[tuple[float, float, float], tuple[float, float, float]]) -> None
        ...

    def rotate(self, dx=0, dy=0, dz=0, *, center=(0, 0, 0), axis=None):
        # type: (float, float, float, ..., tuple[float, float, float], tuple[tuple[float, float, float], tuple[float, float, float]] | None) -> None
        """旋转几何体中的所有 3D 对象

        * `dx`: x 方向逆时针旋转弧度，或者绕旋转轴线的旋转弧度
        * `dy`: y 方向逆时针旋转弧度
        * `dz`: z 方向逆时针旋转弧度
        * `center`: 旋转中心，默认为原点
        * `axis`: 旋转轴线，无默认值
        """
        for side in self.sides:
            side.rotate(dx, dy, dz, center=center, axis=axis)

    def scale(self, kx=1, ky=1, kz=1, *, center=None):
        # type: (float, float, float, ..., tuple[float, float, float] | None) -> None
        """缩放几何体中的所有 3D 对象

        * `kx`: x 方向缩放比例
        * `ky`: y 方向缩放比例
        * `kz`: z 方向缩放比例
        * `center`: 缩放中心，默认为几何中心
        """
        if center is None:
            center = self.center()
        for side in self.sides:
            side.scale(kx, ky, kz, center=center)

    def center(self):  # type: () -> tuple[float, float, float]
        """几何中心"""
        return tuple(statistics.mean(axis) for axis in zip(*set(tuple(coord) for side in self.sides for coord in side.coordinates)))

    def update(self):  # type: () -> None
        """更新几何体"""
        for side in self.sides:
            side.update()

    def append(self, *sides):  # type: (Plane) -> None
        """给几何体添加更多新的面

        * `sides`: `Side` 类
        """
        for side in sides:
            self.sides.append(side)
