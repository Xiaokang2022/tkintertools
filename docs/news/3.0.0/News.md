Release Notes - 版本发布说明
===========================

* Version - 最新版本 : `3.0.0.dev5`
* Last Update - 上次更新 : 2023/11/17

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

tk = tkt.Tk(title="666")
tk.after(1, tk.center)

nestedTk = tkt.NestedTk(tk, size_expand="xy", position_expand="xy")
# nestedTk.after(1, nestedTk.center)

nestedTk_2 = tkt.NestedTk(nestedTk, size_expand="xy",
                          position_expand="xy", size=(320, 180))

# toplevel = tkt.Toplevel(tk, state="zoomed")
# toplevel.center()

tk.mainloop()
```

</details>

ChangeLog - 更新日志
-------------------

...

Todos - 待办事项
---------------

...

