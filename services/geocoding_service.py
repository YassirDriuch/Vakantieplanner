from config import GEOCODING_URL
from services.api_client import call_api


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