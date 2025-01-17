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
    data['hours'] = total_seconds / 3600
    data['minutes'] = int((total_seconds % 3600) // 60)
    return data

def group_weekly_hours(data):    
    weekly_data = {}

    for entry in data:
            workfrom = entry['from']
            workfrom = datetime.strptime(workfrom, "%Y-%m-%dT%H:%M")
            # Calculate the Monday of the week the date belongs to
            weekday = workfrom.weekday()  # Monday is 0, Sunday is 6
            monday_of_week = workfrom - timedelta(days=weekday)
            monday = monday_of_week.strftime('%Y-%m-%d')

            if monday not in weekly_data:
                weekly_data[monday] = 0
                
            weekly_data[monday] += entry['hours']

    # Return grouped data
    result = [
        {
            # "period": f"{monday.strftime('%Y-%m-%d')} to {(monday + timedelta(days=6)).strftime('%Y-%m-%d')}",
            "week": f"{monday}",
            "hours": hours
        }
        for monday, hours in sorted(weekly_data.items(), reverse=True)  # Descending order
    ]
    return result 