**目录**

- [混合使用的规则](#混合使用的规则)
- [推荐的做法](#推荐的做法)

> ⚠️**警告**  
> 此文还在更新中，仍有大量问题待解决，不建议参考！

### 混合使用的规则

本质上 tkintertools 中的容器控件都是从 tkinter 中继承而来的，所以自然可以与 tkinter 混合使用。  
但是仍有几点需要注意一下：

* tkintertools 中的虚拟控件都只能在 tkintertools 中的 `Canvas` 中使用；
* tkintertools 中的 `Canvas` 也只能在 tkintertools 中的 `Tk` 中使用；
* tkinter 中的控件均可以在 tkintertools 中的 `Tk` 里使用，但是它们无法拥有某些特殊功能，比如控件自动缩放；
* tkintertools 的 `Toplevel` 同 `Tk` 一样，不再赘述；
* tkinter.ttk 的样式无法对 tkintertools 的控件生效；
* 某些时候若产生了报错，将 tkintertools 中 `Canvas` 的参数 `expand` 设为 `False` 可能有助于解决问题；
* 混合使用时大部分不兼容的问题和报错都是窗口缩放产生的，将 `Tk` 或者 `Toplevel` 设为大小固定可能可以解决这个问题；

### 推荐的做法

个人推荐尽量不要混用太多，只在某些地方混用它们即可，不然可能会带来一些无法处理的问题。

此外，若是要开发稍大型的界面程序，还是建议全程使用 `tkinter`；若是小型程序或者临时用来显示某些东西，建议使用 `tkintertools`；由于目前 `tkintertools` 模块还比较小，在很多地方还不够完善，控件也还不够完整，因此建议只用来做小型的项目，这也是目前 `tkintertools` 的开发设想。
