import requests
import time
import os

_image_dir_path = "./img/"

_headers = { 'User-Agent' : 'Hitomebot/0.0 (tetra1738@gmail.com)' }
_sleep_sec = 1
_long_sleep_sec = 5

def request_to_wikipedia(params):
    jsons = []

    wikipedia_url = "https://ja.wikipedia.org/w/api.php"
    while True: 
        response = requests.get(wikipedia_url, params=params, headers=_headers)
        response.raise_for_status()
        time.sleep(_sleep_sec)

        json = response.json()
        jsons.append(json)

        try:
            cmcontinue = json["continue"]["cmcontinue"]
            params["cmcontinue"] = cmcontinue
        except KeyError:
            return jsons

def download_image(image):
    response = requests.get(image["url"], headers=_headers)
    response.raise_for_status()
    time.sleep(_long_sleep_sec)

    if not os.path.isdir(_image_dir_path):
        os.mkdir(_image_dir_path)
    with open(_image_dir_path + image["image_title"], "wb") as f:
        f.write(response.content)

