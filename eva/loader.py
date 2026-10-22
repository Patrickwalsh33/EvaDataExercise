import json


def load_eva_data(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
