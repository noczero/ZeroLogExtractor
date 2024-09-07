import csv
import datetime
import json

import requests

ip_records = {}


def parse_json_log(path: str) -> list:
    """Parses the given JSON-formatted log file and returns a list of dictionaries."""
    res = []
    with open(path, 'r') as f:
        for line in f:
            parsed = json.loads(line)
            res.append(parsed)
    return res


def get_ip_location(ip_address: str) -> dict:
    """Gets the location of the given IP address."""

    ip_location = ip_records.get(ip_address, None)
    if ip_location:
        return ip_location

    response = requests.get(f"https://api.techniknews.net/ipgeo/{ip_address}")
    if response.status_code == 200:
        ip_records[ip_address] = response.json()
        return ip_records[ip_address]
    else:
        ip_records[ip_address] = response.text
        return {}


def save_array_to_csv(array: list, file_name: str):
    """Saves the given array to the given CSV file."""
    with open(file_name, 'w') as f:
        csv_writer = csv.writer(f)
        for row in array:
            csv_writer.writerow(row)


def convert_unix_time_to_local_time(unix_time: int) -> str:
    """Converts the given Unix time miliseconds to local time."""
    if unix_time:
        unix_time /= 1000
        return datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
    return ''
