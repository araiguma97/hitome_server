import os
import json
from typing import Any

_dir_paths = {
    "config": "./config/",
    "output": "./output/"
}

def load_json(key: str, file_name: str) -> Any:
    if not os.path.isdir(_dir_paths[key]):
        os.mkdir(_dir_paths[key])
    with open(_dir_paths[key] + file_name, "r") as f:
        return json.load(f)

def dump_json(key: str, d: dict, file_name: str):
    if not os.path.isdir(_dir_paths[key]):
        os.mkdir(_dir_paths[key])
    with open(_dir_paths[key] + file_name, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)