import json
import random
import re
import time
from datetime import datetime
from multiprocessing import Process

from ..utils import gpt4_tools as gpt4
from iq_prompt import iq_prompt

engine = "deepseek-coder"


def format_parser(data, format="json") -> str:
    pattern = None
    if format == "json":
        pattern = r"```json(.*?)```"
    elif format == "python":
        pattern = r"```python(.*?)```"
    raw_data = re.findall(pattern, data, re.DOTALL)
    # maybe ```json``` pattern or not
    if raw_data:
        raw_data = raw_data[0]
    else:
        raw_data = data
    return raw_data


def worker(examples, id, retries=4):
    path = f"./gpt4_generations/plots/{id}.png"

    context = [{"role": "user", "content": iq_prompt(examples, path)}]

    for i in range(retries):
        try:
            res, _ = gpt4.send_chat_request_azure(
                context, temp=1, sample_n=1, engine=engine
            )
            res = format_parser(res, format="json")
            context.append({"role": "assistant", "content": res})

            json_res = json.loads(res)

            code = json_res["code"]
            exec(code, globals())

            with open(f"./gpt4_generations/iq_test.json", "r") as f:
                data_list = json.load(f)
            with open(f"./gpt4_generations/iq_test.json", "w") as f:
                json_res["id"] = id
                data_list.append(json_res)
                json.dump(data_list, f, indent=2)
            break

        except Exception as e:
            context.append(
                {"role": "user", "content": f"Error: {e}, correct your code."}
            )
            print(f"Trying correcting code for {i + 1} times, {e}")


if __name__ == "__main__":
    with open(f"./gpt4_generations/iq_test.json", "r") as f:
        data_list = json.load(f)

    processes = []
    for _ in range(10):
        random.shuffle(data_list)
        examples = data_list[:2]

        time.sleep(random.randint(5, 10) / 10)

        now = datetime.now()
        microsecond = f"{int(now.microsecond / 1000):03d}"
        nanosecond = f"{now.microsecond % 1000:03d}"

        id = now.strftime("%Y%m%d%H%M%S") + str(microsecond) + str(nanosecond)

        p = Process(target=worker, args=(examples, id, 4))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
