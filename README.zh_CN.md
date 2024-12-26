> [!IMPORTANT]  
> 根据社区[投票](https://github.com/Xiaokang2022/tkintertools/discussions/41)结果，本项目将在正式版的时候**重命名**！

<h1 align="center">tkintertools</h1>

<p align="center"><img src="docs/logo.png" alt="Logo" title="Logo" /></p>

<p align="center"><a href="README.md">English</a> | 简体中文 | <a href="README.zh_TW.md">繁體中文</a></p>

<p align="center">
<code>tkintertools</code> 是一个基于 <code>tkinter</code> 的 <code>Canvas</code> 类的 UI 框架
</p>

<p align="center">
<a href="https://github.com/Xiaokang2022/tkintertools/releases"><img src="https://custom-icon-badges.demolab.com/github/v/release/Xiaokang2022/tkintertools?logo=tag&label=%e7%89%88%e6%9c%ac" alt="版本" title="版本" /></a>
<a href="https://pypistats.org/packages/tkintertools"><img src="https://custom-icon-badges.demolab.com/pypi/dm/tkintertools?logo=download&label=%e4%b8%8b%e8%bd%bd" alt="下载" title="下载" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/actions"><img src="https://custom-icon-badges.demolab.com/github/actions/workflow/status/Xiaokang2022/tkintertools/python-package.yml?logo=play&label=%e6%a3%80%e6%9f%a5%e5%92%8c%e6%b5%8b%e8%af%95" alt="检查和测试" title="检查和测试"/></a>
<a href="https://codecov.io/gh/Xiaokang2022/tkintertools"><img src="https://img.shields.io/codecov/c/github/Xiaokang2022/tkintertools?logoColor=white&logo=codecov&label=%e4%bb%a3%e7%a0%81%e8%a6%86%e7%9b%96%e7%8e%87" alt="代码覆盖率" title="代码覆盖率"></a>
<br/>
<a href="https://github.com/Xiaokang2022/tkintertools/watchers"><img src="https://custom-icon-badges.demolab.com/github/watchers/Xiaokang2022/tkintertools?style=flat&logo=eye&label=%e5%85%b3%e6%b3%a8" alt="关注" title="关注" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/forks"><img src="https://custom-icon-badges.demolab.com/github/forks/Xiaokang2022/tkintertools?style=flat&logo=repo-forked&label=%e5%a4%8d%e5%88%bb" alt="复刻" title="复刻" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/stargazers"><img src="https://custom-icon-badges.demolab.com/github/stars/Xiaokang2022/tkintertools?color=gold&style=flat&logo=star&label=%e6%98%9f%e6%a0%87" alt="星标" title="星标" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/issues"><img src="https://custom-icon-badges.demolab.com/github/issues/Xiaokang2022/tkintertools?logo=issue-opened&label=%e8%ae%ae%e9%a2%98" alt="议题" title="议题" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/pulls"><img src="https://custom-icon-badges.demolab.com/github/issues-pr/Xiaokang2022/tkintertools?logo=git-pull-request&label=%e6%8b%89%e5%8f%96%e8%af%b7%e6%b1%82" alt="拉取请求" title="拉取请求" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/discussions"><img src="https://custom-icon-badges.demolab.com/github/discussions/Xiaokang2022/tkintertools?logo=comment-discussion&label=%e8%ae%a8%e8%ae%ba" alt="讨论" title="讨论" /></a>
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

## 📦 安装

用以下命令进行安装：

```bash
pip install tkintertools[recommended]==3.0.0rc5
```

### 📌 依赖包

下面是该项目唯一必须需要的依赖包：

* [`typing_extensions`](https://github.com/python/typing_extensions): 提供额外的类型提示

### 🎨 可选包

下面的包都是可选的，不安装也能让该项目正常运行，但安装它们可以为你提供更多的功能：

* [`darkdetect`](https://github.com/albertosottile/darkdetect): 提供操作系统主题检测
* [`pillow`](https://github.com/python-pillow/Pillow): 提供更多类型图片的使用及优化图片缩放速度
* [`pywinstyles`](https://github.com/Akascape/py-window-styles): 提供一些 Windows 系统的窗口效果
* [`hPyT`](https://github.com/Zingzy/hPyT): 提供更多 Windows 系统窗口的配置选项
* [`win32material`](https://github.com/littlewhitecloud/win32style): 提供更多 Windows 系统窗口的配置选项

用以下命令可以安装全部的可选包：

```bash
pip install tkintertools[all]==3.0.0rc5
```

### 📦 扩展包

除了基础功能之外，我们还提供一些扩展包来实现某些特定的功能。目前已有的官方扩展包如下：

* [`tkintertools-mpl`](https://github.com/Xiaokang2022/tkintertools-mpl): 提供 `matplotlib` 包的相关支持
* [`tkintertools-media`](https://github.com/Xiaokang2022/tkintertools-media): 提供媒体文件的相关支持
* [`tkintertools-3d`](https://github.com/Xiaokang2022/tkintertools-3d): 提供简单 3D 绘图的相关支持

用以下命令可以安装全部的官方扩展包：

```bash
pip install tkintertools[extension]==3.0.0rc5
```

## 👀 更多

* 📑 项目许可: [*LICENSE.txt*](LICENSE.txt)
* 📘 更新日志: [*CHANGELOG.md*](CHANGELOG.md)
* 📕 安全策略: [*SECURITY.md*](SECURITY.md)
* 📗 贡献指南: [*CONTRIBUTING.md*](CONTRIBUTING.md)
* 📙 行为准则: [*CODE_OF_CONDUCT.md*](CODE_OF_CONDUCT.md)
* 📚 教程和文档: [Tutorials & Documents](https://xiaokang2022.github.io/tkintertools-docs/)
* 🎉 官方网站: [Official Website](https://xiaokang2022.github.io/tkintertools/)
* ❤️ 赞助我们: [Sponsor](https://xiaokang2022.github.io/tkintertools/Sponsor/)
* 🚀 存储库镜像源:
[GitHub](https://github.com/Xiaokang2022/tkintertools) |
[GitCode](https://gitcode.com/Xiaokang2022/tkintertools) |
[Gitee](https://gitee.com/Xiaokang2022/tkintertools)
