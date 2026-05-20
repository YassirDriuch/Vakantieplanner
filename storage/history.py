import json
import os

from config import GESCHIEDENIS_BESTAND


def print_geschiedenis():
    geschiedenis = laad_geschiedenis()

    print("\n----- GESCHIEDENISMENU -----")

    if not geschiedenis:
        print("Nog geen resultaten. Probeer eerst een stad/locatie op te zoeken!")

    for index, zoekterm in enumerate(geschiedenis, start=1):
        print(f"{index}. {zoekterm}")

def laad_geschiedenis():
    if not os.path.exists(GESCHIEDENIS_BESTAND):
        return []

    try:
        with open(GESCHIEDENIS_BESTAND, "r") as f:
            return json.load(f)
    except json.decoder.JSONDecodeError:
        return []

def save_geschiedenis(geschiedenis):
    with open(GESCHIEDENIS_BESTAND, "w") as f:
        json.dump(geschiedenis, f, indent=4)

def toevoegen_geschiedenis(zoekterm):
    zoekterm = zoekterm.strip()
    if zoekterm == "":
        return

    geschiedenis = laad_geschiedenis()

    geschiedenis.append(zoekterm)

    save_geschiedenis(geschiedenis)