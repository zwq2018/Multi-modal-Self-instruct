import json

from . import gpt4_tools as gpt4


class CalculationProcessor:
    def __init__(self, data):
        self.context = []
        self.context.append({"role": "user", "content": f"The information: {data}"})
        self.context.append({"role": "user", "content": "You are given some information and several QA pairs having calculations."
                                                        "You need to get the answer step by step.\n"
                                                        "Do not generate any other content except {\"steps\": [\"...\"]}"})

    def process(self, query):

        self.context.append({"role": "user", "content": f"{query}"})
        solution, _ = gpt4.send_chat_request_azure(self.context, temp=0.2, sample_n=1, engine='deepseek-coder')
        self.context.pop()

        solution = json.loads(solution)
        steps = solution['steps']

        return steps
