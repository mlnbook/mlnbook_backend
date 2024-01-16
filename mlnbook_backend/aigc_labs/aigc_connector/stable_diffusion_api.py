import json
import base64
import requests


def submit_post(url: str, data: dict):
    return requests.post(url, data=json.dumps(data))


def save_encoded_image(b64_image: str, output_path: str):
    with open(output_path, 'wb') as image_file:
        image_file.write(base64.b64decode(b64_image))


if __name__ == '__main__':
    txt2img_url = r'http://127.0.0.1:7861/sdapi/v1/txt2img'
    data = {'prompt': 'a dog wearing a hat',
            'negative_prompt': '',
            'sampler_index': 'DPM++ SDE',
            'seed': 1234,
            'steps': 20,
            'width': 512,
            'height': 512,
            'cfg_scale': 8}
    response = submit_post(txt2img_url, data)
    save_image_path = r'tmp.png'
    save_encoded_image(response.json()['images'][0], save_image_path)
