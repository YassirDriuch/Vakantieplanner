import locale
from datetime import datetime
from tabulate import tabulate
from airports import airport_data
import requests

# Locale wordt gebruikt voor nummer format (om populatiegrootte duidelijker weer te geven)
locale.setlocale(locale.LC_ALL, "")
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
WEATHER_CODES = {
    0: "Helder",

    1: "Overwegend helder",
    2: "Gedeeltelijk bewolkt",
    3: "Bewolkt",

    45: "Mist",
    48: "Aanvriezende mist",

    51: "Lichte motregen",
    53: "Matige motregen",
    55: "Dichte motregen",
    56: "Lichte ijzelmotregen",
    57: "Dichte ijzelmotregen",

    61: "Lichte regen",
    63: "Matige regen",
    65: "Zware regen",
    66: "Lichte ijzelregen",
    67: "Zware ijzelregen",

    71: "Lichte sneeuwval",
    73: "Matige sneeuwval",
    75: "Zware sneeuwval",
    77: "Sneeuwkorrels",

    80: "Lichte regenbuien",
    81: "Matige regenbuien",
    82: "Hevige regenbuien",
    85: "Lichte sneeuwbuien",
    86: "Zware sneeuwbuien",

    95: "Onweer",
    96: "Onweer met lichte hagel",
    99: "Onweer met zware hagel",
}

def call_api(url, params):
    # Een API call functie om boilerplate te verminderen.
    # Deze functie doet een get request naar een url naar keuze, met de parameters die je wilt meegeven.
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"--- Er is iets misgegaan! ---\n{e}")
        return None

def zoek_bestemming(bestemming):
    # Deze functie stelt de nodige parameters op voor de Get request om de Geodata op te halen. Ik controleer hier ook of ik überhaupt resultaten heb teruggekregen.
    # Deze functie geeft een Json object terug of geeft niks terug. Indien niks wordt teruggeven, gaan we terug naar het hoofdmenu
    params = {
        "name": bestemming,
        "count": 1,
        "language": "nl"
    }

    data = call_api(GEOCODING_URL, params)

    if not data or "results" not in data:
        # Bij geen resultaten moeten we terug naar het hoofdmenu
        print("Geen locatie gevonden! Pas je zoekopdracht aan en probeer opnieuw.")
        return None

    # Geef alleen het resultaat terug
    return data["results"][0]


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
        row = [datetime.strptime(data["daily"]["time"][x], "%Y-%m-%d").strftime("%d-%m-%Y"), f"{data["daily"]["temperature_2m_max"][x]}\u00b0C", f"{data["daily"]["temperature_2m_min"][x]}\u00b0C",datetime.strptime(data["daily"]["sunrise"][x], "%Y-%m-%dT%H:%M").strftime("%H:%M"), datetime.strptime(data["daily"]["sunset"][x], "%Y-%m-%dT%H:%M").strftime("%H:%M"), WEATHER_CODES.get(data["daily"]["weather_code"][x], "Onbekende weercode")]
        table.append(row)

    headers = ["Datum", "Temperatuur (Max)", "Temperatuur (Min)", "Zonsopgang", "Zonsondergang", "Weercode"]
    print("\n" ,tabulate(table, headers=headers))


def zoek_vlucht():
    print("Zoek vlucht")


def locatie_menu():

    print("\n----- LOCATIE MENU -----\n")
    bestemming = input("Voer de stadsnaam in van je vakantiebestemming:").lower().strip()

    # Nadat gebruiker ons de bestemming geeft doen we een GET call naar Open Meteo Geocaching API om geolocatie op te halen.
    bestemming_data = zoek_bestemming(bestemming)
    if not bestemming_data:
        return None

    # Airports-py wordt hier gebruikt om de dichtsbijzijnde vliegveld te berekenen
    dichtbij_vliegveld = airport_data.find_nearby_airports(bestemming_data.get("latitude"), bestemming_data.get("longitude")).pop(0)

    print("\n----- BESTEMMINGSOVERZICHT -----")
    # Een lijst met waardes maken voor Tabulate. Elke lijst binnen onderstaande lijst kan je zien als een rij
    tabel_data = [["Stad", bestemming_data.get("name")],
            ["Land", bestemming_data.get("country")],
            ["Hoogte", f"{int(bestemming_data.get("elevation"))} meter"],
            ["Populatiegrootte", f"{bestemming_data.get("population"):n}"],
            ["Lat", bestemming_data.get("latitude")],
            ["Long", bestemming_data.get("longitude")],
            ["Dichtbijzijnste vliegveld", f"{dichtbij_vliegveld.get("airport")} ({dichtbij_vliegveld.get("iata")})"]]

    print(tabulate(tabel_data))

    while True:
        print("\nKeuzemenu")
        print("1. Weerinformatie")
        print("2. Vlucht zoeken")
        print("9. Terug naar het Hoofdmenu")
        print("0. Sluiten")
        try:
            keuze = int(input("Maak een keuze:"))
        except ValueError:
            print("\nOngeldige keuze. Probeer opnieuw.")
            continue

        match keuze:
            case 1:
                get_weer(bestemming_data)
            case 2:
                zoek_vlucht()
            case 9:
                break
            case 0:
                exit(0)



def print_geschiedenis():
    print("\n----- Geschiedenis MENU -----\n")

# Hoofdmenu
def hoofdmenu():
    while True:
        print("\n----- HOOFDMENU -----\n"
              "1. Nieuwe vakantiebestemming\n"
              "2. Geschiedenis\n"
              "0. Sluiten")

        # Try-except om situaties op te vangen waarbij gebruiker een String invoert in variabel, keuze, waardoor de applicatie breekt (keuze wordt een String, waardoor de Match-case altijd faalt bij een volgende poging)
        try:
            keuze = int(input("Maak een keuze:"))
        except ValueError:
            print("\nOngeldige keuze. Probeer opnieuw.")
            continue

        match keuze:
            case 1:
                locatie_menu()
            case 2:
                print_geschiedenis()
            case 0:
                break
            case _:
                print("\nOngeldige keuze. Probeer opnieuw.")

# Start de applicatie
hoofdmenu()