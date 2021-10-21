import hashlib
import datetime
from django.db import models
from django.core.validators import int_list_validator
from users.models import CustomUser

# if not authorised user
DEFAULT_USER_ID = 0


class TestResult(models.Model):
    """
    Class defining a model, for representing test result with.
    """
    created_date = models.DateTimeField(auto_now_add=True)
    results = models.CharField(validators=[int_list_validator], max_length=80)
    type = 1
    url = models.CharField(max_length=32, editable=False)

    def save(self, *args, **kwargs):
        resulted = f"{datetime.datetime.now()}{self.results}{self.type}".encode('utf-8')
        self.url = hashlib.md5(resulted).hexdigest()
        super().save()

    def __str__(self):
        return f"{self.url}"


class UserTestResult(models.Model):
    """
    Class defining a model, for representing linked user and test result.
    """
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=DEFAULT_USER_ID)
    result_id = models.ForeignKey(TestResult, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.result_id}"


class QuestionsBase(models.Model):
    question = models.TextField("Запитання", blank=True)
    answer_1 = models.TextField("Відповідь 1", blank=True)
    answer_2 = models.TextField("Відповідь 2", blank=True)
    result_id_1 = models.PositiveSmallIntegerField("Індекс відповіді 1", null=True)
    result_id_2 = models.PositiveSmallIntegerField("Індекс відповіді 2", null=True)
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
