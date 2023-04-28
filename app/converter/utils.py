import json


def load_json_file(file_path):
    with open(file_path, "r") as f:
        json_data = f.read()
    return json.loads(json_data)
