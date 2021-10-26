from .models import Housing, University, City, Region
from django.db.models import Q


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
    def by_city_for_uni(uni:University, city:City):
        q = Housing.objects.filter(city=city)
        return q.filter(Q(university=uni) | Q(university__isnull=True))

    @staticmethod
    def all_for_uni(uni:University):
        return HousingService.by_city_for_uni(uni=uni, city=uni.city)
