import os
import requests
from requests.exceptions import ConnectionError
from django.core.cache import cache
from .models import Region, StudyField, City, Speciality

DATABASES = {
    'region': Region,
    'city': City,
    'field': StudyField,
    'speciality': Speciality,
}


def params_translation(params):
    translated_params = {DATABASES[key].objects.filter(name=value).first().name_uk for key, value in params.items() if
                         DATABASES.get(key)}
    return translated_params


def get_universities_api(region: str, city: str, field: str, speciality: str) -> list:
    base_url = os.environ.get("UNI_PARSE_URL")
    url = os.path.join(base_url, 'univerdata/')
    # url = "http://127.0.0.1:8080/
    params = params_translation({
        'region': region,
        'city': city,
        'field': field,
        'speciality': speciality
    })
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
    try:
        base_url = os.environ.get("UNI_PARSE_URL")
        url = os.path.join(base_url, 'favs/')
        params = {'univers': univers_ids}

        response = requests.post(url, json=params)
        return response.json()
    except Exception:
        return
