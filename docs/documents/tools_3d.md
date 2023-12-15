tkintertools.tools_3d
===

描述: 3D support  
外部引用: `Image`, `ImageTk`, `array`, `fractions`, `math`, `statistics`, `tkinter`, `typing`  
源代码位置: site-packages\tkintertools\tools_3d.py

Functions - 函数
---

### 01. project

!!! note "project `Function`"

    ```python
    project(
        coordinate,
        distance
    )
    ```

    将一个三维空间中的点投影到指定距离的正向平面上，并返回在该平面上的坐标

    * `coordinate`: 点的空间坐标
    * `distance`: 正向平面的距离（平面正对着我们）
    
### 02. rotate

!!! note "rotate `Function`"

    ```python
    rotate(
        coordinate,
        dx=0,
        dy=0,
        dz=0,
        *,
        center,
        axis=None
    )
    ```

    将一个三维空间中的点以一个点或线为参照进行旋转（实现方式为欧拉角）

    * `coordinate`: 点的空间坐标
    * `dx`: x 方向逆时针旋转弧度，或者绕旋转轴线的旋转弧度
    * `dy`: y 方向逆时针旋转弧度
    * `dz`: z 方向逆时针旋转弧度
    * `center`: 旋转中心的空间坐标
    * `axis`: 旋转轴线的空间坐标
    
### 03. scale

!!! note "scale `Function`"

    ```python
    scale(
        coordinate,
        kx=1,
        ky=1,
        kz=1,
        *,
        center
    )
    ```

    将一个三维空间中的点以另一个点为缩放中心进行缩放

    * `coordinate`: 点的空间坐标
    * `kx`: x 方向缩放比例
    * `ky`: y 方向缩放比例
    * `kz`: z 方向缩放比例
    * `center`: 缩放中心的空间坐标
    
### 04. translate

!!! note "translate `Function`"

    ```python
    translate(
        coordinate,
        dx=0,
        dy=0,
        dz=0
    )
    ```

    将一个三维空间中的点进行平移

    * `coordinate`: 点的空间坐标
    * `dx`: x 方向位移长度
    * `dy`: y 方向位移长度
    * `dz`: z 方向位移长度
    
Classes - 类
---

### 01. Canvas3D

!!! note "Canvas3D(Canvas) `Class`"

    3D 画布基类

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            master,
            width,
            height,
            x=None,
            y=None,
            *,
            lock=True,
            expand=True,
            keep=True,
            camera_distance=1000,
            **kw
        )
        ```


        * `master`: 父控件
        * `width`: 画布宽度
        * `height`: 画布高度
        * `x`: 画布左上角的横坐标
        * `y`: 画布左上角的纵坐标
        * `lock`: 画布内控件的功能锁，为 `False` 时功能暂时失效
        * `expand`: 画布内控件是否能缩放
        * `keep`: 画布比例是否保持不变
        * `camera_distance`: 相机位置与原点间的距离，默认值为 1000
        * `**kw`: 与 `tkinter.Canvas` 类的参数相同



    !!! note "geos `Method`"

        ```python
        geos(
            self
        )
        ```

        返回 `Canvas3D` 类全部的几何体对象


    !!! note "items\_3d `Method`"

        ```python
        items_3d(
            self
        )
        ```

        返回 `Canvas3D` 类全部的基本 3D 对象


    !!! note "space\_sort `Method`"

        ```python
        space_sort(
            self
        )
        ```

        空间位置排序

### 02. Cuboid

!!! note "Cuboid(Geometry) `Class`"

    长方体

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            x,
            y,
            z,
            length,
            width,
            height,
            *,
            boardwidth=1,
            color_fill_up='',
            color_fill_down='',
            color_fill_left='',
            color_fill_right='',
            color_fill_front='',
            color_fill_back='',
            color_outline_up='#000000',
            color_outline_down='#000000',
            color_outline_left='#000000',
            color_outline_right='#000000',
            color_outline_front='#000000',
            color_outline_back='#000000'
        )
        ```


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


### 03. Geometry

