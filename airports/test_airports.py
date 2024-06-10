import pytest
from airports import *
import requests_mock


def test_404_airport_not_found(requests_mock):
    # Use the exact URL that will be generated in the function
    spoof_iata = "§§§"
    url = f"https://airlabs.co/api/v9/schedules?dep_iata={
        spoof_iata}&api_key={AIRLABS_API_KEY}"

    requests_mock.get(url, status_code=404)

    with pytest.raises(APIError) as exception:
        get_flights_from_airport(spoof_iata)

    assert exception.value.message == "Airport not recognised"
    assert exception.value.code == 404


def test_500_air_labs_not_responding(requests_mock):
    # Use the exact URL that will be generated in the function
    spoof_iata = "§§§"
    url = f"https://airlabs.co/api/v9/schedules?dep_iata={
        spoof_iata}&api_key={AIRLABS_API_KEY}"

    requests_mock.get(url, status_code=500)

    with pytest.raises(APIError) as exception:
        get_flights_from_airport(spoof_iata)

    assert exception.value.message == "Airlabs server not responding"
    assert exception.value.code == 500


def test_air_labs_misc_error(requests_mock):
    # Use the exact URL that will be generated in the function

    api_error_response = {'error': {'message': 'Unknown api_key', 'code': 'unknown_api_key'},
                          'terms': "Unauthorized access is prohibited and punishable by law. \nReselling data 'As Is' without AirLabs.Co permission is strictly prohibited. \nFull terms on https://airlabs.co/. \nContact us info@airlabs.co"}

    spoof_iata = "§§§"
    url = f"https://airlabs.co/api/v9/schedules?dep_iata={
        spoof_iata}&api_key={AIRLABS_API_KEY}"

    requests_mock.get(url, status_code=200, json=api_error_response)

    with pytest.raises(APIError) as exception:
        get_flights_from_airport(spoof_iata)

    assert "API returned an error" in str(exception.value)
