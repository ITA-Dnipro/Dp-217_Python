import os
import requests
from requests.exceptions import ConnectionError
from django.core.cache import cache


def get_universities_api(region: str, city: str, field: str, speciality: str) -> list:
    base_url = os.environ.get("UNI_PARSE_URL")
    url = os.path.join(base_url, 'univerdata/')
    print(url)
    # url = "http://127.0.0.1:8080/
    params = {
        'region': region,
        'city': city,
        'field': field,
        'speciality': speciality
    }
    try:
        if cache.get(params):
            response = cache.get(params)
        else:
            response = requests.get(url, params=params)
            cache.set(params, response)
        if response.status_code == 200:
            return response.json()
        else:
            return [{"error": response.status_code}]
    except ConnectionError:
        return [{"error": "connection error"}]


def get_universities(univers_ids):
    base_url = os.environ.get("UNI_PARSE_URL")
    url = os.path.join(base_url, 'favs/')
    params = {'univers': univers_ids}

    response = requests.post(url, json=params)
    return response.json()
