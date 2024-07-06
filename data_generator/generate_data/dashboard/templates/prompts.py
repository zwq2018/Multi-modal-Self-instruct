import json
import random

from .plot_params import *
from .qa_template import *

code_matplotlib = {
    "Draw the outer border":
    """
x = np.cos(theta) * outer_radius
y = np.sin(theta) * outer_radius
ax.plot(x, y, c='#203360', alpha=0.5)
""",
    "Calculate scale":
    """
tick_theta = np.arange(...)
point_x_on_circle = [np.cos(i) for i in tick_theta]
point_y_on_circle = [np.sin(i) for i in tick_theta]
tick_point_y = [18 / 20 * i for i in point_y_on_circle]
tick_point_x = [18 / 20 * i for i in point_x_on_circle]
label_point_y = [17 / 20 * i for i in point_y_on_circle]
label_point_x = [17 / 20 * i for i in point_x_on_circle]
""",
    "Draw scale and scale labels":
    """
for i in np.arange(len(tick_theta)):
    # Draw Scale
    x = [tick_point_x[i], point_x_on_circle[i]]
    y = [tick_point_y[i], point_y_on_circle[i]]
    ax.plot(x, y, c='#1f3354', linewidth=...)
    ax.plot(x, y, c='#41b2f1')
    # Draw Scale Labels
    x = label_point_x[i]
    y = label_point_y[i] * 9 / 10
    ax.text(s=..., x=x, y=y, c=..., fontsize=10,
            horizontalalignment='center',
            verticalalignment='bottom')
""",
    "Draw the center of a circle":
    """
heart_x = 0
heart_y = 0
ax.plot(heart_x, heart_y, 'o', color=..., markersize=14, alpha=.4)
ax.plot(heart_x, heart_y, 'bo', markersize=7)
""",
    "draw pointer":
    """
ax.annotate(text='', xy=(a_x, a_y), xytext=(-a_x * .15, -a_y * .15),
            arrowprops=dict(width=.3, headwidth=4, headlength=6, fc=..., ec=...))
""",
    "Hide axis":
    """
ax.axis('off')
"""
}

code_matplotlib_detail = {
    "Draw the inner border":
    """
x = np.cos(theta) * inner_radius
y = np.sin(theta) * inner_radius
ax.plot(x, y, c=..., alpha=...)
""",
    "Draw smaller scale":
    """
point_x_on_circle = [np.cos(i) for i in tick_theta]
point_y_on_circle = [np.sin(i) for i in tick_theta]
 
for i in np.arange(len(tick_theta)):
    x = [point_x[i], point_x_on_circle[i]]
    y = [point_y[i], point_y_on_circle[i]]
    ax.plot(x, y, c=...)
"""
}

code_pyecharts = {
    "Overall":
    """
def chart():
    c = (
        Gauge()
        .add(
            "description",
            [("...", ...)],
            split_number=5,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(
                    color=[(..., "..."), ...], width=30
                )
            ),
            detail_label_opts=opts.LabelOpts(formatter="{value}"),
            start_angle=...,
            end_angle=...,
            min_=...,
            max_=...,
            radius=...,
            tooltip_opts=...,
            itemstyle_opts=...,
            is_clock_wise=...,
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="..."),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    return c
""",
    "Save as .png":
    """
from pyecharts.render import make_snapshot
make_snapshot(snapshot, chart().render(), \"xxx.png\", is_remove_html=True)
"""
}

code_none = {
    "Hide axis":
    """
ax.axis('off')
"""
}

parameters = {
    "matplotlib": ["Scale interval(5%, 10%, 20%)", "Outer border radius(0.9, 1, 1.2)", "Thickness of lines"],
    "pyecharts": ["color", "detail_text_color", "axis_label_formatter", "split_number", "radius", "angle_range", "start_angle", "end_angle", ],
    "none": ["color", "font_family", "font_size"]
}

