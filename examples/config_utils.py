import json
import os

CONFIG_PATH = 'config.json'

def read_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def write_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)