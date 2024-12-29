> [!IMPORTANT]  
> 根據社區[投票](https://github.com/Xiaokang2022/tkintertools/discussions/41)結果，本項目將在正式版的時候**重命名**！

<h1 align="center">tkintertools</h1>

<p align="center"><img src="docs/logo.png" alt="Logo" title="Logo" /></p>

<p align="center"><a href="README.md">English</a> | <a href="README.zh-Hans.md">简体中文</a> | 繁體中文</p>

<p align="center">
一個基於 <code>tkinter</code> 且所有控件都由 <code>Canvas</code> 繪製的羽量級 UI 框架
</p>

<p align="center">
<a href="https://github.com/Xiaokang2022/tkintertools/releases"><img src="https://custom-icon-badges.demolab.com/github/v/release/Xiaokang2022/tkintertools?logo=tag&label=%e7%89%88%e6%9c%ac" alt="版本" title="版本" /></a>
<a href="https://pypistats.org/packages/tkintertools"><img src="https://custom-icon-badges.demolab.com/pypi/dm/tkintertools?logo=download&label=%e4%b8%8b%e8%bc%89" alt="下載" title="下載" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/actions"><img src="https://custom-icon-badges.demolab.com/github/actions/workflow/status/Xiaokang2022/tkintertools/python-package.yml?logo=play&label=%e6%aa%a2%e6%9f%a5%e5%92%8c%e6%b8%ac%e8%a9%a6" alt="檢查和測試" title="檢查和測試"/></a>
<a href="https://codecov.io/gh/Xiaokang2022/tkintertools"><img src="https://img.shields.io/codecov/c/github/Xiaokang2022/tkintertools?logoColor=white&logo=codecov&label=%e4%bb%a3%e7%a2%bc%e8%a6%86%e8%93%8b%e7%8e%87" alt="代碼覆蓋率" title="代碼覆蓋率"></a>
<br/>
<a href="https://github.com/Xiaokang2022/tkintertools/watchers"><img src="https://custom-icon-badges.demolab.com/github/watchers/Xiaokang2022/tkintertools?style=flat&logo=eye&label=%e9%97%9c%e6%b3%a8" alt="關注" title="關注" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/forks"><img src="https://custom-icon-badges.demolab.com/github/forks/Xiaokang2022/tkintertools?style=flat&logo=repo-forked&label=%e5%be%a9%e5%88%bb" alt="復刻" title="復刻" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/stargazers"><img src="https://custom-icon-badges.demolab.com/github/stars/Xiaokang2022/tkintertools?color=gold&style=flat&logo=star&label=%e6%98%9f%e6%a8%99" alt="星標" title="星標" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/issues"><img src="https://custom-icon-badges.demolab.com/github/issues/Xiaokang2022/tkintertools?logo=issue-opened&label=%e8%ad%b0%e9%a1%8c" alt="議題" title="議題" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/pulls"><img src="https://custom-icon-badges.demolab.com/github/issues-pr/Xiaokang2022/tkintertools?logo=git-pull-request&label=%e6%8b%89%e5%8f%96%e8%ab%8b%e6%b1%82" alt="拉取請求" title="拉取請求" /></a>
<a href="https://github.com/Xiaokang2022/tkintertools/discussions"><img src="https://custom-icon-badges.demolab.com/github/discussions/Xiaokang2022/tkintertools?logo=comment-discussion&label=%e8%a8%8e%e8%ab%96" alt="討論" title="討論" /></a>
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

## 📦 安裝

用以下命令進行安裝：

```bash
pip install tkintertools[recommended]==3.0.0rc5
```

### 🛠️ 依賴包

下面是該項目唯一必須需要的依賴包：

* [`typing_extensions`](https://github.com/python/typing_extensions): 提供額外的類型提示

### 🎨 可選包

下面的包都是可選的，不安裝也能讓該項目正常運行，但安裝它們可以爲你提供更多的功能：

* [`darkdetect`](https://github.com/albertosottile/darkdetect): 提供操作系統主題檢測
* [`pillow`](https://github.com/python-pillow/Pillow): 提供更多類型圖片的使用及優化圖片縮放速度
* [`pywinstyles`](https://github.com/Akascape/py-window-styles): 提供一些 Windows 系統的窗口效果
* [`hPyT`](https://github.com/Zingzy/hPyT): 提供更多 Windows 系統窗口的配置選項
* [`win32material`](https://github.com/littlewhitecloud/win32style): 提供更多 Windows 系統窗口的配置選項

用以下命令可以安裝全部的可選包：

```bash
pip install tkintertools[all]==3.0.0rc5
```

### 🧩 擴展包

除了基礎功能之外，我們還提供一些擴展包來實現某些特定的功能。目前已有的官方擴展包如下：

* [`tkintertools-mpl`](https://github.com/Xiaokang2022/tkintertools-mpl): 提供 `matplotlib` 包的相關支持
* [`tkintertools-media`](https://github.com/Xiaokang2022/tkintertools-media): 提供媒體文件的相關支持
* [`tkintertools-3d`](https://github.com/Xiaokang2022/tkintertools-3d): 提供簡單 3D 繪圖的相關支持

用以下命令可以安裝全部的官方擴展包：

```bash
pip install tkintertools[extension]==3.0.0rc5
```

## 👀 更多

* 📑 項目許可: [*LICENSE.txt*](LICENSE.txt)
* 📘 更新日誌: [*CHANGELOG.md*](CHANGELOG.md)
* 📕 安全策略: [*SECURITY.md*](SECURITY.md)
* 📗 貢獻指南: [*CONTRIBUTING.md*](CONTRIBUTING.md)
* 📙 行爲準則: [*CODE_OF_CONDUCT.md*](CODE_OF_CONDUCT.md)
* 📚 教程和文檔: [Tutorials & Documents](https://xiaokang2022.github.io/tkintertools-docs/)
* 🌏 官方網站: [Official Website](https://xiaokang2022.github.io/tkintertools/)
* ❤️ 贊助我們: [Sponsor](https://xiaokang2022.github.io/tkintertools/Sponsor/)
* 🚀 存儲庫鏡像源:
[GitHub](https://github.com/Xiaokang2022/tkintertools) |
[GitCode](https://gitcode.com/Xiaokang2022/tkintertools) |
[Gitee](https://gitee.com/Xiaokang2022/tkintertools)
