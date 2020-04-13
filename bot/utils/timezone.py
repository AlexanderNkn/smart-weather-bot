import requests
import datetime

from bot.config import TIMEZONEDB_TOKEN


def get_timezone_by_coords(longitude, latitude):
    url = "https://api.timezonedb.com/v2.1/get-time-zone"
    params = {
        "key": TIMEZONEDB_TOKEN,
        "format": "json",
        "fields": "gmtOffset,zoneName",
        "by": "position",
        "lat": latitude,
        "lng": longitude
    }
    try:
        response = requests.get(url, params=params)
        return response.json()
    except requests.RequestException:
        return


def parse_timezone(timezone):
    return datetime.timezone(datetime.timedelta(seconds=timezone.get('gmtOffset'))), timezone.get('zoneName')
