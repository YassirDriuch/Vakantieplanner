from tabulate import tabulate

from config import FLIGHTS_URL, FLIGHTS_API_KEY
from services.api_client import call_api

def haal_dataset(resultaat):
    if not resultaat:
        return None

    if resultaat.get("best_flights"):
        return resultaat["best_flights"]

    if resultaat.get("other_flights"):
        return resultaat["other_flights"]

    return None

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

    dataset = haal_dataset(resultaat)

    if not dataset:
        print("\nWe hebben helaas geen resultaten gevonden")
        return

    print(f"\nWe hebben {len(dataset)} vluchten gevonden voor jou.\n")

    for result in dataset:
        table = []
        headers = ["Vertrek", "Aankomst", "Vertrektijd", "Aankomsttijd", "Maatschappij"]
        if len(result["flights"]) > 1:
            for flight in result["flights"]:
                table.append([flight["departure_airport"]["name"], flight["arrival_airport"]["name"], flight["departure_airport"]["time"], flight["arrival_airport"]["time"], flight["airline"]])
        else:
            table.append([result["flights"][0]["departure_airport"]["name"], result["flights"][0]["arrival_airport"]["name"],
                          result["flights"][0]["departure_airport"]["time"], result["flights"][0]["arrival_airport"]["time"], result["flights"][0]["airline"]])



        if "departure_token" in result:

            print("===== Heenreis =====")
            print(tabulate(table, headers, tablefmt="fancy_grid"), "\n")
            duur_uren, duur_minuten = divmod(result['total_duration'], 60)
            print("Totale reistijd:", f"{duur_uren} uur en {duur_minuten} min" if duur_uren > 0 else f"{duur_minuten} min")

            table = []
            retour_param = params.copy()
            retour_param["departure_token"] = result["departure_token"]
            retour_result = haal_dataset(call_api(FLIGHTS_URL, params=retour_param))

            if len(retour_result[0]["flights"]) > 1:
                for flight in retour_result[0]["flights"]:
                    table.append([flight["departure_airport"]["name"], flight["arrival_airport"]["name"],
                                  flight["departure_airport"]["time"], flight["arrival_airport"]["time"],
                                  flight["airline"]])
            else:
                table.append(
                    [retour_result[0]["flights"][0]["departure_airport"]["name"], retour_result[0]["flights"][0]["arrival_airport"]["name"],
                     retour_result[0]["flights"][0]["departure_airport"]["time"], retour_result[0]["flights"][0]["arrival_airport"]["time"],
                     retour_result[0]["flights"][0]["airline"]])
            print("\n===== Terugreis =====")
            print(tabulate(table, headers, tablefmt="fancy_grid"), f"€{retour_result[0]['price']}\n")

            duur_uren, duur_minuten = divmod(retour_result[0]['total_duration'], 60)
            print("Totale reistijd:", f"{duur_uren} uur en {duur_minuten} min" if duur_uren > 0 else f"{duur_minuten} min")
        else:
            print("\n===== Heenreis =====")
            print(tabulate(table, headers, tablefmt="fancy_grid"), f"€{result['price']}\n")
            duur_uren, duur_minuten = divmod(result['total_duration'], 60)
            print("Totale reistijd:", f"{duur_uren} uur en {duur_minuten} min" if duur_uren > 0 else f"{duur_minuten} min")

    print(f"\nGoogle Vluchten: {resultaat["search_metadata"]["google_flights_url"]}")

