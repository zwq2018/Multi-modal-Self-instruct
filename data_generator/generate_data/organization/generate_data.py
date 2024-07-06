import os
import time
from datetime import datetime
import random
import re
import json
from multiprocessing import Process, Manager

from .templates import prompts
from ..utils import gpt4_tools as gpt4


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


def generate_raw_data(domain, context):
    """
    Generate raw data by `prompt`
    """
    prompt = prompts.data_prompt(domain)
    context.append({"role": "user", "content": prompt})
    data, _ = gpt4.send_chat_request_azure(
        context, temp=1.2, sample_n=1
    )
    data = format_parser(data, format="json")
    context.append({"role": "assistant", "content": data})

    # print(data)
    return data


def generate_caption_summary(domain, context):
    """
    Generate caption & summary for the data
    """
    prompt = prompts.caption_prompt()
    context.append({"role": "user", "content": prompt})
    caption, _ = gpt4.send_chat_request_azure(
        context, temp=0.6, sample_n=1
    )
    context.append({"role": "assistant", "content": caption})

    return caption, ""


def generate_data(domain, context, semi_finished_list, args):
    # create a new batch directory
    batch_dir = (
        args.batch_dir + "batch" + datetime.now().strftime("%Y%m%d") + "/"
    )
    os.makedirs(batch_dir, exist_ok=True)
    os.makedirs(os.path.join(batch_dir, "plots"), exist_ok=True)

    # load existing data for `domain`
    previous_caption = []
    previous_caption.extend(semi_finished_list)

    previous_summary_ids = set()
    for data_point in previous_caption:
        previous_summary_ids.add(data_point["id"])

    if os.path.exists(os.path.join(batch_dir, "lm_generated_semi.json")):
        with open(batch_dir + "lm_generated_semi.json", "r") as fin:
            for line in fin:
                data_point = json.loads(line)
                if (
                    data_point["domain"] == domain
                    and data_point["id"] not in previous_summary_ids
                ):
                    previous_caption.append(data_point["caption"])

    # generate data
    try:
        raw_data = generate_raw_data(domain, context)
        data = json.loads(raw_data)

        # generate caption and summary
        caption, summary = generate_caption_summary(domain, context)
        caption_text = json.loads(caption)["caption"]

        now = datetime.now()
        microsecond = f"{int(now.microsecond / 1000):03d}"
        nanosecond = f"{now.microsecond % 1000:03d}"

        semi_finished_data_point = {
            "domain": domain,
            "data": data["data"],
            "caption": caption_text,
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

    context.append({"role": "user", "content": "The data is:\n"})
    context.append({"role": "user", "content": json.dumps(data_point["data"])})

    batch_dir = (
        args.batch_dir + "batch" + datetime.now().strftime("%Y%m%d") + "/plots/"
    )

    additional_requirements = {
        "save path": f"{batch_dir}{data_point['id']}.png",
        "show plot": "do not show the plot",
    }

    prompt = prompts.code_prompt(data_point["caption"], additional_requirements)
    context.append({"role": "user", "content": prompt})

    pattern = r"```python(.*?)```"
    raw_code = None

    for i in range(retries):
        try:
            code, _ = gpt4.send_chat_request_azure(
                context, temp=1, sample_n=1
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
            context.append({"role": "assistant", "content": raw_code[0]})
            context.append(
                {"role": "user", "content": f"Error: {e}, correct your code.\n"}
            )
            print(e)
            print(f"Trying correcting code for {i + 1} times for {domain}")
            if i + 1 >= retries:
                print(f"Error: {e}, the plot for {domain} will be discarded.")
                return None

    return raw_code[0]


def generate_qa(domain, data_point, context, args):
    """
    Generate QA pairs for the plot
    """
    prompt = prompts.qa_prompt()
    context.append({"role": "user", "content": prompt})
    qa, _ = gpt4.send_chat_request_azure(
        context, temp=0.5, sample_n=1
    )
    qa = format_parser(qa, format="json")

    try:
        qa = json.loads(qa)
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


def organization_batch_worker(domain, args):
    semi_finished_list = []
    context_msgs = []
    random.seed(os.getpid())
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
