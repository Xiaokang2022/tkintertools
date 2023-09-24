**目录**

- [运行环境](#运行环境)
- [获取稳定版](#获取稳定版)
- [获取开发版](#获取开发版)
- [查看版本](#查看版本)

## 运行环境

tkintertools 是跨平台的，至少可以在下面多个平台上运行：

![Windows10](https://img.shields.io/badge/Windows-10-green?logo=windows)
![Windows11](https://img.shields.io/badge/Windows-11-green?logo=windows11)
![Ubuntu22.04](https://img.shields.io/badge/Ubuntu-22.04-green?logo=ubuntu)

同时支持以下版本的 Python：

![Python3.8.*](https://img.shields.io/badge/Python-3.8.*-blue?logo=python)
![Python3.9.*](https://img.shields.io/badge/Python-3.9.*-blue?logo=python)
![Python3.10.*](https://img.shields.io/badge/Python-3.10.*-blue?logo=python)
![Python3.11.*](https://img.shields.io/badge/Python-3.11.*-blue?logo=python)
![Python3.12.*](https://img.shields.io/badge/Python-3.12.*-blue?logo=python)

相关的依赖包（小部分 Python 没有自带）：

![tkinter8.6.*](https://img.shields.io/badge/tkinter-8.6.*-yellow)

## 获取稳定版

稳定版，相对于开发版本而言比较稳定，在发布之前有个测试的步骤，经过测试之后（各项功能正常运行，多平台兼容）才会发布，bug 大体上是没有那么多的，推荐使用这个。

稳定版可以通过 Python 的包下载工具 `pip` 来直接从 PyPi 上获取 `tkintertools`！以下命令默认安装最新稳定版 `tkintertools`。

```
pip install tkintertools
```

## 获取开发版

开发的版本，可能有新功能，bug 可能会比较多，但也可能会比原来的版本更加稳定。开发版没有经过多操作系统的测试，仅能保证在 Windows 系统下运行所有功能，在其他的操作系统上，可能有部分功能无法正常运行。  

若想要提前获取更多新功能的 `tkintertools`，可以安装 dev 版的 `tkintertools`！

> **Note**  
> 开发版本必须要指定版本号才能下载！若不指定版本号，则将会下载最新的稳定版本！  
> 开发版本号可在仓库中的 README.md 中找到，一般格式为版本号后加 `.dev*`，下面的只是一个格式，并非具体的版本号！

```
pip install tkintertools==*.*.*.dev*
```

> **Warning**  
> 开发版仅作示例，各函数或类的 API 并非最终确定结果，直接使用开发版可能导致后续无法与稳定版兼容！  
> 若要使用开发版，请先卸载稳定版后再进行 pip 安装，再次使用稳定版时也是一样，先卸载开发版再安装稳定版，否则会导致安装无效！

## 查看版本

若要查看当前 tkintertools 的版本，可以运行以下程序，输出结果就是当前已安装的版本：

```python
import tkintertools as tkt

print(tkt.__version__)
```
