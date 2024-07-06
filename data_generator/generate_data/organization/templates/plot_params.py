import random

# packages
# packages = ["matplotlib", "pandas", "textwrap"]
packages = ["graphviz"]

plot_styles = [
    "Solarize_Light2",
    "_classic_test_patch",
    "_mpl-gallery",
    "_mpl-gallery-nogrid",
    "bmh",
    "classic",
    "fast",
    "fivethirtyeight",
    "ggplot",
    "grayscale",
    "seaborn-v0_8",
    "seaborn-v0_8-bright",
    "seaborn-v0_8-colorblind",
    "seaborn-v0_8-deep",
    "seaborn-v0_8-muted",
    "seaborn-v0_8-notebook",
    "seaborn-v0_8-paper",
    "seaborn-v0_8-pastel",
    "seaborn-v0_8-poster",
    "seaborn-v0_8-talk",
    "seaborn-v0_8-ticks",
    "seaborn-v0_8-white",
    "seaborn-v0_8-whitegrid",
    "tableau-colorblind10",
]

header_colors = [
    "(31.0, 119.0, 180.0)",  # 深蓝色
    "(214.0, 39.0, 40.0)",  # 鲜红色
    "(148.0, 103.0, 189.0)",  # 深紫色
    "(140.0, 86.0, 75.0)",  # 深棕色
    "(227.0, 119.0, 194.0)",  # 鲜粉色
    "(127.0, 127.0, 127.0)",  # 深灰色
    "(188.0, 189.0, 34.0)",  # 橄榄绿
    "(23.0, 190.0, 207.0)",  # 青蓝色
    "(49.0, 130.0, 189.0)",  # 铁蓝色
    "(44.0, 160.0, 44.0)",  # 暗绿色
    "(31.0, 119.0, 180.0)",  # 深灰蓝色
    "(214.0, 39.0, 40.0)",  # 深红色
    "(140.0, 86.0, 75.0)",  # 棕褐色
]

row_colors = [
    "(174.0, 199.0, 232.0)",  # 浅蓝色
    "(255.0, 187.0, 120.0)",  # 桃色
    "(152.0, 223.0, 138.0)",  # 浅绿色
    "(255.0, 152.0, 150.0)",  # 浅红色
    "(197.0, 176.0, 213.0)",  # 浅紫色
    "(196.0, 156.0, 148.0)",  # 浅棕色
    "(199.0, 199.0, 199.0)",  # 浅灰色
    "(219.0, 219.0, 141.0)",  # 淡黄色
    "(158.0, 218.0, 229.0)",  # 天蓝色
    "(255, 255, 255)",  # 白色
    "(255, 223, 186)",  # 米色
    "(207, 207, 207)",  # 淡蓝灰色
    "(158, 218, 229)",  # 浅青色
    "(188, 189, 34)",  # 淡橄榄色
    "(255, 247, 188)",  # 象牙色
]

chart_types = ["pie", "line", "bar"]

grid_visibility = [True, False]

grid_line_styles = ["-", "--", "-.", ":"]

line_styles = ["solid", "dashed", "dotted", "dashdot"]

marker_styles = [
    ".",
    ",",
    "v",
    "^",
    "<",
    ">",
    "s",
    "p",
    "P",
    "*",
    "h",
    "H",
    "+",
    "x",
    "X",
    "D",
    "d",
    "|",
    "_",
]

bar_styles = ["grouped", "stacked"]

bar_arrangement = ["vertical", "horizontal"]

font_types = ["serif", "sans-serif", "monospace"]

tick_label_styles = ["sci", "scientific", "plain"]

legend_positions = {
    "upper-right": {"loc": 2, "bbox_to_anchor": "(1.1, 1.1)"},  # upper left
    "lower-right": {"loc": 3, "bbox_to_anchor": "(1.1, -0.1)"},  # lower left
    "upper-left": {"loc": 1, "bbox_to_anchor": "(-0.1, 1.1)"},  # upper right
    "lower-left": {"loc": 4, "bbox_to_anchor": "(-0.1, -0.1)"},  # lower right
}


def legend_position():
    return random.choice(list(legend_positions.keys()))
