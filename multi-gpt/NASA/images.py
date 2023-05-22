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

    def generate(self, date: str = None, start_date: str = None, end_date: str = None):
        if start_date is None and end_date or end_date is None and start_date:
            raise ValueError(
                "You must provide both the start_date and end_date but you only provided one of them. Either leave "
                "both blank, provide both dates, or provide a date value.")
