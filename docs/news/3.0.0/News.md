# Release Notes - 版本发布说明

- Version - 最新版本 : `3.0.0.dev9`
- Last Update - 上次更新 : 2024/02/16

```

```

!!! info "Note - 说明"
This section is still in development...  
 此部分仍在开发中...

## Example - 样例演示

- OS - 操作系统 : Windows11 23H2
- Interpreter - 解释器 : Python 3.12.0

![png](example.png)

The widget framework is almost complete, and the details are not yet complete  
控件框架基本完成，细节部分还未完成

<details><summary><b>Source Code - 源代码</b></summary>

```python
import tkintertools as tkt
from tkintertools import shapes

root = tkt.Tk(title="tkt 3.0.0.dev9")
root.center()

canvas = tkt.Canvas(root, bg='green', free_anchor=True)
canvas.place(width=1152, height=720, x=640, y=360, anchor="center")

canvas_2 = tkt.Canvas(canvas, bg='white', free_anchor=True, keep_ratio="full")
canvas_2.place(width=1152, height=648, x=576, y=360, anchor="center")

label = tkt.Label(canvas_2, (100, 50), (100, 100), text='Label')
x1, y1, x2, y2 = label.text.region()
tkt.Label(canvas_2, (x2-x1, y2-y1), (x1, y1))

root.mainloop()
```

</details>

## ChangeLog - 更新日志

...

## Todos - 待办事项

...
