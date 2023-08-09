import json


def read_json(file: str):
    with open(file, encoding='utf8') as fp:
        return json.load(fp)