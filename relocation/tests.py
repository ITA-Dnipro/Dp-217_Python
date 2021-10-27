from django.test import TestCase
from relocation.models import Region, City, University, Housing
from relocation.forms import HousingForm

class RelocationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.regions = {obj.name: obj for obj in (
            Region.objects.create(name='Region-R1'),
            Region.objects.create(name='Region-R2'),
            Region.objects.create(name='Region-R3'),
            Region.objects.create(name='Region-R4'),
        )}
        cls.cities = {obj.name: obj for obj in (
            City.objects.create(name='City-R1C1', region=cls.regions['Region-R1']),
            City.objects.create(name='City-R1C2', region=cls.regions['Region-R1']),
            City.objects.create(name='City-R1C3', region=cls.regions['Region-R1']),
            City.objects.create(name='City-R2C1', region=cls.regions['Region-R2']),
            City.objects.create(name='City-R2C2', region=cls.regions['Region-R2']),
            City.objects.create(name='City-R3C1', region=cls.regions['Region-R3']),
        )}
        cls.unies = {obj.name: obj for obj in (
            University.objects.create(name='Uni-R1C2U1', city=cls.cities['City-R1C2']),
            University.objects.create(name='Uni-R1C2U2', city=cls.cities['City-R1C2']),
            University.objects.create(name='Uni-R1C3U1', city=cls.cities['City-R1C3']),
            University.objects.create(name='Uni-R3C1U1', city=cls.cities['City-R3C1']),
        )}
        cls.houses = {obj.name: obj for obj in (
            Housing.objects.create(name='House-R1C1H1', city=cls.cities['City-R1C1']),
            Housing.objects.create(name='House-R1C1H2-R1C3U1', city=cls.cities['City-R1C1'], university=cls.unies['Uni-R1C3U1']),
            Housing.objects.create(name='House-R1C2H1-R1C2U1', city=cls.cities['City-R1C2'], university=cls.unies['Uni-R1C2U1']),
            Housing.objects.create(name='House-R1C2H2-R1C2U1', city=cls.cities['City-R1C2'], university=cls.unies['Uni-R1C2U1']),
            Housing.objects.create(name='House-R1C2H3-R1C2U2', city=cls.cities['City-R1C2'], university=cls.unies['Uni-R1C2U2']),
            Housing.objects.create(name='House-R1C2H4', city=cls.cities['City-R1C2']),
            Housing.objects.create(name='House-R2C2H1', city=cls.cities['City-R2C2']),
        )}
        cls.test_data = {
            'housings': (
                {
                    'input': {'uni': [cls.unies['Uni-R1C3U1'].id]},
                    'output': tuple()
                },
                {
                    'input': {'uni': [cls.unies['Uni-R1C2U1'].id]},
                    'output': (cls.houses['House-R1C2H1-R1C2U1'], cls.houses['House-R1C2H2-R1C2U1'], cls.houses['House-R1C2H4'], )
                },
                {
                    'input': {'uni': [cls.unies['Uni-R1C2U2'].id]},
                    'output': (cls.houses['House-R1C2H3-R1C2U2'], cls.houses['House-R1C2H4'], )
                },
            ),
            'filters': (
                {
                    'input': {},
                    'output': {
                        'regions': tuple(cls.regions[i] for i in cls.regions),
                        'cities': tuple(cls.cities[i] for i in cls.cities),
                        'unies': tuple(cls.unies[i] for i in cls.unies),
                        'housings': tuple(),
                    },
                },
                {
                    'input': {
                        'region_filter': 'Region-R4',
                        'city_filter': 'City-R1C1',
                        'uni_filter': 'Uni-R3C1U1',
                        },
                    'output': {
                        'regions': (cls.regions['Region-R4'], ),
                        'cities': (cls.cities['City-R1C1'], ),
                        'unies': (cls.unies['Uni-R3C1U1'], ),
                        'housings': tuple(),
                    },
                },
            ),
        }

    def test_housing_output(self):
        for case in self.test_data['housings']:
            self.assertSequenceEqual(HousingForm(case['input']).get_housings(), case['output'])

    def test_filters(self):
        for case in self.test_data['filters']:
            form = HousingForm(case['input'])
            self.assertSequenceEqual(case['output']['regions'], form.fields['region'].queryset)
            self.assertSequenceEqual(case['output']['cities'], form.fields['city'].queryset)
            self.assertSequenceEqual(case['output']['unies'], form.fields['uni'].queryset)
            self.assertSequenceEqual(case['output']['housings'], form.get_housings())
