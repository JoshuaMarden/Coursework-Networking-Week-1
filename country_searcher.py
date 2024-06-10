
import json
import requests
import pprint


def get_country_data_by_name():

    user_input = input("Please input the name of a country -> ")
    user_input = user_input.lower()

    response = requests.get(
        f"https://restcountries.com/v3.1/name/{user_input}/")

    json_data = response.json()
    return json_data


if __name__ == "__main__":

    json_data = get_country_data_by_name()
    pprint.pprint(json_data)
