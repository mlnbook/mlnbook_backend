import os
import requests

xi_key = os.environ.get('ELEVENLABS_ACCESS_KEY')
CHUNK_SIZE = 1024


def tts_generator(req_txt, req_type='txt'):
    url = "https://api.elevenlabs.io/v1/text-to-speech/jBpfuIE2acCO8z3wKNLl"

    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": xi_key
    }

    data = {
      "text": "Dog.Dog.Dog.Here is dog.",
      "model_id": "eleven_monolingual_v1",
      "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
      }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('path/to/output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
