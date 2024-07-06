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
    '#1f77b4',
    '#aec7e8',
    '#ff7f0e',
    '#ffbb78',
    '#2ca02c',
    '#98DF8A',
    '#D62728',
    '#FF9896',
    '#9467BD',
    '#C5B0D5',
    '#8C564B',
    '#C49C94',
    '#E377C2',
    '#F7B6D2',
    '#7F7F7F',
    '#C7C7C7',
    '#BCBD22',
    '#DBDB8D',
    '#17BECF',
    '#9EDADA'
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