!!! note "Geometry `Class`"

    几何体

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            *sides
        )
        ```


        * `canvas`: 父画布
        * `sides`: 组成几何体的面



    !!! note "append `Method`"

        ```python
        append(
            self,
            *sides
        )
        ```

        给几何体添加更多新的面

        * `sides`: `Side` 类



    !!! note "center `Method`"

        ```python
        center(
            self
        )
        ```

        几何中心


    !!! note "rotate `Method`"

        ```python
        rotate(
            self,
            dx=0,
            dy=0,
            dz=0,
            *,
            center=(0, 0, 0),
            axis=None
        )
        ```

        旋转几何体中的所有 3D 对象

        * `dx`: x 方向逆时针旋转弧度，或者绕旋转轴线的旋转弧度
        * `dy`: y 方向逆时针旋转弧度
        * `dz`: z 方向逆时针旋转弧度
        * `center`: 旋转中心，默认为原点
        * `axis`: 旋转轴线，无默认值



    !!! note "scale `Method`"

        ```python
        scale(
            self,
            kx=1,
            ky=1,
            kz=1,
            *,
            center=None
        )
        ```

        缩放几何体中的所有 3D 对象

        * `kx`: x 方向缩放比例
        * `ky`: y 方向缩放比例
        * `kz`: z 方向缩放比例
        * `center`: 缩放中心，默认为几何中心



    !!! note "translate `Method`"

        ```python
        translate(
            self,
            dx=0,
            dy=0,
            dz=0
        )
        ```

        平移几何体中的所有 3D 对象

        * `dx`: x 方向位移长度
        * `dy`: y 方向位移长度
        * `dz`: z 方向位移长度



    !!! note "update `Method`"

        ```python
        update(
            self
        )
        ```

        更新几何体

### 04. Line

!!! note "Line(_Object3D) `Class`"

    线

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            point_start,
            point_end,
            *,
            width=1,
            fill='#000000'
        )
        ```


        * `canvas`: 父画布
        * `point_start`: 起点坐标
        * `point_end`: 终点坐标
        * `width`: 线的宽度
        * `fill`: 线的颜色



    !!! note "\_camera\_distance `Method` `Internal`"

        ```python
        _camera_distance(
            self
        )
        ```

        与相机距离


    !!! note "update `Method`"

        ```python
        update(
            self
        )
        ```

        更新对象的显示

### 05. Point

!!! note "Point(_Object3D) `Class`"

    点

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            coords,
            *,
            size=1,
            width=1,
            fill='#000000',
            outline='#000000',
            markuptext='',
            markupdelta=(0, 0),
            markupfont=('Microsoft YaHei', -24),
            markupfill='#000000',
            markupjustify='center'
        )
        ```


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



    !!! note "\_camera\_distance `Method` `Internal`"

        ```python
        _camera_distance(
            self
        )
        ```

        与相机距离


    !!! note "update `Method`"

        ```python
        update(
            self
        )
        ```

        更新对象的显示

### 06. Side

!!! note "Side(_Object3D) `Class`"

    面

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            *points,
            width=1,
            fill='',
            outline='#000000'
        )
        ```


        * `canvas`: 父画布
        * `points`: 各点的空间坐标
        * `width`: 面轮廓的宽度
        * `fill`: 面内部的填充颜色
        * `outline`: 面轮廓的颜色



    !!! note "\_camera\_distance `Method` `Internal`"

        ```python
        _camera_distance(
            self
        )
        ```

        与相机距离


    !!! note "update `Method`"

        ```python
        update(
            self
        )
        ```

        更新对象的显示

### 07. Space

