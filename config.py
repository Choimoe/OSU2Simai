import json

# 读取 JSON 配置文件
with open('config.json', 'r') as f:
    config = json.load(f)

# 将配置绑定到变量
KEYS = config["KEYS"]
TEMP_DIR = config["TEMP_DIR"]
AUTHOR = config["AUTHOR"]
LEVEL = config["LEVEL"]
RANDOM = config["RANDOM"]
SAME = config["SAME"]
ONGEKI = config["ONGEKI"]
