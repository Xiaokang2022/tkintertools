> [!IMPORTANT]  
> According to the results of the community [vote](https://github.com/Xiaokang2022/tkintertools/discussions/41), this project will be **RENAMED** when it is released!

<h1 align="center">tkintertools</h1>

<p align="center"><img src="docs/logo.png" alt="Logo" title="Logo" /></p>

<p align="center">English · <a href="README.zh-Hans.md">简体中文</a> · <a href="README.zh-Hant.md">繁體中文</a></p>

<p align="center"><a title="Official Website" href="https://xiaokang2022.github.io/tkintertools/">https://xiaokang2022.github.io/tkintertools/</a></p>

<p align="center">
A lightweight UI framework based on <code>tkinter</code> with all UI drawn in <code>Canvas</code>
</p>

<p align="center">
<a href="https://github.com/Xiaokang2022/tkintertools/releases"><img alt="Version" title="Version" src="https://img.shields.io/github/v/release/Xiaokang2022/tkintertools?label=Version&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPQoid2hpdGUiIGQ9Ik0xIDcuNzc1VjIuNzVDMSAxLjc4NCAxLjc4NCAxIDIuNzUgMWg1LjAyNWMuNDY0IDAgLjkxLjE4NCAxLjIzOC41MTNsNi4yNSA2LjI1YTEuNzUgMS43NSAwIDAgMSAwIDIuNDc0bC01LjAyNiA1LjAyNmExLjc1IDEuNzUgMCAwIDEtMi40NzQgMGwtNi4yNS02LjI1QTEuNzUyIDEuNzUyIDAgMCAxIDEgNy43NzVabTEuNSAwYzAgLjA2Ni4wMjYuMTMuMDczLjE3N2w2LjI1IDYuMjVhLjI1LjI1IDAgMCAwIC4zNTQgMGw1LjAyNS01LjAyNWEuMjUuMjUgMCAwIDAgMC0uMzU0bC02LjI1LTYuMjVhLjI1LjI1IDAgMCAwLS4xNzctLjA3M0gyLjc1YS4yNS4yNSAwIDAgMC0uMjUuMjVaTTYgNWExIDEgMCAxIDEgMCAyIDEgMSAwIDAgMSAwLTJaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://pypistats.org/packages/tkintertools"><img alt="Downloads" title="Downloads" src="https://img.shields.io/pypi/dm/tkintertools?label=Downloads&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTIuNzUgMTRBMS43NSAxLjc1IDAgMCAxIDEgMTIuMjV2LTIuNWEuNzUuNzUgMCAwIDEgMS41IDB2Mi41YzAgLjEzOC4xMTIuMjUuMjUuMjVoMTAuNWEuMjUuMjUgMCAwIDAgLjI1LS4yNXYtMi41YS43NS43NSAwIDAgMSAxLjUgMHYyLjVBMS43NSAxLjc1IDAgMCAxIDEzLjI1IDE0WiI+PC9wYXRoPjxwYXRoIGZpbGw9IndoaXRlIiBkPSJNNy4yNSA3LjY4OVYyYS43NS43NSAwIDAgMSAxLjUgMHY1LjY4OWwxLjk3LTEuOTY5YS43NDkuNzQ5IDAgMSAxIDEuMDYgMS4wNmwtMy4yNSAzLjI1YS43NDkuNzQ5IDAgMCAxLTEuMDYgMEw0LjIyIDYuNzhhLjc0OS43NDkgMCAxIDEgMS4wNi0xLjA2bDEuOTcgMS45NjlaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/actions"><img alt="Lint & Test" title="Lint & Test" src="https://img.shields.io/github/actions/workflow/status/Xiaokang2022/tkintertools/python-package.yml?label=Lint%20%26%20Test&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggMGE4IDggMCAxIDEgMCAxNkE4IDggMCAwIDEgOCAwWk0xLjUgOGE2LjUgNi41IDAgMSAwIDEzIDAgNi41IDYuNSAwIDAgMC0xMyAwWm00Ljg3OS0yLjc3MyA0LjI2NCAyLjU1OWEuMjUuMjUgMCAwIDEgMCAuNDI4bC00LjI2NCAyLjU1OUEuMjUuMjUgMCAwIDEgNiAxMC41NTlWNS40NDJhLjI1LjI1IDAgMCAxIC4zNzktLjIxNVoiPjwvcGF0aD48L3N2Zz4=" /></a>
<a href="https://codecov.io/gh/Xiaokang2022/tkintertools"><img alt="Code Coverage" title="Code Coverage" src="https://img.shields.io/codecov/c/github/Xiaokang2022/tkintertools?label=Code Coverage&logoColor=white&logo=codecov" /></a>
<br/>
<a href="https://github.com/Xiaokang2022/tkintertools/watchers"><img alt="Watchers" title="Watchers" src="https://img.shields.io/github/watchers/Xiaokang2022/tkintertools?label=Watchers&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggMmMxLjk4MSAwIDMuNjcxLjk5MiA0LjkzMyAyLjA3OCAxLjI3IDEuMDkxIDIuMTg3IDIuMzQ1IDIuNjM3IDMuMDIzYTEuNjIgMS42MiAwIDAgMSAwIDEuNzk4Yy0uNDUuNjc4LTEuMzY3IDEuOTMyLTIuNjM3IDMuMDIzQzExLjY3IDEzLjAwOCA5Ljk4MSAxNCA4IDE0Yy0xLjk4MSAwLTMuNjcxLS45OTItNC45MzMtMi4wNzhDMS43OTcgMTAuODMuODggOS41NzYuNDMgOC44OThhMS42MiAxLjYyIDAgMCAxIDAtMS43OThjLjQ1LS42NzcgMS4zNjctMS45MzEgMi42MzctMy4wMjJDNC4zMyAyLjk5MiA2LjAxOSAyIDggMlpNMS42NzkgNy45MzJhLjEyLjEyIDAgMCAwIDAgLjEzNmMuNDExLjYyMiAxLjI0MSAxLjc1IDIuMzY2IDIuNzE3QzUuMTc2IDExLjc1OCA2LjUyNyAxMi41IDggMTIuNWMxLjQ3MyAwIDIuODI1LS43NDIgMy45NTUtMS43MTUgMS4xMjQtLjk2NyAxLjk1NC0yLjA5NiAyLjM2Ni0yLjcxN2EuMTIuMTIgMCAwIDAgMC0uMTM2Yy0uNDEyLS42MjEtMS4yNDItMS43NS0yLjM2Ni0yLjcxN0MxMC44MjQgNC4yNDIgOS40NzMgMy41IDggMy41Yy0xLjQ3MyAwLTIuODI1Ljc0Mi0zLjk1NSAxLjcxNS0xLjEyNC45NjctMS45NTQgMi4wOTYtMi4zNjYgMi43MTdaTTggMTBhMiAyIDAgMSAxLS4wMDEtMy45OTlBMiAyIDAgMCAxIDggMTBaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/forks"><img alt="Forks" title="Forks" src="https://img.shields.io/github/forks/Xiaokang2022/tkintertools?label=Forks&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTUgNS4zNzJ2Ljg3OGMwIC40MTQuMzM2Ljc1Ljc1Ljc1aDQuNWEuNzUuNzUgMCAwIDAgLjc1LS43NXYtLjg3OGEyLjI1IDIuMjUgMCAxIDEgMS41IDB2Ljg3OGEyLjI1IDIuMjUgMCAwIDEtMi4yNSAyLjI1aC0xLjV2Mi4xMjhhMi4yNTEgMi4yNTEgMCAxIDEtMS41IDBWOC41aC0xLjVBMi4yNSAyLjI1IDAgMCAxIDMuNSA2LjI1di0uODc4YTIuMjUgMi4yNSAwIDEgMSAxLjUgMFpNNSAzLjI1YS43NS43NSAwIDEgMC0xLjUgMCAuNzUuNzUgMCAwIDAgMS41IDBabTYuNzUuNzVhLjc1Ljc1IDAgMSAwIDAtMS41Ljc1Ljc1IDAgMCAwIDAgMS41Wm0tMyA4Ljc1YS43NS43NSAwIDEgMC0xLjUgMCAuNzUuNzUgMCAwIDAgMS41IDBaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/stargazers"><img alt="Stars" title="Stars" src="https://img.shields.io/github/stars/Xiaokang2022/tkintertools?label=Stars&color=gold&style=flat&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggLjI1YS43NS43NSAwIDAgMSAuNjczLjQxOGwxLjg4MiAzLjgxNSA0LjIxLjYxMmEuNzUuNzUgMCAwIDEgLjQxNiAxLjI3OWwtMy4wNDYgMi45Ny43MTkgNC4xOTJhLjc1MS43NTEgMCAwIDEtMS4wODguNzkxTDggMTIuMzQ3bC0zLjc2NiAxLjk4YS43NS43NSAwIDAgMS0xLjA4OC0uNzlsLjcyLTQuMTk0TC44MTggNi4zNzRhLjc1Ljc1IDAgMCAxIC40MTYtMS4yOGw0LjIxLS42MTFMNy4zMjcuNjY4QS43NS43NSAwIDAgMSA4IC4yNVptMCAyLjQ0NUw2LjYxNSA1LjVhLjc1Ljc1IDAgMCAxLS41NjQuNDFsLTMuMDk3LjQ1IDIuMjQgMi4xODRhLjc1Ljc1IDAgMCAxIC4yMTYuNjY0bC0uNTI4IDMuMDg0IDIuNzY5LTEuNDU2YS43NS43NSAwIDAgMSAuNjk4IDBsMi43NyAxLjQ1Ni0uNTMtMy4wODRhLjc1Ljc1IDAgMCAxIC4yMTYtLjY2NGwyLjI0LTIuMTgzLTMuMDk2LS40NWEuNzUuNzUgMCAwIDEtLjU2NC0uNDFMOCAyLjY5NFoiPjwvcGF0aD48L3N2Zz4=" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/issues"><img alt="Issues" title="Issues" src="https://img.shields.io/github/issues/Xiaokang2022/tkintertools?label=Issues&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTggOS41YTEuNSAxLjUgMCAxIDAgMC0zIDEuNSAxLjUgMCAwIDAgMCAzWiI+PC9wYXRoPjxwYXRoIGZpbGw9IndoaXRlIiBkPSJNOCAwYTggOCAwIDEgMSAwIDE2QTggOCAwIDAgMSA4IDBaTTEuNSA4YTYuNSA2LjUgMCAxIDAgMTMgMCA2LjUgNi41IDAgMCAwLTEzIDBaIj48L3BhdGg+PC9zdmc+" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/pulls"><img alt="Pull Requests" title="Pull Requests" src="https://img.shields.io/github/issues-pr/Xiaokang2022/tkintertools?label=Pull%20Requests&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTEuNSAzLjI1YTIuMjUgMi4yNSAwIDEgMSAzIDIuMTIydjUuMjU2YTIuMjUxIDIuMjUxIDAgMSAxLTEuNSAwVjUuMzcyQTIuMjUgMi4yNSAwIDAgMSAxLjUgMy4yNVptNS42NzctLjE3N0w5LjU3My42NzdBLjI1LjI1IDAgMCAxIDEwIC44NTRWMi41aDFBMi41IDIuNSAwIDAgMSAxMy41IDV2NS42MjhhMi4yNTEgMi4yNTEgMCAxIDEtMS41IDBWNWExIDEgMCAwIDAtMS0xaC0xdjEuNjQ2YS4yNS4yNSAwIDAgMS0uNDI3LjE3N0w3LjE3NyAzLjQyN2EuMjUuMjUgMCAwIDEgMC0uMzU0Wk0zLjc1IDIuNWEuNzUuNzUgMCAxIDAgMCAxLjUuNzUuNzUgMCAwIDAgMC0xLjVabTAgOS41YS43NS43NSAwIDEgMCAwIDEuNS43NS43NSAwIDAgMCAwLTEuNVptOC4yNS43NWEuNzUuNzUgMCAxIDAgMS41IDAgLjc1Ljc1IDAgMCAwLTEuNSAwWiI+PC9wYXRoPjwvc3ZnPg==" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/discussions"><img alt="Discussions" title="Discussions" src="https://img.shields.io/github/discussions/Xiaokang2022/tkintertools?label=Discussions&logo=data:image/svg+xml;charset=utf-8;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxNiAxNiIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2Ij48cGF0aCBmaWxsPSJ3aGl0ZSIgZD0iTTEuNzUgMWg4LjVjLjk2NiAwIDEuNzUuNzg0IDEuNzUgMS43NXY1LjVBMS43NSAxLjc1IDAgMCAxIDEwLjI1IDEwSDcuMDYxbC0yLjU3NCAyLjU3M0ExLjQ1OCAxLjQ1OCAwIDAgMSAyIDExLjU0M1YxMGgtLjI1QTEuNzUgMS43NSAwIDAgMSAwIDguMjV2LTUuNUMwIDEuNzg0Ljc4NCAxIDEuNzUgMVpNMS41IDIuNzV2NS41YzAgLjEzOC4xMTIuMjUuMjUuMjVoMWEuNzUuNzUgMCAwIDEgLjc1Ljc1djIuMTlsMi43Mi0yLjcyYS43NDkuNzQ5IDAgMCAxIC41My0uMjJoMy41YS4yNS4yNSAwIDAgMCAuMjUtLjI1di01LjVhLjI1LjI1IDAgMCAwLS4yNS0uMjVoLTguNWEuMjUuMjUgMCAwIDAtLjI1LjI1Wm0xMyAyYS4yNS4yNSAwIDAgMC0uMjUtLjI1aC0uNWEuNzUuNzUgMCAwIDEgMC0xLjVoLjVjLjk2NiAwIDEuNzUuNzg0IDEuNzUgMS43NXY1LjVBMS43NSAxLjc1IDAgMCAxIDE0LjI1IDEySDE0djEuNTQzYTEuNDU4IDEuNDU4IDAgMCAxLTIuNDg3IDEuMDNMOS4yMiAxMi4yOGEuNzQ5Ljc0OSAwIDAgMSAuMzI2LTEuMjc1Ljc0OS43NDkgMCAwIDEgLjczNC4yMTVsMi4yMiAyLjIydi0yLjE5YS43NS43NSAwIDAgMSAuNzUtLjc1aDFhLjI1LjI1IDAgMCAwIC4yNS0uMjVaIj48L3BhdGg+PC9zdmc+" /></a>
</p>

<p align="center">
<a href="https://github.com/Xiaokang2022/tkintertools/pulse"><img src="https://repobeats.axiom.co/api/embed/ab8fae686a5a96f91fa71c40c53c189310924f5e.svg" /></a>
</p>

<p align="center">
    <a href="https://star-history.com/#Xiaokang2022/tkintertools&Date">
        <picture>
            <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Xiaokang2022/tkintertools&type=Date&theme=dark" />
            <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Xiaokang2022/tkintertools&type=Date" />
            <img src="https://api.star-history.com/svg?repos=Xiaokang2022/tkintertools&type=Date" />
        </picture>
    </a>
</p>

## 📦 Installation

Install it with the following command:

```shell
pip install tkintertools==3.0.0rc6
```

### 🛠️ Dependencies

Here are the only dependencies that the project must need:

* [`typing-extensions`](https://github.com/python/typing_extensions): provide additional type hints

### 🎨 Optional

The following packages are optional and will make the project work without installation, but installing them can give you more functionality:

* [`darkdetect`](https://github.com/albertosottile/darkdetect): provide operating system theme detection
* [`pillow`](https://github.com/python-pillow/Pillow): provide more types of images and optimize image scaling speed
* [`pywinstyles`](https://github.com/Akascape/py-window-styles): provide some window effects for Windows systems
* [`hPyT`](https://github.com/Zingzy/hPyT): provide more configuration options for Windows system windows
* [`win32material`](https://github.com/littlewhitecloud/win32style): provide more configuration options for Windows system windows

**Recommended**, these packages should be installed. You can install all the optional packages with the following command:

```shell
pip install tkintertools[opt]==3.0.0rc6
```

### 🧩 Extensions

In addition to the basic functionality, we also offer a number of extension packs to implement specific functionality. The following official extensions are available:

* [`tkintertools-mpl`](https://github.com/Xiaokang2022/tkintertools-mpl): support for `matplotlib`
* [`tkintertools-media`](https://github.com/Xiaokang2022/tkintertools-media): support for media files
* [`tkintertools-3d`](https://github.com/Xiaokang2022/tkintertools-3d): support for simple 3D drawings

You can install all the official extensions with the following command:

```shell
pip install tkintertools[ext]==3.0.0rc6
```

## 👀 More

### 🖼️ Gallery

The demos below are some of the things that can be achieved with the project, they may be built with the latest version of the project, or they may be built with an older version, but either way, the code for the demo below can be found in the [demo repository](https://github.com/Xiaokang2022/tkintertools-demos)!

> [!TIP]  
> Please click **"Expand"** to view the gallery

<details><summary><b>Expand</b></summary>

![preview_1](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo9-1.png?raw=true)

![preview_2](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo9-2.png?raw=true)

![preview_3](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo9-3.png?raw=true)

![preview_4](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo9-4.png?raw=true)

![preview_5](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo0-1.png?raw=true)

![preview_6](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo0-2.png?raw=true)

![preview_7](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo1-1.png?raw=true)

![preview_8](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo1-2.png?raw=true)

![preview_9](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo2.png?raw=true)

![preview_10](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo3.png?raw=true)

![preview_11](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo4-1.png?raw=true)

![preview_12](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo4-2.png?raw=true)

![preview_13](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo5-1.png?raw=true)

![preview_14](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo5-2.png?raw=true)

![preview_15](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo6-1.png?raw=true)

![preview_16](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo7-1.png?raw=true)

![preview_17](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo7-2.png?raw=true)

![preview_18](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo8-1.png?raw=true)

![preview_19](https://github.com/Xiaokang2022/tkintertools-demos/blob/main/preview/demo10-1.png?raw=true)

![project_1](https://github.com/Xiaokang2022/Intelligent-Magic-Cube/blob/main/preview.png?raw=true)

![project_2](https://github.com/Xiaokang2022/Chess/blob/master/preview.png?raw=true)

![project_3](https://github.com/Xiaokang2022/Super-Gobang/blob/main/preview.png?raw=true)

![project_4](https://github.com/Xiaokang2022/TodoList/blob/master/preview.png?raw=true)

</details>

### 🔗 Links

Here are some links that may be helpful to you:

* 📑 License: [*MIT License*](LICENSE.txt)
* 📘 Changelog: [*CHANGELOG.md*](CHANGELOG.md)
* 📕 Security Policy: [*SECURITY.md*](SECURITY.md)
* 📗 Contribution Guideline: [*CONTRIBUTING.md*](CONTRIBUTING.md)
* 📙 Code of Conduct: [*CODE_OF_CONDUCT.md*](CODE_OF_CONDUCT.md)
* 📚 Tutorials and Documents: [Tutorials & Documents](https://xiaokang2022.github.io/tkintertools-docs/)
* ❤️ Sponsor this Project: [Sponsor](https://xiaokang2022.github.io/tkintertools/Sponsor/)
* 🚀 Repository Mirrors:
[GitCode](https://gitcode.com/Xiaokang2022/tkintertools),
[Gitee](https://gitee.com/Xiaokang2022/tkintertools)
