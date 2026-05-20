from datetime import datetime

from airports import airport_data
from tabulate import tabulate

from services.flight_service import zoek_vluchten
from services.geocoding_service import zoek_bestemming
from services.weather_service import get_weer
from storage.history import print_geschiedenis, toevoegen_geschiedenis


def zoek_vluchten_menu(bestemming_id):
    data = {}
    while True:
        oorsprong_locatie = input("\nWaar vlieg je vandaan?\n")
        # Nadat gebruiker ons de bestemming geeft doen we een GET call naar Open Meteo Geocaching API om geolocatie op te halen.
        oorsprong_data = zoek_bestemming(oorsprong_locatie)
        if not oorsprong_data:
            continue
        break
    while True:
        try:
            retour = int(input("\nWil je een retourvlucht of enkel?\n1. Retour\n2. Enkel\n"))

            match retour:
                case 1 | 2:
                    break
                case _:
                    print("\nOngeldige keuze. Kies 1 of 2.")

        except ValueError:
            print("\nOngeldige keuze. Probeer opnieuw.")

    while True:
        try:
            vertrek_datum = datetime.strptime(input("\nWanneer wil je vertrekken? (dd-mm-yyyy)\n"), "%d-%m-%Y")
            if vertrek_datum.date() < datetime.today().date():
                print("\nOngeldige keuze. Datum ligt in het verleden!")
                continue
            if retour == 1:
                terug_datum = datetime.strptime(input("\nWanneer wil je terugkomen? (dd-mm-yyyy)\n"), "%d-%m-%Y")
                if terug_datum.date() >= datetime.today().date() and terug_datum > vertrek_datum:
                    data["retour_datum"]= terug_datum.strftime("%Y-%m-%d")
                else:
                    print("Ongeldige keuze. Datum ligt in het verleden of is vóór/op de vertrekdatum!")
                    continue
            break
        except ValueError:
            print("Ongeldig keuze. Typ de datum exact als dd-mm-yyyy (bijv. 25-05-2026).")


    if not oorsprong_data:
        return None

    # Airports-py wordt hier gebruikt om de dichtsbijzijnde vliegveld te berekenen
    oorsprong_id = airport_data.find_nearest_airport(oorsprong_data.get("latitude"),
                                                           oorsprong_data.get("longitude"), {
                                                         'has_scheduled_service': True,
                                                         'min_runway_ft': 100,
                                                         'country_code': oorsprong_data.get("country_code")
                                                     }).get("iata")

    data.update({
        "vertrek_id": oorsprong_id,
        "aankomst_id": bestemming_id,
        "vertrek_datum": vertrek_datum.strftime("%Y-%m-%d"),
        "retour": retour
    })

    zoek_vluchten(data)

def vraag_bestemming():

    while True:
        print("\n----- LOCATIE MENU -----")
        bestemming = input("Voer de stadsnaam in van je vakantiebestemming:\n").strip()

        # Nadat gebruiker ons de bestemming geeft doen we een GET call naar Open Meteo Geocaching API om geolocatie op te halen.
        bestemming_data = zoek_bestemming(bestemming)
        if not bestemming_data:
            continue
        break

    toevoegen_geschiedenis(f"{bestemming_data.get('name')}, {bestemming_data.get('country')}")

    if not bestemming_data:
        return None

    # Airports-py wordt hier gebruikt om de dichtsbijzijnde vliegveld te berekenen
    dichtbij_vliegveld = airport_data.find_nearest_airport(bestemming_data.get("latitude"),
                                                           bestemming_data.get("longitude"), {
                                                        'has_scheduled_service': True,
                                                        'min_runway_ft': 100,
                                                        'country_code': bestemming_data.get("country_code")
                                                     })
    print("\n----- BESTEMMINGSOVERZICHT -----")
    # Een lijst met waardes maken voor Tabulate. Elke lijst binnen onderstaande lijst kan je zien als een rij
    tabel_data = [["Stad", bestemming_data.get("name")],
            ["Land", bestemming_data.get("country")],
            ["Hoogte", f"{int(bestemming_data.get("elevation"))} meter"],
            ["Populatiegrootte", f"{bestemming_data.get("population"):n}"],
            ["Lat", bestemming_data.get("latitude")],
            ["Long", bestemming_data.get("longitude")],
            ["Dichtbijzijnste vliegveld", f"{dichtbij_vliegveld.get("airport")} ({dichtbij_vliegveld.get("iata")})"]]

    print(tabulate(tabel_data, tablefmt="fancy_grid"))

    while True:
        print("\nKeuzemenu")
        print("1. Weerinformatie")
        print("2. Vlucht zoeken")
        print("9. Sluiten")
        print("0. Terug naar het Hoofdmenu")
        try:
            keuze = int(input("Maak een keuze:"))
        except ValueError:
            print("\nOngeldige keuze. Probeer opnieuw.")
            continue

        match keuze:
            case 1:
                get_weer(bestemming_data)
            case 2:
                zoek_vluchten_menu(dichtbij_vliegveld.get("iata"))
            case 9:
                exit(0)
            case 0:
                break


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