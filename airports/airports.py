import requests
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
import argparse
import json
from thefuzz import fuzz
from errors import *
import datetime

AIRLABS_API_KEY = "f7315410-8148-4f2a-a599-6868f3741983"
WEATHER_API_KEY = "f3b1006be0774e9ebd1141815243005"


def load_airport_JSON() -> list:
    """Load airport data from airports.json"""
    with open("airports.json", "r") as file:
        data = json.load(file)
        file.close
    return data


def find_airport_from_name(name: str, airport_data: list) -> str:
    """
    Find an airport from the airportData given a name
    Could return one or more airport objects
    """
    similar_airport_names = []
    name_match_threshold = 90

    for airport in airport_data:

        if airport.get("name") and\
                fuzz.partial_token_sort_ratio(name.lower(), airport["name"].lower()) > name_match_threshold:
            similar_airport_names.append(f"{
                airport['name']}, ({airport['iata']})")

        elif len(name) == 3 and\
                fuzz.partial_token_sort_ratio(name.lower(), airport["iata"].lower()) > 90:
            similar_airport_names.append(f"{
                airport['name']}, ({airport['iata']})")

    if len(similar_airport_names) == 0:
        raise InputError(f"Input '{name}', cannot be matched to an airport.")

    if len(similar_airport_names) == 1:
        response = Prompt.ask(
            f"Did you mean {similar_airport_names[0]}", choices=["Y", "n"], default="Y")

        if response.lower() == "y":
            return similar_airport_names[0]
        else:
            raise InputError(
                f"Input '{name}', cannot be matched to an airport.")

    if len(similar_airport_names) > 1:

        similar_airport_names.insert(0, "None of the below")
        choices_dict = {}

        for index, option in enumerate(similar_airport_names):
            option_number = len(similar_airport_names) - index
            choices_dict[str(option_number)] = option

        choices_display = "\n".join(
            [f"{key}: {description}" for key, description in choices_dict.items()])

        response = Prompt.ask(
            f"{choices_display}\n\nChose a number from the above options ^\n\nYour choices:",
            choices=list(choices_dict.keys())[::-1],
            default="1"
        )

        return choices_dict[response]


def return_airport_iata_from_name(name_with_iata: str) -> str:

    first_bracket_index = name_with_iata.find("(")
    iata = name_with_iata[first_bracket_index + 1: first_bracket_index + 4]

    return iata


def find_airport_lat_lon_from_iata(iata: str, airport_data: list) -> tuple:
    """
    """
    lat = lon = "N/A"

    for airport in airport_data:
        if airport.get("iata") == iata:

            lat = airport.get("lat", "N/A")
            lon = airport.get("lon", "N/A")

            if lat == "N/A" or lon == "N/A":
                lat = lon = "N/A"

            break

    return lat, lon


def load_weather_for_location(lat: str, lon: str) -> dict:
    """Given a location, load the current weather for that location"""

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return "N/A"

    url = f"http://api.weatherapi.com/v1/current.json?key={
        WEATHER_API_KEY}&q={lat},{lon}"

    response = requests.get(url)
    if response.status_code == 200:
        body = response.json()

    return body


def turn_weather_stats_into_text(weather_data: dict) -> str:

    if weather_data == "N/A":
        return "N/A"

    wind_speed_categories = {
        (0, 4): "Calm",
        (4, 13): "Light Breeze",
        (13, 19): "Moderate Breeze",
        (19, 25): "Strong Breeze",
        (25, 39): "Gale",
        (39, 47): "Strong Gale",
        (47, 55): "Storm",
        (55, 64): "Violent Storm",
        (64, float('inf')): "Hurricane"
    }

    condition_text = weather_data["current"]["condition"]["text"].title()
    temp_c = weather_data["current"]["temp_c"]
    wind_mph = weather_data["current"]["wind_mph"]
    wind_dir = weather_data["current"]["wind_dir"]

    for (low, high), category in wind_speed_categories.items():
        if low <= wind_mph < high:
            wind_text = category
            break

    full_description = f"{condition_text}, {
        temp_c}C, {wind_text} ({wind_dir}) "

    return full_description


def get_flights_from_airport(name_with_iata: str) -> dict:

    iata = return_airport_iata_from_name(name_with_iata)

    url = f"https://airlabs.co/api/v9/schedules?dep_iata={
        iata}&api_key={AIRLABS_API_KEY}"
    response = requests.get(url)

    if response.status_code == 404:
        raise APIError("Airport not recognised", 404)
    if response.status_code == 500:
        raise APIError("Airlabs server not responding", 500)

    error_info = response.json().get("error")
    if error_info:
        error_code = error_info.get("code")
        raise APIError(f"API returned an error: (Code:", error_code)

    flights_data = response.json()
    flights_data = flights_data["response"]

    return flights_data


