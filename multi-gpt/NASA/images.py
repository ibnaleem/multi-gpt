import datetime, json, requests

class APOD:
    def __init__(self, api_key):
        if not api_key:
            raise ValueError("api_key is required. Please obtain one from https://api.nasa.gov/")
        self.api_key = api_key
