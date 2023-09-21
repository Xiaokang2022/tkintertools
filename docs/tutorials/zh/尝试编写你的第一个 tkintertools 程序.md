**目录**

- [基本框架](#基本框架)
  - [tkinter 界面程序的开发框架](#tkinter-界面程序的开发框架)
  - [tkintertools 的开发框架](#tkintertools-的开发框架)
- [用“搭积木”的方式去编写界面](#用搭积木的方式去编写界面)
  - [第一步：创建一个基本的框架](#第一步创建一个基本的框架)
  - [第二步：添加按钮和文本输入框](#第二步添加按钮和文本输入框)
  - [第三步：给按钮添加相应的功能](#第三步给按钮添加相应的功能)

---

## 基本框架

### tkinter 界面程序的开发框架

对 tkinter 开发了解的开发人员会知道，tkinter 的开发框架一般是下面这样的：

1. 引入模块；
2. 创建根窗口；
3. 建立界面和程序逻辑；
4. 根窗口进入消息事件循环；

其中 1、2 和 4 是必须的，其所有的控件都以最顶级的容器控件 —— 根窗口，为基础。  
也就是说，所有的控件都必须以它为父控件。

下面是一段示例：

```python
import tkinter as tk  # 引入模块

root = tk.Tk()  # 创建根窗口

# 在这里建立界面和程序逻辑

root.mainloop()  # 根窗口进入消息事件循环
```

### tkintertools 的开发框架

若你十分熟悉 tkinter 的开发框架，那么你将极速掌握 tkintertools 的开发框架：

1. 引入模块；
2. 创建根窗口；
3. 创建根画布控件；
4. 建立界面和程序逻辑；
5. 根窗口进入消息事件循环；

在 tkintertools 里，应该时刻将根画布控件视作最顶层的容器控件。  
但这里有一点不同的是，根画布控件不只一个，我们可以将其每一个都视为一个页面，为其单独设计UI。  
其他的部分都和 tkinter 的开发思想基本完全一致的。

下面是一段简单的示例：

```python
import tkintertools as tkt  # 引入模块

root = tkt.Tk('tkintertools', 1280, 720)  # 创建根窗口

canvas_1 = tkt.Canvas(root, 1280, 720, 0, 0)
# 在这里建立界面和程序逻辑

canvas_2 = tkt.Canvas(root, 1280, 720, 1280, 0)
# 在这里建立界面和程序逻辑

root.mainloop()  # 根窗口进入消息事件循环
```

页面可以有很多个，我们后续会了解到如何在页面之间进行切换。

## 用“搭积木”的方式去编写界面

使用 tkintertools 模块进行界面开发和搭积木比较像，我们不用管这个控件具体什么样，我们只需要知道它的大小，和所属的页面（画布），然后将其放置到我们预期的位置就可以了。若是摆放空间有重叠部分，那么先被“放置”上去的控件会在下面，这和“搭积木”十分类似。

下面我们用这种思想，利用 tkintertools 模块手把手地教大家“搭建”一个登录的界面！

### 第一步：创建一个基本的框架

**预期设计**

* 窗口大小: 360 × 180
* 窗口位置: 不刻意设定，由系统自动管理
* 页面数量: 1 个
* 页面大小: 360 × 180
* 页面位置: x=0, y=0

我们的代码如下: 

```python
import tkintertools as tkt

root = tkt.Tk('登录窗口', 360, 180)
page = tkt.Canvas(root, 360, 180, 0, 0)
root.mainloop()
```

<details><summary><b>点击查看实现效果</b></summary>

![png](res/pic_1.png)

</details>

### 第二步：添加按钮和文本输入框

我们在中间添加一个用户名输入框和密码输入框，下面横排并列添加注册和登录按钮，这样一个像模像样的界面就搭建好了！

代码如下：

```python
import tkintertools as tkt

root = tkt.Tk('登录窗口', 360, 180)
page = tkt.Canvas(root, 360, 180, 0, 0)
tkt.Entry(page, 30, 20, 300, 40, text=('用户名', '点击输入用户名'))
tkt.Entry(page, 30, 70, 300, 40, text=('密码', '点击输入密码'), show='●')
tkt.Button(page, 30, 120, 145, 40, text='注册')
tkt.Button(page, 185, 120, 145, 40, text='登录')
root.mainloop()
```

<details><summary><b>点击查看实现效果</b></summary>

![png](res/pic_2.png)

</details>

### 第三步：给按钮添加相应的功能

这个和 tkinter 中的 Button 十分相似，也是用其 command 参数来绑定的。  
这里我们让点击注册按钮时打印当前用户名，点击登录按钮时打印当前密码。

代码这样写：

```python
import tkintertools as tkt

root = tkt.Tk('登录窗口', 360, 180)
page = tkt.Canvas(root, 360, 180, 0, 0)
act = tkt.Entry(page, 30, 20, 300, 40, text=('用户名', '点击输入用户名'))
psd = tkt.Entry(page, 30, 70, 300, 40, text=('密码', '点击输入密码'), show='●')
tkt.Button(page, 30, 120, 145, 40, text='注册', command=lambda: print(act.get()))
tkt.Button(page, 185, 120, 145, 40, text='登录', command=lambda: print(psd.get()))
root.mainloop()
```

---

恭喜你！看到这里说明你已经掌握如何使用 tkintertools 来编写一个简单的界面程序了！
