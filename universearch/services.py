import os
import requests
from requests.exceptions import ConnectionError


def get_universities_api(region: str, city: str, field: str, speciality: str) -> list:
    url = os.environ.get("UNI_PARSE_URL")
    # url = "http://127.0.0.1:8080/univerdata/"

    params = {
        'region': region,
        'city': city,
        'field': field,
        'speciality': speciality
    }
    try:
        responce = requests.get(url, params=params)

        if responce.status_code == 200:
            return responce.json()
        else:
            return [{"error": responce.status_code}]
    except ConnectionError:
        return [{"error": "connection error"}]
