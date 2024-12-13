from bson import json_util


def return_json(data):
    return json_util.dumps(data, indent=4)