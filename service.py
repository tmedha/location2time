import requests
from datetime import datetime

from constants import LAT_LON_API_URL, TIME_ZONE_API_URL

class NotFoundError(Exception):
    ...

def get_coordinates(name):
    payload = {
        "q": name,
        "format":"json"
    }
    headers = {
        "User-Agent": "location2time/0.0.0.0"
    }
    resp = requests.get(LAT_LON_API_URL, params=payload, headers=headers)
    if not resp.ok:
        raise Exception(f"Coordinate Request Failed for Location {name} with status {resp.status_code}")
    
    items = resp.json()
    if len(items) == 0:
        raise NotFoundError(f"No Location Found for location {name}")
    
    most_relevant = return_lowest_ranked_item(items)
    lat = float(most_relevant["lat"])
    lon = float(most_relevant["lon"])
    return lat, lon

def return_lowest_ranked_item(items):
    items = sorted(items, key=lambda item: item["place_rank"])
    return items[0]

def get_time(lat, lon):
    payload = {
        "lat": lat,
        "lng": lon,
        "username": "location2time"
    }
    resp = requests.get(TIME_ZONE_API_URL, params=payload)
    if not resp.ok:
        raise Exception(f"Time-zone not found for {lat} and {lon}")
    
    time_data = resp.json()
    time_string = time_data["time"]
    date_obj = datetime.strptime(time_string, "%Y-%m-%d %H:%M")
    return date_obj

def format_time(time):
    format = "%-I:%M %p, %B %-d, %Y, %A"
    return time.strftime(format)