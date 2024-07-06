import os
import time
from datetime import datetime
import random
import re
import json
from multiprocessing import Process, Manager

from .templates import prompts
from ..utils import gpt4_tools as gpt4


def generate_raw_data(algorithm, context):
    """
    Generate raw data by `prompt`
    """
    prompt = prompts.algorithm_data_prompt(algorithm)
    context.append({"role": "user", "content": prompt})
    code, _ = gpt4.send_chat_request_azure(
        context, temp=0.7, sample_n=1
    )
    pattern = r"```python(.*?)```"
    code = re.findall(pattern, code, re.DOTALL)[0]
    context.append({"role": "assistant", "content": code})

    prompt = prompts.algorithm_step_prompt(algorithm)
    context.append({"role": "user", "content": prompt})
    steps, _ = gpt4.send_chat_request_azure(
        context, temp=0.6, sample_n=1
    )
    context.append({"role": "assistant", "content": steps})
    return steps, code


def format_parser(data, format="json") -> str:
    pattern = None
    if format == "json":
        pattern = r"```json(.*?)```"
    elif format == "python":
        pattern = r"```python(.*?)```"
    raw_data = re.findall(pattern, data, re.DOTALL)
    # maybe ```json``` pattern
    if raw_data:
        raw_data = raw_data[0]
    return raw_data


def generate_data(domain, context, semi_finished_list, args):
    # create a new batch directory
    batch_dir = (
        args.batch_dir + "batch" + datetime.now().strftime("%Y%m%d") + "/"
    )
    os.makedirs(batch_dir, exist_ok=True)
    os.makedirs(os.path.join(batch_dir, "plots"), exist_ok=True)

    # generate algorithm steps
    try:
        steps, code = generate_raw_data(domain, context)

        now = datetime.now()
        microsecond = f"{int(now.microsecond / 1000):03d}"
        nanosecond = f"{now.microsecond % 1000:03d}"

        semi_finished_data_point = {
            "algorithm": domain,
            "step": steps,
            "code": code,
            "id": now.strftime("%Y%m%d%H%M%S") + str(microsecond) + str(nanosecond),
        }

        with open(os.path.join(batch_dir, "lm_generated_semi.json"), "a") as fout:
            fout.write(json.dumps(semi_finished_data_point) + "\n")

        return semi_finished_data_point
    except Exception as e:
        print(f"Error: {e}, the semi-finished data for {domain} will be discarded.")
        return None


def execute_code(code, result):
    try:
        exec(code, globals())
    except Exception as e:
        result["error"] = e


def generate_plots(domain: str, data_point: dict, context: list[dict], args, retries=3):
    """
    Use python code to generate plots
    """
    context.append({"role": "user", "content": "The algorithm is:\n"})
    context.append({"role": "user", "content": json.dumps(data_point["code"])})
    context.append({"role": "user", "content": "The algorithm steps are:\n"})
    context.append({"role": "user", "content": json.dumps(data_point["step"])})

    batch_dir = (
        args.batch_dir + "batch" + datetime.now().strftime("%Y%m%d") + "/plots/"
    )

    additional_requirements = {
        "save path": f"{batch_dir}{data_point['id']}",
        # "save parameters": "bbox_inches='tight', dpi=80",
        "save format": "save the result plot as png",
        "show plot": "do not show the plot",
    }

    prompt = prompts.algorithm_plot_prompt(
        data_point["algorithm"], additional_requirements
    )
    context.append({"role": "user", "content": prompt})

    pattern = r"```python(.*?)```"
    code = None
    raw_code = None

    for i in range(retries):
        try:
            code, _ = gpt4.send_chat_request_azure(
                context, temp=0.2, sample_n=1
            )
            raw_code = re.findall(pattern, code, re.DOTALL)
            if not raw_code:
                return None
            else:
                with Manager() as manager:
                    res = manager.dict()
                    p = Process(target=execute_code, args=(raw_code[0], res))
                    p.start()
                    p.join()

                    if "error" in res.keys():
                        raise Exception(res["error"])

                    data_point["code"] = raw_code[0]
                    context.append({"role": "assistant", "content": code})
                    break

        except Exception as e:
            context.append({"role": "assistant", "content": code})
            context.append(
                {"role": "user", "content": f"Error: {e}, correct your code.\n"}
            )
            print(f"Error: {e}, correct your code.")
            print(f"Trying correcting code for {i + 1} times for {domain}")
            if i + 1 >= retries:
                print(f"Error: {e}, the plot for {domain} will be discarded.")
                return None

    return raw_code[0]


