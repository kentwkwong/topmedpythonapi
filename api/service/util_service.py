from datetime import datetime, timedelta
from bson import json_util


def return_json(data):
    return json_util.dumps(data, indent=4)

def calculate_work_hours(data):
    workfrom = data.get('from')
    workfrom = datetime.strptime(workfrom, "%Y-%m-%dT%H:%M")
    workto = data.get('to')
    workto = datetime.strptime(workto, "%Y-%m-%dT%H:%M")
    hadlunch = data.get('lunch')
    time_diff = workto-workfrom
    time_diff = time_diff - timedelta(minutes=30) if hadlunch else time_diff
    total_seconds = time_diff.total_seconds()
    data['hours'] = int(total_seconds // 3600)
    data['minutes'] = int((total_seconds % 3600) // 60)
    return data
