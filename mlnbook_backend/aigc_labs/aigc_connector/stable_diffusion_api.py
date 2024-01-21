import json
import base64
import io
from PIL import Image
import requests


def save_encoded_image(b64_image: str, output_path: str):
    with open(output_path, 'wb') as image_file:
        image_file.write(base64.b64decode(b64_image))
    return image_file


def call_txt2img_api(payload, override_settings=None):
    # prompt, negative_prompt, sampler_index, seed, steps = 20, width = 1024, height = 1024
    txt2img_url = r'http://127.0.0.1:7861/sdapi/v1/txt2img'
    data = {'prompt': payload["prompt"],
            'negative_prompt': payload["negative_prompt"],
            'sampler_index': payload["prompt"],  # 'DPM++ SDE'
            'seed': payload["seed"],
            'steps': payload.get("steps", 20),
            'width': payload.get("width", 1024),
            'height': payload.get("width", 1024),
            'cfg_scale': payload.get("cfg_scale", 8)}

    option_settings = {
        "filter_nsfw": override_settings.get("filter_nsfw", True),
        'sd_model_checkpoint': override_settings.get('sd_model_checkpoint', 'sd_xl_base_1.0'),
    }
    if override_settings:
        option_settings.update(override_settings)
    payload["override_settings"] = option_settings

    response = requests.post(txt2img_url, data=json.dumps(data))
    # save_image_path = r'tmp.png'
    # save_encoded_image(response.json()['images'][0], save_image_path)
    # b64_image = response.json()['images'][0]
    # return b64_image
    image = Image.open(io.BytesIO(base64.b64decode(response.json()['images'][0])))
    # image.save('output.png')
    return image