packages = {
    "matplotlib": "matplotlib",
    "pyecharts": ["pyecharts", "snapshot_phantomjs"],
    "none": "whatever you want"
}

def disk_data_prompt(domain):
    prompt = f"Generate data related to {domain}, pay attention to requirements above and below:\n"
    requirements = (
        "Requirements:\n"
        "The range should only contain numbers, with '-' separating the min and max number.\n"
        "Generate only one set of json data.\n"
        'Don\'t generate any other content except {"reading": "...", "unit": "...", "range": "..."}\n'
    )
    return prompt + requirements


def disk_caption_prompt():
    prompt = "Generate caption for the dashboard.\n"
    requirements = (
        "Requirements:\n"
        "The caption should be brief and concise.\n"
        "The caption should describe the general content of the dashboard.\n"
        'Don\'t generate any other content except {"caption": "..." }'
    )
    return prompt + requirements


def disk_code_prompt(value, title, data_range, unit, additional_format_spec):
    # color control
    random.shuffle(colors)
    prompt = "Generate high quality python code for plotting disk dashboard.\n"

    external = random.choice(["pyecharts", "matplotlib"])
    # external = random.choice(["pyecharts", "none"])
    # external = random.choice(["matplotlib"])
    if external == "pyecharts":
        code_examples = code_pyecharts
        spec_req = {
            "figure size": "no larger than 600 * 600 pixels",
            "font size": "use medium fonts",
            "background color": "white or black",
        }
    elif external == "matplotlib":
        code_examples = code_matplotlib
        if random.random() < 0.5:
            code_examples.update(code_matplotlib_detail)
        spec_req = {
            "figure size": "no larger than 1000 * 1000 pixels",
            "font size": "use large fonts (for scale labels and title)",
        }
    else:
        code_examples = code_none
        spec_req = {
            "font size": "use large fonts (for scale labels and title)",
        }

    # general requirements
    general_spec = {
        "title": f"{title}",
        "palette": f"{colors}",
        "component": "border, scale, scale labels, center, pointer. No overlap between all components",
        "color": "replace the colors in the sample code with colors in palette",
        "font family": f"replace the font type in the sample code with {random.choice(font_types)}",
        "scale label": "the max and min values of the range must be drawn",
        "other params": f"other parameters such as {parameters[external]} should also be changed",
    }

    requirements = (
        "Requirements:\n"
        f"The code should use packages {packages[external]}.\n"
        f"The code example (given in JSON format) is {code_examples}.\n"
        "You must not be limited by the code sample and draw different styles of dials.\n"
        f"The code must conform general requirements (given in JSON format):\n{json.dumps(general_spec, indent=2)}.\n"
        f"The code must conform specific requirements (given in JSON format):\n{json.dumps(spec_req, indent=2)}.\n"
        f"The scale range must be the same as {data_range}, the min and max values of which are separated by a '-'."
        f"The pointer must point at the reading {value}!!!"
    )
    if additional_format_spec is not None:
        requirements += f"The code must conform additional requirements (given in JSON format):\n{json.dumps(additional_format_spec, indent=2)}\n"

    requirements += "Output format: ```python ... ```\n"

    return prompt + requirements


def disk_qa_prompt(domain):
    prompt = "Generate correct and high quality question-answer pairs about the data and the plot.\n"
    requirements = (
        "Requirements:\n"
        f"Question-answer types: {qa_types}.\n"
        "Questions distribution: DATA_EXTRACTION: 5; MATH_REASONING: 10; COLOR: 1\n"
        "Come up with questions based on the domain, and you should not be limited to example questions.\n"
        "The questions(especially MATH_REASONING) should be rich in variety and scenarios.\n"
        "If applicable, the answer should be a single arabic numeral or word.\n"
        "Otherwise set the question and give the answer in multiple choice (A, B, C, D) format.\n"
        "Consider the data and code together to get the answer.\n"
        f"Output format: {qa_template()}\n"
    )
    return prompt + requirements
