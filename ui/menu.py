from airports import airport_data
from tabulate import tabulate

from services.flight_service import zoek_vlucht
from services.geocoding_service import zoek_bestemming
from services.weather_service import get_weer
from storage.history import print_geschiedenis


def vraag_bestemming():

    print("\n----- LOCATIE MENU -----")
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
                vraag_bestemming()
            case 2:
                print_geschiedenis()
            case 0:
                break
            case _:
                print("\nOngeldige keuze. Probeer opnieuw.")