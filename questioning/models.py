import hashlib
import datetime
from django.utils import timezone
from django.db import models
from django.core.validators import int_list_validator
from users.models import CustomUser
from universearch.models import StudyField, Speciality


class TestResult(models.Model):
    """
    Class defining a model, for representing test result with.
    """
    created_date = models.DateTimeField(default=timezone.now)
    results = models.CharField(validators=[int_list_validator], max_length=240)
    type = models.PositiveSmallIntegerField(default=1)
    url = models.CharField(max_length=32, editable=False)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        resulted = f"{datetime.datetime.now()}{self.results}{self.type}{self.user_id}".encode('utf-8')
        self.url = hashlib.md5(resulted).hexdigest()
        super().save()

    def __str__(self):
        return f"{self.url}"


class QuestionsBase(models.Model):
    question = models.TextField("Запитання", blank=True)
    answer = models.TextField("Відповіді", blank=True)
    result = models.TextField("Результат відповідей", null=True)
    type = models.PositiveSmallIntegerField(default=1)

    class Meta:
        verbose_name = "Запитання"
        verbose_name_plural = "Запитання"


class KlimovCategory(models.Model):
    name = models.CharField("Категорія", max_length=20)
    desc = models.TextField("Опис категорії", blank=True)
    professions = models.TextField("Професії", blank=True)

    class Meta:
        verbose_name = "Категорія професії"
        verbose_name_plural = "Категорії професій"


class ConnectionKlimovCatStudyField(models.Model):
    category_id = models.ForeignKey(KlimovCategory, on_delete=models.CASCADE)
    field_id = models.ForeignKey(StudyField, on_delete=models.CASCADE)


class InterestCategory(models.Model):
    name = models.CharField("Категорія", max_length=30)
    desc = models.TextField("Опис категорії", blank=True)
    professions = models.TextField("Професії", blank=True)

    class Meta:
        verbose_name = "Категорія професії"
        verbose_name_plural = "Категорії професій"


class ConnectionInterestCatSpec(models.Model):
    category_id = models.ForeignKey(InterestCategory, on_delete=models.CASCADE)
    spec_id = models.ForeignKey(Speciality, on_delete=models.CASCADE)
