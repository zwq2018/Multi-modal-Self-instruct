import random

# packages
# packages = ['matplotlib==3.8.0', 'pandas==2.1.2', 'textwrap']
packages = ['matplotlib==3.8.0']

plot_styles = [
    'default',
    'classic',
    'Solarize_Light2',
    'dark_background',
    'ggplot',
    'fivethirtyeight',
    'fast',
    'bmh'
]

# tab20 palette
colors = [
    '(31.0, 119.0, 180.0)',
    '(174.0, 199.0, 232.0)',
    '(255.0, 127.0, 14.0)',
    '(255.0, 187.0, 120.0)',
    '(44.0, 160.0, 44.0)',
    '(152.0, 223.0, 138.0)',
    '(214.0, 39.0, 40.0)',
    '(255.0, 152.0, 150.0)',
    '(148.0, 103.0, 189.0)',
    '(197.0, 176.0, 213.0)',
    '(140.0, 86.0, 75.0)',
    '(196.0, 156.0, 148.0)',
    '(227.0, 119.0, 194.0)',
    '(247.0, 182.0, 210.0)',
    '(127.0, 127.0, 127.0)',
    '(199.0, 199.0, 199.0)',
    '(188.0, 189.0, 34.0)',
    '(219.0, 219.0, 141.0)',
    '(23.0, 190.0, 207.0)',
    '(158.0, 218.0, 229.0)'
]

colors_graphviz = [
    'aquamarine',
    'azure2',
    'bisque',
    'burlywood',
    'darkolivegreen1',
    'darksalmon',
    'deepskyblue',
    'goldenrod1',
    'gray55',
    'greenyellow',
    'khaki',
    'lightskyblue',
    'lime',
    'peru',
    'snow',
    'turquoise',
    'yellow',
    'violet'
]

chart_types = ['pie', 'line', 'bar']
# chart_types = ['bar']

grid_visibility = [True, False]

grid_line_styles = ['-', '--', '-.', ':']

line_styles = ['solid', 'dashed', 'dotted', 'dashdot']

marker_styles = [".", ",", "v", "^", "<", ">", "s", "p", "P", "*", "h", "H", "+", "x", "X", "D", "d", "|", "_"]

bar_styles = ['grouped', 'stacked']

bar_arrangement = ['vertical', 'horizontal']

font_types = ['serif', 'sans-serif', 'monospace']

tick_label_styles = ['sci', 'scientific', 'plain']

legend_positions = {
    "upper-right": {
        "loc": 2,  # upper left
        "bbox_to_anchor": "(1.1, 1.1)"
    },
    "lower-right": {
        "loc": 3,  # lower left
        "bbox_to_anchor": "(1.1, -0.1)"
    },
    "upper-left": {
        "loc": 1,  # upper right
        "bbox_to_anchor": "(-0.1, 1.1)"
    },
    "lower-left": {
        "loc": 4,  # lower right
        "bbox_to_anchor": "(-0.1, -0.1)"
    }
}


def legend_position():
    return random.choice(list(legend_positions.keys()))
