# Release Notes - 版本发布说明

- Version - 最新版本 : `3.0.0.alpha1`
- Last Update - 上次更新 : 2024/02/17

```

```

!!! info "Note - 说明"
This section is still in development...  
 此部分仍在开发中...

## Example - 样例演示

- OS - 操作系统 : Windows11 23H2
- Interpreter - 解释器 : Python 3.12.0

![png](example.png)

The widget framework has been built, the details are not yet completed, and some widgets have been built for testing  
控件框架搭建完成，细节部分还未完成，已构建部分控件用于测试

<details><summary><b>Source Code - 源代码</b></summary>

```python
import webbrowser

import tkintertools as tkt

root = tkt.Tk(title="tkt 3.0.0.alpha1")

canvas = tkt.Canvas(root, bg='green', free_anchor=True)
canvas.place(width=1152, height=720, x=640, y=360, anchor="center")

canvas_2 = tkt.Canvas(canvas, bg='white', free_anchor=True, keep_ratio="full")
canvas_2.place(width=1152, height=648, x=576, y=360, anchor="center")

tkt.Label(canvas_2, (100, 50), (100, 100), text='Label')
tkt.Button(canvas_2, (100, 50), (250, 100),
           text='Button', command=lambda: print(1))
tkt.UnderLineButton(canvas_2, (100, 50), (400, 100),
                    text='UnderLine',
                    command=lambda: webbrowser.open_new_tab("https://github.com/Xiaokang2022/tkintertools"))

root.mainloop()
```

</details>
