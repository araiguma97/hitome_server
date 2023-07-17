import requests
import json
import time
import os

from tqdm import tqdm

_json_dir_path  = "./json/"
_image_dir_path = "./img/"
_file_names = {
    "category_pageids": "category_pageids.json",
    "pageids":          "pageids.json",
    "pages":            "pages.json",
    "images":           "images.json",
}

_headers = { 'User-Agent' : 'Hitomebot/0.0 (tetra1738@gmail.com)' }
_sleep_sec = 1
_long_sleep_sec = 5

def request_to_wikipedia_api(params):
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

def download_images(images):
    for image in tqdm(images, desc="Downloading images"):
        if "url" not in image:
            continue

        response = requests.get(image["url"], headers=_headers)
        response.raise_for_status()
        time.sleep(_long_sleep_sec)

        if not os.path.isdir(_image_dir_path):
            os.mkdir(_image_dir_path)
        with open(_image_dir_path + image["image_title"], "wb") as f:
            f.write(response.content)

def exists_json(key):
    file_name = _file_names[key]
    return os.path.isfile(_json_dir_path + file_name)

def load_json(key):
    file_name = _file_names[key]
    with open(_json_dir_path + file_name, "r") as f:
        return json.load(f)

def dump_json(d, key):
    file_name = _file_names[key]
    if not os.path.isdir(_json_dir_path):
        os.mkdir(_pages_json_path)
    with open(_json_dir_path + file_name, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)

def split_list(l, n):
    ls = []

    for i in range(0, len(l), n):
        ls.append(l[i:i+n])

    return ls

