import os
import json

KEYS = None
TEMP_DIR = None
AUTHOR = None
LEVEL = None
RANDOM = None
SAME = None
ONGEKI = None
ONGEKI_KEYS = None


def init_config_file(file_path='config.json'):
    global KEYS, TEMP_DIR, AUTHOR, LEVEL, RANDOM, SAME, ONGEKI, ONGEKI_KEYS
    default_content = {
        "KEYS": [
            [],
            [],
            [5, 4],
            [],
            [6, 5, 4, 3],
            [],
            [7, 6, 5, 4, 3, 2],
            [8, 7, 6, 5, 4, 3, 2],
            [8, 7, 6, 5, 4, 3, 2, 1]
        ],
        "TEMP_DIR": "./tmp",
        "AUTHOR": "OSU2Simai",
        "LEVEL": 15,
        "RANDOM": 0,
        "SAME": False,
        "ONGEKI": False,
        "ONGEKI_KEYS": [
            -16, -10, -4, 4, 10, 16
        ]
    }

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(default_content, f, indent=2)
        print(f"Config file '{file_path}' created with default content.")
    else:
        print(f"Config file '{file_path}' already exists.")

    with open('config.json', 'r') as f:
        config = json.load(f)

    KEYS = config["KEYS"]
    TEMP_DIR = config["TEMP_DIR"]
    AUTHOR = config["AUTHOR"]
    LEVEL = config["LEVEL"]
    RANDOM = config["RANDOM"]
    SAME = config["SAME"]
    ONGEKI = config["ONGEKI"]
    ONGEKI_KEYS = config["ONGEKI_KEYS"]
