<div align="center">

# 🚀tkintertools🚀

<img src="tkt.png" style="height: 128px" alt="Logo" />

`tkintertools` 模块是 `tkinter` 模块的一个辅助模块\
The `tkintertools` module is an auxiliary module of the `tkinter` module

[![Version](https://img.shields.io/badge/Version-2.6.5-blue)](.)
[![License](https://img.shields.io/badge/License-Mulan%20PSL%20v2-green)](LICENSE.txt)
[![ChangeLog](https://img.shields.io/badge/ChangeLog-2023/06/17-orange)](CHANGELOG.md)
[![ToDo](https://img.shields.io/badge/ToDo-14-yellow?logo=cachet)](TODO.md)
[![Wiki](https://img.shields.io/badge/Wiki-15-purple)](https://github.com/Xiaokang2022/tkintertools/wiki)\
[![Downloads](https://img.shields.io/badge/Download-8k-white?logo=pypi)](https://pypistats.org/packages/tkintertools)
[![Author](https://img.shields.io/badge/Author-小康2022-springgreen)](https://github.com/Xiaokang2022)
[![Blog](https://img.shields.io/badge/Blog-小康2022@CSDN-red)](https://xiaokang2022.blog.csdn.net)
[![Email](https://img.shields.io/badge/Email-2951256653@qq.com-cyan)](mailto:2951256653@qq.com)

[![Insights](https://repobeats.axiom.co/api/embed/ab8fae686a5a96f91fa71c40c53c189310924f5e.svg)](https://github.com/Xiaokang2022/tkintertools/pulse)

</div>

Install/模块安装👇
-----------------

### Stable Version/稳定版本

* Version/最新版本 : `2.6.5`
* Release/发布日期 : 2023/06/17 (UTC+08)

这个是目前的最新稳定版，相对于开发版本而言比较稳定，bug 大体上是没有那么多的，推荐使用这个。  
稳定版和开发版相比，它在发布之前有个测试的步骤，经过测试之后（各项功能正常运行，多平台兼容）才会发布。

**PIP Cmd/安装命令：**

```
pip install tkintertools==2.6.5
```

### Development Version/开发版本

* Version/最新版本 : `2.6.5`
* Release/发布日期 : 2023/06/13 (UTC+08)

这个是我正在开发的版本，可能有新功能，bug 可能会比较多，但也可能会比原来的版本更加稳定。  
开发版没有经过多操作系统的测试，仅能保证在 Windows 系统下运行所有功能，在其他的操作系统上，可能有部分功能无法正常运行。  
大家可以在 Issues 中提出一些建议，我可能会适当采纳一些并在开发版本中更改或实现。

**PIP Cmd/安装命令：**

```
pip install tkintertools-dev==2.6.5
```

> **Warning**  
> 开发版仅作示例，各函数或类的 API 并非最终确定结果，直接使用开发版可能导致后续无法与稳定版兼容！  
> 若要使用开发版，请先卸载稳定版后再进行 pip 安装，再次使用稳定版时也是一样，先卸载开发版再安装稳定版，否则会导致安装无效！

### Requirements/环境需求

目前稳定版在以下操作系统中已经测试通过:

![Windows10](https://img.shields.io/badge/Windows-10-green?logo=windows)
![Windows11](https://img.shields.io/badge/Windows-11-green?logo=windows11)
![Ubuntu22.04](https://img.shields.io/badge/Ubuntu-22.04-green?logo=ubuntu)

可能还有其他的操作系统也是可以运行 tkintertools 的，我没有进行更多的验证。  
没有任何额外的依赖包（除了一般 Python 内置的 tkinter），但只支持以下 Python 版本:

![Python3.8](https://img.shields.io/badge/Python-3.8.*-blue?logo=python)
![Python3.9](https://img.shields.io/badge/Python-3.9.*-blue?logo=python)
![Python3.10](https://img.shields.io/badge/Python-3.10.*-blue?logo=python)
![Python3.11](https://img.shields.io/badge/Python-3.11.*-blue?logo=python)
![Python3.12](https://img.shields.io/badge/Python-3.12.*-blue?logo=python)

News/最新功能👇
--------------

**最新版本: tkintertools-2.6.5 稳定版**

> **Note**  
> 重磅炸裂更新：新增了 Wiki 供大家查看，方便大家迅速掌握 tkintertools 的使用方法和小技巧！[点此传送](https://github.com/Xiaokang2022/tkintertools/wiki)  
> 近期本人将暂时停止对 tkintertools 模块本身的更新，本人先去完善 Wiki 再继续更新 tkintertools！

下面是本次版本更新内容条目：

- [X] 子模块 `tools_3d` 新增类 `Space` 可以直接提供对 3D 对象进行平移、旋转和缩放等操作的功能；
- [X] 修复了类 `Cuboid` 和类 `Tetrahedron` 没有将实例添加到父类 `Canvas_3D` 的 bug；
- [X] 修复了当 3D 对象出现在相机位置后面时会显示错误的 bug（目前更改为透视，即不显示）；
- [X] 修复了部分错误的类型提示和错误的参数默认值；
- [X] 移除常量 `BACKGROUND` 并且不再对类 `Canvas` 的默认背景颜色做限定；

下面是一个主要新功能的示例程序，运行下面的示例程序时，其拥有以下功能：

* 按住鼠标左键拖动可以旋转这多个几何体；
* 按住鼠标右键拖动可以移动这些几何体在空间中的位置；
* 滚动鼠标中键可以放大和缩小画面；
* 按“=”和“-”键分别可以放大和缩小几何体的大小；

下面是示例程序的效果图（运行环境为 Windows11-Python3.11.4）：

![news.png](news.png)

<details><summary><b>点击查看源代码</b></summary>

```python
import tkintertools as tkt
from tkintertools import tools_3d as t3d

root = tkt.Tk('tkintertools-2.6.5', 1280, 720)
cv3d = t3d.Space(root, 1280, 720, 0, 0)

for a in -100, 0, 100:
    for b in -100, 0, 100:
        for c in -100, 0, 100:
            t3d.Cuboid(cv3d, a-50, b-50, c-50, 100, 100, 100,
                       color_up='white', color_down='yellow', color_left='red',
                       color_right='orange', color_front='blue', color_back='green')
cv3d.space_sort()


def scale(event):
    """ 缩放事件 """
    k = 1.05 if event.keysym == 'equal' else 0.95 if event.keysym == 'minus' else 1
    for geo in cv3d.geos():
        geo.scale(k, k, k)
        geo.update()
    cv3d.space_sort()


root.bind('<Any-Key>', scale)
root.mainloop()
```

</details>

More/更多👇
-----------

[GitHub](https://github.com/Xiaokang2022/tkintertools): 仓库根源，完整无误  
[Gitee(镜像源)](https://gitee.com/xiaokang-2022/tkintertools): 主镜像源，（应该）完整无误  
[GitCode(镜像源)](https://gitcode.net/weixin_62651706/tkintertools): 次镜像源，缺少 Wiki  
