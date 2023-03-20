""" All constants """

from ctypes import OleDLL

PROCESS_SYSTEM_DPI_AWARE = 1  # DPI级别
SCALE = OleDLL('shcore').GetScaleFactorForDevice(0)/100  # 屏幕缩放因子

COLOR_BUTTON_FILL = '#E1E1E1', '#E5F1FB', '#CCE4F7', '#E0E0E0'      # 默认的按钮内部颜色
COLOR_BUTTON_OUTLINE = '#C0C0C0', '#288CDB', '#4884B4', '#D0D0D0'   # 默认的按钮外框颜色
COLOR_TEXT_FILL = '#FFFFFF', '#FFFFFF', '#FFFFFF', '#E0E0E0'        # 默认的文本内部颜色
COLOR_TEXT_OUTLINE = '#C0C0C0', '#414141', '#288CDB', '#D0D0D0'     # 默认的文本外框颜色
COLOR_TEXT = '#000000', '#000000', '#000000', '#A3A3A3'             # 默认的文本颜色
COLOR_NONE = '', '', '', ''                                         # 透明颜色
COLOR_BAR = '#E1E1E1', '#06b025'                                    # 默认的进度条颜色

BORDERWIDTH = 1             # 默认控件外框宽度
CURSOR = '│'                # 文本光标
FONT = 'KaiTi'              # 默认字体
SIZE = 20                   # 默认字体大小
LIMIT = -1                  # 默认文本长度
RADIUS = 0                  # 默认控件圆角半径
FRAMES = 60                 # 默认帧数
