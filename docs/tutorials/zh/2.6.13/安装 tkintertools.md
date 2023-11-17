# §1.1 安装 tkintertools

- [§1.1 安装 tkintertools](#11-安装-tkintertools)
  - [一、运行环境](#一运行环境)
  - [二、获取稳定版](#二获取稳定版)
    - [2.1 Windows 平台](#21-windows-平台)
    - [2.2 Linux 平台](#22-linux-平台)
      - [2.2.1 检测是否有 tkinter](#221-检测是否有-tkinter)
      - [2.2.2 通过 miniconda 安装合适的 Python 环境](#222-通过-miniconda-安装合适的-python-环境)
  - [三、获取预览版（可选）](#三获取预览版可选)
  - [四、更新与查看版本](#四更新与查看版本)
    - [4.1 更新版本](#41-更新版本)
    - [4.2 查看版本](#42-查看版本)

一、运行环境
-----------

tkintertools 是跨平台的，至少可以在下面多个平台上运行（已测试）：

![Windows10](https://img.shields.io/badge/Windows-10-green?logo=windows)
![Windows11](https://img.shields.io/badge/Windows-11-green?logo=windows11)
![Ubuntu22.04](https://img.shields.io/badge/Ubuntu-22.04-green?logo=ubuntu)
![Deepin20.9](https://img.shields.io/badge/Deepin-20.9-green?logo=deepin)

同时支持以下版本的 Python：

![Python3.8](https://img.shields.io/badge/Python-3.8-blue?logo=python)
![Python3.9](https://img.shields.io/badge/Python-3.9-blue?logo=python)
![Python3.10](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Python3.11](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Python3.12](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Python3.13](https://img.shields.io/badge/Python-3.13-blue?logo=python)

相关的依赖包（小部分 Python 没有自带，如 Linux 自带的 Python）：

![tkinter8.6.*](https://img.shields.io/badge/tkinter-≥8.6-yellow)

可提升性能和效果的相关第三方包（非必须安装）：

![Pillow](https://img.shields.io/badge/Pillow-≥10.0-red)

二、获取稳定版
-------------

稳定版，相对于开发版本而言比较稳定，在发布之前有个测试的步骤，经过测试之后（各项功能正常运行，多平台兼容）才会发布，bug 大体上是没有那么多的，推荐使用这个。

### 2.1 Windows 平台

稳定版可以通过 Python 的包下载工具 `pip` 来直接从 PyPI 上获取 `tkintertools`！以下命令默认安装最新稳定版 `tkintertools`。

```
pip install tkintertools
```

若网速较慢，可选取镜像源来下载，但是镜像源可能不是最新的，下面是使用清华大学镜像源的方式进行安装：

```
pip install tkintertools -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 2.2 Linux 平台

由于 Linux 自带的 Python 环境可能不满足要求，因此在 Windows 平台操作的基础上还需添加一些额外的步骤。

#### 2.2.1 检测是否有 tkinter

打开终端输入 python3 进入 Linux 自带的 Python3 交互环境，输入下面的命令来验证 tkinter 是否安装：

```python
import tkinter
```

若没有出现报错则说明已安装 tkinter，但是一般情况都是没有安装的，会报错。

#### 2.2.2 通过 miniconda 安装合适的 Python 环境

我们不直接安装 tkinter，因为直接安装 tkinter 的步骤非常繁琐且容易出错，这里推荐使用 Miniconda 来构建虚拟环境，不易出错且不影响 Linux 自带的 Python 环境。

> ℹ️**注意**  
> 这里我们不使用 Anaconda 来搭建虚拟环境，Anaconda 因为附带很多我们用不到的功能导致非常庞大，而 Miniconda 只有其核心部分，占用存储空间比较小，操作起来也比较方便。

1. 安装 Miniconda

    这里给出官方安装操作：https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html

    尽量选择较新版本的 Miniconda，这将决定 Miniconda 的 base 环境 Python 版本。

2. 进入 base 环境并验证 tkinter 是否安装
    
    一般来说，安装完 Miniconda 后终端将会进入 base 环境，此时输入 python 将会进入 base 中的 Python 环境，输入以下命令来确认 tkinter 是否安装：

    ```python
    import tkinter
    ```

    正常来说，此时是不会报错的，到这里 tkintertools 的运行环境就安装完毕了。

3. 安装 tkintertools

    在对应环境（非交互环境）中输入以下指令进行安装：

    ```
    python -m pip install tkintertools
    ```

三、获取预览版（可选）
-------------------

预览版本，可能有新功能，bug 可能会比较多，但也可能会比原来的版本更加稳定。预览版没有经过多操作系统的测试，仅能保证在 Windows 系统下运行所有功能，在其他的操作系统上，可能有部分功能无法正常运行。  

若想要提前获取更多新功能的 `tkintertools`，可以安装各种预览版的 `tkintertools`！下面对预览关键词做出说明：

* `dev`: 开发中的版本，没有任何稳定保证（甚至可能无法运行）
* `alpha`: 前测试版本，不太稳定，API 仍可能被更改
* `beta`: 后测试版本，基本稳定，API 不再更改
* `rc`: 准备发布的版本，与稳定版无太大差异

> ℹ️**注意**  
> 预览版本必须要指定版本号才能下载！若不指定版本号，则将会下载最新的稳定版本！  
> 预览版本号可在仓库中的 README.md 中找到，一般格式为版本号后加 `.alpha*` 等，下面的只是一个格式，并非具体的版本号！（* 表示数字通配符）

```
pip install tkintertools==*.*.*.alpha2
```

> ⚠️**警告**  
> 开发版仅作示例，各函数或类的 API 并非最终确定结果，直接使用开发版可能导致后续无法与稳定版兼容！

四、更新与查看版本
----------------

### 4.1 更新版本

你可以手动更新版本，也可以通过某些软件来更新版本。若使用 PyCharm，则可以打开其软件包管理器，在里面找到 tkintertools 来更新。手动跟香港，可打开终端，在进入对应 Python 环境（非交互环境）后输入以下指令来更新：

```
pip install tkintertools --upgrade
```

### 4.2 查看版本

若要查看当前 tkintertools 的版本，可以运行以下程序，输出结果就是当前已安装的版本：

```python
import tkintertools as tkt

print(tkt.__version__)
```

也可以通过 PyCharm 中解释器软件包管理工具进行查看。

---
Last Section - 上一节 | [Content - 目录](README.md) | [Next Section - 下一节](认识%20tkintertools.md)