def add_arrival_weather_to_flight(flight_data: dict, airport_data: dict) -> None:

    airport_iata = flight_data["arr_iata"]
    lat_lon = find_airport_lat_lon_from_iata(airport_iata, airport_data)
    weather_data = load_weather_for_location(lat_lon[0], lat_lon[1])
    weather_string = turn_weather_stats_into_text(weather_data)

    flight_data["weather_str"] = weather_string


def render_flights(flights_data: list) -> None:
    """Render a list of flights to the console using the Rich Library"""
    custom_theme = Theme({
        "flight_number": "cyan",
        "destination": "magenta",
        "delayed": "green",
        "airline": "blue",
        "arrival": "yellow",
        "departure": "yellow",
        "duration": "red",
        "status": "white",
        "weather": "bright_blue",
    })

    console = Console(theme=custom_theme, record=True)
    flight_table = Table(title="Flight Information")

    flight_table.add_column(
        "Flight Number (iata)", justify="center",
        style="flight_number", max_width=9)
    flight_table.add_column("Airline", justify="center", style="airline")
    flight_table.add_column("Status", justify="center", style="status")
    flight_table.add_column(
        "Delayed (Y/N)", justify="center", style="delayed", max_width=7)
    flight_table.add_column(
        "Destination", justify="center", style="destination")
    flight_table.add_column("Estimated Departure",
                            justify="center", style="departure", max_width=10)
    flight_table.add_column(
        "Actual Departure", justify="center", style="departure", max_width=10)
    flight_table.add_column("Estimated Arrival",
                            justify="center", style="arrival", max_width=10)
    flight_table.add_column(
        "Original Arrival", justify="center", style="arrival", max_width=10)
    flight_table.add_column(
        "Duration (min)", justify="center", style="duration", max_width=8)
    flight_table.add_column("Weather at Destination",
                            justify='center', style="weather")

    for flight in flights_data:
        flight_iata = flight.get('flight_number', 'N/A')
        airline = flight.get('airline_iata', 'N/A')
        status = flight.get('status', 'N/A')
        delayed = 'Y' if flight.get('arr_delayed') else 'N'
        destination = flight.get('arr_iata', 'N/A')
        est_departure = flight.get('dep_estimated', 'N/A')
        actual_departure = flight.get('dep_actual', 'N/A')
        est_arrival = flight.get('arr_estimated', 'N/A')
        orig_arrival = flight.get('arr_time', 'N/A')
        duration = str(flight.get('duration', 'N/A'))
        weather = flight.get('weather_str', 'N/A')

        flight_table.add_row(
            flight_iata, airline, status, delayed, destination, est_departure,
            actual_departure, est_arrival, orig_arrival, duration, weather
        )

    console.print(flight_table)
    return console


def get_airport_and_export_format() -> tuple:
    """Get the airport and export format from the CLI"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--airport", required=True,
                        help="Name or IATA code of the airport")
    parser.add_argument("--export", required=False,
                        help="Export as `JSON` or `HTML`")
    args = parser.parse_args()
    return args.airport, args.export


def save_table_as_html(console: Console) -> None:
    """Save the rendered flights table as an HTML file using the recorded Console."""
    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"./airport_flight_data_{time}.html"
    console.save_html(filename)
    print(f"Table saved as {filename}")


def save_flights_as_json(flights_data: list) -> None:
    """Save the flights data to a JSON file."""
    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"./airport_flights_data_{time}.json"

    with open(filename, 'w') as json_file:
        json.dump(flights_data, json_file, indent=4)

    print(f"Table saved as {filename}")


def save_data(export_format: str, console: Console,
              flights_data: dict) -> None:
    "Saves data given the user's requested format"

    if export_format == None:
        print("No export command given - data not saved")

    elif export_format.lower() == "html":
        save_table_as_html(console)

    elif export_format.lower() == "json":
        save_flights_as_json(flights_data)

    else:
        print(f"Requested save format '{export_format}' not recognised!")
        save_flights_as_json(flights_data)
        save_table_as_html(console)


if __name__ == "__main__":
    airport_data = load_airport_JSON()
    airport_to_search, export_format = get_airport_and_export_format()
    airport = find_airport_from_name(airport_to_search, airport_data)
    airport_iata = return_airport_iata_from_name(airport)

    flights_data = get_flights_from_airport(airport)

    for flight in flights_data:
        add_arrival_weather_to_flight(flight, airport_data)

    console = render_flights(flights_data)

    save_data(export_format, console, flights_data)
