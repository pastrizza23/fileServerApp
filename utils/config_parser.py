"""Used for parse json config file"""
import json
import os

CONFIG_FILE = 'resources/config.json'
CONFIG_PATH = os.path.relpath(CONFIG_FILE)


def read_json(file_path=CONFIG_FILE) -> json:
    """Reads provided config json file"""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def config() -> json:
    """Return loaded json config file"""
    return _config


_config = read_json()
