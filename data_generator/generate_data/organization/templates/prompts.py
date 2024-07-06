import json
import random

from .qa_template import *
from .plot_params import *


def data_prompt(domain):
    prompt = f"Generate data related to {domain}, pay attention to requirements above and below:\n"
    requirements = (
        "Requirements:\n"
        f"The data should describe a tree-like structure of {domain}.\n"
        "There can be multiple layers and certain nodes can have no children.\n"
        "The data should not contain too much nodes and should not be too complicated.\n"
        "Increase the depth of the data, but no more than 3 nodes in the same layer.\n"
        "The total number of nodes should not exceed 8.\n"
        'Don\'t generate any other content except {"data": {...}}\n'
    )
    return prompt + requirements


def caption_prompt():
    prompt = "Generate caption for the data.\n"
    requirements = (
        "Requirements:\n"
        "The caption should be brief and concise.\n"
        "The caption should describe the general content of the data.\n"
        'Don\'t generate any other content except {"caption": "..." }'
    )
    return prompt + requirements


def summary_prompt(domain):
    prompt = "Generate summary for the data.\n"
    requirements = (
        "Requirements:\n"
        "The summary must describe the general content of the data.\n"
        f"The summary must describe in what ways the data illustrate {domain}.\n"
        'Don\'t generate any other content except {"summary": "..." }\n'
    )
    return prompt + requirements


def code_prompt(title, additional_format_spec):
    prompt = "Generate high quality python code for drawing a organization chart for the data.\n"
    # general requirements
    general_format_spec = {
        "title": f"{title}",
        "resolution": "no more than 800 x 800 pixels",
        "data": [
            "all data must be used",
            "annotate the node on the organization chart",
        ],
        "style": f"use '{random.choice(plot_styles)}'",
        "color": [
            "use colors appropriately (academic and business style are preferred)",
            "specify the colors you use in the code",
        ],
        "font type": random.choice(font_types),
        "font size": "use appropriate font size",
        "layout": [
            "draw an hierarchy structured organization chart of the data!!!",
            "nodes different levels are positioned vertically, nodes on the same level are positioned horizontally"
            "use arrows or lines to connect nodes",
            "do not show axis",
        ],
    }

    requirements = (
        "Requirements:\n"
        f"The code should only use packages from {packages} (notice the version).\n"
        f"The code must conform general requirements (given in JSON format):\n{json.dumps(general_format_spec, indent=2)}\n"
        f"The code must not use for-loop instead of list comprehension\n"
    )
    if additional_format_spec is not None:
        requirements += f"The code must conform additional requirements (given in JSON format):\n{json.dumps(additional_format_spec, indent=2)}\n"

    requirements += "Output format: ```python ... ```\n"

    return prompt + requirements

def qa_prompt():
    prompt = "Generate correct and high quality question-answer pairs about the data and the organization chart\n"
    requirements = (
        "Requirements:\n"
        f"Question-answer types: {qa_types}.\n"
        "Questions distribution: STRUCTURAL: 2; MATH_REASONING: 5;\n"
        "If applicable, the answer can be a single word.\n"
        "Consider the data and code together to get the answer.\n"
        f"Output format: {qa_template()}\n"
    )
    return prompt + requirements
