<div align="center">

# 🚀tkintertools🚀

<img src="tkt.png" style="height: 128px" alt="Logo" />

`tkintertools` 模块是 `tkinter` 模块的一个辅助模块\
The `tkintertools` module is an auxiliary module of the `tkinter` module

[![Version](https://img.shields.io/pypi/v/tkintertools?label=Version)](.)
[![License](https://img.shields.io/pypi/l/tkintertools?label=License)](LICENSE.txt)
[![ChangeLog](https://img.shields.io/badge/ChangeLog-2023/08/06-orange)](CHANGELOG.md)
[![ToDo](https://img.shields.io/badge/ToDo-15-yellow)](TODO.md)
[![Size](https://img.shields.io/github/languages/code-size/Xiaokang2022/tkintertools?label=Size)](tkintertools)
[![Wiki](https://img.shields.io/badge/Wiki-14-purple)](https://github.com/Xiaokang2022/tkintertools/wiki)\
[![Downloads](https://img.shields.io/pypi/dm/tkintertools?label=Downloads&logo=pypi)](https://pypistats.org/packages/tkintertools)
[![Owner](https://img.shields.io/badge/Owner-Xiaokang2022-white)](https://github.com/Xiaokang2022)
[![Blog](https://img.shields.io/badge/Blog-小康2022@CSDN-red)](https://xiaokang2022.blog.csdn.net)
[![Email](https://img.shields.io/badge/Email-2951256653@qq.com-cyan)](mailto:2951256653@qq.com)

[![Insights](https://repobeats.axiom.co/api/embed/ab8fae686a5a96f91fa71c40c53c189310924f5e.svg)](https://github.com/Xiaokang2022/tkintertools/pulse)

</div>

Install/模块安装👇
-----------------

### Stable Version/稳定版本

* Version/最新版本 : `2.6.8`
* Release/发布日期 : 2023/08/03 (UTC+08)

这个是目前的最新稳定版，相对于开发版本而言比较稳定，bug 大体上是没有那么多的，推荐使用这个。稳定版和开发版相比，它在发布之前有个测试的步骤，经过测试之后（各项功能正常运行，多平台兼容）才会发布。

**PIP Cmd/安装命令：**

```
pip install tkintertools==2.6.8
```

### Development Version/开发版本

* Version/最新版本 : `2.6.9.dev0` (第 1 个预发布版本)
* Release/发布日期 : 2023/08/06 (UTC+08)

这个是我正在开发的版本，可能有新功能，bug 可能会比较多，但也可能会比原来的版本更加稳定。开发版没有经过多操作系统的测试，仅能保证在 Windows 系统下运行所有功能，在其他的操作系统上，可能有部分功能无法正常运行。大家可以在 Issues 中提出一些建议，我可能会适当采纳一些并在开发版本中更改或实现。

**PIP Cmd/安装命令：**

```
pip install tkintertools==2.6.9.dev0
```

> **Warning**  
> 开发版仅作示例，各函数或类的 API 并非最终确定结果，直接使用开发版可能导致后续无法与稳定版兼容！  
> 若不指定具体的版本号，则会下载最新的稳定版本，也就是说，开发版本只能通过指定的版本号获取！

### Requirements/环境需求

目前 **稳定版** 在以下操作系统中已经测试通过:

![Windows10](https://img.shields.io/badge/Windows-10-green?logo=windows)
![Windows11](https://img.shields.io/badge/Windows-11-green?logo=windows11)
![Ubuntu22.04](https://img.shields.io/badge/Ubuntu-22.04-green?logo=ubuntu)

可能还有其他的操作系统也是可以运行 tkintertools 的，我没有进行更多的验证。  
没有任何额外的依赖包（除了一般 Python 内置的 tkinter），但只支持以下 Python 版本:

![Python3.8.*](https://img.shields.io/badge/Python-3.8.*-blue?logo=python)
![Python3.9.*](https://img.shields.io/badge/Python-3.9.*-blue?logo=python)
![Python3.10.*](https://img.shields.io/badge/Python-3.10.*-blue?logo=python)
![Python3.11.*](https://img.shields.io/badge/Python-3.11.*-blue?logo=python)
![Python3.12.*](https://img.shields.io/badge/Python-3.12.*-blue?logo=python)

News/最新功能👇
--------------

### Release Notes/版本说明

**最新版本: `tkintertools-v2.6.9.dev0`**

> **Note**   
> tkintertools 的介绍、使用教程和开发文档均在 [Wiki](https://github.com/Xiaokang2022/tkintertools/wiki) 中，大家可前往查阅

下面是本次开发版本（`v2.6.8` -> `v2.6.9.dev0`）的更新内容条目：

- [X] Added widget Tip (`ToolTip`) and all virtual widgets added the parameter `tooltip`  
新增控件提示框（`ToolTip`），且所有虚拟控件新增参数 `tooltip`
- [X] Added constants `DURATION`、`TOOLTIP_FG`、`TOOLTIP_BG`、`TOOLTIP_HIGNLIGHT_THICKNESS` and `TOOLTIP_HIGNLIGHT_BACKGROUND`  
新增常量 `DURATION`、`TOOLTIP_FG`、`TOOLTIP_BG`、`TOOLTIP_HIGNLIGHT_THICKNESS` 和 `TOOLTIP_HIGNLIGHT_BACKGROUND`
- [X] Fixed an issue where the text class widget called method `clear` was invalid  
修复了文本类控件调用方法 `clear` 无效的问题
- [X] Optimized the method `wm_geometry` of class `Tk` to accommodate some specially formatted parameters  
优化了类 `Tk` 的方法 `wm_geometry` 以适应某些特殊格式的参数

### Template Demo/模板演示

下面是一个主要新功能的示例程序，当按照示例代码方式给虚拟控件传入一个名为 `tooltip` 的参数之后，便可以让这个控件拥有提示框

下面是示例程序的效果图（运行环境为 Windows11-Python3.11.4）：

![news](news.png)

<details><summary><b>CODE/源代码</b></summary>

```python
# 此处只展示核心代码

tip = tkt.ToolTip('模块介绍\nToolTip 测试')
tkt.Button(canvas, 10, 660, 200, 50, text='Doc', tooltip=tip)
```

</details>

More/更多👇
-----------

[![GitHub](https://img.shields.io/badge/GitHub-仓库根源%20完整无误%20以此为准-blue?logo=github)](https://github.com/Xiaokang2022/tkintertools)
[![Gitee](https://img.shields.io/badge/Gitee-主镜像源%20比较完整%20可能延迟-green?logo=gitee)](https://gitee.com/xiaokang-2022/tkintertools)
[![GitCode](https://img.shields.io/badge/GitCode-次镜像源%20缺少Wiki%20CSDN-yellow)](https://gitcode.net/weixin_62651706/tkintertools)\
[![GitHub Watchers](https://img.shields.io/github/watchers/Xiaokang2022/tkintertools?label=GitHub%20Watchers&color=green)](https://github.com/Xiaokang2022/tkintertools/watchers)
[![GitHub Forks](https://img.shields.io/github/forks/Xiaokang2022/tkintertools?label=GitHub%20Forks)](https://github.com/Xiaokang2022/tkintertools/forks)
[![GitHub Stars](https://img.shields.io/github/stars/Xiaokang2022/tkintertools?label=GitHub%20Stars&color=gold)](https://github.com/Xiaokang2022/tkintertools/stargazers)
[![GitHub Contributors](https://img.shields.io/github/contributors/Xiaokang2022/tkintertools?label=GitHub%20Contributors)](https://github.com/Xiaokang2022/tkintertools/graphs/contributors)
[![GitHub Issues](https://img.shields.io/github/issues/Xiaokang2022/tkintertools?label=GitHub%20Issues)](https://github.com/Xiaokang2022/tkintertools/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/Xiaokang2022/tkintertools?label=GitHub%20Pull%20Requests)](https://github.com/Xiaokang2022/tkintertools/pulls)
