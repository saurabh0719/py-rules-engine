import json

def load_json_rules(json_file) -> dict:
    """
    Load a rules from a JSON file.
    """
    with open(json_file) as f:
        rules = json.load(f)
    return rules
