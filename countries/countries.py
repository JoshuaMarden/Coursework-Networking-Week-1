import json
import requests
import pprint


class APIError(Exception):
    """Describes an error triggered by a failing API call."""

    def __init__(self, message: str, code: int):
        """Creates a new APIError instance."""
        self.message = message
        self.code = code

    def print_error(self):
        print(f"{str(self.code)}: {self.message}")


def fetch_data(country_name: str) -> dict:
    """Returns a dict of country data from the API."""
    country_name = country_name.lower()
    response = requests.get(
        f"https://restcountries.com/v3.1/name/{country_name}/", timeout=60)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise APIError("Unable to locate matching country.", 404)
    elif response.status_code == 500:
        raise APIError("Unable to connect to server.", 500)

    json_data = response.json()
    return json_data


def print_data(country_data: dict):
    """Displays country data from a dict."""
    flag = {country_data[0]["flag"]}

    print(
        f"-----------------------{flag}-----------------------")
    print("Name: "
          f"{country_data[0]["name"]["common"]} "
          "(Native Name: "
          f"{country_data[0]["name"]["nativeName"]})")
    print(f"Capital: {country_data[0]["capital"][0]}")
    print()
    pprint.pprint(f"Currencies: {country_data[0]["currencies"]}")
    pprint.pprint(f"Languages:  {country_data[0]["languages"]}")
    print(
        f"-----------------------{flag}-----------------------")


def main():
    """Repeatedly prompts the user for country names and displays the result."""
    print(" ")
    print("####################")
    print("Welcome to the REST Countries Searcher")
    print("####################")
    print(" ")

    while 1:
        entry = input("Search for a country: ")
        print(f"You searched for: {entry}")
        print("Fetching...")
        print(" ")
        try:
            country_data = fetch_data(entry)
            print_data(country_data)
        except APIError as e:
            print(e.message)
        print(" ")


if __name__ == "__main__":

    main()
