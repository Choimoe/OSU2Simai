import json

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
