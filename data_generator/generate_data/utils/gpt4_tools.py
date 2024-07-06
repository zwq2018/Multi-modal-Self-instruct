import time
from functools import wraps
import threading

from openai import OpenAI


def retry(exception_to_check, tries=3, delay=5, backoff=1):
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
        engine="xxx",
        temp=0.2,
        logit_bias: dict = {},
        max_new_token=4096,
        sample_n=1,
):
    data_res_list = []
    # Config your api_key, base_url and model
    client = OpenAI(api_key="xxx", base_url="xxx")

    response = client.chat.completions.create(
        model=engine,
        messages=message_text,
        temperature=temp,
        max_tokens=max_new_token,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        n=sample_n,
    )

    for index in range(sample_n):
        data_res = response.choices[index].message.content
        data_res_list.append(data_res)

    return data_res_list[0], data_res_list
