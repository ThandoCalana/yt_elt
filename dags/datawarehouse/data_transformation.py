from datetime import timedelta, datetime


def parse_duration(duration_str):
    
    duration = duration_str.replace('P', '').replace('T', '') # PT simply mean the duration_str represents a period of time
    # PT34H23M -> 34H23M

    components = ['D', 'H', 'M', 'S']
    values = {'D': 0, 'H': 0, 'M':0, 'S':0}

    for c in components:
        if c in duration:
            value, duration = duration.split(c) # 34H23M -> [34, 23M]. On next iteration, duration == 23M
            values[c] = int(value) # {'D': 0, 'H': 34, 'M': 23, 'S': 0}

    total_duration = timedelta(
        days = values['D'],
        hours = values['H'],
        minutes = values['M'],
        seconds = values['S']
    )

    return total_duration


def transform_data(row):

    duration_td = parse_duration(row['duration'])

    duration_sec = duration_td.total_seconds() # Convert to seconds, to categorise videos into shorts or normal-length 

    row['duration'] = duration_td # Assigning parse time as the duration

    row['video_type'] = ['SHORT' if duration_sec <= 60 else 'NORMAL']

    return row