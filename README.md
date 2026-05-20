# Vakantieplanner

A command-line holiday planner written in Python. You look up a destination, see an overview of
the city including the nearest airport, and then check the weather forecast or search for flights.
Every destination you look up is saved to a history file.

The application interface is in Dutch.

> Documentation is available in [English](#english) and [Nederlands](#nederlands).

---

## English

### Features

* Look up a destination by city name and get an overview with country, elevation, population,
  coordinates and the nearest airport.
* View a 7-day weather forecast with maximum and minimum temperature, sunrise, sunset and a
  description of the weather in Dutch.
* Search for one-way or return flights between your departure location and your destination,
  with prices in euros, travel times and a link to Google Flights.
* Keep a history of every destination you have looked up.

### Project structure

```
Vakantieplanner/
├── main.py                    # Entry point of the application
├── config.py                  # Configuration: API URLs, key and weather codes
├── requirements.txt           # Python dependencies
├── .env.example               # Example of the .env file
├── services/
│   ├── api_client.py          # Generic wrapper around HTTP GET requests
│   ├── geocoding_service.py   # City to geolocation (Open-Meteo Geocoding)
│   ├── weather_service.py     # 7-day weather forecast (Open-Meteo Forecast)
│   └── flight_service.py      # Flight search (SerpAPI / Google Flights)
├── storage/
│   └── history.py             # Loading and saving the search history
└── ui/
    └── menu.py                # Menu structure and user interaction
```

### Requirements

* Python 3.12 or higher. The code uses `match`/`case` and nested quotes inside f-strings.
* A SerpAPI key for searching flights. You can create a free key at
  [serpapi.com](https://serpapi.com/). The application will not start without a valid key.
* The weather and geocoding features use the free APIs from
  [Open-Meteo](https://open-meteo.com/) and do not need a key.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/YassirDriuch/Vakantieplanner.git
   cd Vakantieplanner
   ```

2. (Recommended) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The packages used are:

   | Package         | Purpose                                          |
   | --------------- | ------------------------------------------------ |
   | `requests`      | HTTP requests to the external APIs               |
   | `tabulate`      | Clean tables in the terminal                     |
   | `airports-py`   | Finding the nearest airport                      |
   | `python-dotenv` | Loading the API key from the `.env` file         |

### Configuration

The application reads your SerpAPI key from a `.env` file so it stays out of the code. Create the
file based on the included example:

```bash
cp .env.example .env
```

Open `.env` and fill in your own key:

```
FLIGHTS_API_KEY=your_serpapi_key_here
```

### Usage

Run the application from the project root:

```bash
python main.py
```

You will see the main menu:

```
----- HOOFDMENU -----
1. Nieuwe vakantiebestemming
2. Geschiedenis
0. Sluiten
```

* Option 1 (Nieuwe vakantiebestemming): enter a city name. After the destination overview you get
  a sub-menu to view the weather, search for flights, go back, or exit.
* Option 2 (Geschiedenis): show all destinations you have looked up before.
* Option 0 (Sluiten): close the application.

Dates are entered in the format `dd-mm-yyyy`.

### APIs used

| API                       | Purpose                            | Authentication needed |
| ------------------------- | ---------------------------------- |-----------------------|
| Open-Meteo Geocoding API  | Convert a city name to geolocation | No                    |
| Open-Meteo Forecast API   | 7-day weather forecast             | No                    |
| SerpAPI (Google Flights)  | Flight search                      | Yes                   |

---

## Nederlands

Een command-line vakantieplanner geschreven in Python. Je zoekt een bestemming op, ziet een
overzicht van de stad inclusief het dichtstbijzijnde vliegveld, en kunt vervolgens de
weersverwachting bekijken of vluchten zoeken. Elke bestemming die je opzoekt wordt bewaard in een
geschiedenisbestand.

### Functionaliteiten

* Zoek een bestemming op stadsnaam en krijg een overzicht met land, hoogte, populatiegrootte,
  coördinaten en het dichtstbijzijnde vliegveld.
* Bekijk een 7-daagse weersverwachting met maximum- en minimumtemperatuur, zonsopgang,
  zonsondergang en een omschrijving van het weer in het Nederlands.
* Zoek enkele reis- of retourvluchten tussen je vertreklocatie en je bestemming, met prijzen in
  euro's, reistijden en een link naar Google Flights.
* Houd een geschiedenis bij van elke bestemming die je hebt opgezocht.

### Projectstructuur

```
Vakantieplanner/
├── main.py                    # Startpunt van de applicatie
├── config.py                  # Configuratie: API-URL's, sleutel en weercodes
├── requirements.txt           # Python-afhankelijkheden
├── .env.example               # Voorbeeld van het .env-bestand
├── services/
│   ├── api_client.py          # Generieke wrapper rond HTTP GET-requests
│   ├── geocoding_service.py   # Stad naar geolocatie (Open-Meteo Geocoding)
│   ├── weather_service.py     # 7-daagse weersverwachting (Open-Meteo Forecast)
│   └── flight_service.py      # Vluchten zoeken (SerpAPI / Google Flights)
├── storage/
│   └── history.py             # Inladen en opslaan van de zoekgeschiedenis
└── ui/
    └── menu.py                # Menustructuur en gebruikersinteractie
```

### Vereisten

* Python 3.12 of hoger. De code gebruikt `match`/`case` en geneste quotes in f-strings.
* Een SerpAPI-sleutel om vluchten te zoeken. Je kunt gratis een sleutel aanmaken op
  [serpapi.com](https://serpapi.com/). Zonder geldige sleutel start de applicatie niet.
* De weer- en geocoding-functionaliteit gebruikt de gratis API's van
  [Open-Meteo](https://open-meteo.com/) en heeft geen sleutel nodig.

### Installatie

1. Clone de repository:

   ```bash
   git clone https://github.com/YassirDriuch/Vakantieplanner.git
   cd Vakantieplanner
   ```

2. (Aanbevolen) Maak een virtuele omgeving aan en activeer deze:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Op Windows: venv\Scripts\activate
   ```

3. Installeer de afhankelijkheden:

   ```bash
   pip install -r requirements.txt
   ```

   De gebruikte packages zijn:

   | Package         | Doel                                              |
   | --------------- | ------------------------------------------------- |
   | `requests`      | HTTP-requests naar de externe API's               |
   | `tabulate`      | Nette tabellen in de terminal                     |
   | `airports-py`   | Het dichtstbijzijnde vliegveld berekenen          |
   | `python-dotenv` | Inladen van de API-sleutel uit het `.env`-bestand |

### Configuratie

De applicatie leest je SerpAPI-sleutel uit een `.env`-bestand, zodat deze niet in de code
terechtkomt. Maak het bestand aan op basis van het meegeleverde voorbeeld:

```bash
cp .env.example .env
```

Open `.env` en vul je eigen sleutel in:

```
FLIGHTS_API_KEY=jouw_serpapi_sleutel_hier
```

### Gebruik

Start de applicatie vanuit de hoofdmap:

```bash
python main.py
```

Je krijgt het hoofdmenu te zien:

```
----- HOOFDMENU -----
1. Nieuwe vakantiebestemming
2. Geschiedenis
0. Sluiten
```

* Optie 1 (Nieuwe vakantiebestemming): voer een stadsnaam in. Na het bestemmingsoverzicht krijg je
  een keuzemenu om het weer te bekijken, vluchten te zoeken, terug te gaan of af te sluiten.
* Optie 2 (Geschiedenis): toon alle bestemmingen die je eerder hebt opgezocht.
* Optie 0 (Sluiten): sluit de applicatie af.

Data worden ingevoerd in het formaat `dd-mm-yyyy`.

### Gebruikte API's

| API                       | Doel                                | Authenticatie nodig |
| ------------------------- | ----------------------------------- |---------------------|
| Open-Meteo Geocoding API  | Stadsnaam omzetten naar geolocatie  | Nee                 |
| Open-Meteo Forecast API   | 7-daagse weersverwachting           | Nee                 |
| SerpAPI (Google Flights)  | Vluchten zoeken                     | Ja                  |
