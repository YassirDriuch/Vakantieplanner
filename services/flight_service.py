from tabulate import tabulate

from config import FLIGHTS_URL, FLIGHTS_API_KEY
from services.api_client import call_api


def zoek_vluchten(data):
    params = {
        "engine": "google_flights",
        "currency": "EUR",
        "departure_id": data["vertrek_id"],
        "arrival_id": data["aankomst_id"],
        "type": data["retour"],
        "outbound_date": data["vertrek_datum"],
        "api_key": FLIGHTS_API_KEY,
        "hl": "nl",
        "gl": "nl"
    }
    if data["retour"] == 1:
        params["return_date"] = data["retour_datum"]

    resultaat = call_api(FLIGHTS_URL, params)

    if not resultaat or "error" in resultaat:
        print(f"Er is iets misgegaan.\n{data["aankomst_id"]}")


    print(f"\nHier heb je de {len(resultaat['best_flights'])} beste vluchten voor jou.")
    for result in resultaat["best_flights"]:
        table = []
        headers = ["Vertrek", "Aankomst", "Vertrektijd", "Aankomsttijd", "Maatschappij"]
        if len(result["flights"]) > 1:
            for flight in result["flights"]:
                table.append([flight["departure_airport"]["name"], flight["arrival_airport"]["name"], flight["departure_airport"]["time"], flight["arrival_airport"]["time"], flight["airline"]])
        else:
            table.append([result["flights"][0]["departure_airport"]["name"], result["flights"][0]["arrival_airport"]["name"],
                          result["flights"][0]["departure_airport"]["time"], result["flights"][0]["arrival_airport"]["time"], result["flights"][0]["airline"]])

        print(tabulate(table, headers, tablefmt="fancy_grid"), f"€{result['price']}")
