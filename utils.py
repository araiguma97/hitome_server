import os
import json
from typing import Any

_json_dir_path = "./json/"

def load_json(file_name: str) -> Any:
    if not os.path.isdir(_json_dir_path):
        os.mkdir(_json_dir_path)
    with open(_json_dir_path + file_name, "r") as f:
        return json.load(f)

def dump_json(d, file_name: str):
    if not os.path.isdir(_json_dir_path):
        os.mkdir(_json_dir_path)
    with open(_json_dir_path + file_name, "w") as f:
        json.dump(d, f, ensure_ascii=False, indent=4)