def generate_math_qa(algorithm, retries=3):
    context = []
    prompt = prompts.algorithm_math_code_prompt(algorithm)
    context.append({"role": "user", "content": prompt})
    data = None
    math_qa = []
    for i in range(retries):
        try:
            # Generate algorithm code and algorithm input
            data, _ = gpt4.send_chat_request_azure(
                context, temp=0.2, sample_n=1
            )
            code = format_parser(data, format="python")
            if not code:
                raise Exception("Code output format is wrong, correct your code")
            params = format_parser(data, format="json")
            if not params:
                raise Exception("Data output format is wrong, correct your data")
            params = json.loads(params)["params"]

            # 10 sets of params in total
            for param in params:
                qa = {"Q": json.dumps(param)}
                exec(code, {"params": param})
                qa["A"] = json.dumps(param["result"])
                # DEBUG
                # print(param["result"])
                math_qa.append(qa)
            break

        except Exception as e:
            context.append({"role": "assistant", "content": data})
            context.append(
                {"role": "user", "content": f"Error: {e}, try to correct.\n"}
            )
            print(f"Error: {e}, try to correct.")
            print(f"Trying correcting code for {i + 1} times for {algorithm}")
            if i + 1 >= retries:
                print(f"Error: {e}, the qa for {algorithm} will be discarded.")
                return None

    return math_qa

def generate_qa(domain, data_point, context, args):
    """
    Generate QA pairs for the plot
    """
    prompt = prompts.algorithm_qa_prompt(domain)
    context.append({"role": "user", "content": prompt})
    qa, _ = gpt4.send_chat_request_azure(
        context, temp=0.2, sample_n=1
    )

    qa = json.loads(format_parser(qa, format="json"))
    qa["MATH_REASONING"] = generate_math_qa(data_point["algorithm"])
    if qa["MATH_REASONING"] is None:
        return None

    try:
        data_point["qa"] = qa

        batch_dir = (
            args.batch_dir + "batch" + datetime.now().strftime("%Y%m%d") + "/"
        )

        with open(os.path.join(batch_dir, "lm_generated_data.json"), "a") as fout:
            fout.write(json.dumps(data_point) + "\n")
    except Exception as e:
        print(f"Error: {e}, QAs for {domain} will be discarded.")
        return None

    return qa


def algorithm_batch_worker(domain, args):
    semi_finished_list = []
    context_msgs = []
    random.seed(os.getpid())

    # number of data generated for each domain
    while len(semi_finished_list) < args.batch_size:
        semi_finished_data_point = generate_data(
            domain, context_msgs, semi_finished_list, args
        )
        if semi_finished_data_point is not None:
            semi_finished_list.append(semi_finished_data_point)
        context_msgs.clear()
        time.sleep(random.randint(1, 10) / 10)

    # generate plots and qa
    success = 0
    for data_point in semi_finished_list:
        context_msgs.clear()
        code = generate_plots(domain, data_point, context_msgs, args)

        if code is None:
            continue
        qa = generate_qa(domain, data_point, context_msgs, args)
        if qa is None:
            batch_dir = (
                args.batch_dir
                + "batch"
                + datetime.now().strftime("%Y%m%d")
                + "/"
            )
            os.remove(os.path.join(batch_dir, "plots/" + data_point["id"] + ".png"))
            continue
        success += 1

    return success, len(semi_finished_list) - success