!!! note "Space(Canvas3D) `Class`"

    三维空间

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            master,
            width,
            height,
            x=None,
            y=None,
            *,
            lock=True,
            expand=True,
            keep=True,
            camera_distance=1000,
            origin_size=1,
            origin_width=1,
            origin_fill='',
            origin_outline='',
            **kw
        )
        ```


        * `master`: 父控件
        * `width`: 画布宽度
        * `height`: 画布高度
        * `x`: 画布左上角的横坐标
        * `y`: 画布左上角的纵坐标
        * `lock`: 画布内控件的功能锁，为 `False` 时功能暂时失效
        * `expand`: 画布内控件是否能缩放
        * `keep`: 画布比例是否保持不变
        * `camera_distance`: 相机位置与原点间的距离，默认值为 1000
        * `origin_size`: 原点大小，默认值为 1
        * `origin_width`: 原点轮廓宽度，默认值为 1
        * `origin_fill`: 原点填充颜色，默认为无色
        * `origin_outline`: 原点轮廓颜色，默认为无色
        * `**kw`: 与 `tkinter.Canvas` 类的参数相同



    !!! note "\_rotate `Method` `Internal`"

        ```python
        _rotate(
            self,
            event,
            flag=None,
            _cache=[]
        )
        ```

        旋转事件


    !!! note "\_scale `Method` `Internal`"

        ```python
        _scale(
            self,
            event,
            flag=None
        )
        ```

        缩放事件


    !!! note "\_translate `Method` `Internal`"

        ```python
        _translate(
            self,
            event,
            flag=None,
            _cache=[]
        )
        ```

        平移事件

### 08. Tetrahedron

!!! note "Tetrahedron(Geometry) `Class`"

    四面体

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            point_1,
            point_2,
            point_3,
            point_4,
            *,
            boardwidth=1,
            color_fill=('', '', '', ''),
            color_outline=('#000000', '#000000', '#000000', '#000000')
        )
        ```


        * `canvas`: 父画布
        * `point_1`: 第一个顶点
        * `point_2`: 第二个顶点
        * `point_3`: 第三个顶点
        * `point_4`: 第四个顶点
        * `boardwidth`: 边框线条宽度
        * `color_fill`: 内部颜色序列
        * `color_outline`: 边框颜色序列


### 09. Text

!!! note "Text(_Object3D) `Class`"

    三维文本

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            canvas,
            coords,
            text='',
            *,
            font=('Microsoft YaHei', -24),
            justify='center',
            fill='#000000'
        )
        ```


        * `canvas`: 父画布
        * `coords`: 点的空间坐标
        * `text`: 显示的文本
        * `size`: 点的大小
        * `font`: 点轮廓的宽度
        * `justify`: 多行文本对齐方式
        * `fill`: 点内部的填充颜色



    !!! note "\_camera\_distance `Method` `Internal`"

        ```python
        _camera_distance(
            self
        )
        ```

        与相机距离


    !!! note "update `Method`"

        ```python
        update(
            self
        )
        ```

        更新对象的显示

### 10. _Object3D

!!! note "_Object3D `Class` `Internal`"

    3D 对象基类

    !!! tip "\_\_init\_\_ `Method` `Special`"

        ```python
        __init__(
            self,
            *coordinates
        )
        ```



    !!! note "\_project `Method` `Internal`"

        ```python
        _project(
            self,
            distance,
            canvas=None
        )
        ```

        投影对象自身

        * `distance`: 对象与观察者的距离
        * `canvas`: 投影到的画布



    !!! note "center `Method`"

        ```python
        center(
            self
        )
        ```

        几何中心


    !!! note "rotate `Method`"

        ```python
        rotate(
            self,
            dx=0,
            dy=0,
            dz=0,
            *,
            center=(0, 0, 0),
            axis=None
        )
        ```

        旋转对象本身

        * `dx`: x 方向逆时针旋转弧度，或者绕旋转轴线的旋转弧度
        * `dy`: y 方向逆时针旋转弧度
        * `dz`: z 方向逆时针旋转弧度
        * `center`: 旋转中心，默认为原点
        * `axis`: 旋转轴线，无默认值



    !!! note "scale `Method`"

        ```python
        scale(
            self,
            kx=1,
            ky=1,
            kz=1,
            *,
            center=None
        )
        ```

        缩放对象本身

        * `kx`: x 方向缩放比例
        * `ky`: y 方向缩放比例
        * `kz`: z 方向缩放比例
        * `center`: 缩放中心，默认为几何中心



    !!! note "translate `Method`"

        ```python
        translate(
            self,
            dx=0,
            dy=0,
            dz=0
        )
        ```

        平移对象本身

        * `dx`: x 方向位移长度
        * `dy`: y 方向位移长度
        * `dz`: z 方向位移长度


