"""Used for parse json config file"""
import json
import os

CONFIG_FILE = 'resources/config.json'
CONFIG_PATH = os.path.relpath(CONFIG_FILE)


def update_config(module: str, key: str, new_value: str) -> None:
    """Update config file"""
    json_config = read_json(CONFIG_FILE)
    json_config[module][key] = new_value
    new_config = json.dumps(json_config)
    with open(CONFIG_FILE, "w") as file:  # pylint: disable=unspecified-encoding
        file.write(new_config)


def get_config_file() -> str:
    """Return config file path"""
    return CONFIG_PATH


def read_json(file_path=CONFIG_FILE) -> json:
    """Reads provided config json file"""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def config() -> json:
    """Return loaded json config file"""
    return _config


_config = read_json()
