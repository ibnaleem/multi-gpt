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
            
        if date and start_date and end_date:
            raise ValueError("Too many arguments. Either provide a single date, or provide a start_date and end_date.")

        if date is not None and not is_valid_date(date):
            raise ValueError(f"{date} is not a valid date. Date must be in the format YYYY-MM-DD.")
        if start_date is not None and not is_valid_date(start_date):
            raise ValueError(f"{start_date} is not a valid date. Date must be in the format YYYY-MM-DD.")
        if end_date is not None and not is_valid_date(end_date):
            raise ValueError(f"{end_date} is not a valid date. Date must be in the format YYYY-MM-DD.")
            
        if start_date is not None and end_date is not None:

            url = f"https://api.nasa.gov/planetary/apod?start_date={start_date}&end_date={end_date}&api_key={self.api_key}"

            response = requests.get(url=url)

            if response.status_code == 400:
                print("Your API_KEY is invalid. Obtain a new one from https://api.nasa.gov/")
                raise response.raise_for_status()

            elif response.status_code == 500:
                print("Looks like NASA's API is down. Please try again later.")
                raise response.raise_for_status

            data = json.loads(response.text)

            return data[0]["hdurl"]
        
        elif date is not None:

            url = f"https://api.nasa.gov/planetary/apod?date={date}&api_key={self.api_key}"

            response = requests.get(url=url)

            if response.status_code == 400:
                print("Your api_key is invalid. Obtain a new one from https://api.nasa.gov/")
                raise response.raise_for_status()

            elif response.status_code == 500:
                print("Looks like NASA's API is down. Please try again later.")
                raise response.raise_for_status

            data = json.loads(response.text)
            return data["hdurl"]
        
        else:
            url = f"https://api.nasa.gov/planetary/apod?api_key={self.api_key}"

            response = requests.get(url=url)

            if response.status_code == 400:
                print("Your api_key is invalid. Obtain a new one from https://api.nasa.gov/")
                raise response.raise_for_status()

            elif response.status_code == 500:
                print("Looks like NASA's API is down. Please try again later.")
                raise response.raise_for_status

            data = json.loads(response.text)
            return data["hdurl"]
