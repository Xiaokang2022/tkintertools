# Chess 🚀

A Chinese chess program based on tkintertools and written in Python 3.12 and C++ 20.

![](https://github.com/Xiaokang2022/Chess/blob/master/preview.png?raw=true)

This program is implemented using a mix of `tkinter` and `tkintertools` modules, [`tkintertools`](https://github.com/Xiaokang2022/tkintertools) is a third-party Python module that I developed on my own to beautify `tkinter` and provide some advanced features! 🎉

!!! note

    Since the original program was written by me one year ago, the `tkintertools` module uses the test version, and the AI of the program was added later, and the previous code quality is relatively poor, please understand. 😅

## Star History

<a href="https://star-history.com/#Xiaokang2022/Chess&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Xiaokang2022/Chess&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Xiaokang2022/Chess&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Xiaokang2022/Chess&type=Date" />
 </picture>
</a>

## How to use

### Before use

!!! info

    Make sure your Python version is **3.12** or greater and C++ version is **20** or greater.

### Choose the mode

run the `main.py` and choose a game mode you want.

I've provided **4** modes, Three of them can be selected in "新游戏"，and "残局挑战" needs to be selected in the "棋局库".

### One last step

have fun! 😁

## Brief introduction

### Base Features

1. Two-player match
2. Man-machine battles
3. Endgame Challenge
4. LAN connection

### About the AI

I've provided **2** AI algorithms, one of which also provides an implementation of C++20:

1. **Minimum-Max search algorithm**
    - Python: min_max_search.py
2. **Alpha-beta pruning algorithm**
    - Python: alpha_beta_search.py
    - C++ (default):
        * src: ./cpp/HelloWorld.cpp
        * dll: ./PyDLL.dll

You can change them in the settings. By the way, default value of the search depth is 4.

!!! tip

    Due to the smaller number of pieces in endgame mode, the search space is smaller, and you can increase the AI's search depth a little more, and the results could be even better!

!!! danger

    You can also modify the pieces of the individual AI algorithms to evaluate the scores if you want, but be careful not to set the score to a limit value (like `math.inf`), which will cause the algorithm to not come up with the correct result!

### Some really great features

When you're playing chess, the terminal actually has an output! For example:

<font color="yellow">SCORE</font>: 2  
<font color="royalblue">STEP</font>: 5  
〇〇<font color="green">象士将士象马车  
车</font>〇〇〇〇〇〇〇〇  
〇<font color="green">炮马</font>〇〇〇〇<font color="green">炮</font>〇  
<font color="green">卒</font>〇<font color="green">卒</font>〇<font color="green">卒</font>〇<font color="green">卒</font>〇<font color="green">卒</font>  
〇〇〇〇〇〇〇〇〇  
〇〇〇〇〇〇〇〇〇  
<font color="red">兵</font>〇<font color="red">兵</font>〇<font color="red">兵</font>〇<font color="red">兵</font>〇<font color="red">兵</font>  
〇〇<font color="red">馬</font>〇<font color="red">砲</font>〇〇<font color="red">砲</font>〇  
〇〇〇〇〇〇〇〇〇  
〇<font color="red">車相仕帥仕相馬車</font>  

It provides a very clear picture of the game state and the current AI score.

!!! warning

    Some of the pictures and other resources involved in the project come from the Internet and are not used for commercial purposes.  
    Please contact me for infringement: 2951256653@qq.com

---

If you want to know more about this program, see: https://xiaokang2022.blog.csdn.net/article/details/128852029
