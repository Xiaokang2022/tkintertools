# Release Notes - 版本发布说明

- Version - 最新版本 : `3.0.0.dev8`
- Last Update - 上次更新 : 2024/02/15

```

```

!!! info "Note - 说明"
This section is still in development...  
 此部分仍在开发中...

## Example - 样例演示

- OS - 操作系统 : Windows11 23H2
- Interpreter - 解释器 : Python 3.12.0

![png](example.png)

容器控件 `tkt.Canvas` 已完成 `tkinter._CanvasItemId` 的实现，以及其它大量改进

<details><summary><b>Source Code - 源代码</b></summary>

```python
import tkintertools_dev as tkt

root = tkt.Tk(title="tkt 3.0.0.dev8")
root.center()

canvas = tkt.Canvas(root, bg='green', free_anchor=True)
canvas.place(width=1152, height=720, x=640, y=360, anchor="center")

canvas_2 = tkt.Canvas(canvas, bg='white', free_anchor=True, keep_ratio="full")
canvas_2.place(width=1152, height=648, x=576, y=360, anchor="center")

canvas_2.create_text(400, 400, text="Test")
canvas_2.create_oval(100, 100, 200, 200)

root.mainloop()
```

</details>

## ChangeLog - 更新日志

...

## Todos - 待办事项

...
