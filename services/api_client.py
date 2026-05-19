import requests


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