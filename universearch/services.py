import os
import requests
from requests.exceptions import ConnectionError
from django.core.cache import cache
from .models import Region, StudyField, City, Speciality

BASE_URL = os.environ.get("UNI_PARSE_URL")
DATABASES = {
    'region': Region,
    'city': City,
    'field': StudyField,
    'speciality': Speciality,
}


def translate(db_table, value):
    return db_table.objects.filter(name=value).first().name_uk


def get_universities_api(region: str, city: str, field: str, speciality: str) -> list:
    url = os.path.join(BASE_URL, 'univerdata/')
    # url = "http://127.0.0.1:8080/
    params = {
        'region': region,
        'city': city,
        'field': field,
        'speciality': speciality
    }

    translated_params = {key: (translate(DATABASES[key], value) if value else value)
                         for (key, value) in params.items()}

    if cache.get(translated_params):
        response = cache.get(params)
    else:
        response = requests.get(url, params=translated_params)
        cache.set(params, response)
    return response.json()


def get_universities(univers_ids):
    url = os.path.join(BASE_URL, 'favourites/')
    params = {'univers': univers_ids}
    try:
        response = requests.post(url, json=params)
        return response.json()
    except ConnectionError:
        return {'error': "Помилка з'єднання. Спробуйте пізніше"}
