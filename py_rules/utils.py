import json


def load_from_json(file_path) -> dict:
    """
    Load a rules from a JSON file.
    """
    with open(file_path) as f:
        data = json.load(f)
    return data


def save_dict_to_json(file_path, data: dict):
    with open(file_path, 'w') as f:
        json.dump(data, f)
