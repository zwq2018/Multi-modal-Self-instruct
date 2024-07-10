import time

from llm_tools import send_chat_request_azure
import random, json
from tqdm import tqdm

import base64
from mimetypes import guess_type


# Function to encode a local image into data URL
def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"


if __name__ == '__main__':

    eval_data = []
    engine = 'xxx'
    task = 'xxx'
    with open('xxx/eval_xxxk.json') as f:
        for line in f:
            eval_data.append(json.loads(line))

        random_count = len(eval_data)

        human_select = eval_data[:random_count]

        res_list = []
        try:
            for data in tqdm(human_select):
                img_path = './' + data['image']
                url = local_image_to_data_url(img_path)

                msgs = [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": data['text'] + " Answer format (do not generate any other content): The answer is <answer>."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": url
                                }
                            }
                        ]
                    }
                ]

                res, _ = send_chat_request_azure(message_text=msgs, engine=engine, sample_n=1)

                if 'markers' in data.keys():
                    markers = data['markers']

                res = {
                    "question_id": data['question_id'],
                    "prompt": data['text'],
                    "text": res,
                    "truth": data['answer'],
                    "type": data['type'],
                    "answer_id": "",
                    "markers": markers,
                    "model_id": engine,
                    "metadata": {}
                }

                res_list.append(res)

                time.sleep(0.1)

                with open(f'{engine}/eval_{engine}_{task}_{random_count}.json', 'a') as fout:
                    fout.write(json.dumps(res) + '\n')
        except Exception as e:
            print(e)
            with open(f'{engine}/eval_{engine}_{task}_{random_count}.json', 'w') as fout:
                for res in res_list:
                    fout.write(json.dumps(res) + '\n')
