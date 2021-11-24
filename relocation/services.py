import json
from django.db.models import Q
from .models import Housing, University, City, Region
import os
import requests


def get_housings() -> list:
    url = os.environ.get("HOSTEL_PARSE_URL")
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}


def parse_housings():
    housings = get_housings().get('content', [])
    for housing_dict in housings:
        housing_dict['city'] = City.objects.filter(name__icontains=housing_dict.get('city', '').first())
        if housing := Housing.objects.filter(name=housing_dict.get('name', '')).first():
            housing.address = housing_dict.get('address') or housing.address
            housing.phone = housing_dict.get('phone') or housing.phone
            housing.save()
        else:
            Housing.objects.create(**housing_dict)


class RegionService:

    @staticmethod
    def all():
        return Region.objects.all().order_by('name')

    @staticmethod
    def by_name(prompt:str):
        return Region.objects.filter(name__icontains=prompt).order_by('name')

    @staticmethod
    def get(region_id:str):
        return Region.objects.filter(id=region_id).first()


class CityService:

    @staticmethod
    def all():
        return City.objects.all().order_by('name')

    @staticmethod
    def by_region_or_name(region_id:str=None, prompt:str=None):
        qs = City.objects.all()
        if prompt:
            qs = qs.filter(name__icontains=prompt)
        if region_id:
            qs = qs.filter(region=Region.objects.filter(id=region_id).first())
        return qs.order_by('name')

    @staticmethod
    def get(city_id:str):
        return City.objects.filter(id=city_id).first()


class UniversityService:

    @staticmethod
    def all():
        return University.objects.all().order_by('name')

    @staticmethod
    def by_region(region_id:str):
        return University.objects.filter(city__region=RegionService.get(region_id)).order_by('name')

    @staticmethod
    def by_city_or_name(city_id:str=None, prompt:str=None):
        qs = University.objects.all()
        if prompt:
            qs = qs.filter(name__icontains=prompt)
        if city_id:
            qs = qs.filter(city=City.objects.filter(id=city_id).first())
        return qs.order_by('name')

    @staticmethod
    def get(uni_id:str):
        return University.objects.filter(id=uni_id).first()


class HousingService:

    @staticmethod
    def all():
        return Housing.objects.all()

    @staticmethod
    def by_city_for_uni(uni:University, city:City):
        q = Housing.objects.filter(city=city)
        return q.filter(Q(university=uni) | Q(university__isnull=True))

    @staticmethod
    def all_for_uni(uni:University):
        return HousingService.by_city_for_uni(uni=uni, city=uni.city)

    @staticmethod
    def all_json():
        return json.dumps([h.json for h in HousingService.all()])
