<div align="center">

# 🚀tkintertools🚀

<img src="tkt.png" style="height: 128px" alt="Logo" />

`tkintertools` 模块是 `tkinter` 模块的一个辅助模块\
The `tkintertools` module is an auxiliary module of the `tkinter` module

[![Version](https://img.shields.io/pypi/v/tkintertools?label=Version)](.)
[![License](https://img.shields.io/pypi/l/tkintertools?label=License)](LICENSE.txt)
[![ChangeLog](https://img.shields.io/badge/ChangeLog-2023/08/10-orange)](CHANGELOG.md)
[![ToDo](https://img.shields.io/badge/ToDo-13-yellow)](TODO.md)
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

* Version/最新版本 : `2.6.9`
* Release/发布日期 : 2023/08/09 (UTC+08)

这个是目前的最新稳定版，相对于开发版本而言比较稳定，bug 大体上是没有那么多的，推荐使用这个。稳定版和开发版相比，它在发布之前有个测试的步骤，经过测试之后（各项功能正常运行，多平台兼容）才会发布。

**PIP Cmd/安装命令：**

```
pip install tkintertools==2.6.9
```

### Development Version/开发版本

* Version/最新版本 : `2.6.10.dev0` (第 1 个预发布版本)
* Release/发布日期 : 2023/08/10 (UTC+08)

这个是我正在开发的版本，可能有新功能，bug 可能会比较多，但也可能会比原来的版本更加稳定。开发版没有经过多操作系统的测试，仅能保证在 Windows 系统下运行所有功能，在其他的操作系统上，可能有部分功能无法正常运行。大家可以在 Issues 中提出一些建议，我可能会适当采纳一些并在开发版本中更改或实现。

**PIP Cmd/安装命令：**

```
pip install tkintertools==2.6.10.dev0
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

如果拥有 PIL 库，则 tkintertools 会运行得更快，但 PIL 并不是必须的，没有 PIL 的情况下 tkintertools 依然可以正常使用。

News/最新功能👇
--------------

### Release Notes/版本说明

**最新版本: `tkintertools-v2.6.10.dev0`**

> **Note**   
> tkintertools 的介绍、使用教程和开发文档均在 [Wiki](https://github.com/Xiaokang2022/tkintertools/wiki) 中，大家可前往查阅

下面是本次开发版本（`v2.6.9` -> `v2.6.10.dev0`）的更新内容条目：

- [X] The widget `Progressbar` adds a indeterminate mode  
控件 `Progressbar` 新增不定模式
- [X] The value of the constant `SWITCH_WIDTH` is changed from 0 to 60  
常量 `SWITCH_WIDTH` 的值从 0 更改为 60
- [X] The parameter `width` of class `Switch` was changed from positional argument to keyword argument  
类 `Switch` 的参数 `width` 由位置参数更改为关键字参数

### Template Demo/模板演示

下面是一个主要新功能的示例程序：进度条控件为不定模式

下面是示例程序的效果图（运行环境为 **Windows11 家庭中文版 23H2 - Python3.11.4**）：

![news](news.png)

<details><summary><b>CODE/源代码</b></summary>

```python
# 此处只展示核心代码

pb = tkt.Progressbar(canvas, 320, 320, 640, 35, mode='indeterminate')  # 不定模式
pb.load(0.7)  # 加载到 70% 的状态
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
