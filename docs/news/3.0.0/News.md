Release Notes - 版本发布说明
===========================

* Version - 最新版本 : `3.0.0.dev6`
* Last Update - 上次更新 : 2024/01/19

```

```

!!! info "Note - 说明"
    This section is still in development...  
    此部分仍在开发中...

Example - 样例演示
-----------------

* OS - 操作系统 : Windows11 23H2
* Interpreter - 解释器 : Python 3.12.0

![png](example.png)

<details><summary><b>Source Code - 源代码</b></summary>

```python
import tkintertools_dev as tkt

root = tkt.Tk(title="123", bordercolor='red',
              titlecolor='cyan', background='green')
root.center()

nestedTk = tkt.NestedTk(root)
nestedTk.center()

tkt.NestedTk(nestedTk, size=(320, 180)).center()

tkt.Toplevel(root).center()

root.mainloop()
```

</details>

ChangeLog - 更新日志
-------------------

...

Todos - 待办事项
---------------

...

