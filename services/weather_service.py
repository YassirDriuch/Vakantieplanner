from datetime import datetime

from tabulate import tabulate

from config import FORECAST_URL, WEATHER_CODES
from services.api_client import call_api


def get_weer(bestemming_data):
    params = {
        "latitude": bestemming_data.get("latitude"),
        "longitude": bestemming_data.get("longitude"),
        "daily": "temperature_2m_max,temperature_2m_min,sunrise,sunset,weather_code",
        "timezone": "auto"
    }

    data = call_api(FORECAST_URL, params)

    if not data or "error" in data:
        print("Er is iets misgegaan.")
        return None

    table = []

    for x in range(7):
        dag = [datetime.strptime(data["daily"]["time"][x], "%Y-%m-%d").strftime("%d-%m-%Y"), f"{data['daily']['temperature_2m_max'][x]}\u00b0C", f"{data['daily']['temperature_2m_min'][x]}\u00b0C",datetime.strptime(data["daily"]["sunrise"][x], "%Y-%m-%dT%H:%M").strftime("%H:%M"), datetime.strptime(data["daily"]["sunset"][x], "%Y-%m-%dT%H:%M").strftime("%H:%M"), WEATHER_CODES.get(data["daily"]["weather_code"][x], "Onbekende weercode")]
        table.append(dag)

    headers = ["Datum", "Temperatuur (Max)", "Temperatuur (Min)", "Zonsopgang", "Zonsondergang", "Weercode"]
    print("\n" ,tabulate(table, headers=headers))