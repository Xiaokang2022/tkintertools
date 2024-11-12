---
comments: true
date:
    created: 2024-09-09
    updated: 2024-11-12
authors:
  - I-love-study
  - _Xiaokang2022
categories:
  - 用户投稿
tags:
  - 经验
  - 3.0.0rc1
---

# 几种相对坐标转绝对坐标的实现方法

因为 `tkintertools` 是基于坐标绘制的 UI 库，所以需要很多绝对坐标，但是如果有些组件坐标关联程度较大的话，就可能会出现牵一发而动全身的效果，并且由于 `position` 的 type hint 要求是 `#!py tuple[int, int]`，所以像是使用 `list`, `#!py numpy.array` 之类的就会在类型检查的时候报红。
为了能够不要每次修改坐标都需要牵一发而动全身，下面有几种方法能够简化大家计算绝对路径的方法。

<!-- more -->

## 一、使用函数工厂

```python
def create_reletive_coords(x: int, y: int):

    def trans_coords(x_rele: int, y_rele: int):
        return (x + x_rele, y + y_rele)

    return trans_coords

rc = create_reletive_coords(450, 300)
tkt.Text(cv, rc(0, 0) , text="账号", anchor="nw")
tkt.InputBox(cv, rc(0, 40), (380, 50), placeholder="点击输入账号")
```

通过创建一个工厂函数，返回可以创建一个绝对坐标转相对坐标的函数。

基于上面的理念，我们还可以创建一个类来实现更多功能。

## 二、类

```python
from typing import NamedTuple
import tkintertools as tkt


class ReletiveCoords(NamedTuple):
    x: int
    y: int

    def __add__(self, other: tuple[int, int]) -> "ReletiveCoords":
        return ReletiveCoords(self.x + other[0], self.y + other[1])

    __radd__ = __add__

    def __sub__(self, other: tuple[int, int]) -> "ReletiveCoords":
        return ReletiveCoords(self.x - other[0], self.y - other[1])

    def __rsub__(self, other: tuple[int, int]) -> "ReletiveCoords":
        return ReletiveCoords(other[0] - self.x, other[1] - self.y)

    def __call__(self, x: int, y: int) -> "ReletiveCoords":
        return ReletiveCoords(self.x + x, self.y + y)

rc = ReletiveCoords(450, 300)
tkt.Text(cv, rc , text="账号", anchor="nw")
tkt.InputBox(cv, rc(0, 40), (380, 50), placeholder="点击输入账号")

rc2 = rc + (0, 100)
tkt.Text(cv, rc2, text="密码", anchor="nw")
tkt.InputBox(cv, rc(0, 40), (380, 50), show="●", placeholder="点击输入密码")
```

通过让 `#!py NamedTuple` 添加了 `#!py __add__`, `#!py __radd__`, `#!py __sub__`, `#!py __rsub__`, `#!py __call__` 的魔法方法，以实现相关方法，相比于第一个方法，该方法**能够自由加减，以达到更好的使用便利性**。

---

<small>原链接: <https://github.com/Xiaokang2022/tkintertools/discussions/35></small>
