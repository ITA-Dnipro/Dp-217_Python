from django.utils import timezone
from questioning.models import TestResult


def remove_obsolete_records():
    TestResult.objects.filter(created_date__lt=(timezone.now() - timezone.timedelta(days=365))).delete()
