from django.test import TestCase
from .models import Region, City, StudyField, Speciality


class TestUniverseachModels(TestCase):
    def test_region(self):
        region = Region.objects.create(name='Одеська область')
        self.assertEqual(str(region), 'Одеська область')

    def test_city(self):
        reg1 = Region.objects.create(name='Одеська область')
        city = City.objects.create(name='Iзмаiл', region=reg1)
        self.assertEqual(str(city), 'Iзмаiл')
        self.assertEqual(str(city.region), 'Одеська область')

    def test_studyfield(self):
        field = StudyField.objects.create(name='Бiологiя')
        self.assertEqual(str(field), 'Бiологiя')

    def test_speciality(self):
        field = StudyField.objects.create(name='Бiологiя')
        speciality = Speciality.objects.create(name='Бiологiя', study_field=field)
        self.assertEqual(str(speciality), 'Бiологiя')
        self.assertEqual(str(speciality.study_field), 'Бiологiя')


class TestGetRegions(TestCase):
    def setUp(self):
        self.region1 = Region.objects.create(name='Киiвська область')
        self.region2 = Region.objects.create(name='Львiвська область')

    def test_data(self):
        response = self.client.get('/search/region-data/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'data': [{'id': self.region1.id, 'name': 'Киiвська область'},
                                   {'id': self.region2.id, 'name': 'Львiвська область'}]})


class TestGetCities(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name='Одеська область')
        self.city1 = City.objects.create(name='Iзмаiл', region=self.region)
        self.city2 = City.objects.create(name='Білгород-Дністровський', region=self.region)

    def test_city_data(self):
        response = self.client.get('/search/cities-data/Одеська область/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'data': [{'id': self.city1.id, 'name': 'Iзмаiл', 'region_id': self.region.id},
                                   {'id': self.city2.id, 'name': 'Білгород-Дністровський', 'region_id': self.region.id}]})


class TestGetStudyfields(TestCase):
    def setUp(self):
        self.studyfield1 = StudyField.objects.create(name='Освіта')
        self.studyfield2 = StudyField.objects.create(name='Право')

    def test_data(self):
        response = self.client.get('/search/fields-data/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'data': [{'id': self.studyfield1.id, 'name': 'Освіта'},
                                   {'id': self.studyfield2.id, 'name': 'Право'}]})


class TestGetSpecialities(TestCase):
    def setUp(self):
        self.studyfield = StudyField.objects.create(name='Соціальні науки')
        self.speciality1 = Speciality.objects.create(name='Економіка', study_field=self.studyfield)
        self.speciality2 = Speciality.objects.create(name='Соціологія', study_field=self.studyfield)

    def test_city_data(self):
        response = self.client.get('/search/specialities-data/Соціальні науки/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
                         {'data': [{'id': self.speciality1.id, 'name': 'Економіка', 'study_field_id': self.studyfield.id},
                                   {'id': self.speciality2.id, 'name': 'Соціологія', 'study_field_id': self.studyfield.id}]})


class TestUnisearch(TestCase):
    def test_view_exists(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'universearch/search_form.html')
