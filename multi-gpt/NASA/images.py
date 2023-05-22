import datetime, json, requests

def is_valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

class APOD:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("api_key is required. Please obtain one from https://api.nasa.gov/")
        self.api_key = api_key
