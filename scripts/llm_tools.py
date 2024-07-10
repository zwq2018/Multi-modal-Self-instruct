import time
from functools import wraps
import threading

import random
from openai import AzureOpenAI, OpenAI
import requests
import json

def retry(exception_to_check, tries=3, delay=3, backoff=1):
    """
    Decorator used to automatically retry a failed function. Parameters:

    exception_to_check: The type of exception to catch.
    tries: Maximum number of retry attempts.
    delay: Waiting time between each retry.
    backoff: Multiplicative factor to increase the waiting time after each retry.
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except exception_to_check as e:
                    print(f"{str(e)}, Retrying in {mdelay} seconds...")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def timeout_decorator(timeout):
    class TimeoutException(Exception):
        pass

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = [
                TimeoutException("Function call timed out")
            ]  # Nonlocal mutable variable

            def target():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    result[0] = e

            thread = threading.Thread(target=target)
            thread.start()
            thread.join(timeout)
            if thread.is_alive():
                print(f"Function {func.__name__} timed out, retrying...")
                return wrapper(*args, **kwargs)
            if isinstance(result[0], Exception):
                raise result[0]
            return result[0]

        return wrapper

    return decorator


@timeout_decorator(180)
@retry(Exception, tries=3, delay=5, backoff=1)
def send_chat_request_azure(
        message_text,
        engine="gpt35",
        temp=0.2,
        logit_bias: dict = {},
        max_new_token=4096,
        sample_n=1,
):
    data_res_list = []

    if engine == "xxx":

        url = "xxx"

        payload = json.dumps({
            "model": engine,
            "stream": False,
            "messages": message_text,
            "temperature": temp,
            "max_tokens": max_new_token,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "n": sample_n,
        })
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + '<Your-Api Key>',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        res = json.loads(response.text)
        data_res_list = []
        for choice in res['choices']:
            data_res = choice['message']['content']
            data_res_list.append(data_res)

        return data_res_list[0], data_res_list
