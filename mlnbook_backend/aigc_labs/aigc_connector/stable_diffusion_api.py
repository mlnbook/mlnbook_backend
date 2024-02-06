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
    if override_settings is None:
        override_settings = {}
    txt2img_url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'
    reqeust_data = {'prompt': payload["prompt"],
                    'negative_prompt': payload.get("negative_prompt", ""),
                    'sampler_index': payload.get("sampler_index", "DPM++ 2M Karras"),  # 'DPM++ SDE'
                    'seed': payload.get("seed", -1),
                    'steps': payload.get("steps", 20),
                    'width': payload.get("width", 1024),
                    'height': payload.get("width", 1024),
                    'cfg_scale': payload.get("cfg_scale", 7)}

    option_settings = {
        'sd_model_checkpoint': override_settings.get('sd_model_checkpoint', 'juggernautXL_v7Rundiffusion.safetensors'),
    }
    if override_settings:
        option_settings.update(override_settings)
    reqeust_data["override_settings"] = option_settings
    response = requests.post(txt2img_url, data=json.dumps(reqeust_data))
    if response.status_code > 300:
        print(response)
        return
    # save_image_path = r'tmp.png'
    # save_encoded_image(response.json()['images'][0], save_image_path)
    # b64_image = response.json()['images'][0]
    # return b64_image
    image = Image.open(io.BytesIO(base64.b64decode(response.json()['images'][0])))
    # image.save('output.png')
    return image
