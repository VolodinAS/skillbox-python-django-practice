import json


def pretty(data):
    output = json.dumps(data, indent=4, ensure_ascii=False)
    print(output)
