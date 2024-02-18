# Release Notes - 版本发布说明

- Version - 最新版本 : `3.0.0.alpha2`
- Last Update - 上次更新 : 2024/02/18

```

```

!!! info "Note - 说明"
    This section is still in development...  
    此部分仍在开发中...

## Example - 样例演示

- OS - 操作系统 : Windows11 23H2
- Interpreter - 解释器 : Python 3.12.0

![png](example.png)

Fixed a few bugs and added a lot of content to the framework  
修复些许 bug，框架内增加大量内容

<details><summary><b>Source Code - 源代码</b></summary>

```python
import webbrowser

import tkintertools as tkt

root = tkt.Tk(title=f"tkt {tkt.__version__}")

canvas = tkt.Canvas(root, bg='orange', free_anchor=True)
canvas.place(width=1152, height=720, x=640, y=360, anchor="center")

canvas_2 = tkt.Canvas(canvas, bg='white', free_anchor=True, keep_ratio="full")
canvas_2.place(width=1152, height=648, x=576, y=360, anchor="center")

tkt.Information(canvas_2, (100, 100), (200, 50), text="Information")
tkt.Label(canvas_2, (350, 100), (100, 50), text='Label')
tkt.Button(canvas_2,  (500, 100), (100, 50),
           text='Button', command=lambda: print("Button"))
tkt.UnderlineButton(canvas_2, (650, 100), (200, 50), text='UnderlineButton',
                    command=lambda: webbrowser.open_new_tab("https://github.com/Xiaokang2022/tkintertools"))
tkt.HighlightButton(canvas_2, (900, 100), (200, 50), text='HighlightButton',
                    command=lambda: webbrowser.open_new_tab("https://github.com/Xiaokang2022/tkintertools"))

root.mainloop()
```

</details>
