from django.test import TestCase
from django.utils import timezone
from questioning.cron import remove_obsolete_records
from questioning.models import TestResult


class CronTestCase(TestCase):
    results = "[1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]"

    def test_cron1(self):
        TestResult.objects.create(results=self.results, created_date=(timezone.now() - timezone.timedelta(days=367)))
        TestResult.objects.create(results=self.results, created_date=(timezone.now() - timezone.timedelta(days=368)))
        self.assertEqual(len(TestResult.objects.all()), 2)
        remove_obsolete_records()
        self.assertEqual(len(TestResult.objects.all()), 0)

    def test_cron2(self):
        TestResult.objects.create(results=self.results, created_date=(timezone.now() - timezone.timedelta(days=367)))
        TestResult.objects.create(results=self.results)
        self.assertEqual(len(TestResult.objects.all()), 2)
        remove_obsolete_records()
        self.assertTrue(TestResult.objects.get(id=4))

    def test_cron3(self):
        TestResult.objects.create(results=self.results)
        TestResult.objects.create(results=self.results)
        self.assertEqual(len(TestResult.objects.all()), 2)
        remove_obsolete_records()
        self.assertEqual(len(TestResult.objects.all()), 2)
