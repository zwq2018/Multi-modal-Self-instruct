import json

from .plot_params import *
from .qa_template import *

symbols = {
    "Oval": "An oval represents a start and end point",
    "Parallelogram": "A parallelogram represents input or output",
    "Rectangle": "A rectangle represents a process",
    "Diamond": "A diamond indicates a decision",
    "Arrow": "A line is a connector that shows relationships between the representative shapes"
}


def algorithm_data_prompt(algorithm):
    prompt = f"Generate high quality python code for {algorithm}.\n"
    requirements = "Output format: ```python ... ```\n"

    return prompt + requirements


def algorithm_step_prompt(algorithm):
    prompt = f"Generate a step-by-step flow for the algorithm {algorithm}.\n"
    requirements = (
        "Requirements:\n"
        "Steps should be as detailed as possible.\n"
        "Parameters and variables should be introduced for clarity of description.\n"
    )
    requirements += "Output format: 1. ...; 2. ...; 3. ...\n"

    return prompt + requirements


def daily_step_prompt(scenario):
    prompt = f"Generate a step-by-step flow for the Daily Life Scenario {scenario}.\n"
    requirements = (
        "Requirements:\n"
        # "Steps should be as detailed as possible, but the depth should be no more than 8.\n"
        "6 steps at most.\n"
        "Introducing sequential structures, selection structures(at least one) to illustrate scenarios.\n"
    )
    requirements += "Output format: 1. ...; 2. ...; 3. ...\n"

    return prompt + requirements


def algorithm_caption_prompt():
    prompt = "Generate caption for the algorithm.\n"
    requirements = (
        "Requirements:\n"
        "The caption should be brief and concise.\n"
        'Don\'t generate any other content except {"caption": "..." }'
    )
    return prompt + requirements


def algorithm_plot_prompt(algorithm, additional_format_spec):
    prompt = f"Generate high quality python code to convert the above algorithm into a flowchart.\n"

    # general requirements
    general_spec = {
        "title": f"{algorithm}",
        "figure size": "no larger than 1000 * 1000 pixels",
        "font family": f"replace the font type in the sample code with {random.choice(font_types)}",
        "font size": "use large fonts",
        "palette": f"{colors}"
    }

    requirements = (
        "Requirements:\n"
        f"The code should use packages graphviz.\n"
        f"Use symbols reasonably to draw the flowchart, and the symbols and their meanings are given in JSON format: {json.dumps(symbols)}.\n"
        "Choose different colors from palette to fill in these symbols.\n"
        "Use the same color for the same shape.\n"
        "Introduce sequential structures, selection structures, loops, etc. to draw the entire flowchart.\n"
        "Based on the above algorithm code and flow, combine them and draw a flowchart.\n"
        "Each step should not be overly wordy and should be described in terms of parameters and variables wherever possible.\n"
        "The total depth should be no more than 8.\n"
        f"The code must conform general requirements (given in JSON format):\n{json.dumps(general_spec, indent=2)}\n"
    )
    if additional_format_spec is not None:
        requirements += f"The code must conform additional requirements (given in JSON format):\n{json.dumps(additional_format_spec, indent=2)}\n"

    requirements += "Output format: ```python ... ```\n"

    return prompt + requirements


def daily_plot_prompt(scenario, additional_format_spec):
    prompt = f"Generate high quality python code to convert the above steps into a flowchart.\n"

    # general requirements
    general_spec = {
        "title": f"{scenario}",
        "figure size": "no larger than 1000 * 1000 pixels",
        "font family": f"replace the font type in the sample code with {random.choice(font_types)}",
        "font size": "use large fonts",
        "palette": f"{colors_graphviz}"
    }

    requirements = (
        "Requirements:\n"
        f"The code should use packages graphviz.\n"
        f"Use symbols reasonably to draw the flowchart, and the symbols and their meanings are given in JSON format: {json.dumps(symbols)}.\n"
        "Choose different colors from palette to fill in these symbols.\n"
        "Use the same color for the same symbol.\n"
        "Introduce sequential structures, selection structures(at least one) to draw the entire flowchart.\n"
        "Streamline the number of words in each step and express the semantics clearly and completely.\n"
        "The structure of the flowchart can be(randomly choose from them) top-to-bottom, bottom-to-top, left-to-right, right-to-left or circular.\n"
        f"The code must conform general requirements (given in JSON format):\n{json.dumps(general_spec, indent=2)}\n"
    )
    if additional_format_spec is not None:
        requirements += f"The code must conform additional requirements (given in JSON format):\n{json.dumps(additional_format_spec, indent=2)}\n"

    requirements += "Output format: ```python ... ```\n"

    return prompt + requirements


def algorithm_qa_prompt(domain):
    prompt = "Generate correct and high quality question-answer pairs about the data and the plot.\n"
    requirements = (
        "Requirements:\n"
        f"Question-answer types: {algorithm_qa_types}.\n"
        "Questions distribution: STRUCTURAL: 5;\n"
        "Come up with questions based on the flowchart, and you should not be limited to example questions.\n"
        "If applicable, the answer should be a single number or word.\n"
        f"Output format: {algorithm_qa_template()}\n"
    )
    return prompt + requirements


def daily_qa_prompt(domain):
    prompt = "Generate correct and high quality question-answer pairs about the data and the plot.\n"
    requirements = (
        "Requirements:\n"
        f"Question-answer types: {daily_qa_types}.\n"
        "Questions distribution: STRUCTURAL: 5; REASONING: 10.\n"
        "Come up with questions based on the flowchart, and you should not be limited to example questions.\n"
        "Design REASONING type questions as multiple choice questions where all information must come from the flowchart.\n"
        "If applicable, the answer should be a single arabic numeral or word or choice.\n"
        f"Output format: {daily_qa_template()}\n"
    )
    return prompt + requirements


def algorithm_math_code_prompt(algorithm):
    prompt = f"Generate high quality python code for {algorithm}.\n"
    requirements = (
        "Requirements:\n"
        "The generated code and params can be executed as exec(code, params) later.\n"
        "params is a dictionary containing the necessary input values for the algorithm.\n"
        "Generate 10 sets of params in a list.\n"
        "The return value is located in the 'result' field of params.\n"
        "Don't throw exceptions in the generated code and params if possible.\n"
    )
    requirements += "Output format for the python code: ```python ... ``` \n"
    requirements += "Output format for params: ```json { \"params\": [{...}, ...] } ``` "

    return prompt + requirements
