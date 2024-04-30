# Intelligent Magic Cube 🚀

A variety of intelligent search algorithms visually restore the 3D Magic Cube.

![](https://github.com/Xiaokang2022/Intelligent-Magic-Cube/blob/main/preview.png?raw=true)

!!! note

    This program is implemented by `tkinter` in combination with the third-party library [`tkintertools`](https://github.com/Xiaokang2022/tkintertools). `tkintertools` is a third-party library developed by me, I hope you will support me a lot!

## Star History

<a href="https://star-history.com/#Xiaokang2022/Intelligent-Magic-Cube&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Xiaokang2022/Intelligent-Magic-Cube&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Xiaokang2022/Intelligent-Magic-Cube&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=Xiaokang2022/Intelligent-Magic-Cube&type=Date" />
 </picture>
</a>

## How to use

### Before use

!!! info

    Make sure your Python version is **3.12** or greater.

### Install dependency

Install the third-party library tkintertools:

```sh
pip install tkintertools==2.6.21.1
```

or

```sh
pip install -r requirements.txt
```

### One last step

Run the `main.py`, and then, have fun! 😁

## Brief introduction

### List of algorithms

|      BFS      |     DFS     |     UCS      |    A/A*    |      HC       |             REV             |
| :-----------: | :---------: | :----------: | :--------: | :-----------: | :-------------------------: |
| Breadth First | Depth First | Uniform Cost | A / A Star | Hill Climbing | Not Algo, reverse operation |

### Evaluation functions

|   CBSV    |  ECLD  |    MHT    |   HM    |   MKVSK   |            h*             |
| :-------: | :----: | :-------: | :-----: | :-------: | :-----------------------: |
| Chebyshev | Euclid | Manhattan | Hamming | Minkowski | Ideal evaluation function |

### Customized actions

|   L   |   R   |   U   |   D   |   F   |   B   |
| :---: | :---: | :---: | :---: | :---: | :---: |
| Left  | Right |  Up   | Down  | Front | Back  |

### Some operations

* Hold down the left mouse button and drag to rotate the Rubik's Cube;
* Hold down the right mouse button and drag to move the Rubik's Cube;
* Scroll the mouse wheel to zoom in and out of the Rubik's Cube;

!!! warning

    Some of the pictures and other resources involved in the project come from the Internet and are not used for commercial purposes.  
    Please contact me for infringement: 2951256653@qq.com

---

For illustrated tutorials, see: https://xiaokang2022.blog.csdn.net/article/details/136768000  
For an introductory video, see: https://www.bilibili.com/video/BV1Gt421j7Sx/
